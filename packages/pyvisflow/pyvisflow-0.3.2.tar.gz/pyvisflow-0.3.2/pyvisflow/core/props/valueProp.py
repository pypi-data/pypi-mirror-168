from __future__ import annotations

from typing import Any, Callable, List, Optional, Set, Tuple, Dict, TYPE_CHECKING, Generator, Union
from pyvisflow.core.props.methodProp import LambdaPropInfo
from pyvisflow.utils.helper import value2code
from .absProp import AbsPropInfo



class ConstantsPropInfo(AbsPropInfo):
    def __init__(self,
            value:Any) -> None:
        super().__init__()
        self.value=value

    def _ex_maybe_child(self) -> Generator:
        yield self.value

    @staticmethod
    def try2PropInfo(value: Any):
        if (value is None) or isinstance(value, (float, str, int)):
            return ConstantsPropInfo( value)

        if isinstance(value, Dict):
            return JsObjectValuePropInfo( value)
        return value

    def gen_expr(self) -> str:
        return value2code(self.value)



class DictValuePropInfo(AbsPropInfo):
    def __init__(self,  value: Dict) -> None:
        super().__init__()
        self.value = value

    def _ex_maybe_child(self) -> Generator:
        yield self.value

    @staticmethod
    def try2PropInfo(value: Any):
        if isinstance(value, (dict)):
            return DictValuePropInfo( value)
        return value

    def gen_expr(self) -> str:
        def to_code(key, value):
            if not isinstance(value, (AbsPropInfo)):
                value = value2code(value)
            else:
                m = LambdaPropInfo([],value)
                value=m.gen_expr()
            return f'[{value2code(key)},{value}]'

        pairs = [to_code(key, value) for key, value in self.value.items()]
        return f"[{','.join(pairs)}]"

  


class JsObjectValuePropInfo(AbsPropInfo):
    def __init__(self,  obj: Dict) -> None:
        super().__init__()
        self.obj = obj

    def _ex_maybe_child(self) -> Generator:
        yield self.obj

    @staticmethod
    def try2PropInfo(value: Any):
        if isinstance(value, (dict)):
            return DictValuePropInfo( value)
        return value

    def gen_expr(self) -> str:
        def to_code(key, value):
            if not isinstance(value, (AbsPropInfo)):
                value = value2code(value)
            else:
                m = LambdaPropInfo([],value)
                value=m.gen_expr()
            return f'{value2code(key)}:{value}'

        pairs = [to_code(key, value) for key, value in self.obj.items()]
        return f"{{{','.join(pairs)}}}"
