from typing import Union,Dict,List
from pyvisflow.core.components.containers import Container
from pyvisflow.core.props import StrTypePropInfo, NumberTypePropInfo, BoolTypePropInfo
from pyvisflow.models.TComponent import TComponentType
from pyvisflow.core.props import *

TypePropInfo=Union[StrTypePropInfo,NumberTypePropInfo,BoolTypePropInfo]

class _Tabs(Container):
    '''
    分隔内容上有关联但属于不同类别的数据集合
    '''

    def __init__(self) -> None:
        super().__init__('tabs', TComponentType.builtIn)

    def _ex_get_react_data(self):
        return super()._ex_get_react_data()


    @property
    def names(self):
        '''
        可选值：nan \n
        选项卡名字
        '''

        
        p = self.get_prop('names')
        return SubscriptableTypePropInfo[int,StrTypePropInfo](p)

        


    @names.setter
    def names(self, value: Union[SubscriptableTypePropInfo[int,StrTypePropInfo],List[str]]):
        '''
        可选值：nan \n
        选项卡名字
        '''
        self.set_prop('names', value)

    @property
    def pageMode(self):
        '''
        可选值：nan \n
        是否采用页面顶部栏显示模式。此模式页签样式不一样而已
        '''

        
        p = self.get_prop('pageMode')
        return BoolTypePropInfo(p)

        


    @pageMode.setter
    def pageMode(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：nan \n
        是否采用页面顶部栏显示模式。此模式页签样式不一样而已
        '''
        self.set_prop('pageMode', value)

    @property
    def activeName(self):
        '''
        可选值：nan \n
        当前激活的选项卡名字
        '''

        
        p = self.get_prop('activeName')
        return StrTypePropInfo(p)

        


    @activeName.setter
    def activeName(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：nan \n
        当前激活的选项卡名字
        '''
        self.set_prop('activeName', value)

    @property
    def value(self):
        '''
        可选值：nan \n
        绑定值，选中选项卡的 name
        '''

        
        p = self.get_prop('value')
        return StrTypePropInfo(p)

        


    @value.setter
    def value(self, value: Union[StrTypePropInfo,Union[str,float]]):
        '''
        可选值：nan \n
        绑定值，选中选项卡的 name
        '''
        self.set_prop('value', value)
