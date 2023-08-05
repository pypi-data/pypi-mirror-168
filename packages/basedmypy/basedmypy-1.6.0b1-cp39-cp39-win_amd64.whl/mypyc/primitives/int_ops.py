"""Arbitrary-precision integer primitive ops.

These mostly operate on (usually) unboxed integers that use a tagged pointer
representation (CPyTagged) and correspond to the Python 'int' type.

See also the documentation for mypyc.rtypes.int_rprimitive.

Use mypyc.ir.ops.IntOp for operations on fixed-width/C integers.
"""

from __future__ import annotations

from typing import NamedTuple

from mypyc.ir.ops import ERR_ALWAYS, ERR_MAGIC, ERR_MAGIC_OVERLAPPING, ERR_NEVER, ComparisonOp
from mypyc.ir.rtypes import (
    RType,
    bit_rprimitive,
    bool_rprimitive,
    c_pyssize_t_rprimitive,
    float_rprimitive,
    int32_rprimitive,
    int64_rprimitive,
    int_rprimitive,
    object_rprimitive,
    str_rprimitive,
    void_rtype,
)
from mypyc.primitives.registry import (
    CFunctionDescription,
    binary_op,
    custom_op,
    function_op,
    load_address_op,
    unary_op,
)

# These int constructors produce object_rprimitives that then need to be unboxed
# I guess unboxing ourselves would save a check and branch though?

# Get the type object for 'builtins.int'.
# For ordinary calls to int() we use a load_address to the type
load_address_op(name="builtins.int", type=object_rprimitive, src="PyLong_Type")

# int(float). We could do a bit better directly.
function_op(
    name="builtins.int",
    arg_types=[float_rprimitive],
    return_type=object_rprimitive,
    c_function_name="CPyLong_FromFloat",
    error_kind=ERR_MAGIC,
)

# int(string)
function_op(
    name="builtins.int",
    arg_types=[str_rprimitive],
    return_type=object_rprimitive,
    c_function_name="CPyLong_FromStr",
    error_kind=ERR_MAGIC,
)

# int(string, base)
function_op(
    name="builtins.int",
    arg_types=[str_rprimitive, int_rprimitive],
    return_type=object_rprimitive,
    c_function_name="CPyLong_FromStrWithBase",
    error_kind=ERR_MAGIC,
)

# str(int)
int_to_str_op = function_op(
    name="builtins.str",
    arg_types=[int_rprimitive],
    return_type=str_rprimitive,
    c_function_name="CPyTagged_Str",
    error_kind=ERR_MAGIC,
    priority=2,
)

# We need a specialization for str on bools also since the int one is wrong...
function_op(
    name="builtins.str",
    arg_types=[bool_rprimitive],
    return_type=str_rprimitive,
    c_function_name="CPyBool_Str",
    error_kind=ERR_MAGIC,
    priority=3,
)


def int_binary_op(
    name: str,
    c_function_name: str,
    return_type: RType = int_rprimitive,
    error_kind: int = ERR_NEVER,
) -> None:
    binary_op(
        name=name,
        arg_types=[int_rprimitive, int_rprimitive],
        return_type=return_type,
        c_function_name=c_function_name,
        error_kind=error_kind,
    )


# Binary, unary and augmented assignment operations that operate on CPyTagged ints
# are implemented as C functions.

int_binary_op("+", "CPyTagged_Add")
int_binary_op("-", "CPyTagged_Subtract")
int_binary_op("*", "CPyTagged_Multiply")
int_binary_op("&", "CPyTagged_And")
int_binary_op("|", "CPyTagged_Or")
int_binary_op("^", "CPyTagged_Xor")
# Divide and remainder we honestly propagate errors from because they
# can raise ZeroDivisionError
int_binary_op("//", "CPyTagged_FloorDivide", error_kind=ERR_MAGIC)
int_binary_op("%", "CPyTagged_Remainder", error_kind=ERR_MAGIC)
# Negative shift counts raise an exception
int_binary_op(">>", "CPyTagged_Rshift", error_kind=ERR_MAGIC)
int_binary_op("<<", "CPyTagged_Lshift", error_kind=ERR_MAGIC)

# This should work because assignment operators are parsed differently
# and the code in irbuild that handles it does the assignment
# regardless of whether or not the operator works in place anyway.
int_binary_op("+=", "CPyTagged_Add")
int_binary_op("-=", "CPyTagged_Subtract")
int_binary_op("*=", "CPyTagged_Multiply")
int_binary_op("&=", "CPyTagged_And")
int_binary_op("|=", "CPyTagged_Or")
int_binary_op("^=", "CPyTagged_Xor")
int_binary_op("//=", "CPyTagged_FloorDivide", error_kind=ERR_MAGIC)
int_binary_op("%=", "CPyTagged_Remainder", error_kind=ERR_MAGIC)
int_binary_op(">>=", "CPyTagged_Rshift", error_kind=ERR_MAGIC)
int_binary_op("<<=", "CPyTagged_Lshift", error_kind=ERR_MAGIC)


def int_unary_op(name: str, c_function_name: str) -> CFunctionDescription:
    return unary_op(
        name=name,
        arg_type=int_rprimitive,
        return_type=int_rprimitive,
        c_function_name=c_function_name,
        error_kind=ERR_NEVER,
    )


int_neg_op = int_unary_op("-", "CPyTagged_Negate")
int_invert_op = int_unary_op("~", "CPyTagged_Invert")


# Primitives related to integer comparison operations:

# Description for building int comparison ops
#
# Fields:
#   binary_op_variant: identify which IntOp to use when operands are short integers
#   c_func_description: the C function to call when operands are tagged integers
#   c_func_negated: whether to negate the C function call's result
#   c_func_swap_operands: whether to swap lhs and rhs when call the function
IntComparisonOpDescription = NamedTuple(
    "IntComparisonOpDescription",
    [
        ("binary_op_variant", int),
        ("c_func_description", CFunctionDescription),
        ("c_func_negated", bool),
        ("c_func_swap_operands", bool),
    ],
)


# Equals operation on two boxed tagged integers
int_equal_ = custom_op(
    arg_types=[int_rprimitive, int_rprimitive],
    return_type=bit_rprimitive,
    c_function_name="CPyTagged_IsEq_",
    error_kind=ERR_NEVER,
)

# Less than operation on two boxed tagged integers
int_less_than_ = custom_op(
    arg_types=[int_rprimitive, int_rprimitive],
    return_type=bit_rprimitive,
    c_function_name="CPyTagged_IsLt_",
    error_kind=ERR_NEVER,
)

# Provide mapping from textual op to short int's op variant and boxed int's description.
# Note that these are not complete implementations and require extra IR.
int_comparison_op_mapping: dict[str, IntComparisonOpDescription] = {
    "==": IntComparisonOpDescription(ComparisonOp.EQ, int_equal_, False, False),
    "!=": IntComparisonOpDescription(ComparisonOp.NEQ, int_equal_, True, False),
    "<": IntComparisonOpDescription(ComparisonOp.SLT, int_less_than_, False, False),
    "<=": IntComparisonOpDescription(ComparisonOp.SLE, int_less_than_, True, True),
    ">": IntComparisonOpDescription(ComparisonOp.SGT, int_less_than_, False, True),
    ">=": IntComparisonOpDescription(ComparisonOp.SGE, int_less_than_, True, False),
}

int64_divide_op = custom_op(
    arg_types=[int64_rprimitive, int64_rprimitive],
    return_type=int64_rprimitive,
    c_function_name="CPyInt64_Divide",
    error_kind=ERR_MAGIC_OVERLAPPING,
)

int64_mod_op = custom_op(
    arg_types=[int64_rprimitive, int64_rprimitive],
    return_type=int64_rprimitive,
    c_function_name="CPyInt64_Remainder",
    error_kind=ERR_MAGIC_OVERLAPPING,
)

int32_divide_op = custom_op(
    arg_types=[int32_rprimitive, int32_rprimitive],
    return_type=int32_rprimitive,
    c_function_name="CPyInt32_Divide",
    error_kind=ERR_MAGIC_OVERLAPPING,
)

int32_mod_op = custom_op(
    arg_types=[int32_rprimitive, int32_rprimitive],
    return_type=int32_rprimitive,
    c_function_name="CPyInt32_Remainder",
    error_kind=ERR_MAGIC_OVERLAPPING,
)

# Convert tagged int (as PyObject *) to i64
int_to_int64_op = custom_op(
    arg_types=[object_rprimitive],
    return_type=int64_rprimitive,
    c_function_name="CPyLong_AsInt64",
    error_kind=ERR_MAGIC_OVERLAPPING,
)

ssize_t_to_int_op = custom_op(
    arg_types=[c_pyssize_t_rprimitive],
    return_type=int_rprimitive,
    c_function_name="CPyTagged_FromSsize_t",
    error_kind=ERR_MAGIC,
)

int64_to_int_op = custom_op(
    arg_types=[int64_rprimitive],
    return_type=int_rprimitive,
    c_function_name="CPyTagged_FromInt64",
    error_kind=ERR_MAGIC,
)

# Convert tagged int (as PyObject *) to i32
int_to_int32_op = custom_op(
    arg_types=[object_rprimitive],
    return_type=int32_rprimitive,
    c_function_name="CPyLong_AsInt32",
    error_kind=ERR_MAGIC_OVERLAPPING,
)

int32_overflow = custom_op(
    arg_types=[],
    return_type=void_rtype,
    c_function_name="CPyInt32_Overflow",
    error_kind=ERR_ALWAYS,
)
