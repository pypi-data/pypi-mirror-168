# this file is included with `include_str!()` in py_types.rs

import functools
import hashlib
from typing import Tuple
import numpy as np
import torch

PER_BLOCK_THREAD_COUNT = 128


@functools.lru_cache(maxsize=None)
def get_cuda_kernels():
    import pycuda.driver as cuda  # type: ignore
    import pycuda.autoinit  # type: ignore
    from pycuda.compiler import SourceModule  # type: ignore

    # cuda hash by Peter Schmidt-Nielsen
    mod = SourceModule(
        """
    #include <cstdint>
    static const int PER_BLOCK_THREAD_COUNT = %i;
    // Constants are chunks digits of pi, but |1 to be odd.
    __device__ static const uint32_t ODD_CONSTANT32[8]= { 0x243f6a89ul, 0x85a308d3ul, 0x13198a2ful, 0x03707345ul,
    0xa4093823ul, 0x299f31d1ul, 0x082efa99ul, 0xec4e6c89ul,
    };
    #define MIX_STATE(s) do { \
        s[0] ^= s[1] >> 17; s[1] ^= s[2] >> 15; s[2] ^= s[3] >> 11; s[3] ^= s[4] >> 13; \
        s[4] ^= s[5] >> 13; s[5] ^= s[6] >> 13; s[6] ^= s[7] >> 19; s[7] ^= s[0] >> 11; \
        s[0] ^= s[5] >> 13; s[5] ^= s[2] >> 11; s[2] ^= s[7] >> 11; s[7] ^= s[4] >> 15; \
        s[4] ^= s[1] >> 19; s[1] ^= s[6] >> 17; s[6] ^= s[3] >> 19; s[3] ^= s[0] >> 13; \
        s[0] *= ODD_CONSTANT32[0]; s[1] *= ODD_CONSTANT32[1]; \
        s[2] *= ODD_CONSTANT32[2]; s[3] *= ODD_CONSTANT32[3]; \
        s[4] *= ODD_CONSTANT32[4]; s[5] *= ODD_CONSTANT32[5]; \
        s[6] *= ODD_CONSTANT32[6]; s[7] *= ODD_CONSTANT32[7]; \
    } while(0)
    __global__ void _gpuhash(
    const uint32_t* data,
    int64_t length,
    uint32_t* block_hash_buffer
    ) {
    extern __shared__ uint32_t sdata[];
    // Each CUDA block hashes one contiguous sub-block of the data -- figure out ours.
    int64_t per_block_length = (length + (int64_t) gridDim.x - 1) / (int64_t) gridDim.x;
    int64_t our_limit = min(length, (1 + (int64_t) blockIdx.x) * per_block_length);
    uint32_t state[8] = { blockIdx.x, threadIdx.x, 1, 2, 3, 4, 5, 6 };
    for (int i = 0; i < 8; i++)
        MIX_STATE(state);
    // Hash the entire sub-block, with each thread having a 256-bit state.
    for (size_t i = threadIdx.x + blockIdx.x * per_block_length; i < our_limit; i += PER_BLOCK_THREAD_COUNT) {
        state[0] ^= data[i];
        MIX_STATE(state);
        state[7] ^= data[i];
    }
    for (int i = 0; i < 8; i++)
        sdata[8 * threadIdx.x + i] = state[i];
    __syncthreads();
    // Reduce the individual thread hashes down into a single 256-bit block hash.
    #define REDUCE(n) \
        if (PER_BLOCK_THREAD_COUNT >= 2 * n) { \
        if (threadIdx.x < n) \
            for (int i = 0; i < 8; i++) \
                sdata[8 * threadIdx.x + i] ^= sdata[8 * (threadIdx.x + n) + i] * ODD_CONSTANT32[7 - i]; \
        __syncthreads(); \
        }
    static_assert(PER_BLOCK_THREAD_COUNT <= 1024, "block_size too large");
    REDUCE(512) REDUCE(256) REDUCE(128) REDUCE(64) REDUCE(32)
    REDUCE(16)  REDUCE(8)   REDUCE(4)   REDUCE(2)  REDUCE(1)
    if (threadIdx.x < 8)
        block_hash_buffer[8 * blockIdx.x + threadIdx.x] = sdata[threadIdx.x];
    }
    __global__ void _gpuhash_finalize(
    uint32_t* block_hash_buffer,
    int length,
    int tail_length,
    const uint8_t* tail
    ) {
    uint32_t state[8] = {1, 2, 3, 4, 5, 6, 7, 8};
    // Absorb all of the 256-bit block hashes.
    for (int i = 0; i < length; i++) {
        state[0] ^= block_hash_buffer[i];
        for (int j = 0; j < 2; j++)
        MIX_STATE(state);
    }
    // Absorb any extra bytes at the end. (There usually should be none.)
    for (int i = 0; i < tail_length; i++) {
        state[0] ^= tail[i];
        MIX_STATE(state);
    }
    // Final mixing, and then output the 256-bit hash.
    for (int i = 0; i < 8; i++)
        MIX_STATE(state);
    block_hash_buffer[threadIdx.x] = state[threadIdx.x];
    }
    """
        % PER_BLOCK_THREAD_COUNT
    )

    _gpuhash = mod.get_function("_gpuhash")
    _gpuhash_finalize = mod.get_function("_gpuhash_finalize")
    return (_gpuhash, _gpuhash_finalize)


dtypes_to_bytes = {
    torch.float32: b"float32",
    torch.float64: b"float64",
    torch.float16: b"float16",
    torch.int32: b"int32--",
    torch.int64: b"int64--",
}


@functools.lru_cache(maxsize=None)
def int_tuple_to_bytes(s: Tuple[int, ...], b):
    for x in s:
        b += x.to_bytes(8, "big", signed=True)
    return b


def hash_tensor(tensor):
    m = hashlib.blake2b()
    m.update(b"c3c5ce3e-7d06-4939-8340-2a7e6b2984b4")
    m.update(int_tuple_to_bytes(tensor.shape, b""))
    m.update(b"fb782993-5fe7-43ac-acc2-d57fb429c2fc")
    m.update(dtypes_to_bytes[tensor.dtype])
    m.update(str(tensor.device).encode("utf-8"))
    m.update(b"9430f5c7-3c58-4339-b863-5449a4d74ee6")
    if str(tensor.device) == "cpu":
        m.update(tensor.detach().numpy().tobytes())  # this copies, could be optimized more
    else:
        m.update(tensor.detach().cpu().numpy().tobytes())
        # try:
        #     # hash function is corrupting gpu, sad
        #     m.update(hash_tensor_contents_gpu(tensor))
        # except Exception as e:
        #     print("gpu hashing failed, maybe because cuda version < 11.4 or pycuda not installed")
        #     print(e)
        #     m.update(tensor.detach().cpu().numpy().tobytes())

    return m.digest()[:32]


def hash_tensor_contents_gpu(tensor):
    tensor = tensor.contiguous()
    data_length = tensor.element_size() * tensor.nelement()
    block_count = 32
    if data_length > 1e6:
        block_count = 64
    if data_length > 1e7:
        block_count = 128
    if data_length > 1e8:
        block_count = 256
    block_hash_buffer = torch.zeros(size=(block_count * 8,), dtype=torch.int32, device=tensor.device)
    _gpuhash, _gpuhash_finalize = get_cuda_kernels()
    tail_length = data_length % 4
    _gpuhash(
        tensor,
        np.int64(data_length // 4),
        block_hash_buffer,
        grid=(block_count, 1, 1),
        block=(PER_BLOCK_THREAD_COUNT, 1, 1),
        shared=32 * PER_BLOCK_THREAD_COUNT,
    )
    tail_ptr = tensor.storage().data_ptr() + data_length - tail_length
    _gpuhash_finalize(
        block_hash_buffer,
        np.int32(len(block_hash_buffer)),
        np.int32(tail_length),
        np.uint64(tail_ptr),
        grid=(1, 1, 1),
        block=(8, 1, 1),
    )
    b = block_hash_buffer[:8].cpu().numpy().tobytes()
    return b


if __name__ == "__main__":
    tensor1 = torch.randn(10, 10, device="cuda:0")
    hash_tensor(tensor1)
