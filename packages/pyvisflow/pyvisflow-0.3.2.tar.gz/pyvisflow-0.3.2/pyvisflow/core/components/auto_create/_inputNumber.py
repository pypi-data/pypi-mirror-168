from typing import Union,Dict,List
from pyvisflow.core.components.components import Component
from pyvisflow.core.props import StrTypePropInfo, NumberTypePropInfo, BoolTypePropInfo
from pyvisflow.models.TComponent import TComponentType
from pyvisflow.core.props import *

TypePropInfo=Union[StrTypePropInfo,NumberTypePropInfo,BoolTypePropInfo]

class _InputNumber(Component):
    '''
    Input Number 数字输入框
仅允许输入标准的数字值，可定义范围
    '''

    def __init__(self) -> None:
        super().__init__('input-number', TComponentType.builtIn)

    def _ex_get_react_data(self):
        return super()._ex_get_react_data()


    @property
    def value(self):
        '''
        可选值：— \n
        选中项绑定值
        '''

        
        p = self.get_prop('value')
        return NumberTypePropInfo(p)

        


    @value.setter
    def value(self, value: Union[NumberTypePropInfo,float]):
        '''
        可选值：— \n
        选中项绑定值
        '''
        self.set_prop('value', value)

    @property
    def min(self):
        '''
        可选值：— \n
        设置计数器允许的最小值
        '''

        
        p = self.get_prop('min')
        return NumberTypePropInfo(p)

        


    @min.setter
    def min(self, value: Union[NumberTypePropInfo,float]):
        '''
        可选值：— \n
        设置计数器允许的最小值
        '''
        self.set_prop('min', value)

    @property
    def max(self):
        '''
        可选值：— \n
        设置计数器允许的最大值
        '''

        
        p = self.get_prop('max')
        return NumberTypePropInfo(p)

        


    @max.setter
    def max(self, value: Union[NumberTypePropInfo,float]):
        '''
        可选值：— \n
        设置计数器允许的最大值
        '''
        self.set_prop('max', value)

    @property
    def step(self):
        '''
        可选值：— \n
        计数器步长
        '''

        
        p = self.get_prop('step')
        return NumberTypePropInfo(p)

        


    @step.setter
    def step(self, value: Union[NumberTypePropInfo,float]):
        '''
        可选值：— \n
        计数器步长
        '''
        self.set_prop('step', value)

    @property
    def step_strictly(self):
        '''
        可选值：— \n
        是否只能输入 step 的倍数
        '''

        
        p = self.get_prop('step-strictly')
        return BoolTypePropInfo(p)

        


    @step_strictly.setter
    def step_strictly(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：— \n
        是否只能输入 step 的倍数
        '''
        self.set_prop('step-strictly', value)

    @property
    def precision(self):
        '''
        可选值：— \n
        数值精度
        '''

        
        p = self.get_prop('precision')
        return NumberTypePropInfo(p)

        


    @precision.setter
    def precision(self, value: Union[NumberTypePropInfo,float]):
        '''
        可选值：— \n
        数值精度
        '''
        self.set_prop('precision', value)

    @property
    def size(self):
        '''
        可选值：large/small \n
        计数器尺寸
        '''

        
        p = self.get_prop('size')
        return StrTypePropInfo(p)

        


    @size.setter
    def size(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：large/small \n
        计数器尺寸
        '''
        self.set_prop('size', value)

    @property
    def disabled(self):
        '''
        可选值：large/small \n
        是否禁用计数器
        '''

        
        p = self.get_prop('disabled')
        return BoolTypePropInfo(p)

        


    @disabled.setter
    def disabled(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：large/small \n
        是否禁用计数器
        '''
        self.set_prop('disabled', value)

    @property
    def controls(self):
        '''
        可选值：large/small \n
        是否使用控制按钮
        '''

        
        p = self.get_prop('controls')
        return BoolTypePropInfo(p)

        


    @controls.setter
    def controls(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：large/small \n
        是否使用控制按钮
        '''
        self.set_prop('controls', value)

    @property
    def controls_position(self):
        '''
        可选值：right \n
        控制按钮位置
        '''

        
        p = self.get_prop('controls-position')
        return StrTypePropInfo(p)

        


    @controls_position.setter
    def controls_position(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：right \n
        控制按钮位置
        '''
        self.set_prop('controls-position', value)

    @property
    def name(self):
        '''
        可选值：right \n
        原生 name 属性
        '''

        
        p = self.get_prop('name')
        return StrTypePropInfo(p)

        


    @name.setter
    def name(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：right \n
        原生 name 属性
        '''
        self.set_prop('name', value)

    @property
    def label(self):
        '''
        可选值：right \n
        输入框关联的 label 文字
        '''

        
        p = self.get_prop('label')
        return StrTypePropInfo(p)

        


    @label.setter
    def label(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：right \n
        输入框关联的 label 文字
        '''
        self.set_prop('label', value)

    @property
    def placeholder(self):
        '''
        可选值：right \n
        输入框默认 placeholder
        '''

        
        p = self.get_prop('placeholder')
        return StrTypePropInfo(p)

        


    @placeholder.setter
    def placeholder(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：right \n
        输入框默认 placeholder
        '''
        self.set_prop('placeholder', value)
