# %%
from pdb import post_mortem
import torch
from rust_circuit import (
    Einsum,
    ScalarConstant,
    ArrayConstant,
    Symbol,
    Add,
    Rearrange,
    RearrangeSpec,
    Index,
    add_collapse_scalar_inputs,
    add_deduplicate,
    add_flatten_once,
    distribute_all,
    einsum_pull_removable_axes,
    remove_add_few_input,
    add_pull_removable_axes,
    einsum_flatten_once,
)

# %%

base_add = Add(
    [
        ScalarConstant(0.2, name="hi"),
        ScalarConstant(0.2, name="hi"),
    ]
)

nested_add = Add([base_add, base_add])
nested_add.compiler_print()
flattened = add_flatten_once(nested_add)
assert flattened is not None
flattened.compiler_print()

deduped = add_deduplicate(flattened)
assert deduped is not None
deduped.compiler_print()
deduped_2 = add_deduplicate(base_add)
assert deduped_2 is not None
deduped_2.compiler_print()

elimed = remove_add_few_input(deduped)
assert elimed is not None
elimed.compiler_print()

scalar_merged = add_collapse_scalar_inputs(
    Add(
        [
            ScalarConstant(171),
            ScalarConstant(9),
        ]
    )
)
assert scalar_merged is not None
scalar_merged.compiler_print()

scalar_merged_call = add_collapse_scalar_inputs(
    Add(
        [
            ScalarConstant(171),
            ScalarConstant(9),
        ]
    )
)
assert scalar_merged_call is not None
scalar_merged_call.compiler_print()

add_with_rearrange = Add(
    [
        Rearrange(ScalarConstant(2), RearrangeSpec([], [[0], [1]], [2, 3])),
        Rearrange(ScalarConstant(2, (2,)), RearrangeSpec([[0]], [[0], [1]], [2, 3])),
    ]
)
post_rearrange = add_pull_removable_axes(add_with_rearrange, True)
assert post_rearrange is not None
post_rearrange.compiler_print()
# %%

ein = Einsum((ScalarConstant(2, (2, 3)), (0, 1)), (ScalarConstant(3, (3, 4)), (1, 2)), out_axes=(0, 2))
ein.compiler_print()
ein_deep = Einsum((ein, (0, 1)), (ein, (0, 1)), out_axes=(0,))
ein_deep.compiler_print()
ein_flat = einsum_flatten_once(ein_deep)
assert ein_flat is not None
ein_flat.compiler_print()

# %%

for_distribute = Einsum((base_add, ()), (base_add, ()), out_axes=())

distributed = distribute_all(for_distribute)
assert distributed is not None
distributed.compiler_print()

for_pull = Einsum(
    (Rearrange(ScalarConstant(2), RearrangeSpec([], [[0], [1]], [2, 3])), (0, 1)),
    (Rearrange(ScalarConstant(2, (2,)), RearrangeSpec([[0]], [[0], [1]], [2, 3])), (0, 1)),
    out_axes=(0, 1),
)
pulled = einsum_pull_removable_axes(for_pull)
assert pulled is not None
pulled.compiler_print()

rearrange_identity = Rearrange(ScalarConstant(2, (2,)), RearrangeSpec([[0]], [[0]], [2]))
rearrange_identity_2 = Rearrange(ScalarConstant(2, (1, 1)), RearrangeSpec([[0], [1]], [[1], [0]], [1, 1]))
print(rearrange_identity.spec.is_identity())
print(rearrange_identity.spec.is_identity())
print(rearrange_identity_2.spec.is_identity())
print(rearrange_identity_2.spec.is_identity())

# %%

r1 = Rearrange(ArrayConstant(torch.randn(2, 15)), RearrangeSpec([[0], [1]], [[0, 1]], [2, 15]))
r2 = Rearrange(r1, RearrangeSpec([[0, 1]], [[0], [1]], [10, 3]))
r1.node

# %%
print(RearrangeSpec([[0], [1]], [[1], [0]], [1, 1]).canonicalize(True))

print(Einsum(out_axes=(), name=None) == Add([], None))
