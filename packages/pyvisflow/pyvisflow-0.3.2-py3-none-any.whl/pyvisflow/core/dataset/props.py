from __future__ import annotations

from typing import Any, Dict, Generator, Iterable, List,TYPE_CHECKING, Optional, Union
from pyvisflow.core.props.absProp import AbsPropInfo,PropInfoNodeVisitor
from pyvisflow.core.props.methodProp import LambdaPropInfo, MethodPropInfo
from pyvisflow.core.props.typeProp import (
    ConstantsPropInfo, 
    BoolTypePropInfo, 
    NumberTypePropInfo, 
    ObjectGetItemPropInfo, 
    StrTypePropInfo, 
    SubscriptableTypePropInfo,
    ValueTypePropInfo)


from pyvisflow.core.props.combineProp import CombinePropInfo
from pyvisflow.core.props.valueProp import DictValuePropInfo

TOther = Union[float, int,str, NumberTypePropInfo,StrTypePropInfo]

m_propInfoNodeVisitor = PropInfoNodeVisitor()





class ReactiveDatasetPropInfo(AbsPropInfo):

    def __init__(self,value:AbsPropInfo) -> None:
        super().__init__()
        self.value = value

    def _ex_maybe_child(self) -> Generator:
        yield self.value

    @property
    def values(self):
        get_col = DatasetMethodPropInfo('getValues',[self])
        return DatasetArrayPropInfo(get_col)

    @property
    def columns(self):
        get_col = DatasetMethodPropInfo('getColumns',[self])
        return SubscriptableTypePropInfo[int,StrTypePropInfo](get_col)

    def rename(self,mapping:Dict[str | int,str]):
        '''
        dataset 列名将被修改，没有指定的列保持原样

        >>> ds.rename({'oldname':'newname'})
        '''
        fn = DatasetMethodPropInfo('recolumnName',[self,DictValuePropInfo(mapping)])
        return ReactiveDatasetPropInfo(fn)


    def __getitem__(self,key:Union[str,BoolTypePropInfo,bool,List,DatasetSeriesBoolTypePropInfo]) -> ReactiveDatasetPropInfo | DatasetSeriesPropInfo:
        if isinstance(key,List):
            get_col = DatasetMethodPropInfo('getbyColumns',[self,key])
            return ReactiveDatasetPropInfo(get_col)

        if isinstance(key,DatasetSeriesBoolTypePropInfo):
            return self.filter(key)

        return DatasetSeriesPropInfo(self,key)

    def filter(self,condition:bool | DatasetSeriesBoolTypePropInfo):
        
        for ds in m_propInfoNodeVisitor.visit(condition,DatasetSeriesPropInfo):
            if isinstance(ds,DatasetSeriesPropInfo):
                ds.is_filter_mode=True

        lamd=LambdaPropInfo(['r'],condition)
        exec = DatasetMethodPropInfo(name='filter',args= [self.value,lamd])
        return ReactiveDatasetPropInfo(exec)


    def to_jsObject(self):
        '''
        表将被转换成 js 中的对象(类似python 中的字典)
        '''
        fn = DatasetMethodPropInfo('toJsObjects',[self])
        return DatasetJsObjectArrayTypePropInfo(fn) 

    def gen_expr(self) -> str:
        return self.value.gen_expr()

class DatasetMethodPropInfo(MethodPropInfo):

    def __init__(self,name:str, args: Optional[List] = None) -> None:
        super().__init__(f'ds.{name}', args)

class DatasetArrayPropInfo(AbsPropInfo):

    def __init__(self,context:AbsPropInfo) -> None:
        super().__init__()
        self.context=context

    def _ex_maybe_child(self) -> Generator:
        yield self.context

    def gen_expr(self) -> str:
        return self.context.gen_expr()


class DatasetSeriesArrayPropInfo(AbsPropInfo):

    def __init__(self,context:AbsPropInfo) -> None:
        super().__init__()
        self.context=context

    def drop_duplicates(self):
        dup =  DatasetMethodPropInfo('seriesDup',[self])
        return DatasetSeriesArrayPropInfo(dup)

    def contains(self,values: Iterable | AbsPropInfo):
        '''
        列值将被筛选，只保留在 values 中存在的值
        '''
        dup =  DatasetMethodPropInfo('seriesContains',[self,values])
        return DatasetSeriesArrayPropInfo(dup)

    def __getitem__(self,key:int):
        dup =  DatasetMethodPropInfo('seriesTakeSingle',[self,key])
        return ValueTypePropInfo(dup)

    def _ex_maybe_child(self) -> Generator:
        yield self.context

    def gen_expr(self) -> str:
        return self.context.gen_expr()

class DatasetSeriesPropInfo(DatasetSeriesArrayPropInfo):

    def __init__(self,context:AbsPropInfo,column_name:str | AbsPropInfo) -> None:
        super().__init__(context)
        self.column_name=column_name
        self.is_filter_mode=False

    def clone(self):
        return DatasetSeriesPropInfo(self.context,self.column_name)

    def _ex_maybe_child(self) -> Generator:
        yield self.column_name
        yield self.context

    def gen_expr(self) -> str:

        if self.is_filter_mode:
            return ObjectGetItemPropInfo('r',self.column_name).gen_expr()

        res = DatasetMethodPropInfo('getSeries',[self.context,self.column_name])

        return res.gen_expr()

    def __combine(self, logic: str,
                  other: TOther):
        val = None
        if isinstance(other, (float, int,str)):
            val =ConstantsPropInfo(other)
        else:
            val = other
        cb = CombinePropInfo(logic, self.clone(), val)
        return DatasetSeriesBoolTypePropInfo(cb)

    def __eq__(self, other: TOther):
        return self.__combine('==', other)

    def __ne__(self, other: TOther):
        return self.__combine('!=', other)

    def __lt__(self, other: TOther):
        return self.__combine('<', other)

    def __le__(self, other: TOther):
        return self.__combine('<=', other)

    def __gt__(self, other: TOther):
        return self.__combine('>', other)

    def __ge__(self, other: TOther):
        return self.__combine('>=', other)



class DatasetSeriesBoolTypePropInfo(AbsPropInfo):
    def __init__(self, value: AbsPropInfo) -> None:
        super().__init__()
        self.value=value

    def _ex_maybe_child(self) -> Generator:
        yield self.value

    def __and__(self, other: DatasetSeriesBoolTypePropInfo):
        cb = CombinePropInfo('&&', self, other)
        return DatasetSeriesBoolTypePropInfo(cb)

    def __or__(self, other: DatasetSeriesBoolTypePropInfo):
        cb = CombinePropInfo('||', self, other)
        return DatasetSeriesBoolTypePropInfo(cb)

    def gen_expr(self) -> str:
        return self.value.gen_expr()



class DatasetJsObjectArrayTypePropInfo(AbsPropInfo):

    def __init__(self,value:AbsPropInfo) -> None:
        super().__init__()
        self.value=value

    def _ex_maybe_child(self) -> Generator:
        yield self.value

    def gen_expr(self) -> str:
        return self.value.gen_expr()