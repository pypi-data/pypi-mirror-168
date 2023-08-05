"""Fixture used in type-related test cases.

It contains class TypeInfos and Type objects.
"""

from __future__ import annotations

from mypy.nodes import (
    ARG_OPT,
    ARG_POS,
    ARG_STAR,
    COVARIANT,
    MDEF,
    Block,
    ClassDef,
    FuncDef,
    SymbolTable,
    SymbolTableNode,
    TypeAlias,
    TypeInfo,
)
from mypy.semanal_shared import set_callable_name
from mypy.types import (
    AnyType,
    CallableType,
    Instance,
    LiteralType,
    NoneType,
    Type,
    TypeAliasType,
    TypeOfAny,
    TypeType,
    TypeVarLikeType,
    TypeVarTupleType,
    TypeVarType,
    UninhabitedType,
    UnionType,
)


class TypeFixture:
    """Helper class that is used as a fixture in type-related unit tests.

    The members are initialized to contain various type-related values.
    """

    def __init__(self, variance: int = COVARIANT) -> None:
        # The 'object' class
        self.oi = self.make_type_info("builtins.object")  # class object
        self.o = Instance(self.oi, [])  # object

        # Type variables (these are effectively global)

        def make_type_var(
            name: str, id: int, values: list[Type], upper_bound: Type, variance: int
        ) -> TypeVarType:
            return TypeVarType(name, name, id, values, upper_bound, variance)

        def make_type_var_tuple(name: str, id: int, upper_bound: Type) -> TypeVarTupleType:
            return TypeVarTupleType(name, name, id, upper_bound)

        self.t = make_type_var("T", 1, [], self.o, variance)  # T`1 (type variable)
        self.tf = make_type_var("T", -1, [], self.o, variance)  # T`-1 (type variable)
        self.tf2 = make_type_var("T", -2, [], self.o, variance)  # T`-2 (type variable)
        self.s = make_type_var("S", 2, [], self.o, variance)  # S`2 (type variable)
        self.s1 = make_type_var("S", 1, [], self.o, variance)  # S`1 (type variable)
        self.sf = make_type_var("S", -2, [], self.o, variance)  # S`-2 (type variable)
        self.sf1 = make_type_var("S", -1, [], self.o, variance)  # S`-1 (type variable)

        self.ts = make_type_var_tuple("Ts", 1, self.o)  # Ts`1 (type var tuple)
        self.ss = make_type_var_tuple("Ss", 2, self.o)  # Ss`2 (type var tuple)
        self.us = make_type_var_tuple("Us", 3, self.o)  # Us`3 (type var tuple)

        # Simple types
        self.anyt = AnyType(TypeOfAny.special_form)
        self.nonet = NoneType()
        self.uninhabited = UninhabitedType()

        # Abstract class TypeInfos

        # class F
        self.fi = self.make_type_info("F", is_abstract=True)

        # class F2
        self.f2i = self.make_type_info("F2", is_abstract=True)

        # class F3(F)
        self.f3i = self.make_type_info("F3", is_abstract=True, mro=[self.fi])

        # Class TypeInfos
        self.std_tuplei = self.make_type_info(
            "builtins.tuple", mro=[self.oi], typevars=["T"], variances=[COVARIANT]
        )  # class tuple
        self.type_typei = self.make_type_info("builtins.type")  # class type
        self.bool_type_info = self.make_type_info("builtins.bool")
        self.str_type_info = self.make_type_info("builtins.str")
        self.functioni = self.make_type_info("builtins.function")  # function TODO
        self.ai = self.make_type_info("A", mro=[self.oi])  # class A
        self.bi = self.make_type_info("B", mro=[self.ai, self.oi])  # class B(A)
        self.ci = self.make_type_info("C", mro=[self.ai, self.oi])  # class C(A)
        self.di = self.make_type_info("D", mro=[self.oi])  # class D
        # class E(F)
        self.ei = self.make_type_info("E", mro=[self.fi, self.oi])
        # class E2(F2, F)
        self.e2i = self.make_type_info("E2", mro=[self.f2i, self.fi, self.oi])
        # class E3(F, F2)
        self.e3i = self.make_type_info("E3", mro=[self.fi, self.f2i, self.oi])

        # Generic class TypeInfos
        # G[T]
        self.gi = self.make_type_info("G", mro=[self.oi], typevars=["T"], variances=[variance])
        # G2[T]
        self.g2i = self.make_type_info("G2", mro=[self.oi], typevars=["T"], variances=[variance])
        # H[S, T]
        self.hi = self.make_type_info(
            "H", mro=[self.oi], typevars=["S", "T"], variances=[variance, variance]
        )
        # GS[T, S] <: G[S]
        self.gsi = self.make_type_info(
            "GS",
            mro=[self.gi, self.oi],
            typevars=["T", "S"],
            variances=[variance, variance],
            bases=[Instance(self.gi, [self.s])],
        )
        # GS2[S] <: G[S]
        self.gs2i = self.make_type_info(
            "GS2",
            mro=[self.gi, self.oi],
            typevars=["S"],
            variances=[variance],
            bases=[Instance(self.gi, [self.s1])],
        )

        self.gvi = self.make_type_info("GV", mro=[self.oi], typevars=["Ts"], typevar_tuple_index=0)
        self.gv2i = self.make_type_info(
            "GV2", mro=[self.oi], typevars=["T", "Ts", "S"], typevar_tuple_index=1
        )
        # list[T]
        self.std_listi = self.make_type_info(
            "builtins.list", mro=[self.oi], typevars=["T"], variances=[variance]
        )

        # Instance types
        self.std_tuple = Instance(self.std_tuplei, [self.anyt])  # tuple
        self.type_type = Instance(self.type_typei, [])  # type
        self.function = Instance(self.functioni, [])  # function TODO
        self.str_type = Instance(self.str_type_info, [])
        self.a = Instance(self.ai, [])  # A
        self.b = Instance(self.bi, [])  # B
        self.c = Instance(self.ci, [])  # C
        self.d = Instance(self.di, [])  # D

        self.e = Instance(self.ei, [])  # E
        self.e2 = Instance(self.e2i, [])  # E2
        self.e3 = Instance(self.e3i, [])  # E3

        self.f = Instance(self.fi, [])  # F
        self.f2 = Instance(self.f2i, [])  # F2
        self.f3 = Instance(self.f3i, [])  # F3

        # Generic instance types
        self.ga = Instance(self.gi, [self.a])  # G[A]
        self.gb = Instance(self.gi, [self.b])  # G[B]
        self.gd = Instance(self.gi, [self.d])  # G[D]
        self.go = Instance(self.gi, [self.o])  # G[object]
        self.gt = Instance(self.gi, [self.t])  # G[T`1]
        self.gtf = Instance(self.gi, [self.tf])  # G[T`-1]
        self.gtf2 = Instance(self.gi, [self.tf2])  # G[T`-2]
        self.gs = Instance(self.gi, [self.s])  # G[S]
        self.gdyn = Instance(self.gi, [self.anyt])  # G[Any]
        self.gn = Instance(self.gi, [NoneType()])  # G[None]

        self.g2a = Instance(self.g2i, [self.a])  # G2[A]

        self.gsaa = Instance(self.gsi, [self.a, self.a])  # GS[A, A]
        self.gsab = Instance(self.gsi, [self.a, self.b])  # GS[A, B]
        self.gsba = Instance(self.gsi, [self.b, self.a])  # GS[B, A]

        self.gs2a = Instance(self.gs2i, [self.a])  # GS2[A]
        self.gs2b = Instance(self.gs2i, [self.b])  # GS2[B]
        self.gs2d = Instance(self.gs2i, [self.d])  # GS2[D]

        self.hab = Instance(self.hi, [self.a, self.b])  # H[A, B]
        self.haa = Instance(self.hi, [self.a, self.a])  # H[A, A]
        self.hbb = Instance(self.hi, [self.b, self.b])  # H[B, B]
        self.hts = Instance(self.hi, [self.t, self.s])  # H[T, S]
        self.had = Instance(self.hi, [self.a, self.d])  # H[A, D]
        self.hao = Instance(self.hi, [self.a, self.o])  # H[A, object]

        self.lsta = Instance(self.std_listi, [self.a])  # List[A]
        self.lstb = Instance(self.std_listi, [self.b])  # List[B]

        self.lit1 = LiteralType(1, self.a)
        self.lit2 = LiteralType(2, self.a)
        self.lit3 = LiteralType("foo", self.d)
        self.lit4 = LiteralType(4, self.a)
        self.lit1_inst = Instance(self.ai, [], last_known_value=self.lit1)
        self.lit2_inst = Instance(self.ai, [], last_known_value=self.lit2)
        self.lit3_inst = Instance(self.di, [], last_known_value=self.lit3)
        self.lit4_inst = Instance(self.ai, [], last_known_value=self.lit4)

        self.lit_str1 = LiteralType("x", self.str_type)
        self.lit_str2 = LiteralType("y", self.str_type)
        self.lit_str3 = LiteralType("z", self.str_type)
        self.lit_str1_inst = Instance(self.str_type_info, [], last_known_value=self.lit_str1)
        self.lit_str2_inst = Instance(self.str_type_info, [], last_known_value=self.lit_str2)
        self.lit_str3_inst = Instance(self.str_type_info, [], last_known_value=self.lit_str3)

        self.type_a = TypeType.make_normalized(self.a)
        self.type_b = TypeType.make_normalized(self.b)
        self.type_c = TypeType.make_normalized(self.c)
        self.type_d = TypeType.make_normalized(self.d)
        self.type_t = TypeType.make_normalized(self.t)
        self.type_any = TypeType.make_normalized(self.anyt)

        self._add_bool_dunder(self.bool_type_info)
        self._add_bool_dunder(self.ai)

    def _add_bool_dunder(self, type_info: TypeInfo) -> None:
        signature = CallableType([], [], [], Instance(self.bool_type_info, []), self.function)
        bool_func = FuncDef("__bool__", [], Block([]))
        bool_func.type = set_callable_name(signature, bool_func)
        type_info.names[bool_func.name] = SymbolTableNode(MDEF, bool_func)

    # Helper methods

    def callable(self, *a: Type) -> CallableType:
        """callable(a1, ..., an, r) constructs a callable with argument types
        a1, ... an and return type r.
        """
        return CallableType(
            list(a[:-1]), [ARG_POS] * (len(a) - 1), [None] * (len(a) - 1), a[-1], self.function
        )

    def callable_type(self, *a: Type) -> CallableType:
        """callable_type(a1, ..., an, r) constructs a callable with
        argument types a1, ... an and return type r, and which
        represents a type.
        """
        return CallableType(
            list(a[:-1]), [ARG_POS] * (len(a) - 1), [None] * (len(a) - 1), a[-1], self.type_type
        )

    def callable_default(self, min_args: int, *a: Type) -> CallableType:
        """callable_default(min_args, a1, ..., an, r) constructs a
        callable with argument types a1, ... an and return type r,
        with min_args mandatory fixed arguments.
        """
        n = len(a) - 1
        return CallableType(
            list(a[:-1]),
            [ARG_POS] * min_args + [ARG_OPT] * (n - min_args),
            [None] * n,
            a[-1],
            self.function,
        )

    def callable_var_arg(self, min_args: int, *a: Type) -> CallableType:
        """callable_var_arg(min_args, a1, ..., an, r) constructs a callable
        with argument types a1, ... *an and return type r.
        """
        n = len(a) - 1
        return CallableType(
            list(a[:-1]),
            [ARG_POS] * min_args + [ARG_OPT] * (n - 1 - min_args) + [ARG_STAR],
            [None] * n,
            a[-1],
            self.function,
        )

    def make_type_info(
        self,
        name: str,
        module_name: str | None = None,
        is_abstract: bool = False,
        mro: list[TypeInfo] | None = None,
        bases: list[Instance] | None = None,
        typevars: list[str] | None = None,
        typevar_tuple_index: int | None = None,
        variances: list[int] | None = None,
    ) -> TypeInfo:
        """Make a TypeInfo suitable for use in unit tests."""

        class_def = ClassDef(name, Block([]), None, [])
        class_def.fullname = name

        if module_name is None:
            if "." in name:
                module_name = name.rsplit(".", 1)[0]
            else:
                module_name = "__main__"

        if typevars:
            v: list[TypeVarLikeType] = []
            for id, n in enumerate(typevars, 1):
                if typevar_tuple_index is not None and id - 1 == typevar_tuple_index:
                    v.append(TypeVarTupleType(n, n, id, self.o))
                else:
                    if variances:
                        variance = variances[id - 1]
                    else:
                        variance = COVARIANT
                    v.append(TypeVarType(n, n, id, [], self.o, variance=variance))
            class_def.type_vars = v

        info = TypeInfo(SymbolTable(), class_def, module_name)
        if mro is None:
            mro = []
            if name != "builtins.object":
                mro.append(self.oi)
        info.mro = [info] + mro
        if bases is None:
            if mro:
                # By default, assume that there is a single non-generic base.
                bases = [Instance(mro[0], [])]
            else:
                bases = []
        info.bases = bases

        return info

    def def_alias_1(self, base: Instance) -> tuple[TypeAliasType, Type]:
        A = TypeAliasType(None, [])
        target = Instance(
            self.std_tuplei, [UnionType([base, A])]
        )  # A = Tuple[Union[base, A], ...]
        AN = TypeAlias(target, "__main__.A", -1, -1)
        A.alias = AN
        return A, target

    def def_alias_2(self, base: Instance) -> tuple[TypeAliasType, Type]:
        A = TypeAliasType(None, [])
        target = UnionType(
            [base, Instance(self.std_tuplei, [A])]
        )  # A = Union[base, Tuple[A, ...]]
        AN = TypeAlias(target, "__main__.A", -1, -1)
        A.alias = AN
        return A, target

    def non_rec_alias(self, target: Type) -> TypeAliasType:
        AN = TypeAlias(target, "__main__.A", -1, -1)
        return TypeAliasType(AN, [])


class InterfaceTypeFixture(TypeFixture):
    """Extension of TypeFixture that contains additional generic
    interface types."""

    def __init__(self) -> None:
        super().__init__()
        # GF[T]
        self.gfi = self.make_type_info("GF", typevars=["T"], is_abstract=True)

        # M1 <: GF[A]
        self.m1i = self.make_type_info(
            "M1", is_abstract=True, mro=[self.gfi, self.oi], bases=[Instance(self.gfi, [self.a])]
        )

        self.gfa = Instance(self.gfi, [self.a])  # GF[A]
        self.gfb = Instance(self.gfi, [self.b])  # GF[B]

        self.m1 = Instance(self.m1i, [])  # M1
