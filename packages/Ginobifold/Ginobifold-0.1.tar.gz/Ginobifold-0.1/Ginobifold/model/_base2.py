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


class Linear(nn.Module):
    def __init__(self,
                 dims_in: Union[List[int], int],
                 dims_out: Union[List[int], int],
                 bias: bool = True):
        super().__init__()
        self.repr = f"Linear(dims_in={dims_in}, dims_out={dims_out}, bias={bias})"
        self.bias = bias
        if isinstance(dims_in, int):
            dims_in = [dims_in]
        if isinstance(dims_out, int):
            dims_out = [dims_out]
        self.w = nn.Parameter(torch.zeros(dims_in + dims_out, dtype=torch.float))
        if bias:
            self.b = nn.Parameter(torch.zeros(dims_out, dtype=torch.float))
        self.einstr = (f"...{'ijklmn'[:len(dims_in)]},"
                       f"{'ijklmn'[:len(dims_in)]}{'abcdef'[:len(dims_out)]}"
                       f"->...{'abcdef'[:len(dims_out)]}")

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        output = torch.einsum(self.einstr, input, self.w)
        if self.bias:
            output = output + self.b
        return output


class Attention(nn.Module):
    def __init__(self, c_q: int, c_k: int, c_v: int, c_h: int, h: int, use_gate: bool = True):
        super().__init__()
        self.normsize = 1. / math.sqrt(c_h)
        self.linear_q = Linear(c_q, [h, c_h], bias=False)
        self.linear_k = Linear(c_k, [h, c_k], bias=False)
        self.linear_v = Linear(c_v, [h, c_v], bias=False)
        self.linear_o = Linear([h, c_v], c_q)
        if use_gate:
            self.linear_g = Linear(c_q, [h, c_h])

    def forward(self, q: torch.Tensor, kv: torch.Tensor, bias: Optional[torch.Tensor] = None):
        Q = self.linear_q(q) * self.normsize
        K = self.linear_k(kv)
        V = self.linear_v(kv)


