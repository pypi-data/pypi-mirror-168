import importlib
from functools import reduce
from operator import mul

import torch

attn_core_inplace_cuda = importlib.import_module("attn_core_inplace_cuda")

class FastSoftmax(torch.autograd.Function):
    @staticmethod
    def forward(ctx,attention_logits):
        attn_core_inplace_cuda.forward_(
            attention_logits,
            reduce(mul, attention_logits.shape[:-1]),
            attention_logits.shape[-1],
        )
        ctx.save_for_backward(attention_logits)

    @staticmethod
    def backward(ctx,grad_output):
        attention_logits = ctx.saved_tensors
        grad_v = torch.matmul(
            attention_logits.transpose(-1, -2),
            grad_output
        )
        attn_core_inplace_cuda.backward_(
            attention_logits,
            grad_output.contiguous(),
            v.contiguous(),  # v is implicitly transposed in the kernel
            reduce(mul, attention_logits.shape[:-1]),
            attention_logits.shape[-1],
            grad_output.shape[-1],
        )
