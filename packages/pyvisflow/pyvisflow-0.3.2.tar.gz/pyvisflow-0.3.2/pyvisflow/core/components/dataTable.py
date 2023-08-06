from __future__ import annotations

from typing import Any, Dict, List, Optional, Union
from pyvisflow.core.dataset.props import ReactiveDatasetPropInfo
from pyvisflow.core.props import StrTypePropInfo, SubscriptableTypePropInfo, BoolTypePropInfo
from pyvisflow.core.props.absProp import AbsPropInfo
from pyvisflow.models.TWatchInfo import TTableFilterWatch
from pyvisflow.utils.data_gen import StrEnum
from pyvisflow.utils.helper import df2object_dict
from .auto_create._dataTable import _DataTable



class TTableColumnFormatType(StrEnum):
    Percent='percent'


class DataTable(_DataTable):
    def __init__(self, reactDataset: ReactiveDatasetPropInfo) -> None:
        super().__init__()

        self.set_prop('dataframe',reactDataset)
        self.current_page = 1
        self.columnsSetting_formatters:Dict[str,Any]={}

    def set_format(self,column:str,format_type:TTableColumnFormatType,args:Dict):
        self.columnsSetting_formatters[column]={
            'column':column,
            'formatType':format_type,
            'args':args
        }

    @property
    def columns(self):
        return DataTableColumnsType(self)

    @property
    def rowClick(self):
        p = self.get_prop('rowClick')
        return SubscriptableTypePropInfo[str, StrTypePropInfo](p)

    @property
    def rowHover(self):
        p = self.get_prop('rowHover')
        return SubscriptableTypePropInfo[str, StrTypePropInfo](p)

    def _ex_get_react_data(self):
        data = super()._ex_get_react_data()
        data.update({
            'dataframe': {
                "infos": {
                    "columns": [],
                    "rows": 0
                },
                "columnsType": [],
                "data": []
            },
            'columnsSetting':{
                'formatters':list(self.columnsSetting_formatters.values())
            },
            'rowClick': {},
            'rowHover': {},
        })
        return data



class DataTableColumnsType():

    def __init__(self,datatable:DataTable) -> None:
        self._datatable=datatable

    @property
    def show_columns(self):
        '''
        表格显示的列。当你希望页面表格只输出数据一部分列的时候可以设置此属性
        '''
        return self._datatable.get_prop('columnsSetting.showColumns')

    @show_columns.setter
    def show_columns(self,value:List[str]):
        self._datatable.set_prop('columnsSetting.showColumns',value)

    def set_sortable(self,columns:List[str] | bool | AbsPropInfo):
        self._datatable.set_prop('columnsSetting.sortableColumns',columns)


    def __getitem__(self,column_name:str):
        return DataTableSingleColumnType(self,column_name)


class DataTableSingleColumnType():

    def __init__(self,dataTableColumnsType:DataTableColumnsType,name:str) -> None:
        self.__dataTableColumnsType=dataTableColumnsType
        self.name=name

    def percent_format(self,num_digits:int=2 ):
        '''
        百分比格式化。只作用在表格显示上，不影响数值本身
        num_digits:按此位数对 number 参数进行四舍五入
        '''
        self.__dataTableColumnsType._datatable.set_format(self.name,TTableColumnFormatType.Percent,{'style':TTableColumnFormatType.Percent,'minimumFractionDigits':num_digits})

