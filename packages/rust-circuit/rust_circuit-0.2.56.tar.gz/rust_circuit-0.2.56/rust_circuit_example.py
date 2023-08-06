# %%
import uuid

import torch

from rust_circuit import Einsum, ScalarConstant, ArrayConstant, Symbol, Add, Rearrange, RearrangeSpec, Concat, Index

# %%

x = Einsum(
    (ScalarConstant(0.2), ()),
    (Symbol((3, 4, 5), uuid.uuid4()), (0, 1, 2)),
    (ArrayConstant(torch.randn(3, 4, 5)), (0, 1, 2)),
    out_axes=(2, 0),
    name="hi",
)
print(x.out_axes)

assert x == x
x

# %%

x.args

# %%

assert isinstance(x.all_input_circuits()[0], ScalarConstant)
assert isinstance(x.all_input_circuits()[1], Symbol)
assert isinstance(x.all_input_circuits()[2], ArrayConstant)

# %%

assert ScalarConstant(0.2) == ScalarConstant(0.2)
assert hash(ScalarConstant(0.2)) == hash(ScalarConstant(0.2))
assert ScalarConstant(0.2) != ScalarConstant(0.20001)
assert hash(ScalarConstant(0.2)) != hash(ScalarConstant(0.20001))
assert x == Einsum(*x.args, out_axes=x.out_axes, name=x.name)
assert x != Einsum(*x.args, out_axes=x.out_axes, name="different")

# %%

ArrayConstant(torch.randn(3, 4, 5)).value

# %%

try:
    ArrayConstant(8)  # type: ignore
except TypeError as e:
    print(e)

# %%

Symbol((3,), uuid.uuid4(), name="hi").name

# %%

try:
    Symbol((3,), uuid.uuid4().bytes, name="hi")  # type: ignore
except TypeError as e:
    print(e)

# %%

y = Add(
    [
        ScalarConstant(0.2),
        Symbol((3, 1, 5), uuid.uuid4()),
        ArrayConstant(torch.randn(3, 4, 1)),
    ]
)
print(y.nodes)
print(y)

# %%

ScalarConstant(0.5, (3, 5), name="new_scale").shape

# %%

ScalarConstant(0.5, (3, 5), name="new_scale").is_one()

# %%

ScalarConstant(1.0, (3, 5), name="new_scale").is_one()

# %%
assert (
    RearrangeSpec.fuse(RearrangeSpec([[0], [1]], [[0, 1]], [2, 15]), RearrangeSpec([[0, 1]], [[0], [1]], [10, 3]))
    is not None
)
RearrangeSpec.fuse(
    RearrangeSpec([[0], [1]], [[0], [1]], [2, 1]),
    RearrangeSpec(
        [[0], [1]],
        [[1], [0]],
        [2, 1],
    ),
)

RearrangeSpec.canonicalize(RearrangeSpec([[0, 1], [2, 3]], [[0, 1, 2, 3]], [3, 1, 1, 1]))


# %%
i = Index(ArrayConstant(torch.randn(2, 3)), (0, 1))
assert i != Index(ArrayConstant(torch.randn(2, 3)), (0, 1))
assert i == Index(i.node, (0, 1))
assert Index(i.node, (1, 0)) != Index(i.node, (0, 1))
idx = (torch.randint(0, 10, (20,)), 0)
tensor_indexed = Index(i.node, idx)
assert Index(i.node, idx) != Index(i.node, (0, 1))
assert Index(i.node, (slice(0, 1),)) == Index(i.node, (slice(0, 1),))
assert Index(i.node, (slice(None, 1),)) == Index(i.node, (slice(None, 1),))
assert Index(i.node, (slice(1, None),)) == Index(i.node, (slice(1, None),))

# assert Index(tensor_indexed.node,tensor_indexed.index)==tensor_indexed # this is failing atm bc PyObject isnt stable reference to tensor?
print(i)
print(i.index)

# %%

v1 = Concat([ArrayConstant(torch.randn(2, 3)), ArrayConstant(torch.randn(3, 3))], axis=0)
v2 = Concat(v1.nodes, axis=0)
assert v1.shape == (5, 3)
assert v1 == v2

v1 = Concat([ArrayConstant(torch.randn(3, 3)), ArrayConstant(torch.randn(3, 3))], axis=0)
v2 = Concat(v1.nodes, axis=1)
assert v1 != v2


# %%
