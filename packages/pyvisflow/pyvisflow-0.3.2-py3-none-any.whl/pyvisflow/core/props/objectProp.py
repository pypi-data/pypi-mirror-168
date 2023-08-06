from __future__ import annotations

from abc import abstractmethod
from typing import Callable, Generic, List, Optional, TypeVar, Union, Tuple, Dict, TYPE_CHECKING, Generator
from pyvisflow.utils.helper import value2code
from pyvisflow.core.props.methodProp import MethodPropInfo

from .absProp import AbsPropInfo


class ObjectPropCallPropInfo(AbsPropInfo):

    def __init__(self,var:str | AbsPropInfo,prop:str,optional_chaining=True) -> None:
        super().__init__()
        self.var=var
        self.prop=prop
        self.optional_chaining=optional_chaining

    def _ex_maybe_child(self) -> Generator:
        yield self.var
        yield self.prop

    def gen_expr(self) -> str:
        var = self.var.gen_expr() if isinstance(self.var,AbsPropInfo) else str(self.var)
        return f"{var}{'?' if self.optional_chaining else ''}.{self.prop}"

class ObjectMethodCallPropInfo(MethodPropInfo):

    def __init__(self,object:AbsPropInfo, name: str, args: Optional[List] = None,optional_chaining=True) -> None:
        super().__init__(f"{object.gen_expr()}{'?' if optional_chaining else ''}.{name}", args)


