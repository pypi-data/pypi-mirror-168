from __future__ import annotations

from abc import abstractmethod
from typing import Any, Callable, List, Optional, Set, Tuple, Dict, TYPE_CHECKING, Generator, Union

from pyvisflow.utils.helper import value2code

from .absProp import AbsPropInfo

class VarPropInfo(AbsPropInfo):

    def __init__(self,
            name:str) -> None:
        super().__init__()
        self.name=name

    def _ex_maybe_child(self) -> Generator:
        yield self.name

    def gen_expr(self) -> str:
        return self.name


class MethodPropInfo(AbsPropInfo):
    def __init__(self,
                 name: str,
                 args: Optional[List] = None) -> None:
        super().__init__()
        self.name = name
        self.args = args or []


    def _ex_maybe_child(self) -> Generator:
        yield self.name
        yield from self.args

    def gen_expr(self) -> str:
        args = [arg.gen_expr() if isinstance(arg,AbsPropInfo) else value2code(arg) for arg in self.args]
        return f"{self.name}({','.join(args)})"



class LambdaPropInfo(AbsPropInfo):

    def __init__(self,
            vars:Union[List[str],None],
            logic:AbsPropInfo) -> None:
        super().__init__()
        self.vars=vars or []
        self.logic = logic 


    def _ex_maybe_child(self) -> Generator:
        yield from self.vars
        yield self.logic

    def gen_expr(self) -> str:
        vars = ','.join(self.vars)

        varsCount=len(self.vars)
        if varsCount>1 or varsCount==0:
            vars=f"({vars})"
        return f"{vars} => {self.logic.gen_expr()}"



class FnsMethodPropInfo(MethodPropInfo):
    def __init__(self, name: str, args: Optional[List] = None) -> None:
        super().__init__(f"fns.{name}", args)


