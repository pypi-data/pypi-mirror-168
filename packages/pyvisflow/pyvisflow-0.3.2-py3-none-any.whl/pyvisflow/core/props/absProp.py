from __future__ import annotations

from abc import abstractmethod
from typing import Any, Callable, List, Optional, Set, Tuple, Dict, TYPE_CHECKING, Generator, Union

from pyvisflow.utils.helper import value2code


class PropInfoNodeVisitor():

    def visit(self,propInfo:AbsPropInfo,target_type:type):

        stack:List[AbsPropInfo]=[propInfo]

        while len(stack)>0:
            target =  stack.pop()

            for v in target._ex_maybe_child():
                if isinstance(v,AbsPropInfo):
                    stack.append(v)

            if isinstance(target,target_type):
                yield target
        

class AbsPropInfo():
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def _try2expr(value:AbsPropInfo | Any):
        if isinstance(value,AbsPropInfo):
            return value.gen_expr()
        return value2code(value)


    def _ex_maybe_child(self) -> Generator:
        raise NotImplementedError()



    @abstractmethod
    def gen_expr(self) -> str:
        raise NotImplementedError()
