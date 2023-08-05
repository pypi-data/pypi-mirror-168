import dataclasses
import math
import random
from functools import partial
import torch
import torch.nn as nn
from torch.utils.checkpoint import checkpoint
from typing import List, Optional, Tuple, Union
from functools import wraps
from torch import einsum
import torch.nn.functional as F
import copy


def inplace_assign(x0, x1):
    x0 = x1
    # del x1
    # torch.cuda.empty_cache()


def JitModule(cls: nn.Module):
    print("COMPILE", cls.__name__)

    @wraps(cls)
    def JitModuleFn(*args, **kwargs) -> torch.jit.ScriptModule:
        return torch.jit.script(cls(*args, **kwargs))

    return JitModuleFn


def relpos(input: torch.Tensor, window_size: int):
    ''' return the onehot encoding of relative distance of '''  # TODO: change to feature transform?
    reldis = torch.clamp(input[..., None] - input[..., None, :], min=-window_size, max=window_size)
    return F.one_hot(reldis + window_size, num_classes=2 * window_size + 1).float()


def redropout(input, p, dim=-3):
    shape = list(input.shape)
    shape[dim] = 1
    return input * nn.Dropout(p)(input.new_ones(shape))


redropoutRow = partial(redropout, dim=-3)
redropoutCol = partial(redropout, dim=-2)


def AttentionMaskBias(mask):
    return (mask - 1.0) * 1E9


def DeepClone(block, num_blocks):
    return nn.ModuleList([block] + [copy.deepcopy(block) for i in range(num_blocks - 1)])


def get_chunk_slices(s: int, chunk_size: Optional[int] = None):
    chunk_size = s if chunk_size is None else chunk_size
    chunks = math.ceil(s / chunk_size)
    return [i * chunk_size for i in range(chunks - 1)] + [(chunks - 1) * chunk_size], [(i + 1) * chunk_size for i in
                                                                                       range(chunks - 1)] + [s]


# @JitModule
class Dense(nn.Module):
    def __init__(self, dims_in: Union[List[int], int], dims_out: Union[List[int], int], bias: bool = True,
                 act: str = "none"):
        super().__init__()
        self.repr = f"Dense(dims_in={dims_in}, dims_out={dims_out}, bias={bias}, act={act})"
        self.bias = bias
        self.act = act
        if isinstance(dims_in, int):
            dims_in = [dims_in]
        if isinstance(dims_out, int):
            dims_out = [dims_out]
        self.w = nn.Parameter(torch.zeros(dims_in + dims_out, dtype=torch.float))
        if bias:
            self.b = nn.Parameter(torch.zeros(dims_out, dtype=torch.float))
        else:
            self.b = torch.zeros([])
        self.einstr = (f"...{'ijklmn'[:len(dims_in)]},"
                       f"{'ijklmn'[:len(dims_in)]}{'abcdef'[:len(dims_out)]}"
                       f"->...{'abcdef'[:len(dims_out)]}")
        self.act_fn = torch.nn.Identity()
        if act == "relu":
            self.act_fn = nn.ReLU()
        elif act == "sigmoid":
            self.act_fn = nn.Sigmoid()

    def __repr__(self):
        return self.repr

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        out = torch.einsum(self.einstr, input, self.w)
        if self.bias:
            out = out + self.b
        out = self.act_fn(out)
        return out


class Attention(nn.Module):
    def __init__(self, c_q, c_kv, h, c_a, use_gate=True):
        '''

        Args:
            c_q: channels of q
            c_kv: channels of k and v
            h: num of heads
            c_a: channels of hidden state
            use_gate: whether to gate affine
        '''
        super().__init__()
        self.normsize = 1. / math.sqrt(c_a)
        self.use_gate = use_gate

        self.dense_q = Dense(c_q, [h, c_a], bias=False)
        self.dense_k = Dense(c_kv, [h, c_a], bias=False)
        self.dense_v = Dense(c_kv, [h, c_a], bias=False)
        self.dense_g = torch.nn.Identity()
        if self.use_gate:
            self.dense_g = Dense(c_q, [h, c_a], act="sigmoid")
        self.dense_o = Dense([h, c_a], c_q)

    def forward_chunk(self, q, kv, bias: Optional[torch.Tensor] = None, inplace: bool = True):
        '''
            ONLY DIM -3 CAN CHUNK
        Args:
            q: Query params [..., Q, c_q]     e.t [s,r,c_m]
            kv: Key params   [..., K, c_kv]
            mask: [..., Q]
            bias: bias add to affine [..., Q, K, ?] : The same shape as Atten

        Returns:

        '''
        if inplace:
            Q = self.dense_q(q) * self.normsize  # ... Q h c
            K = self.dense_k(kv)  # ... K h c
            V = self.dense_v(kv)  # ... K h c
            AT = torch.einsum("... Q h c, ... K h c -> ... Q K h", Q, K)
            if bias is not None:
                AT += bias
            AT = F.softmax(AT, dim=-2)
            # print("AT", AT.shape)
            O = torch.einsum("... Q K h, ... K h c->... Q h c", AT, V)

            if self.use_gate:
                # G =
                O *= self.dense_g(q)  # ... Q h c
            O = self.dense_o(O)
        else:
            Q = self.dense_q(q) * self.normsize  # ... Q h c
            K = self.dense_k(kv)  # ... K h c
            V = self.dense_v(kv)  # ... K h c
            AT = torch.einsum("... Q h c, ... K h c -> ... Q K h", Q, K)

            if bias is not None:
                AT = F.softmax(AT + bias, dim=-2)
            else:
                AT = F.softmax(AT, dim=-2)
            O = torch.einsum("... Q K h, ... K h c->... Q h c", AT, V)

            if self.use_gate:
                G = self.dense_g(q)  # ... Q h c
                O = O * G
            O = self.dense_o(O)
        return O

    def forward(self, q, kv, bias: Optional[torch.Tensor] = None, bias_mask: Optional[torch.Tensor] = None,
                chunk_size=4, inplace: bool = True):
        slices0, slices1 = get_chunk_slices(q.shape[-3], chunk_size)
        out = torch.empty_like(q)
        if bias is not None and bias_mask is not None:
            for s0, s1 in zip(slices0, slices1):
                bias_ = bias[..., :, :, :, :] + AttentionMaskBias(bias_mask[..., s0:s1, None, :, None])
                out[..., s0:s1, :, :] = self.forward_chunk(q[..., s0:s1, :, :], kv[..., s0:s1, :, :], bias_, inplace)
        elif bias is not None and bias_mask is None:
            for s0, s1 in zip(slices0, slices1):
                bias_ = bias[..., :, :, :, :]
                out[..., s0:s1, :, :] = self.forward_chunk(q[..., s0:s1, :, :], kv[..., s0:s1, :, :], bias_, inplace)
        elif bias is None and bias_mask is not None:
            for s0, s1 in zip(slices0, slices1):
                bias_ = AttentionMaskBias(bias_mask[..., s0:s1, None, :, None])
                out[..., s0:s1, :, :] = self.forward_chunk(q[..., s0:s1, :, :], kv[..., s0:s1, :, :], bias_, inplace)
        else:
            bias_ = None
            for s0, s1 in zip(slices0, slices1):
                out[..., s0:s1, :, :] = self.forward_chunk(q[..., s0:s1, :, :], kv[..., s0:s1, :, :], bias_, inplace)
        return out


# @JitModule
class GlobalColAttention(nn.Module):
    def __init__(self, c_em, h_em, c_a_em):
        super().__init__()
        self.normsize = 1. / math.sqrt(c_a_em)
        self.layernorm = nn.LayerNorm(c_em)

        self.dense_q = Dense(c_em, [h_em, c_a_em], bias=False)
        self.dense_k = Dense(c_em, c_a_em, bias=False)
        self.dense_v = Dense(c_em, c_a_em, bias=False)
        self.dense_g = Dense(c_em, [h_em, c_a_em], act="sigmoid")
        self.dense_o = Dense([h_em, c_a_em], c_em)

    def forward_chunk(self, m, mask, B):
        Q = torch.sum(m * mask[..., None], dim=-3) / (torch.sum(mask, dim=-2)[..., None] + 1E-10)
        # r h c
        Q = self.dense_q(Q) * self.normsize
        # s r c
        K = self.dense_k(m)
        # s r c
        V = self.dense_v(m)
        # s r h c
        G = self.dense_g(m)

        AT = torch.einsum("... r h c,... s r c -> ... s r h", Q, K)
        # print("AT", AT.shape)
        # AT = F.softmax((AT + B).permute([2, 1, 0]), dim=-1)
        # AT = AT.permute([2, 1, 0])
        AT = F.softmax(AT + B, dim=-3)
        O = torch.einsum("... s r h, ... s r c -> ... r h c", AT, V)
        # a=AT.permute([1,2,0])
        # v=V.permute([1,0,2])
        # O=torch.matmul(a,v)
        O = self.dense_o(O[..., None, :, :, :] * G)  # s r c_em
        # torch.cuda.empty_cache()
        # print(torch.cuda.memory_allocated())
        # quit()
        return O

    def forward(self, m, mask, chunk_size: Optional[int] = 4):
        # m: S R C -> R C   m_mask  S R -> R ()
        m = self.layernorm(m)
        # TODO Chunk Checking
        slices0, slices1 = get_chunk_slices(m.shape[-2], chunk_size)
        # print(slices0,slices1)
        O = torch.empty_like(m)
        for s0, s1 in zip(slices0, slices1):
            # ... s r
            B = AttentionMaskBias(mask[..., s0:s1])[..., None]
            O[..., s0:s1, :] = self.forward_chunk(m[..., s0:s1, :], mask[..., s0:s1], B)
        return O


# @JitModule
class RowAttentionWithPair(nn.Module):
    def __init__(self, c_m, h_m, c_a_m, c_z):
        super().__init__()
        self.layernorm = nn.LayerNorm(c_m)
        self.layernorm_z = nn.LayerNorm(c_z)
        self.dense_z = Dense(c_z, h_m, bias=False)
        self.attention = Attention(c_q=c_m, c_kv=c_m, h=h_m, c_a=c_a_m, use_gate=True)

    def forward(self, m: torch.Tensor, m_mask, z):
        '''

        Args:
            m: [..., s, r, c_m]
            m_mask: [..., s, r]
            z: [..., r, R, c_z]

        Returns:

        '''
        m = self.layernorm(m)
        b = self.dense_z(self.layernorm_z(z))[..., None, :, :, :]  # ... r R h_m -> ... () r R h_m
        m = self.attention(q=m, kv=m, bias=b, bias_mask=m_mask)
        return m


class ColAttention(nn.Module):
    def __init__(self, c_m, h_m, c_a_m):
        super().__init__()
        self.layernorm = nn.LayerNorm(c_m)
        self.attention = Attention(c_q=c_m, c_kv=c_m, h=h_m, c_a=c_a_m, use_gate=True)

    def forward(self, m, m_mask):
        # ... s r c_m -> ... r s c_m
        m = m.transpose(-3, -2)
        _m_mask = m_mask.transpose(-2, -1)
        # ... s r -> ... r s
        m = self.layernorm(m)
        m = self.attention(q=m, kv=m, bias_mask=_m_mask)
        # ... r s c_m -> ... s r c_m
        m = m.transpose(-3, -2)
        return m


class TriRowAttention(nn.Module):
    def __init__(self, c_z, h_z, c_a_z):
        super().__init__()
        self.layernorm = nn.LayerNorm(c_z)
        self.dense_z = Dense(c_z, h_z, bias=False)
        self.attention = Attention(c_q=c_z, c_kv=c_z, h=h_z, c_a=c_a_z, use_gate=True)

    def forward(self, z, z_mask):
        # I J c_z
        z = self.layernorm(z)
        # I J C -> 1 I J h
        b = self.dense_z(z)[..., None, :, :, :]
        # I J -> I 1 J 1
        z = self.attention(q=z, kv=z, bias=b, bias_mask=z_mask)
        return z


# @JitModule
class TriColAttention(nn.Module):
    def __init__(self, c_z, h_z, c_a_z):
        super().__init__()
        self.layernorm = nn.LayerNorm(c_z)
        self.dense_z = Dense(c_z, h_z, bias=False)
        self.attention = Attention(c_q=c_z, c_kv=c_z, h=h_z, c_a=c_a_z, use_gate=True)

    def forward(self, z: torch.Tensor, z_mask: torch.Tensor):
        z = self.layernorm(z)
        # ... r R h_z -> ... R r h_z
        z = z.transpose(-3, -2)
        # ... r R -> ... R r
        _z_mask = z_mask.transpose(-2, -1)
        # ... r R h_z -> ... () R r h_z
        b = self.dense_z(z)[..., None, :, :, :]
        z = self.attention(q=z, kv=z, bias=b, bias_mask=_z_mask)
        # ... R r h_z -> ... r R h_z
        z = z.transpose(-3, -2)
        return z


class PairUpdate(nn.Module):
    def __init__(self, c_tz: int, c_u_tz: int, row_mode=True):
        super().__init__()
        self.row_mode = row_mode
        self.dense_q1 = Dense(c_tz, c_u_tz)
        self.dense_q2 = Dense(c_tz, c_u_tz, act="sigmoid")
        self.dense_k1 = Dense(c_tz, c_u_tz)
        self.dense_k2 = Dense(c_tz, c_u_tz, act="sigmoid")
        self.dense_v1 = Dense(c_u_tz, c_tz)
        self.dense_v2 = Dense(c_tz, c_tz, act="sigmoid")
        self.norm_in = nn.LayerNorm(c_tz)
        self.norm_out = nn.LayerNorm(c_u_tz)

    def forward(self, z: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        z = self.norm_in(z)
        Q = self.dense_q1(z) * self.dense_q2(z) * mask[..., None]
        K = self.dense_k1(z) * self.dense_k2(z) * mask[..., None]
        V = self.dense_v2(z)
        if self.row_mode:
            AT = torch.einsum("... q r c, ... k r c -> ... q k c", Q, K)
        else:
            AT = torch.einsum("... s q c, ... s k c ->... k q c", Q, K)
        AT = self.norm_out(AT)
        z = self.dense_v1(AT) * V
        return z


class Transition(nn.Module):
    def __init__(self, c_m: int, ct: int = 4):
        super().__init__()
        self.norm = nn.LayerNorm(c_m)
        self.dense1 = Dense(c_m, ct * c_m, act="relu")
        self.dense2 = Dense(c_m * ct, c_m)

    def forward(self, mz: torch.Tensor) -> torch.Tensor:
        mz = self.norm(mz)
        mz = self.dense1(mz)
        mz = self.dense2(mz)
        return mz


class OutProductMean(nn.Module):
    def __init__(self, c_m: int, c_opm: int, c_z: int):
        super().__init__()
        self.c_z = c_z
        self.layernorm = nn.LayerNorm(c_m)
        self.dense_q = Dense(c_m, c_opm)
        self.dense_k = Dense(c_m, c_opm)
        self.dense_g = Dense([c_opm, c_opm], c_z)

    def forward(self, m: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        '''

        Args:
            m: [..., s, r, c_m]
            mask: [..., s, r]

        Returns:

        '''
        _m = self.layernorm(m)  # cannot change m
        q = self.dense_q(_m) * mask[..., None]
        k = self.dense_k(_m) * mask[..., None]
        at = torch.einsum("... s r c, ... s R C -> ... r R c C", q, k)
        norm = torch.einsum("... s r, ... s R -> ... r R", mask, mask)
        # ... r R -> ... r R ()
        norm = norm[..., None]
        z = self.dense_g(at) / (1E-3 + norm)
        return z


class TemplatePointwiseAttention(nn.Module):
    def __init__(self, c_z, c_t, h_t, c_a_t):
        super().__init__()
        self.attention = Attention(c_z, c_t, h_t, c_a_t, use_gate=False)

    def forward(self, t, z):
        '''

        Args:
            t: Template Embedding [..., n_t, r, r, c_t]
            t_mask: Template Mask [..., n_t]
            z: Pair Embedding     [..., r, r, c_t]

        Returns:

        '''

        t_mask = t.new_ones(t.shape[:-3])
        # nt -> 1 1 1 1 n_t
        # b = AttentionMaskBias(t_mask[..., None, None, None, :, None])  # last dim is the head dim
        # n_t r R c_t -> r R n_t c_t
        t = t.permute([1, 2, 0, 3])
        z = self.attention(q=z[..., :, :, None, :], kv=t, bias=None)
        return z.squeeze(-2)


# # @JitModule
# class Dense(nn.Module):
#     def __init__(self, dims_in: Union[List[int], int], dims_out: Union[List[int], int], bias: bool = True,
#                  act: str = "none"):
#         super().__init__()
#         self.repr = f"Dense(dims_in={dims_in}, dims_out={dims_out}, bias={bias}, act={act})"
#         self.bias = bias
#         self.act = act
#         if isinstance(dims_in, int):
#             dims_in = [dims_in]
#         if isinstance(dims_out, int):
#             dims_out = [dims_out]
#         self.w = nn.Parameter(torch.zeros(dims_in + dims_out, dtype=torch.float))
#         if bias:
#             self.b = nn.Parameter(torch.zeros(dims_out, dtype=torch.float))
#         else:
#             self.b = torch.zeros([])
#         self.einstr = (f"...{'ijklmn'[:len(dims_in)]},"
#                        f"{'ijklmn'[:len(dims_in)]}{'abcdef'[:len(dims_out)]}"
#                        f"->...{'abcdef'[:len(dims_out)]}")
#         self.act_fn = torch.nn.Identity()
#         if act == "relu":
#             self.act_fn = nn.ReLU()
#         elif act == "sigmoid":
#             self.act_fn = nn.Sigmoid()
#
#     def __repr__(self):
#         return self.repr
#
#     def forward(self, input: torch.Tensor, inplace=False) -> torch.Tensor:
#         out = torch.einsum(self.einstr, input, self.w)
#         if self.bias:
#             if inplace:
#                 out += self.b
#             else:
#                 out = out + self.b
#         if inplace:
#             out = self.act_fn(out)
#         else:
#             out = self.act_fn(out)
#         return out
#
#
# # @JitModule
# class Attention(nn.Module):
#     def __init__(self, c_q, c_kv, h, c_a, use_gate=True):
#         '''
#
#         Args:
#             c_q: channels of q
#             c_kv: channels of k and v
#             h: num of heads
#             c_a: channels of hidden state
#             use_gate: whether to gate affine
#         '''
#         super().__init__()
#         self.normsize = 1. / math.sqrt(c_a)
#         self.use_gate = use_gate
#
#         self.dense_q = Dense(c_q, [h, c_a], bias=False)
#         self.dense_k = Dense(c_kv, [h, c_a], bias=False)
#         self.dense_v = Dense(c_kv, [h, c_a], bias=False)
#         self.dense_g = torch.nn.Identity()
#         if self.use_gate:
#             self.dense_g = Dense(c_q, [h, c_a], act="sigmoid")
#         self.dense_o = Dense([h, c_a], c_q)
#
#     def forward_chunk(self, q, kv, bias: Optional[torch.Tensor] = None, inplace: bool = True):
#         '''
#             ONLY DIM -3 CAN CHUNK
#         Args:
#             q: Query params [..., Q, c_q]     e.t [s,r,c_m]
#             kv: Key params   [..., K, c_kv]
#             mask: [..., Q]
#             bias: bias add to affine [..., Q, K, ?] : The same shape as Atten
#
#         Returns:
#
#         '''
#         if inplace:
#             Q = self.dense_q(q) * self.normsize  # ... Q h c
#             K = self.dense_k(kv)  # ... K h c
#             V = self.dense_v(kv)  # ... K h c
#             AT = torch.einsum("... Q h c, ... K h c -> ... Q K h", Q, K)
#             if bias is not None:
#                 AT += bias
#             AT = F.softmax(AT, dim=-2)
#             # print("AT", AT.shape)
#             O = torch.einsum("... Q K h, ... K h c->... Q h c", AT, V)
#
#             if self.use_gate:
#                 # G =
#                 O *= self.dense_g(q)  # ... Q h c
#             O = self.dense_o(O)
#         else:
#             Q = self.dense_q(q) * self.normsize  # ... Q h c
#             K = self.dense_k(kv)  # ... K h c
#             V = self.dense_v(kv)  # ... K h c
#             AT = torch.einsum("... Q h c, ... K h c -> ... Q K h", Q, K)
#
#             if bias is not None:
#                 AT = F.softmax(AT + bias, dim=-2)
#             else:
#                 AT = F.softmax(AT, dim=-2)
#             O = torch.einsum("... Q K h, ... K h c->... Q h c", AT, V)
#
#             if self.use_gate:
#                 G = self.dense_g(q)  # ... Q h c
#                 O = O * G
#             O = self.dense_o(O)
#         return O
#
#     def forward(self, q, kv, bias: Optional[torch.Tensor] = None, bias_mask: Optional[torch.Tensor] = None,
#                 chunk_size=4, inplace: bool = True):
#         slices0, slices1 = get_chunk_slices(q.shape[-3], chunk_size)
#         out = torch.empty_like(q)
#         if bias is not None and bias_mask is not None:
#             for s0, s1 in zip(slices0, slices1):
#                 bias_ = bias[..., :, :, :, :] + AttentionMaskBias(bias_mask[..., s0:s1, None, :, None])
#                 out[..., s0:s1, :, :] = self.forward_chunk(q[..., s0:s1, :, :], kv[..., s0:s1, :, :], bias_, inplace)
#         elif bias is not None and bias_mask is None:
#             for s0, s1 in zip(slices0, slices1):
#                 bias_ = bias[..., :, :, :, :]
#                 out[..., s0:s1, :, :] = self.forward_chunk(q[..., s0:s1, :, :], kv[..., s0:s1, :, :], bias_, inplace)
#         elif bias is None and bias_mask is not None:
#             for s0, s1 in zip(slices0, slices1):
#                 bias_ = AttentionMaskBias(bias_mask[..., s0:s1, None, :, None])
#                 out[..., s0:s1, :, :] = self.forward_chunk(q[..., s0:s1, :, :], kv[..., s0:s1, :, :], bias_, inplace)
#         else:
#             bias_ = None
#             for s0, s1 in zip(slices0, slices1):
#                 out[..., s0:s1, :, :] = self.forward_chunk(q[..., s0:s1, :, :], kv[..., s0:s1, :, :], bias_, inplace)
#         return out
#
#
# # @JitModule
# class GlobalColAttention(nn.Module):
#     def __init__(self, c_em, h_em, c_a_em):
#         super().__init__()
#         self.normsize = 1. / math.sqrt(c_a_em)
#         self.layernorm = nn.LayerNorm(c_em)
#
#         self.dense_q = Dense(c_em, [h_em, c_a_em], bias=False)
#         self.dense_k = Dense(c_em, c_a_em, bias=False)
#         self.dense_v = Dense(c_em, c_a_em, bias=False)
#         self.dense_g = Dense(c_em, [h_em, c_a_em], act="sigmoid")
#         self.dense_o = Dense([h_em, c_a_em], c_em)
#
#     def forward_chunk(self, m, mask, B):
#         # torch.cuda.empty_cache()
#         # print(torch.cuda.memory_allocated())
#         Q = torch.sum(m * mask[..., None], dim=-3) / (torch.sum(mask, dim=-2)[..., None] + 1E-10)
#
#         # r h c
#         Q = self.dense_q(Q) * self.normsize
#         # s r c
#         K = self.dense_k(m)
#         # s r c
#         V = self.dense_v(m)
#         # s r h c
#         G = self.dense_g(m)
#
#         AT = torch.einsum("... r h c,... s r c -> ... s r h", Q, K)
#         # print("AT", AT.shape)
#         # AT = F.softmax((AT + B).permute([2, 1, 0]), dim=-1)
#         # AT = AT.permute([2, 1, 0])
#         AT = F.softmax(AT + B, dim=-3)
#         O = torch.einsum("... s r h, ... s r c -> ... r h c", AT, V)
#         # a=AT.permute([1,2,0])
#         # v=V.permute([1,0,2])
#         # O=torch.matmul(a,v)
#         O = self.dense_o(O[..., None, :, :, :] * G)  # s r c_em
#         # torch.cuda.empty_cache()
#         # print(torch.cuda.memory_allocated())
#         # quit()
#         return O
#
#     def forward(self, m, mask, chunk_size: Optional[int] = 4):
#         print(" Global Col")
#         # m: S R C -> R C   m_mask  S R -> R ()
#         m = self.layernorm(m)
#         # TODO Chunk Checking
#         slices0, slices1 = get_chunk_slices(m.shape[-2], chunk_size)
#         # print(slices0,slices1)
#         O = torch.empty_like(m)
#         for s0, s1 in zip(slices0, slices1):
#             # ... s r
#             B = AttentionMaskBias(mask[..., s0:s1])[..., None]
#             O[..., s0:s1, :] = self.forward_chunk(m[..., s0:s1, :], mask[..., s0:s1], B)
#         return O
#
#
# # @JitModule
# class RowAttentionWithPair(nn.Module):
#     def __init__(self, c_m, h_m, c_a_m, c_z):
#         super().__init__()
#         self.layernorm = nn.LayerNorm(c_m)
#         self.layernorm_z = nn.LayerNorm(c_z)
#         self.dense_z = Dense(c_z, h_m, bias=False)
#         self.attention = Attention(c_q=c_m, c_kv=c_m, h=h_m, c_a=c_a_m, use_gate=True)
#
#     def forward(self, m: torch.Tensor, m_mask, z, inplace=True):
#         '''
#
#         Args:
#             m: [..., s, r, c_m]
#             m_mask: [..., s, r]
#             z: [..., r, R, c_z]
#
#         Returns:
#
#         '''
#
#         # b = b + AttentionMaskBias(m_mask[..., None, :,None])  # mask_bias
#         print(" Row")
#         if inplace:
#             m = self.layernorm(m)
#             b = self.dense_z(self.layernorm_z(z))[..., None, :, :, :]  # ... r R h_m -> ... () r R h_m
#             m = self.attention(q=m, kv=m, bias=b, bias_mask=m_mask)
#         else:
#             m = self.layernorm(m)
#             b = self.dense_z(self.layernorm_z(z))[..., None, :, :, :]  # ... r R h_m -> ... () r R h_m
#             m = self.attention(q=m, kv=m, bias=b, bias_mask=m_mask)
#         return m
#
#
# # @JitModule
# class ColAttention(nn.Module):
#     def __init__(self, c_m, h_m, c_a_m):
#         super().__init__()
#         self.layernorm = nn.LayerNorm(c_m)
#         self.attention = Attention(c_q=c_m, c_kv=c_m, h=h_m, c_a=c_a_m, use_gate=True)
#
#     def forward(self, m, m_mask):
#         print(" Col")
#         # ... s r c_m -> ... r s c_m
#         m = m.transpose(-3, -2)
#
#         _m_mask = m_mask.transpose(-2, -1)
#         # ... s r -> ... r s
#         m = self.layernorm(m)
#
#         # b = AttentionMaskBias(_m_mask)[..., None, :, None]  # mask_bias
#         m = self.attention(q=m, kv=m, bias_mask=_m_mask)
#
#         #     quit()
#         # ... r s c_m -> ... s r c_m
#         m = m.transpose(-3, -2)
#         return m
#
#
# # @JitModule
# class TriRowAttention(nn.Module):
#     def __init__(self, c_z, h_z, c_a_z):
#         super().__init__()
#         self.layernorm = nn.LayerNorm(c_z)
#         self.dense_z = Dense(c_z, h_z, bias=False)
#         self.attention = Attention(c_q=c_z, c_kv=c_z, h=h_z, c_a=c_a_z, use_gate=True)
#
#     def forward(self, z, z_mask):
#         print(" Tri row")
#         # I J c_z
#         z = self.layernorm(z)
#         # I J C -> 1 I J h
#         b = self.dense_z(z)[..., None, :, :, :]
#         # I J -> I 1 J 1
#         # b = b + AttentionMaskBias(z_mask)[..., :, None, :, None]
#         z = self.attention(q=z, kv=z, bias=b, bias_mask=z_mask)
#         return z
#
#
# # @JitModule
# class TriColAttention(nn.Module):
#     def __init__(self, c_z, h_z, c_a_z):
#         super().__init__()
#         self.layernorm = nn.LayerNorm(c_z)
#         self.dense_z = Dense(c_z, h_z, bias=False)
#         self.attention = Attention(c_q=c_z, c_kv=c_z, h=h_z, c_a=c_a_z, use_gate=True)
#
#     def forward(self, z: torch.Tensor, z_mask: torch.Tensor):
#         print(" Tri col")
#         z = self.layernorm(z)
#         # ... r R h_z -> ... R r h_z
#         z = z.transpose(-3, -2)
#         # ... r R -> ... R r
#         _z_mask = z_mask.transpose(-2, -1)
#         # ... r R h_z -> ... () R r h_z
#         b = self.dense_z(z)[..., None, :, :, :]
#
#         # b = b + AttentionMaskBias(_z_mask)[..., :, None, :, None]
#         z = self.attention(q=z, kv=z, bias=b, bias_mask=_z_mask)
#         # ... R r h_z -> ... r R h_z
#         z = z.transpose(-3, -2)
#         return z
#
#
# # @JitModule
# class PairUpdate(nn.Module):
#     def __init__(self, c_tz: int, c_u_tz: int, row_mode=True):
#         super().__init__()
#         self.row_mode = row_mode
#         self.dense_q1 = Dense(c_tz, c_u_tz)
#         self.dense_q2 = Dense(c_tz, c_u_tz, act="sigmoid")
#         self.dense_k1 = Dense(c_tz, c_u_tz)
#         self.dense_k2 = Dense(c_tz, c_u_tz, act="sigmoid")
#         self.dense_v1 = Dense(c_u_tz, c_tz)
#         self.dense_v2 = Dense(c_tz, c_tz, act="sigmoid")
#         self.norm_in = nn.LayerNorm(c_tz)
#         self.norm_out = nn.LayerNorm(c_u_tz)
#
#     def forward(self, z: torch.Tensor, mask: torch.Tensor, chunk_size0=64, chunk_size1=64):
#         print(" Update")
#         slices00, slices01 = get_chunk_slices(z.shape[-2], chunk_size0)
#         slices10, slices11 = get_chunk_slices(z.shape[-2], chunk_size1)
#         O = torch.empty_like(z)
#         if self.row_mode:
#             for s00, s01 in zip(slices00, slices01):
#                 z_chunk0 = self.norm_in(z[..., s00:s01, :, :])
#                 for s10, s11 in zip(slices10, slices11):
#                     z_chunk1 = self.norm_in(z[..., s10:s11, :, :])
#                     Q = self.dense_q1(z_chunk0) * self.dense_q2(z_chunk0) * mask[..., s00:s01, :, None]
#                     K = self.dense_k1(z_chunk1) * self.dense_k2(z_chunk1) * mask[..., s10:s11, :, None]
#                     AT = torch.einsum("... q r c, ... k r c -> ... q k c", Q, K)
#                     V = self.dense_v2(z_chunk0[..., s10:s11, :])
#                     O[..., s00:s01, s10:s11, :] = self.dense_v1(self.norm_out(AT)) * V
#         else:
#             for s00, s01 in zip(slices00, slices01):
#                 z_chunk0 = self.norm_in(z[..., s00:s01, :])
#                 for s10, s11 in zip(slices10, slices11):
#                     z_chunk1 = self.norm_in(z[..., s10:s11, :])
#                     Q = self.dense_q1(z_chunk0) * self.dense_q2(z_chunk0) * mask[..., s00:s01, None]
#                     K = self.dense_k1(z_chunk1) * self.dense_k2(z_chunk1) * mask[..., s10:s11, None]
#                     AT = torch.einsum("... s q c, ... s k c ->... k q c", Q, K)
#                     V = self.dense_v2(z_chunk0[..., s10:s11, :, :])
#                     O[..., s10:s11, s00:s01, :] = self.dense_v1(self.norm_out(AT)) * V
#         return O
#
#     def forward_old(self, z: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
#         print(" Update")
#         z = self.norm_in(z)  # TODO we need fast layernorm
#         Q = self.dense_q1(z) * self.dense_q2(z) * mask[..., None]
#         K = self.dense_k1(z) * self.dense_k2(z) * mask[..., None]
#         V = self.dense_v2(z)
#         if self.row_mode:
#             AT = torch.einsum("... q r c, ... k r c -> ... q k c", Q, K)
#         else:
#             AT = torch.einsum("... s q c, ... s k c ->... k q c", Q, K)
#         AT = self.norm_out(AT)
#         z = self.dense_v1(AT) * V
#         return z
#
#
# # @JitModule
# class Transition(nn.Module):
#     def __init__(self, c_m: int, ct: int = 4):
#         super().__init__()
#         self.norm = nn.LayerNorm(c_m)
#         self.dense1 = Dense(c_m, ct * c_m, act="relu")
#         self.dense2 = Dense(c_m * ct, c_m)
#
#     def forward(self, mz: torch.Tensor, chunk_size=64) -> torch.Tensor:
#         print(" Trans")
#         slices0, slices1 = get_chunk_slices(mz.shape[-2], chunk_size)
#         O = torch.empty_like(mz)
#         for s0, s1 in zip(slices0, slices1):
#             _mz = self.norm(mz[..., s0:s1, :])
#             _mz = self.dense1(_mz)
#             O[..., s0:s1, :] = self.dense2(_mz)
#         return O
#
#
# # @JitModule
# class OutProductMean(nn.Module):
#     def __init__(self, c_m: int, c_opm: int, c_z: int):
#         super().__init__()
#         self.c_z = c_z
#         self.layernorm = nn.LayerNorm(c_m)
#         self.dense_q = Dense(c_m, c_opm)
#         self.dense_k = Dense(c_m, c_opm)
#         self.dense_g = Dense([c_opm, c_opm], c_z)
#
#     def forward_old(self, m: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
#         '''
#
#         Args:
#             m: [..., s, r, c_m]
#             mask: [..., s, r]
#
#         Returns:
#
#         '''
#         print(" OPM")
#         _m = self.layernorm(m)  # cannot change m
#         q = self.dense_q(_m) * mask[..., None]
#         k = self.dense_k(_m) * mask[..., None]
#         at = torch.einsum("... s r c, ... s R C -> ... r R c C", q, k)
#         norm = torch.einsum("... s r, ... s R -> ... r R", mask, mask)
#         # ... r R -> ... r R ()
#         norm = norm[..., None]
#         z = self.dense_g(at) / (1E-3 + norm)
#         print(z.shape)
#         quit()
#         return z
#
#     def forward(self, m: torch.Tensor, mask: torch.Tensor, chunk_size0=64, chunk_size1=64) -> torch.Tensor:
#         '''
#
#         Args:
#             m: [..., s, r, c_m]
#             mask: [..., s, r]
#
#         Returns:
#
#         '''
#         print(" OPM")
#         slices00, slices01 = get_chunk_slices(m.shape[-2], chunk_size0)  # current make slices at axis -2
#         slices10, slices11 = get_chunk_slices(m.shape[-2], chunk_size1)  # current make slices at axis -2
#         O = torch.empty(list(m.shape[:-3]) + [m.shape[-2],m.shape[-2],self.c_z], dtype=m.dtype, device=m.device)
#         for s00, s01 in zip(slices00, slices01):
#             m_chunk0 = self.layernorm(m[..., s00:s01, :])
#             for s10, s11 in zip(slices10, slices11):
#                 m_chunk1 = self.layernorm(m[..., s10:s11, :])
#                 q = self.dense_q(m_chunk0) * mask[..., s00:s01, None]
#                 k = self.dense_k(m_chunk1) * mask[..., s10:s11, None]
#                 at = torch.einsum("... s r c, ... s R C -> ... r R c C", q, k)
#                 norm = torch.einsum("... s r, ... s R -> ... r R", mask[..., s00:s01], mask[..., s10:s11])
#                 O[..., s00:s01, s10:s11,:] = self.dense_g(at) / (1E-3 + norm[..., None])
#         return O
#
#
# # @JitModule
# class TemplatePointwiseAttention(nn.Module):
#     def __init__(self, c_z, c_t, h_t, c_a_t):
#         super().__init__()
#         self.attention = Attention(c_z, c_t, h_t, c_a_t, use_gate=False)
#
#     def forward(self, t, z):
#         '''
#
#         Args:
#             t: Template Embedding [..., n_t, r, r, c_t]
#             t_mask: Template Mask [..., n_t]
#             z: Pair Embedding     [..., r, r, c_t]
#
#         Returns:
#
#         '''
#
#         t_mask = t.new_ones(t.shape[:-3])
#         # nt -> 1 1 1 1 n_t
#         # b = AttentionMaskBias(t_mask[..., None, None, None, :, None])  # last dim is the head dim
#         # n_t r R c_t -> r R n_t c_t
#         t = t.permute([1, 2, 0, 3])
#         # quit()
#         z = self.attention(q=z[..., :, :, None, :], kv=t, bias=None)
#         return z.squeeze(-2)


if __name__ == '__main__':
    import torchsummary

    # a = torch.rand([2, 1, 3])
    # b = torch.rand([2, 3, 1])
    # print(torch.matmul(a, b).shape)
    # a = torch.rand([10, 10])

# class Attention(nn.Module):
#     def __init__(self, c_io, h, c_a):
#         super().__init__()
#         self.norm_coe = math.sqrt(c_a)
#
#         self.dense_q = Dense(c_io, [h, c_a], bias=False)
#         self.dense_k = Dense(c_io, [h, c_a], bias=False)
#         self.dense_v = Dense(c_io, [h, c_a], bias=False)
#         self.dense_g = Dense(c_io, [h, c_a], act="sigmoid")  # gate
#         self.dense_o = Dense([h, c_a], c_io)
#         self.softmax = nn.Softmax(dim=-2)
#
#     def forward(self, in_repr, mask, bias: Optional = None):
#         '''
#
#         Args:
#             in_repr: [..., s, r, c]
#             mask: [..., s, r]
#             bias: [..., (), () ,(), ()]
#
#         Returns:
#
#         '''
#         Q = self.dense_q(in_repr) / self.norm_coe
#         K = self.dense_k(in_repr)
#         V = self.dense_v(in_repr)
#         G = self.dense_g(in_repr)
#         affine = torch.einsum("s r h c, s R h c->s r R h", Q, K)
#         total_bias = rearrange((mask - 1.) * 1E10, "s r -> s r () ()")
#         if bias is not None:
#             total_bias = total_bias + bias
#         affine = self.softmax(affine + total_bias)
#
#         out_repr = torch.einsum("s q v h,s v h c->s q h c", affine, V)
#         out_repr = self.dense_o(out_repr * G)
#         return out_repr


# class Attention(nn.Module):
#     def __init__(self):
#         super().__init__()
#
#     def forward(self,Q:torch.Tensor,K:torch.Tensor,V:torch.Tensor,bias:torch.Tensor):
#         ''' The mask is inherit in bias '''


# class PairAttention(nn.Module):
#     def __init__(self, cm: int, h: int, c: int, row_mode: bool = True, bias: bool = False):
#         super().__init__()
#         self.row_mode = row_mode
#         self.c = c
#         self.norm_in = nn.LayerNorm(cm)
#         self.dense_q = Dense(cm, [h, c], bias=False)
#         self.dense_k = Dense(cm, [h, c], bias=False)
#         self.dense_v = Dense(cm, [h, c], bias=False)
#         self.dense_g = Dense(cm, [h, c], act="sigmoid")  # gate
#         # print(self.dense_g)
#         self.dense_o = Dense([h, c], cm)
#         self.softmax = nn.Softmax(dim=-2)
#         # self.chunk_slices = get_chunk_slices(s, chunk_size) if self.row_mode else get_chunk_slices(r, chunk_size)
#
#     def forward(self, in_repr: torch.Tensor, bias: Optional[torch.Tensor] = None) -> torch.Tensor:
#         '''
#         We need to be care that the mask is inherit in bias
#         :param in_repr: [s, r ,cm]
#         :param bias: [r, r, cm, *]
#         :return:
#         '''
#         if not self.row_mode:
#             in_repr = in_repr.transpose(-2, -3)
#             bias = bias.transpose(-2, -3)
#         out_repr = self.norm_in(in_repr)
#         q = self.dense_q(out_repr) / math.sqrt(self.c)
#         k = self.dense_k(out_repr)
#         v = self.dense_v(out_repr)
#         g = self.dense_g(out_repr)
#         out_repr = torch.einsum("sqhc,svhc->sqvh", q, k)
#         if bias is not None:
#             out_repr = out_repr + bias
#         out_repr = self.softmax(out_repr)
#         out_repr = torch.einsum("sqvh,svhc->sqhc", out_repr, v)
#         out_repr = self.dense_o(out_repr * g)
#         if not self.row_mode:
#             out_repr = out_repr.transpose(-2, -3)
#         return out_repr

# def forward(self, in_repr: torch.Tensor, bias: Optional[torch.Tensor] = None) -> torch.Tensor:
#     out_repr = torch.empty_like(in_repr)
#
#     for chunk_id, chunk_slice in enumerate(self.chunk_slices):
#         print("chunk size", chunk_slice, torch.cuda.memory_allocated())
#         if self.row_mode:
#             out_repr[chunk_slice, :, :] = self.chunk_forward(in_repr[chunk_slice, :, :], bias)
#         else:
#             out_repr[:, chunk_slice, :] = self.chunk_forward(in_repr[:, chunk_slice, :], bias)
#
#     return out_repr
