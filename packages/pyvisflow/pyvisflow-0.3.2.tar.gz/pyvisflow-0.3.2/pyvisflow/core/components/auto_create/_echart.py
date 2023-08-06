from typing import Union,Dict,List
from pyvisflow.core.components.components import Component
from pyvisflow.core.props import StrTypePropInfo, NumberTypePropInfo, BoolTypePropInfo
from pyvisflow.models.TComponent import TComponentType
from pyvisflow.core.props import *

TypePropInfo=Union[StrTypePropInfo,NumberTypePropInfo,BoolTypePropInfo]

class _EChart(Component):
    '''
    echart 图表
    '''

    def __init__(self) -> None:
        super().__init__('echart', TComponentType.builtIn)

    def _ex_get_react_data(self):
        return super()._ex_get_react_data()


    @property
    def title(self):
        '''
        可选值：nan \n
        图表标题
        '''

        
        p = self.get_prop('option.title.text')
        return StrTypePropInfo(p)

        


    @title.setter
    def title(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：nan \n
        图表标题
        '''
        self.set_prop('option.title.text', value)
