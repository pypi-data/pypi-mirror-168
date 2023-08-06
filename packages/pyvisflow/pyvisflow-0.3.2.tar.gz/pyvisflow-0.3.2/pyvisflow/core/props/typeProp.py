from __future__ import annotations

from abc import abstractmethod
from typing import Callable, Generic, List, Optional, Set, Tuple, Dict, TYPE_CHECKING, Generator, TypeVar, Union
from pyvisflow.core.props.objectProp import ObjectMethodCallPropInfo, ObjectPropCallPropInfo
from pyvisflow.core.props.valueProp import ConstantsPropInfo

from pyvisflow.utils.helper import value2code

from .absProp import AbsPropInfo
from .combineProp import CombinePropInfo
from .methodProp import FnsMethodPropInfo, MethodPropInfo, VarPropInfo

class ValueTypePropInfo(AbsPropInfo):
    def __init__(self, value: AbsPropInfo) -> None:
        super().__init__()
        self.value=value


    def _ex_maybe_child(self) -> Generator:
        yield self.value

    def gen_expr(self) -> str:
        return self.value.gen_expr()

class ObjectGetItemPropInfo(AbsPropInfo):

    def __init__(self,var:str | AbsPropInfo,key:str | int | AbsPropInfo) -> None:
        super().__init__()

        if isinstance(var,str):
            var = VarPropInfo(var)
        self.var=var
        self.key=key

    def _ex_maybe_child(self) -> Generator:
        yield self.var
        yield self.key

    def __eq__(self, __o: Union[str, StrTypePropInfo]):
        v = None
        if isinstance(__o, str):
            v = ConstantsPropInfo(__o)
        else:
            v = __o
        cb = CombinePropInfo('==', self, v)
        return BoolTypePropInfo(cb)

    def __ne__(self, __o: Union[str, StrTypePropInfo]):
        v = None
        if isinstance(__o, str):
            v = ConstantsPropInfo(__o)
        else:
            v = __o
        cb = CombinePropInfo('!=', self, v)
        return BoolTypePropInfo(cb)


    def gen_expr(self) -> str:
        var = AbsPropInfo._try2expr(self.var)
        key = AbsPropInfo._try2expr(self.key)
        return f"{var}[{key}]"

class StrTypePropInfo(AbsPropInfo):
    def __init__(self, value: AbsPropInfo) -> None:
        super().__init__()
        self.value=value


    def _ex_maybe_child(self) -> Generator:
        yield self.value

    def __eq__(self, __o: Union[str, StrTypePropInfo]):
        v = None
        if isinstance(__o, str):
            v = ConstantsPropInfo( __o)
        else:
            v = __o
        cb = CombinePropInfo('==', self, v)
        return BoolTypePropInfo(cb)

    def __ne__(self, __o: StrTypePropInfo):
        cb = CombinePropInfo('!=', self, __o)
        return BoolTypePropInfo(cb)

    @staticmethod
    def __try2PropInfo(value:Union[str, StrTypePropInfo]) -> AbsPropInfo:
        # assert isinstance(
        #     value, (str, StrTypePropInfo)
        # ), f'type is [{type(value)}],it must be str, StrTypePropInfo'

        val = None
        if isinstance(value,str):
            val=ConstantsPropInfo(value)
        else:
            val= value

        return val

    @staticmethod
    def __Combine2str(logic: str,left:Union[str, StrTypePropInfo],right:Union[str, StrTypePropInfo]):
        left = StrTypePropInfo.__try2PropInfo(left)
        right = StrTypePropInfo.__try2PropInfo(right)
        cb = CombinePropInfo('+', left, right)
        return StrTypePropInfo(cb)

    def __add__(self, other: Union[str, StrTypePropInfo]):
        return StrTypePropInfo.__Combine2str('+',self,other)

    def __radd__(self, other: Union[str, StrTypePropInfo]):
        return StrTypePropInfo.__Combine2str('+',other,self)

    def slice(self, start: int, end: Optional[int] = None):
        m = ObjectMethodCallPropInfo(self, 'slice', [start, end])
        res = StrTypePropInfo(m)
        return res

    def toNumber(self):
        m = FnsMethodPropInfo('toNumber', [self])
        return NumberTypePropInfo(m)

    def length(self):
        m = ObjectPropCallPropInfo(self.value, 'length')
        res = NumberTypePropInfo(m)
        return res

    def gen_expr(self) -> str:
        return self.value.gen_expr()


class NumberTypePropInfo(AbsPropInfo):
    def __init__(self, value: AbsPropInfo) -> None:
        super().__init__()
        self.value=value

    def _ex_maybe_child(self) -> Generator:
        yield self.value

    def __eq__(self, other: Union[float, int, NumberTypePropInfo]):
        return self.__combine4comp('==', other)

    def __ne__(self, other: Union[float, int, NumberTypePropInfo]):
        return self.__combine4comp('!=', other)

    def __lt__(self, other: Union[float, int, NumberTypePropInfo]):
        return self.__combine4comp('<', other)

    def __le__(self, other: Union[float, int, NumberTypePropInfo]):
        return self.__combine4comp('<=', other)

    def __gt__(self, other: Union[float, int, NumberTypePropInfo]):
        return self.__combine4comp('>', other)

    def __ge__(self, other: Union[float, int, NumberTypePropInfo]):
        return self.__combine4comp('>=', other)

    def __combine(self, logic: str,
                  other: Union[float, int, NumberTypePropInfo]):
        val = None
        if isinstance(other, (float, int)):
            val = ConstantsPropInfo(other)
        else:
            val = other

        return CombinePropInfo(logic, self, val)

    def __combine4comp(self, logic: str,
                       other: Union[float, int, NumberTypePropInfo]):
        cb = self.__combine(logic, other)
        return BoolTypePropInfo(cb)

    def __combine4cal(self, logic: str,
                      other: Union[float, int, NumberTypePropInfo]):
        cb = self.__combine(logic, other)
        return NumberTypePropInfo(cb)

    def __add__(self, other: Union[float, int, NumberTypePropInfo]):
        return self.__combine4cal('+', other)

    def __radd__(self, other: Union[float, int, NumberTypePropInfo]):
        return self + other

    def __sub__(self, other: Union[float, int, NumberTypePropInfo]):
        return self.__combine4cal('-', other)

    def __rsub__(self, other: Union[float, int, NumberTypePropInfo]):
        return self - other

    def __mul__(self, other: Union[float, int, NumberTypePropInfo]):
        return self.__combine4cal('*', other)

    def __rmul__(self, other: Union[float, int, NumberTypePropInfo]):
        return self * other

    def __truediv__(self, other: Union[float, int, NumberTypePropInfo]):
        return self.__combine4cal('/', other)

    def __rtruediv__(self, other: Union[float, int, NumberTypePropInfo]):
        return self / other

    def __floordiv__(self, other: Union[float, int, NumberTypePropInfo]):
        oper1 = self.__combine4cal('/', other)
        m = MethodPropInfo('Math.floor', [oper1])
        return m

    def __rfloordiv__(self, other: Union[float, int, NumberTypePropInfo]):
        return self // other

    def toString(self):
        m = ObjectMethodCallPropInfo(self,'toString')
        return StrTypePropInfo(m)

    def gen_expr(self) -> str:
        return self.value.gen_expr()


class BoolTypePropInfo(AbsPropInfo):
    def __init__(self, value: AbsPropInfo) -> None:
        super().__init__()
        self.value=value


    def _ex_maybe_child(self) -> Generator:
        yield self.value

    def __and__(self, other: BoolTypePropInfo):
        cb = CombinePropInfo('&&', self, other)
        return BoolTypePropInfo(cb)

    def __or__(self, other: BoolTypePropInfo):
        cb = CombinePropInfo('||', self, other)
        return BoolTypePropInfo(cb)

    def gen_expr(self) -> str:
        return self.value.gen_expr()




T = TypeVar('T', str, int)
TItem = TypeVar('TItem', StrTypePropInfo, NumberTypePropInfo)


class SubscriptableTypePropInfo(AbsPropInfo, Generic[T, TItem]):
    def __init__(self, value: AbsPropInfo) -> None:
        super().__init__()
        self.value=value


    def _ex_maybe_child(self) -> Generator:
        yield self.value

    def __getitem__(self, item: Union[T, TItem]) -> TItem:
        item = ObjectGetItemPropInfo(self,item)

        if hasattr(self, '__orig_class__'):
            if self.__orig_class__.__args__[1] == StrTypePropInfo:
                return StrTypePropInfo(item)

            if self.__orig_class__.__args__[1] == NumberTypePropInfo:
                return NumberTypePropInfo(item)

        return SubscriptableTypePropInfo(item)

    def gen_expr(self) -> str:
        return self.value.gen_expr()
