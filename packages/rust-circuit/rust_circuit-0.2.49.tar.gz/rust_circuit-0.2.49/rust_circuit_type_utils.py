# this file is included with `include_str!()` in py_types.rs
import functools
import itertools
from uuid import UUID
import torch
import torch.nn.functional
from typing import List, Tuple
import math

none = None


def check_type(x, type_v):
    if not isinstance(x, type_v):
        raise TypeError(f"expected type {repr(type_v)} but got {type(x)}")


def get_uuid_bytes(x):
    check_type(x, UUID)
    return x.bytes


def construct_uuid_bytes(b):
    return UUID(bytes=b)


def get_tensor_shape(x):
    check_type(x, torch.Tensor)
    return list(x.size())


def get_id(x):
    return id(x)


def cast_int(x):
    return int(x)


make_bytes = bytes

dtype_from_string = {
    "float32": torch.float32,
    "float64": torch.float64,
    "float16": torch.float16,
    "int64": torch.int64,
    "int32": torch.int32,
    "int16": torch.int16,
    "int8": torch.int8,
}


def scalar_to_tensor(scalar, shape, device_dtype):
    "Makes a stride 0 repeat view into a 1 element tensor"
    scalar_tensor = torch.tensor(scalar, device=device_dtype.device, dtype=dtype_from_string[device_dtype.dtype])
    return torch.broadcast_to(scalar_tensor, tuple(shape))


def tensor_scale(tensor):
    return tensor.abs().mean().cpu().item()


def cast_tensor(tensor, device_dtype):
    return tensor.to(device=device_dtype.device, dtype=dtype_from_string[device_dtype.dtype])


zero_tensor = torch.zeros(())


def un_flat_concat(tensor: torch.Tensor, shapes) -> List[torch.Tensor]:
    lens = [math.prod(x) for x in shapes]
    flats = torch.split(tensor, lens, dim=0)
    return [x.reshape(shape) for x, shape in zip(flats, shapes)]


def log_exp_p_1_fn(x: torch.Tensor):
    # piecewise to nicely handle numerics
    addr = 1.0
    return torch.where(x < 0.0, torch.log(torch.exp(x) + addr), torch.log(1.0 + torch.exp(-x) * addr) + x)


generalfunctions = {
    "gelu": torch.nn.functional.gelu,
    "relu": torch.relu,
    "sigmoid": torch.sigmoid,
    "rsqrt": torch.rsqrt,
    "reciprocal": torch.reciprocal,
    "tanh": torch.tanh,
    "softmax": functools.partial(torch.softmax, dim=-1),
    "log_softmax": functools.partial(torch.log_softmax, dim=-1),
    "log_exp_p_1": log_exp_p_1_fn,
    "gaussian_pdf": lambda x: torch.exp(-(x ** 2) / 2) / math.sqrt(2 * math.pi),
    "gaussian_cdf": lambda x: torch.distributions.normal.Normal(0, 1).cdf(x),
    "q_from_qr": lambda x: torch.linalg.qr(x)[0],
}


def make_diagonal(tensor: torch.Tensor, tensor_ints: Tuple[int, ...], out_ints: Tuple[int, ...]):
    int_sizes = {x: tensor.shape[i] for i, x in enumerate(tensor_ints)}
    deduped_shape = [int_sizes[x] for x in tensor_ints]
    result = torch.zeros(tuple(int_sizes[x] for x in out_ints), dtype=tensor.dtype, device=tensor.device)
    normal_strides_out = result.stride()
    fancy_strides = []
    for i in tensor_ints:
        indices = [j for j, x in enumerate(out_ints) if x == i]
        strides = [normal_strides_out[k] for k in indices]
        stride_here = sum(strides)
        fancy_strides.append(stride_here)
    fancy_strided = torch.as_strided(result, deduped_shape, fancy_strides)
    fancy_strided += tensor
    return result


einsum = lambda tensors_and_axes, out_axes: torch.einsum(*itertools.chain(*tensors_and_axes), out_axes)
