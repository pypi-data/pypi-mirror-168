import ast
import contextlib
import itertools
from typing import Callable, List, Optional

from pure_eval.core import Evaluator
from varname import VarnameRetrievingError
from varname.ignore import IgnoreList
from varname.utils import get_node_by_frame

from chalk.features import Filter
from chalk.utils.collections import ensure_tuple


class ChalkASTParser:
    _ignore_ast_parse_errors: bool = False

    def __init__(self, condition: Callable[[ast.AST], bool]):
        self.func_frame, self.func_node = self._get_func_frame_and_nodes(condition)
        self.evaluator = Evaluator.from_frame(self.func_frame)

    def _get_func_frame_and_nodes(self, condition: Callable[[ast.AST], bool]):
        # Start up three frames -- this function, ChalkASTParser.__init__, and the calling function
        ignore_list = IgnoreList.create(
            None,
            ignore_lambda=False,
            ignore_varname=False,
        )
        for frame_num in itertools.count(start=3):
            frame = ignore_list.get_frame(frame_num)
            func_node = get_node_by_frame(frame)
            if condition(func_node):
                # This is the correct getitem frame.
                # It is important that the "slice" isn't an ast.Name, as otherwise it would be impossible to parse the expression
                # ast.Name would imply something like this:
                # def __getitem__(self, item):
                #    return self.df[item]  # <--- item is of type ast.name. We need to go one frame higher!
                return frame, func_node
        assert False, "unreachable"

    @classmethod
    @contextlib.contextmanager
    def ignore_ast_parse_errors(cls, ignore: bool = True):
        existing = cls._ignore_ast_parse_errors
        cls._ignore_ast_parse_errors = ignore
        try:
            yield
        finally:
            cls._ignore_ast_parse_errors = existing

    @classmethod
    def parse_dataframe_getitem(cls, item) -> List:
        item = ensure_tuple(item)

        parsed_items = []
        ast_indicies = []
        for idx, queried in enumerate(item):
            if isinstance(queried, (Filter, bool)):
                ast_indicies.append(idx)

            else:
                parsed_items.append(queried)
        if len(ast_indicies) > 0:
            try:
                parser = cls(lambda node: isinstance(node, ast.Subscript) and not isinstance(node.slice, ast.Name))
            except VarnameRetrievingError as e:
                if cls._ignore_ast_parse_errors:
                    parsed_items.extend((item[i] for i in ast_indicies))
                else:
                    raise ValueError(
                        "Could not parse DataFrame item. This may happen if you're using some other AST magic at the same time, such as pytest, ipython, macropy, or birdseye. "
                        "Try declaring you DataFrame operation on a new line."
                    ) from e
            else:
                func_node = parser.func_node
                assert isinstance(func_node, ast.Subscript)
                nodes = [func_node.slice]
                if isinstance(func_node.slice, ast.Tuple):
                    nodes = func_node.slice.elts
                items = [parser._parse_node(n) for idx, n in enumerate(nodes) if idx in ast_indicies]
                for idx in ast_indicies:
                    if idx >= len(ast_indicies):
                        # Pass through anything that wasn't parsed
                        items.append(item[idx])
                parsed_items.extend(items)

        return parsed_items

    @classmethod
    def parse_when(cls) -> Optional[Filter]:
        try:
            parser = cls(lambda node: isinstance(node, ast.Call))
            func_node = parser.func_node
            when_filter = None
            assert isinstance(func_node, ast.Call)
            when = next((k for k in func_node.keywords if k.arg == "when"), None)
            when_filter = parser._parse_node(when.value) if when else None
            return when_filter
        except VarnameRetrievingError:
            return None

    def _parse_node(self, n):
        from chalk.features.feature import Filter

        if isinstance(n, ast.Name):
            return self.evaluator[n]

        if isinstance(n, ast.Attribute):
            parent = self._parse_node(n.value)
            return getattr(parent, n.attr)

        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not):
            expr = self._parse_node(n.operand)
            return Filter(expr, "not", None)

        if isinstance(n, ast.BoolOp):
            lhs = self._parse_node(n.values[0])
            rhs = self._parse_node(n.values[1])

            if isinstance(n.op, ast.And):
                return Filter(lhs, "and", rhs)

            if isinstance(n.op, ast.Or):
                return Filter(lhs, "or", rhs)

        if isinstance(n, ast.Compare):
            left = self._parse_node(n.left)
            right = self._parse_node(n.comparators[0])
            ast_op = n.ops[0]
            op = None

            if isinstance(ast_op, ast.NotIn):
                op = "not in"
            elif isinstance(ast_op, ast.In):
                op = "in"
            elif isinstance(ast_op, ast.Gt):
                op = ">"
            elif isinstance(ast_op, ast.GtE):
                op = ">="
            elif isinstance(ast_op, ast.Lt):
                op = "<"
            elif isinstance(ast_op, ast.LtE):
                op = "<="
            elif isinstance(ast_op, (ast.Eq, ast.Is)):
                op = "=="
            elif isinstance(ast_op, (ast.NotEq, ast.IsNot)):
                op = "!="

            if op:
                return Filter(feature=left, operation=op, other=right)
            else:
                raise ValueError("Invalid filter for DataFrame", ast.unparse(n))

        if isinstance(n, ast.Call):
            return eval(ast.unparse(n), self.func_frame.f_globals, self.func_frame.f_locals)

        try:
            return self.evaluator[n]
        except Exception:
            return eval(ast.unparse(n), self.func_frame.f_globals, self.func_frame.f_locals)
