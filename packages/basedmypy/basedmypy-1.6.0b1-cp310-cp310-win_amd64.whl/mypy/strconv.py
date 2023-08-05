"""Conversion of parse tree nodes to strings."""

from __future__ import annotations

import os
import re
from typing import TYPE_CHECKING, Any, Sequence

import mypy.nodes
from mypy.util import IdMapper, short_type
from mypy.visitor import NodeVisitor

if TYPE_CHECKING:
    import mypy.patterns


class StrConv(NodeVisitor[str]):
    """Visitor for converting a node to a human-readable string.

    For example, an MypyFile node from program '1' is converted into
    something like this:

      MypyFile:1(
        fnam
        ExpressionStmt:1(
          IntExpr(1)))
    """

    def __init__(self, show_ids: bool = False) -> None:
        self.show_ids = show_ids
        self.id_mapper: IdMapper | None = None
        if show_ids:
            self.id_mapper = IdMapper()

    def get_id(self, o: object) -> int | None:
        if self.id_mapper:
            return self.id_mapper.id(o)
        return None

    def format_id(self, o: object) -> str:
        if self.id_mapper:
            return f"<{self.get_id(o)}>"
        else:
            return ""

    def dump(self, nodes: Sequence[object], obj: mypy.nodes.Context) -> str:
        """Convert a list of items to a multiline pretty-printed string.

        The tag is produced from the type name of obj and its line
        number. See mypy.util.dump_tagged for a description of the nodes
        argument.
        """
        tag = short_type(obj) + ":" + str(obj.get_line())
        if self.show_ids:
            assert self.id_mapper is not None
            tag += f"<{self.get_id(obj)}>"
        return dump_tagged(nodes, tag, self)

    def func_helper(self, o: mypy.nodes.FuncItem) -> list[object]:
        """Return a list in a format suitable for dump() that represents the
        arguments and the body of a function. The caller can then decorate the
        array with information specific to methods, global functions or
        anonymous functions.
        """
        args: list[mypy.nodes.Var | tuple[str, list[mypy.nodes.Node]]] = []
        extra: list[tuple[str, list[mypy.nodes.Var]]] = []
        for arg in o.arguments:
            kind: mypy.nodes.ArgKind = arg.kind
            if kind.is_required():
                args.append(arg.variable)
            elif kind.is_optional():
                assert arg.initializer is not None
                args.append(("default", [arg.variable, arg.initializer]))
            elif kind == mypy.nodes.ARG_STAR:
                extra.append(("VarArg", [arg.variable]))
            elif kind == mypy.nodes.ARG_STAR2:
                extra.append(("DictVarArg", [arg.variable]))
        a: list[Any] = []
        if args:
            a.append(("Args", args))
        if o.type:
            a.append(o.type)
        if o.is_generator:
            a.append("Generator")
        a.extend(extra)
        a.append(o.body)
        return a

    # Top-level structures

    def visit_mypy_file(self, o: mypy.nodes.MypyFile) -> str:
        # Skip implicit definitions.
        a: list[Any] = [o.defs]
        if o.is_bom:
            a.insert(0, "BOM")
        # Omit path to special file with name "main". This is used to simplify
        # test case descriptions; the file "main" is used by default in many
        # test cases.
        if o.path != "main":
            # Insert path. Normalize directory separators to / to unify test
            # case# output in all platforms.
            a.insert(0, o.path.replace(os.sep, "/"))
        if o.ignored_lines:
            a.append("IgnoredLines(%s)" % ", ".join(str(line) for line in sorted(o.ignored_lines)))
        return self.dump(a, o)

    def visit_import(self, o: mypy.nodes.Import) -> str:
        a = []
        for id, as_id in o.ids:
            if as_id is not None:
                a.append(f"{id} : {as_id}")
            else:
                a.append(id)
        return f"Import:{o.line}({', '.join(a)})"

    def visit_import_from(self, o: mypy.nodes.ImportFrom) -> str:
        a = []
        for name, as_name in o.names:
            if as_name is not None:
                a.append(f"{name} : {as_name}")
            else:
                a.append(name)
        return f"ImportFrom:{o.line}({'.' * o.relative + o.id}, [{', '.join(a)}])"

    def visit_import_all(self, o: mypy.nodes.ImportAll) -> str:
        return f"ImportAll:{o.line}({'.' * o.relative + o.id})"

    # Definitions

    def visit_func_def(self, o: mypy.nodes.FuncDef) -> str:
        a = self.func_helper(o)
        a.insert(0, o.name)
        arg_kinds = {arg.kind for arg in o.arguments}
        if len(arg_kinds & {mypy.nodes.ARG_NAMED, mypy.nodes.ARG_NAMED_OPT}) > 0:
            a.insert(1, f"MaxPos({o.max_pos})")
        if o.abstract_status in (mypy.nodes.IS_ABSTRACT, mypy.nodes.IMPLICITLY_ABSTRACT):
            a.insert(-1, "Abstract")
        if o.is_static:
            a.insert(-1, "Static")
        if o.is_class:
            a.insert(-1, "Class")
        if o.is_property:
            a.insert(-1, "Property")
        return self.dump(a, o)

    def visit_overloaded_func_def(self, o: mypy.nodes.OverloadedFuncDef) -> str:
        a: Any = o.items[:]
        if o.type:
            a.insert(0, o.type)
        if o.impl:
            a.insert(0, o.impl)
        if o.is_static:
            a.insert(-1, "Static")
        if o.is_class:
            a.insert(-1, "Class")
        return self.dump(a, o)

    def visit_class_def(self, o: mypy.nodes.ClassDef) -> str:
        a: list[object] = [o.name, o.defs.body]
        # Display base types unless they are implicitly just builtins.object
        # (in this case base_type_exprs is empty).
        if o.base_type_exprs:
            if o.info and o.info.bases:
                if len(o.info.bases) != 1 or o.info.bases[0].type.fullname != "builtins.object":
                    a.insert(1, ("BaseType", o.info.bases))
            else:
                a.insert(1, ("BaseTypeExpr", o.base_type_exprs))
        if o.type_vars:
            a.insert(1, ("TypeVars", o.type_vars))
        if o.metaclass:
            a.insert(1, f"Metaclass({o.metaclass})")
        if o.decorators:
            a.insert(1, ("Decorators", o.decorators))
        if o.info and o.info._promote:
            a.insert(1, f"Promote({o.info._promote})")
        if o.info and o.info.tuple_type:
            a.insert(1, ("TupleType", [o.info.tuple_type]))
        if o.info and o.info.fallback_to_any:
            a.insert(1, "FallbackToAny")
        return self.dump(a, o)

    def visit_var(self, o: mypy.nodes.Var) -> str:
        lst = ""
        # Add :nil line number tag if no line number is specified to remain
        # compatible with old test case descriptions that assume this.
        if o.line < 0:
            lst = ":nil"
        return "Var" + lst + "(" + o.name + ")"

    def visit_global_decl(self, o: mypy.nodes.GlobalDecl) -> str:
        return self.dump([o.names], o)

    def visit_nonlocal_decl(self, o: mypy.nodes.NonlocalDecl) -> str:
        return self.dump([o.names], o)

    def visit_decorator(self, o: mypy.nodes.Decorator) -> str:
        return self.dump([o.var, o.decorators, o.func], o)

    # Statements

    def visit_block(self, o: mypy.nodes.Block) -> str:
        return self.dump(o.body, o)

    def visit_expression_stmt(self, o: mypy.nodes.ExpressionStmt) -> str:
        return self.dump([o.expr], o)

    def visit_assignment_stmt(self, o: mypy.nodes.AssignmentStmt) -> str:
        a: list[Any] = []
        if len(o.lvalues) > 1:
            a = [("Lvalues", o.lvalues)]
        else:
            a = [o.lvalues[0]]
        a.append(o.rvalue)
        if o.type:
            a.append(o.type)
        return self.dump(a, o)

    def visit_operator_assignment_stmt(self, o: mypy.nodes.OperatorAssignmentStmt) -> str:
        return self.dump([o.op, o.lvalue, o.rvalue], o)

    def visit_while_stmt(self, o: mypy.nodes.WhileStmt) -> str:
        a: list[Any] = [o.expr, o.body]
        if o.else_body:
            a.append(("Else", o.else_body.body))
        return self.dump(a, o)

    def visit_for_stmt(self, o: mypy.nodes.ForStmt) -> str:
        a: list[Any] = []
        if o.is_async:
            a.append(("Async", ""))
        a.append(o.index)
        if o.index_type:
            a.append(o.index_type)
        a.extend([o.expr, o.body])
        if o.else_body:
            a.append(("Else", o.else_body.body))
        return self.dump(a, o)

    def visit_return_stmt(self, o: mypy.nodes.ReturnStmt) -> str:
        return self.dump([o.expr], o)

    def visit_if_stmt(self, o: mypy.nodes.IfStmt) -> str:
        a: list[Any] = []
        for i in range(len(o.expr)):
            a.append(("If", [o.expr[i]]))
            a.append(("Then", o.body[i].body))

        if not o.else_body:
            return self.dump(a, o)
        else:
            return self.dump([a, ("Else", o.else_body.body)], o)

    def visit_break_stmt(self, o: mypy.nodes.BreakStmt) -> str:
        return self.dump([], o)

    def visit_continue_stmt(self, o: mypy.nodes.ContinueStmt) -> str:
        return self.dump([], o)

    def visit_pass_stmt(self, o: mypy.nodes.PassStmt) -> str:
        return self.dump([], o)

    def visit_raise_stmt(self, o: mypy.nodes.RaiseStmt) -> str:
        return self.dump([o.expr, o.from_expr], o)

    def visit_assert_stmt(self, o: mypy.nodes.AssertStmt) -> str:
        if o.msg is not None:
            return self.dump([o.expr, o.msg], o)
        else:
            return self.dump([o.expr], o)

    def visit_await_expr(self, o: mypy.nodes.AwaitExpr) -> str:
        return self.dump([o.expr], o)

    def visit_del_stmt(self, o: mypy.nodes.DelStmt) -> str:
        return self.dump([o.expr], o)

    def visit_try_stmt(self, o: mypy.nodes.TryStmt) -> str:
        a: list[Any] = [o.body]

        for i in range(len(o.vars)):
            a.append(o.types[i])
            if o.vars[i]:
                a.append(o.vars[i])
            a.append(o.handlers[i])

        if o.else_body:
            a.append(("Else", o.else_body.body))
        if o.finally_body:
            a.append(("Finally", o.finally_body.body))

        return self.dump(a, o)

    def visit_with_stmt(self, o: mypy.nodes.WithStmt) -> str:
        a: list[Any] = []
        if o.is_async:
            a.append(("Async", ""))
        for i in range(len(o.expr)):
            a.append(("Expr", [o.expr[i]]))
            if o.target[i]:
                a.append(("Target", [o.target[i]]))
        if o.unanalyzed_type:
            a.append(o.unanalyzed_type)
        return self.dump(a + [o.body], o)

    def visit_match_stmt(self, o: mypy.nodes.MatchStmt) -> str:
        a: list[Any] = [o.subject]
        for i in range(len(o.patterns)):
            a.append(("Pattern", [o.patterns[i]]))
            if o.guards[i] is not None:
                a.append(("Guard", [o.guards[i]]))
            a.append(("Body", o.bodies[i].body))
        return self.dump(a, o)

    # Expressions

    # Simple expressions

    def visit_int_expr(self, o: mypy.nodes.IntExpr) -> str:
        return f"IntExpr({o.value})"

    def visit_str_expr(self, o: mypy.nodes.StrExpr) -> str:
        return f"StrExpr({self.str_repr(o.value)})"

    def visit_bytes_expr(self, o: mypy.nodes.BytesExpr) -> str:
        return f"BytesExpr({self.str_repr(o.value)})"

    def str_repr(self, s: str) -> str:
        s = re.sub(r"\\u[0-9a-fA-F]{4}", lambda m: "\\" + m.group(0), s)
        return re.sub("[^\\x20-\\x7e]", lambda m: r"\u%.4x" % ord(m.group(0)), s)

    def visit_float_expr(self, o: mypy.nodes.FloatExpr) -> str:
        return f"FloatExpr({o.value})"

    def visit_complex_expr(self, o: mypy.nodes.ComplexExpr) -> str:
        return f"ComplexExpr({o.value})"

    def visit_ellipsis(self, o: mypy.nodes.EllipsisExpr) -> str:
        return "Ellipsis"

    def visit_star_expr(self, o: mypy.nodes.StarExpr) -> str:
        return self.dump([o.expr], o)

    def visit_name_expr(self, o: mypy.nodes.NameExpr) -> str:
        pretty = self.pretty_name(
            o.name, o.kind, o.fullname, o.is_inferred_def or o.is_special_form, o.node
        )
        if isinstance(o.node, mypy.nodes.Var) and o.node.is_final:
            pretty += f" = {o.node.final_value}"
        return short_type(o) + "(" + pretty + ")"

    def pretty_name(
        self,
        name: str,
        kind: int | None,
        fullname: str | None,
        is_inferred_def: bool,
        target_node: mypy.nodes.Node | None = None,
    ) -> str:
        n = name
        if is_inferred_def:
            n += "*"
        if target_node:
            id = self.format_id(target_node)
        else:
            id = ""
        if isinstance(target_node, mypy.nodes.MypyFile) and name == fullname:
            n += id
        elif kind == mypy.nodes.GDEF or (fullname != name and fullname is not None):
            # Append fully qualified name for global references.
            n += f" [{fullname}{id}]"
        elif kind == mypy.nodes.LDEF:
            # Add tag to signify a local reference.
            n += f" [l{id}]"
        elif kind == mypy.nodes.MDEF:
            # Add tag to signify a member reference.
            n += f" [m{id}]"
        else:
            n += id
        return n

    def visit_member_expr(self, o: mypy.nodes.MemberExpr) -> str:
        pretty = self.pretty_name(o.name, o.kind, o.fullname, o.is_inferred_def, o.node)
        return self.dump([o.expr, pretty], o)

    def visit_yield_expr(self, o: mypy.nodes.YieldExpr) -> str:
        return self.dump([o.expr], o)

    def visit_yield_from_expr(self, o: mypy.nodes.YieldFromExpr) -> str:
        if o.expr:
            return self.dump([o.expr.accept(self)], o)
        else:
            return self.dump([], o)

    def visit_call_expr(self, o: mypy.nodes.CallExpr) -> str:
        if o.analyzed:
            return o.analyzed.accept(self)
        args: list[mypy.nodes.Expression] = []
        extra: list[str | tuple[str, list[Any]]] = []
        for i, kind in enumerate(o.arg_kinds):
            if kind in [mypy.nodes.ARG_POS, mypy.nodes.ARG_STAR]:
                args.append(o.args[i])
                if kind == mypy.nodes.ARG_STAR:
                    extra.append("VarArg")
            elif kind == mypy.nodes.ARG_NAMED:
                extra.append(("KwArgs", [o.arg_names[i], o.args[i]]))
            elif kind == mypy.nodes.ARG_STAR2:
                extra.append(("DictVarArg", [o.args[i]]))
            else:
                raise RuntimeError(f"unknown kind {kind}")
        a: list[Any] = [o.callee, ("Args", args)]
        return self.dump(a + extra, o)

    def visit_op_expr(self, o: mypy.nodes.OpExpr) -> str:
        return self.dump([o.op, o.left, o.right], o)

    def visit_comparison_expr(self, o: mypy.nodes.ComparisonExpr) -> str:
        return self.dump([o.operators, o.operands], o)

    def visit_cast_expr(self, o: mypy.nodes.CastExpr) -> str:
        return self.dump([o.expr, o.type], o)

    def visit_assert_type_expr(self, o: mypy.nodes.AssertTypeExpr) -> str:
        return self.dump([o.expr, o.type], o)

    def visit_reveal_expr(self, o: mypy.nodes.RevealExpr) -> str:
        if o.kind == mypy.nodes.REVEAL_TYPE:
            return self.dump([o.expr], o)
        else:
            # REVEAL_LOCALS
            return self.dump([o.local_nodes], o)

    def visit_assignment_expr(self, o: mypy.nodes.AssignmentExpr) -> str:
        return self.dump([o.target, o.value], o)

    def visit_unary_expr(self, o: mypy.nodes.UnaryExpr) -> str:
        return self.dump([o.op, o.expr], o)

    def visit_list_expr(self, o: mypy.nodes.ListExpr) -> str:
        return self.dump(o.items, o)

    def visit_dict_expr(self, o: mypy.nodes.DictExpr) -> str:
        return self.dump([[k, v] for k, v in o.items], o)

    def visit_set_expr(self, o: mypy.nodes.SetExpr) -> str:
        return self.dump(o.items, o)

    def visit_tuple_expr(self, o: mypy.nodes.TupleExpr) -> str:
        return self.dump(o.items, o)

    def visit_index_expr(self, o: mypy.nodes.IndexExpr) -> str:
        if o.analyzed:
            return o.analyzed.accept(self)
        return self.dump([o.base, o.index], o)

    def visit_super_expr(self, o: mypy.nodes.SuperExpr) -> str:
        return self.dump([o.name, o.call], o)

    def visit_type_application(self, o: mypy.nodes.TypeApplication) -> str:
        return self.dump([o.expr, ("Types", o.types)], o)

    def visit_type_var_expr(self, o: mypy.nodes.TypeVarExpr) -> str:
        import mypy.types

        a: list[Any] = []
        if o.variance == mypy.nodes.COVARIANT:
            a += ["Variance(COVARIANT)"]
        if o.variance == mypy.nodes.CONTRAVARIANT:
            a += ["Variance(CONTRAVARIANT)"]
        if o.values:
            a += [("Values", o.values)]
        if not mypy.types.is_named_instance(o.upper_bound, "builtins.object"):
            a += [f"UpperBound({o.upper_bound})"]
        return self.dump(a, o)

    def visit_paramspec_expr(self, o: mypy.nodes.ParamSpecExpr) -> str:
        import mypy.types

        a: list[Any] = []
        if o.variance == mypy.nodes.COVARIANT:
            a += ["Variance(COVARIANT)"]
        if o.variance == mypy.nodes.CONTRAVARIANT:
            a += ["Variance(CONTRAVARIANT)"]
        if not mypy.types.is_named_instance(o.upper_bound, "builtins.object"):
            a += [f"UpperBound({o.upper_bound})"]
        return self.dump(a, o)

    def visit_type_var_tuple_expr(self, o: mypy.nodes.TypeVarTupleExpr) -> str:
        import mypy.types

        a: list[Any] = []
        if o.variance == mypy.nodes.COVARIANT:
            a += ["Variance(COVARIANT)"]
        if o.variance == mypy.nodes.CONTRAVARIANT:
            a += ["Variance(CONTRAVARIANT)"]
        if not mypy.types.is_named_instance(o.upper_bound, "builtins.object"):
            a += [f"UpperBound({o.upper_bound})"]
        return self.dump(a, o)

    def visit_type_alias_expr(self, o: mypy.nodes.TypeAliasExpr) -> str:
        return f"TypeAliasExpr({o.type})"

    def visit_namedtuple_expr(self, o: mypy.nodes.NamedTupleExpr) -> str:
        return f"NamedTupleExpr:{o.line}({o.info.name}, {o.info.tuple_type})"

    def visit_enum_call_expr(self, o: mypy.nodes.EnumCallExpr) -> str:
        return f"EnumCallExpr:{o.line}({o.info.name}, {o.items})"

    def visit_typeddict_expr(self, o: mypy.nodes.TypedDictExpr) -> str:
        return f"TypedDictExpr:{o.line}({o.info.name})"

    def visit__promote_expr(self, o: mypy.nodes.PromoteExpr) -> str:
        return f"PromoteExpr:{o.line}({o.type})"

    def visit_newtype_expr(self, o: mypy.nodes.NewTypeExpr) -> str:
        return f"NewTypeExpr:{o.line}({o.name}, {self.dump([o.old_type], o)})"

    def visit_lambda_expr(self, o: mypy.nodes.LambdaExpr) -> str:
        a = self.func_helper(o)
        return self.dump(a, o)

    def visit_generator_expr(self, o: mypy.nodes.GeneratorExpr) -> str:
        condlists = o.condlists if any(o.condlists) else None
        return self.dump([o.left_expr, o.indices, o.sequences, condlists], o)

    def visit_list_comprehension(self, o: mypy.nodes.ListComprehension) -> str:
        return self.dump([o.generator], o)

    def visit_set_comprehension(self, o: mypy.nodes.SetComprehension) -> str:
        return self.dump([o.generator], o)

    def visit_dictionary_comprehension(self, o: mypy.nodes.DictionaryComprehension) -> str:
        condlists = o.condlists if any(o.condlists) else None
        return self.dump([o.key, o.value, o.indices, o.sequences, condlists], o)

    def visit_conditional_expr(self, o: mypy.nodes.ConditionalExpr) -> str:
        return self.dump([("Condition", [o.cond]), o.if_expr, o.else_expr], o)

    def visit_slice_expr(self, o: mypy.nodes.SliceExpr) -> str:
        a: list[Any] = [o.begin_index, o.end_index, o.stride]
        if not a[0]:
            a[0] = "<empty>"
        if not a[1]:
            a[1] = "<empty>"
        return self.dump(a, o)

    def visit_temp_node(self, o: mypy.nodes.TempNode) -> str:
        return self.dump([o.type], o)

    def visit_as_pattern(self, o: mypy.patterns.AsPattern) -> str:
        return self.dump([o.pattern, o.name], o)

    def visit_or_pattern(self, o: mypy.patterns.OrPattern) -> str:
        return self.dump(o.patterns, o)

    def visit_value_pattern(self, o: mypy.patterns.ValuePattern) -> str:
        return self.dump([o.expr], o)

    def visit_singleton_pattern(self, o: mypy.patterns.SingletonPattern) -> str:
        return self.dump([o.value], o)

    def visit_sequence_pattern(self, o: mypy.patterns.SequencePattern) -> str:
        return self.dump(o.patterns, o)

    def visit_starred_pattern(self, o: mypy.patterns.StarredPattern) -> str:
        return self.dump([o.capture], o)

    def visit_mapping_pattern(self, o: mypy.patterns.MappingPattern) -> str:
        a: list[Any] = []
        for i in range(len(o.keys)):
            a.append(("Key", [o.keys[i]]))
            a.append(("Value", [o.values[i]]))
        if o.rest is not None:
            a.append(("Rest", [o.rest]))
        return self.dump(a, o)

    def visit_class_pattern(self, o: mypy.patterns.ClassPattern) -> str:
        a: list[Any] = [o.class_ref]
        if len(o.positionals) > 0:
            a.append(("Positionals", o.positionals))
        for i in range(len(o.keyword_keys)):
            a.append(("Keyword", [o.keyword_keys[i], o.keyword_values[i]]))

        return self.dump(a, o)


def dump_tagged(nodes: Sequence[object], tag: str | None, str_conv: StrConv) -> str:
    """Convert an array into a pretty-printed multiline string representation.

    The format is
      tag(
        item1..
        itemN)
    Individual items are formatted like this:
     - arrays are flattened
     - pairs (str, array) are converted recursively, so that str is the tag
     - other items are converted to strings and indented
    """
    from mypy.types import Type, TypeStrVisitor

    a: list[str] = []
    if tag:
        a.append(tag + "(")
    for n in nodes:
        if isinstance(n, list):
            if n:
                a.append(dump_tagged(n, None, str_conv))
        elif isinstance(n, tuple):
            s = dump_tagged(n[1], n[0], str_conv)
            a.append(indent(s, 2))
        elif isinstance(n, mypy.nodes.Node):
            a.append(indent(n.accept(str_conv), 2))
        elif isinstance(n, Type):
            a.append(indent(n.accept(TypeStrVisitor(str_conv.id_mapper)), 2))
        elif n is not None:
            a.append(indent(str(n), 2))
    if tag:
        a[-1] += ")"
    return "\n".join(a)


def indent(s: str, n: int) -> str:
    """Indent all the lines in s (separated by newlines) by n spaces."""
    s = " " * n + s
    s = s.replace("\n", "\n" + " " * n)
    return s
