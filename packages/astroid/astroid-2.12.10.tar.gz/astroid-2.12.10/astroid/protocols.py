# Licensed under the LGPL: https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html
# For details: https://github.com/PyCQA/astroid/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/astroid/blob/main/CONTRIBUTORS.txt

"""this module contains a set of functions to handle python protocols for nodes
where it makes sense.
"""

from __future__ import annotations

import collections
import itertools
import operator as operator_mod
from collections.abc import Callable, Generator
from typing import Any

from astroid import arguments, bases, decorators, helpers, nodes, util
from astroid.const import Context
from astroid.context import InferenceContext, copy_context
from astroid.exceptions import (
    AstroidIndexError,
    AstroidTypeError,
    AttributeInferenceError,
    InferenceError,
    NoDefault,
)
from astroid.nodes import node_classes
from astroid.typing import ConstFactoryResult

raw_building = util.lazy_import("raw_building")
objects = util.lazy_import("objects")


def _reflected_name(name):
    return "__r" + name[2:]


def _augmented_name(name):
    return "__i" + name[2:]


_CONTEXTLIB_MGR = "contextlib.contextmanager"
BIN_OP_METHOD = {
    "+": "__add__",
    "-": "__sub__",
    "/": "__truediv__",
    "//": "__floordiv__",
    "*": "__mul__",
    "**": "__pow__",
    "%": "__mod__",
    "&": "__and__",
    "|": "__or__",
    "^": "__xor__",
    "<<": "__lshift__",
    ">>": "__rshift__",
    "@": "__matmul__",
}

REFLECTED_BIN_OP_METHOD = {
    key: _reflected_name(value) for (key, value) in BIN_OP_METHOD.items()
}
AUGMENTED_OP_METHOD = {
    key + "=": _augmented_name(value) for (key, value) in BIN_OP_METHOD.items()
}

UNARY_OP_METHOD = {
    "+": "__pos__",
    "-": "__neg__",
    "~": "__invert__",
    "not": None,  # XXX not '__nonzero__'
}
_UNARY_OPERATORS: dict[str, Callable[[Any], Any]] = {
    "+": operator_mod.pos,
    "-": operator_mod.neg,
    "~": operator_mod.invert,
    "not": operator_mod.not_,
}


def _infer_unary_op(obj: Any, op: str) -> ConstFactoryResult:
    """Perform unary operation on `obj`, unless it is `NotImplemented`.

    Can raise TypeError if operation is unsupported.
    """
    if obj is NotImplemented:
        value = obj
    else:
        func = _UNARY_OPERATORS[op]
        value = func(obj)
    return nodes.const_factory(value)


nodes.Tuple.infer_unary_op = lambda self, op: _infer_unary_op(tuple(self.elts), op)
nodes.List.infer_unary_op = lambda self, op: _infer_unary_op(self.elts, op)
nodes.Set.infer_unary_op = lambda self, op: _infer_unary_op(set(self.elts), op)
nodes.Const.infer_unary_op = lambda self, op: _infer_unary_op(self.value, op)
nodes.Dict.infer_unary_op = lambda self, op: _infer_unary_op(dict(self.items), op)

# Binary operations

BIN_OP_IMPL = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "/": lambda a, b: a / b,
    "//": lambda a, b: a // b,
    "*": lambda a, b: a * b,
    "**": lambda a, b: a**b,
    "%": lambda a, b: a % b,
    "&": lambda a, b: a & b,
    "|": lambda a, b: a | b,
    "^": lambda a, b: a ^ b,
    "<<": lambda a, b: a << b,
    ">>": lambda a, b: a >> b,
    "@": operator_mod.matmul,
}
for _KEY, _IMPL in list(BIN_OP_IMPL.items()):
    BIN_OP_IMPL[_KEY + "="] = _IMPL


@decorators.yes_if_nothing_inferred
def const_infer_binary_op(self, opnode, operator, other, context, _):
    not_implemented = nodes.Const(NotImplemented)
    if isinstance(other, nodes.Const):
        if (
            operator == "**"
            and isinstance(self, nodes.Const)
            and isinstance(self.value, (int, float))
            and isinstance(other.value, (int, float))
            and (self.value > 1e5 or other.value > 1e5)
        ):
            yield not_implemented
            return
        try:
            impl = BIN_OP_IMPL[operator]
            try:
                yield nodes.const_factory(impl(self.value, other.value))
            except TypeError:
                # ArithmeticError is not enough: float >> float is a TypeError
                yield not_implemented
            except Exception:  # pylint: disable=broad-except
                yield util.Uninferable
        except TypeError:
            yield not_implemented
    elif isinstance(self.value, str) and operator == "%":
        # TODO(cpopa): implement string interpolation later on.
        yield util.Uninferable
    else:
        yield not_implemented


nodes.Const.infer_binary_op = const_infer_binary_op


def _multiply_seq_by_int(self, opnode, other, context):
    node = self.__class__(parent=opnode)
    filtered_elts = (
        helpers.safe_infer(elt, context) or util.Uninferable
        for elt in self.elts
        if elt is not util.Uninferable
    )
    node.elts = list(filtered_elts) * other.value
    return node


def _filter_uninferable_nodes(elts, context):
    for elt in elts:
        if elt is util.Uninferable:
            yield nodes.Unknown()
        else:
            for inferred in elt.infer(context):
                if inferred is not util.Uninferable:
                    yield inferred
                else:
                    yield nodes.Unknown()


@decorators.yes_if_nothing_inferred
def tl_infer_binary_op(
    self,
    opnode: nodes.BinOp,
    operator: str,
    other: nodes.NodeNG,
    context: InferenceContext,
    method: nodes.FunctionDef,
) -> Generator[nodes.NodeNG | type[util.Uninferable], None, None]:
    """Infer a binary operation on a tuple or list.

    The instance on which the binary operation is performed is a tuple
    or list. This refers to the left-hand side of the operation, so:
    'tuple() + 1' or '[] + A()'
    """
    # For tuples and list the boundnode is no longer the tuple or list instance
    context.boundnode = None
    not_implemented = nodes.Const(NotImplemented)
    if isinstance(other, self.__class__) and operator == "+":
        node = self.__class__(parent=opnode)
        node.elts = list(
            itertools.chain(
                _filter_uninferable_nodes(self.elts, context),
                _filter_uninferable_nodes(other.elts, context),
            )
        )
        yield node
    elif isinstance(other, nodes.Const) and operator == "*":
        if not isinstance(other.value, int):
            yield not_implemented
            return
        yield _multiply_seq_by_int(self, opnode, other, context)
    elif isinstance(other, bases.Instance) and operator == "*":
        # Verify if the instance supports __index__.
        as_index = helpers.class_instance_as_index(other)
        if not as_index:
            yield util.Uninferable
        else:
            yield _multiply_seq_by_int(self, opnode, as_index, context)
    else:
        yield not_implemented


nodes.Tuple.infer_binary_op = tl_infer_binary_op
nodes.List.infer_binary_op = tl_infer_binary_op


@decorators.yes_if_nothing_inferred
def instance_class_infer_binary_op(self, opnode, operator, other, context, method):
    return method.infer_call_result(self, context)


bases.Instance.infer_binary_op = instance_class_infer_binary_op
nodes.ClassDef.infer_binary_op = instance_class_infer_binary_op


# assignment ##################################################################

"""the assigned_stmts method is responsible to return the assigned statement
(e.g. not inferred) according to the assignment type.

The `assign_path` argument is used to record the lhs path of the original node.
For instance if we want assigned statements for 'c' in 'a, (b,c)', assign_path
will be [1, 1] once arrived to the Assign node.

The `context` argument is the current inference context which should be given
to any intermediary inference necessary.
"""


def _resolve_looppart(parts, assign_path, context):
    """recursive function to resolve multiple assignments on loops"""
    assign_path = assign_path[:]
    index = assign_path.pop(0)
    for part in parts:
        if part is util.Uninferable:
            continue
        if not hasattr(part, "itered"):
            continue
        try:
            itered = part.itered()
        except TypeError:
            continue
        try:
            if isinstance(itered[index], (nodes.Const, nodes.Name)):
                itered = [part]
        except IndexError:
            pass
        for stmt in itered:
            index_node = nodes.Const(index)
            try:
                assigned = stmt.getitem(index_node, context)
            except (AttributeError, AstroidTypeError, AstroidIndexError):
                continue
            if not assign_path:
                # we achieved to resolved the assignment path,
                # don't infer the last part
                yield assigned
            elif assigned is util.Uninferable:
                break
            else:
                # we are not yet on the last part of the path
                # search on each possibly inferred value
                try:
                    yield from _resolve_looppart(
                        assigned.infer(context), assign_path, context
                    )
                except InferenceError:
                    break


@decorators.raise_if_nothing_inferred
def for_assigned_stmts(
    self: nodes.For | nodes.Comprehension,
    node: node_classes.AssignedStmtsPossibleNode = None,
    context: InferenceContext | None = None,
    assign_path: list[int] | None = None,
) -> Any:
    if isinstance(self, nodes.AsyncFor) or getattr(self, "is_async", False):
        # Skip inferring of async code for now
        return dict(node=self, unknown=node, assign_path=assign_path, context=context)
    if assign_path is None:
        for lst in self.iter.infer(context):
            if isinstance(lst, (nodes.Tuple, nodes.List)):
                yield from lst.elts
    else:
        yield from _resolve_looppart(self.iter.infer(context), assign_path, context)
    return dict(node=self, unknown=node, assign_path=assign_path, context=context)


nodes.For.assigned_stmts = for_assigned_stmts
nodes.Comprehension.assigned_stmts = for_assigned_stmts


def sequence_assigned_stmts(
    self: nodes.Tuple | nodes.List,
    node: node_classes.AssignedStmtsPossibleNode = None,
    context: InferenceContext | None = None,
    assign_path: list[int] | None = None,
) -> Any:
    if assign_path is None:
        assign_path = []
    try:
        index = self.elts.index(node)  # type: ignore[arg-type]
    except ValueError as exc:
        raise InferenceError(
            "Tried to retrieve a node {node!r} which does not exist",
            node=self,
            assign_path=assign_path,
            context=context,
        ) from exc

    assign_path.insert(0, index)
    return self.parent.assigned_stmts(
        node=self, context=context, assign_path=assign_path
    )


nodes.Tuple.assigned_stmts = sequence_assigned_stmts
nodes.List.assigned_stmts = sequence_assigned_stmts


def assend_assigned_stmts(
    self: nodes.AssignName | nodes.AssignAttr,
    node: node_classes.AssignedStmtsPossibleNode = None,
    context: InferenceContext | None = None,
    assign_path: list[int] | None = None,
) -> Any:
    return self.parent.assigned_stmts(node=self, context=context)


nodes.AssignName.assigned_stmts = assend_assigned_stmts
nodes.AssignAttr.assigned_stmts = assend_assigned_stmts


def _arguments_infer_argname(self, name, context):
    # arguments information may be missing, in which case we can't do anything
    # more
    if not (self.arguments or self.vararg or self.kwarg):
        yield util.Uninferable
        return

    functype = self.parent.type
    # first argument of instance/class method
    if (
        self.arguments
        and getattr(self.arguments[0], "name", None) == name
        and functype != "staticmethod"
    ):
        cls = self.parent.parent.scope()
        is_metaclass = isinstance(cls, nodes.ClassDef) and cls.type == "metaclass"
        # If this is a metaclass, then the first argument will always
        # be the class, not an instance.
        if context.boundnode and isinstance(context.boundnode, bases.Instance):
            cls = context.boundnode._proxied
        if is_metaclass or functype == "classmethod":
            yield cls
            return
        if functype == "method":
            yield cls.instantiate_class()
            return

    if context and context.callcontext:
        callee = context.callcontext.callee
        while hasattr(callee, "_proxied"):
            callee = callee._proxied
        if getattr(callee, "name", None) == self.parent.name:
            call_site = arguments.CallSite(context.callcontext, context.extra_context)
            yield from call_site.infer_argument(self.parent, name, context)
            return

    if name == self.vararg:
        vararg = nodes.const_factory(())
        vararg.parent = self
        if not self.arguments and self.parent.name == "__init__":
            cls = self.parent.parent.scope()
            vararg.elts = [cls.instantiate_class()]
        yield vararg
        return
    if name == self.kwarg:
        kwarg = nodes.const_factory({})
        kwarg.parent = self
        yield kwarg
        return
    # if there is a default value, yield it. And then yield Uninferable to reflect
    # we can't guess given argument value
    try:
        context = copy_context(context)
        yield from self.default_value(name).infer(context)
        yield util.Uninferable
    except NoDefault:
        yield util.Uninferable


def arguments_assigned_stmts(
    self: nodes.Arguments,
    node: node_classes.AssignedStmtsPossibleNode = None,
    context: InferenceContext | None = None,
    assign_path: list[int] | None = None,
) -> Any:
    try:
        node_name = node.name  # type: ignore[union-attr]
    except AttributeError:
        # Added to handle edge cases where node.name is not defined.
        # https://github.com/PyCQA/astroid/pull/1644#discussion_r901545816
        node_name = None  # pragma: no cover

    if context and context.callcontext:
        callee = context.callcontext.callee
        while hasattr(callee, "_proxied"):
            callee = callee._proxied
    else:
        return _arguments_infer_argname(self, node_name, context)
    if node and getattr(callee, "name", None) == node.frame(future=True).name:
        # reset call context/name
        callcontext = context.callcontext
        context = copy_context(context)
        context.callcontext = None
        args = arguments.CallSite(callcontext, context=context)
        return args.infer_argument(self.parent, node_name, context)
    return _arguments_infer_argname(self, node_name, context)


nodes.Arguments.assigned_stmts = arguments_assigned_stmts


@decorators.raise_if_nothing_inferred
def assign_assigned_stmts(
    self: nodes.AugAssign | nodes.Assign | nodes.AnnAssign,
    node: node_classes.AssignedStmtsPossibleNode = None,
    context: InferenceContext | None = None,
    assign_path: list[int] | None = None,
) -> Any:
    if not assign_path:
        yield self.value
        return None
    yield from _resolve_assignment_parts(
        self.value.infer(context), assign_path, context
    )

    return dict(node=self, unknown=node, assign_path=assign_path, context=context)


def assign_annassigned_stmts(
    self: nodes.AnnAssign,
    node: node_classes.AssignedStmtsPossibleNode = None,
    context: InferenceContext | None = None,
    assign_path: list[int] | None = None,
) -> Any:
    for inferred in assign_assigned_stmts(self, node, context, assign_path):
        if inferred is None:
            yield util.Uninferable
        else:
            yield inferred


nodes.Assign.assigned_stmts = assign_assigned_stmts
nodes.AnnAssign.assigned_stmts = assign_annassigned_stmts
nodes.AugAssign.assigned_stmts = assign_assigned_stmts


def _resolve_assignment_parts(parts, assign_path, context):
    """recursive function to resolve multiple assignments"""
    assign_path = assign_path[:]
    index = assign_path.pop(0)
    for part in parts:
        assigned = None
        if isinstance(part, nodes.Dict):
            # A dictionary in an iterating context
            try:
                assigned, _ = part.items[index]
            except IndexError:
                return

        elif hasattr(part, "getitem"):
            index_node = nodes.Const(index)
            try:
                assigned = part.getitem(index_node, context)
            except (AstroidTypeError, AstroidIndexError):
                return

        if not assigned:
            return

        if not assign_path:
            # we achieved to resolved the assignment path, don't infer the
            # last part
            yield assigned
        elif assigned is util.Uninferable:
            return
        else:
            # we are not yet on the last part of the path search on each
            # possibly inferred value
            try:
                yield from _resolve_assignment_parts(
                    assigned.infer(context), assign_path, context
                )
            except InferenceError:
                return


@decorators.raise_if_nothing_inferred
def excepthandler_assigned_stmts(
    self: nodes.ExceptHandler,
    node: node_classes.AssignedStmtsPossibleNode = None,
    context: InferenceContext | None = None,
    assign_path: list[int] | None = None,
) -> Any:
    for assigned in node_classes.unpack_infer(self.type):
        if isinstance(assigned, nodes.ClassDef):
            assigned = objects.ExceptionInstance(assigned)

        yield assigned
    return dict(node=self, unknown=node, assign_path=assign_path, context=context)


nodes.ExceptHandler.assigned_stmts = excepthandler_assigned_stmts


def _infer_context_manager(self, mgr, context):
    try:
        inferred = next(mgr.infer(context=context))
    except StopIteration as e:
        raise InferenceError(node=mgr) from e
    if isinstance(inferred, bases.Generator):
        # Check if it is decorated with contextlib.contextmanager.
        func = inferred.parent
        if not func.decorators:
            raise InferenceError(
                "No decorators found on inferred generator %s", node=func
            )

        for decorator_node in func.decorators.nodes:
            decorator = next(decorator_node.infer(context=context), None)
            if isinstance(decorator, nodes.FunctionDef):
                if decorator.qname() == _CONTEXTLIB_MGR:
                    break
        else:
            # It doesn't interest us.
            raise InferenceError(node=func)
        try:
            yield next(inferred.infer_yield_types())
        except StopIteration as e:
            raise InferenceError(node=func) from e

    elif isinstance(inferred, bases.Instance):
        try:
            enter = next(inferred.igetattr("__enter__", context=context))
        except (InferenceError, AttributeInferenceError, StopIteration) as exc:
            raise InferenceError(node=inferred) from exc
        if not isinstance(enter, bases.BoundMethod):
            raise InferenceError(node=enter)
        yield from enter.infer_call_result(self, context)
    else:
        raise InferenceError(node=mgr)


@decorators.raise_if_nothing_inferred
def with_assigned_stmts(
    self: nodes.With,
    node: node_classes.AssignedStmtsPossibleNode = None,
    context: InferenceContext | None = None,
    assign_path: list[int] | None = None,
) -> Any:
    """Infer names and other nodes from a *with* statement.

    This enables only inference for name binding in a *with* statement.
    For instance, in the following code, inferring `func` will return
    the `ContextManager` class, not whatever ``__enter__`` returns.
    We are doing this intentionally, because we consider that the context
    manager result is whatever __enter__ returns and what it is binded
    using the ``as`` keyword.

        class ContextManager(object):
            def __enter__(self):
                return 42
        with ContextManager() as f:
            pass

        # ContextManager().infer() will return ContextManager
        # f.infer() will return 42.

    Arguments:
        self: nodes.With
        node: The target of the assignment, `as (a, b)` in `with foo as (a, b)`.
        context: Inference context used for caching already inferred objects
        assign_path:
            A list of indices, where each index specifies what item to fetch from
            the inference results.
    """
    try:
        mgr = next(mgr for (mgr, vars) in self.items if vars == node)
    except StopIteration:
        return None
    if assign_path is None:
        yield from _infer_context_manager(self, mgr, context)
    else:
        for result in _infer_context_manager(self, mgr, context):
            # Walk the assign_path and get the item at the final index.
            obj = result
            for index in assign_path:
                if not hasattr(obj, "elts"):
                    raise InferenceError(
                        "Wrong type ({targets!r}) for {node!r} assignment",
                        node=self,
                        targets=node,
                        assign_path=assign_path,
                        context=context,
                    )
                try:
                    obj = obj.elts[index]
                except IndexError as exc:
                    raise InferenceError(
                        "Tried to infer a nonexistent target with index {index} "
                        "in {node!r}.",
                        node=self,
                        targets=node,
                        assign_path=assign_path,
                        context=context,
                    ) from exc
                except TypeError as exc:
                    raise InferenceError(
                        "Tried to unpack a non-iterable value in {node!r}.",
                        node=self,
                        targets=node,
                        assign_path=assign_path,
                        context=context,
                    ) from exc
            yield obj
    return dict(node=self, unknown=node, assign_path=assign_path, context=context)


nodes.With.assigned_stmts = with_assigned_stmts


@decorators.raise_if_nothing_inferred
def named_expr_assigned_stmts(
    self: nodes.NamedExpr,
    node: node_classes.AssignedStmtsPossibleNode,
    context: InferenceContext | None = None,
    assign_path: list[int] | None = None,
) -> Any:
    """Infer names and other nodes from an assignment expression"""
    if self.target == node:
        yield from self.value.infer(context=context)
    else:
        raise InferenceError(
            "Cannot infer NamedExpr node {node!r}",
            node=self,
            assign_path=assign_path,
            context=context,
        )


nodes.NamedExpr.assigned_stmts = named_expr_assigned_stmts


@decorators.yes_if_nothing_inferred
def starred_assigned_stmts(
    self: nodes.Starred,
    node: node_classes.AssignedStmtsPossibleNode = None,
    context: InferenceContext | None = None,
    assign_path: list[int] | None = None,
) -> Any:
    """
    Arguments:
        self: nodes.Starred
        node: a node related to the current underlying Node.
        context: Inference context used for caching already inferred objects
        assign_path:
            A list of indices, where each index specifies what item to fetch from
            the inference results.
    """
    # pylint: disable=too-many-locals,too-many-statements
    def _determine_starred_iteration_lookups(
        starred: nodes.Starred, target: nodes.Tuple, lookups: list[tuple[int, int]]
    ) -> None:
        # Determine the lookups for the rhs of the iteration
        itered = target.itered()
        for index, element in enumerate(itered):
            if (
                isinstance(element, nodes.Starred)
                and element.value.name == starred.value.name
            ):
                lookups.append((index, len(itered)))
                break
            if isinstance(element, nodes.Tuple):
                lookups.append((index, len(element.itered())))
                _determine_starred_iteration_lookups(starred, element, lookups)

    stmt = self.statement(future=True)
    if not isinstance(stmt, (nodes.Assign, nodes.For)):
        raise InferenceError(
            "Statement {stmt!r} enclosing {node!r} must be an Assign or For node.",
            node=self,
            stmt=stmt,
            unknown=node,
            context=context,
        )

    if context is None:
        context = InferenceContext()

    if isinstance(stmt, nodes.Assign):
        value = stmt.value
        lhs = stmt.targets[0]
        if not isinstance(lhs, nodes.BaseContainer):
            yield util.Uninferable
            return

        if sum(1 for _ in lhs.nodes_of_class(nodes.Starred)) > 1:
            raise InferenceError(
                "Too many starred arguments in the assignment targets {lhs!r}.",
                node=self,
                targets=lhs,
                unknown=node,
                context=context,
            )

        try:
            rhs = next(value.infer(context))
        except (InferenceError, StopIteration):
            yield util.Uninferable
            return
        if rhs is util.Uninferable or not hasattr(rhs, "itered"):
            yield util.Uninferable
            return

        try:
            elts = collections.deque(rhs.itered())  # type: ignore[union-attr]
        except TypeError:
            yield util.Uninferable
            return

        # Unpack iteratively the values from the rhs of the assignment,
        # until the find the starred node. What will remain will
        # be the list of values which the Starred node will represent
        # This is done in two steps, from left to right to remove
        # anything before the starred node and from right to left
        # to remove anything after the starred node.

        for index, left_node in enumerate(lhs.elts):
            if not isinstance(left_node, nodes.Starred):
                if not elts:
                    break
                elts.popleft()
                continue
            lhs_elts = collections.deque(reversed(lhs.elts[index:]))
            for right_node in lhs_elts:
                if not isinstance(right_node, nodes.Starred):
                    if not elts:
                        break
                    elts.pop()
                    continue

                # We're done unpacking.
                packed = nodes.List(
                    ctx=Context.Store,
                    parent=self,
                    lineno=lhs.lineno,
                    col_offset=lhs.col_offset,
                )
                packed.postinit(elts=list(elts))
                yield packed
                break

    if isinstance(stmt, nodes.For):
        try:
            inferred_iterable = next(stmt.iter.infer(context=context))
        except (InferenceError, StopIteration):
            yield util.Uninferable
            return
        if inferred_iterable is util.Uninferable or not hasattr(
            inferred_iterable, "itered"
        ):
            yield util.Uninferable
            return
        try:
            itered = inferred_iterable.itered()  # type: ignore[union-attr]
        except TypeError:
            yield util.Uninferable
            return

        target = stmt.target

        if not isinstance(target, nodes.Tuple):
            raise InferenceError(
                "Could not make sense of this, the target must be a tuple",
                context=context,
            )

        lookups: list[tuple[int, int]] = []
        _determine_starred_iteration_lookups(self, target, lookups)
        if not lookups:
            raise InferenceError(
                "Could not make sense of this, needs at least a lookup", context=context
            )

        # Make the last lookup a slice, since that what we want for a Starred node
        last_element_index, last_element_length = lookups[-1]
        is_starred_last = last_element_index == (last_element_length - 1)

        lookup_slice = slice(
            last_element_index,
            None if is_starred_last else (last_element_length - last_element_index),
        )
        last_lookup = lookup_slice

        for element in itered:

            # We probably want to infer the potential values *for each* element in an
            # iterable, but we can't infer a list of all values, when only a list of
            # step values are expected:
            #
            # for a, *b in [...]:
            #   b
            #
            # *b* should now point to just the elements at that particular iteration step,
            # which astroid can't know about.

            found_element = None
            for index, lookup in enumerate(lookups):
                if not hasattr(element, "itered"):
                    break
                if index + 1 is len(lookups):
                    cur_lookup: slice | int = last_lookup
                else:
                    # Grab just the index, not the whole length
                    cur_lookup = lookup[0]
                try:
                    itered_inner_element = element.itered()
                    element = itered_inner_element[cur_lookup]
                except IndexError:
                    break
                except TypeError:
                    # Most likely the itered() call failed, cannot make sense of this
                    yield util.Uninferable
                    return
                else:
                    found_element = element

            unpacked = nodes.List(
                ctx=Context.Store,
                parent=self,
                lineno=self.lineno,
                col_offset=self.col_offset,
            )
            unpacked.postinit(elts=found_element or [])
            yield unpacked
            return

        yield util.Uninferable


nodes.Starred.assigned_stmts = starred_assigned_stmts


@decorators.yes_if_nothing_inferred
def match_mapping_assigned_stmts(
    self: nodes.MatchMapping,
    node: nodes.AssignName,
    context: InferenceContext | None = None,
    assign_path: None = None,
) -> Generator[nodes.NodeNG, None, None]:
    """Return empty generator (return -> raises StopIteration) so inferred value
    is Uninferable.
    """
    return
    yield


nodes.MatchMapping.assigned_stmts = match_mapping_assigned_stmts


@decorators.yes_if_nothing_inferred
def match_star_assigned_stmts(
    self: nodes.MatchStar,
    node: nodes.AssignName,
    context: InferenceContext | None = None,
    assign_path: None = None,
) -> Generator[nodes.NodeNG, None, None]:
    """Return empty generator (return -> raises StopIteration) so inferred value
    is Uninferable.
    """
    return
    yield


nodes.MatchStar.assigned_stmts = match_star_assigned_stmts


@decorators.yes_if_nothing_inferred
def match_as_assigned_stmts(
    self: nodes.MatchAs,
    node: nodes.AssignName,
    context: InferenceContext | None = None,
    assign_path: None = None,
) -> Generator[nodes.NodeNG, None, None]:
    """Infer MatchAs as the Match subject if it's the only MatchCase pattern
    else raise StopIteration to yield Uninferable.
    """
    if (
        isinstance(self.parent, nodes.MatchCase)
        and isinstance(self.parent.parent, nodes.Match)
        and self.pattern is None
    ):
        yield self.parent.parent.subject


nodes.MatchAs.assigned_stmts = match_as_assigned_stmts
