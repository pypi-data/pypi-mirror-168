from typing import Union,Dict,List
from pyvisflow.core.components.components import Component
from pyvisflow.core.props import StrTypePropInfo, NumberTypePropInfo, BoolTypePropInfo
from pyvisflow.models.TComponent import TComponentType
from pyvisflow.core.props import *

TypePropInfo=Union[StrTypePropInfo,NumberTypePropInfo,BoolTypePropInfo]

class _Input(Component):
    '''
    Input 输入框
通过鼠标或键盘输入字符
    '''

    def __init__(self) -> None:
        super().__init__('input', TComponentType.builtIn)

    def _ex_get_react_data(self):
        return super()._ex_get_react_data()


    @property
    def type(self):
        '''
        可选值：text，textarea 和其他原生 input 的 type 值 \n
        类型
        '''

        
        p = self.get_prop('type')
        return StrTypePropInfo(p)

        


    @type.setter
    def type(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：text，textarea 和其他原生 input 的 type 值 \n
        类型
        '''
        self.set_prop('type', value)

    @property
    def value(self):
        '''
        可选值：text，textarea 和其他原生 input 的 type 值 \n
        绑定值
        '''

        
        p = self.get_prop('value')
        return StrTypePropInfo(p)

        


    @value.setter
    def value(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：text，textarea 和其他原生 input 的 type 值 \n
        绑定值
        '''
        self.set_prop('value', value)

    @property
    def maxlength(self):
        '''
        可选值：text，textarea 和其他原生 input 的 type 值 \n
        最大输入长度
        '''

        
        p = self.get_prop('maxlength')
        return NumberTypePropInfo(p)

        


    @maxlength.setter
    def maxlength(self, value: Union[NumberTypePropInfo,int]):
        '''
        可选值：text，textarea 和其他原生 input 的 type 值 \n
        最大输入长度
        '''
        self.set_prop('maxlength', value)

    @property
    def minlength(self):
        '''
        可选值：text，textarea 和其他原生 input 的 type 值 \n
        原生属性，最小输入长度
        '''

        
        p = self.get_prop('minlength')
        return NumberTypePropInfo(p)

        


    @minlength.setter
    def minlength(self, value: Union[NumberTypePropInfo,float]):
        '''
        可选值：text，textarea 和其他原生 input 的 type 值 \n
        原生属性，最小输入长度
        '''
        self.set_prop('minlength', value)

    @property
    def show_word_limit(self):
        '''
        可选值：text，textarea 和其他原生 input 的 type 值 \n
        是否显示输入字数统计，只在 type = "text" 或 type = "textarea" 时有效
        '''

        
        p = self.get_prop('show-word-limit')
        return BoolTypePropInfo(p)

        


    @show_word_limit.setter
    def show_word_limit(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：text，textarea 和其他原生 input 的 type 值 \n
        是否显示输入字数统计，只在 type = "text" 或 type = "textarea" 时有效
        '''
        self.set_prop('show-word-limit', value)

    @property
    def placeholder(self):
        '''
        可选值：text，textarea 和其他原生 input 的 type 值 \n
        输入框占位文本
        '''

        
        p = self.get_prop('placeholder')
        return StrTypePropInfo(p)

        


    @placeholder.setter
    def placeholder(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：text，textarea 和其他原生 input 的 type 值 \n
        输入框占位文本
        '''
        self.set_prop('placeholder', value)

    @property
    def clearable(self):
        '''
        可选值：text，textarea 和其他原生 input 的 type 值 \n
        是否可清空
        '''

        
        p = self.get_prop('clearable')
        return BoolTypePropInfo(p)

        


    @clearable.setter
    def clearable(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：text，textarea 和其他原生 input 的 type 值 \n
        是否可清空
        '''
        self.set_prop('clearable', value)

    @property
    def show_password(self):
        '''
        可选值：text，textarea 和其他原生 input 的 type 值 \n
        是否显示切换密码图标
        '''

        
        p = self.get_prop('show-password')
        return BoolTypePropInfo(p)

        


    @show_password.setter
    def show_password(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：text，textarea 和其他原生 input 的 type 值 \n
        是否显示切换密码图标
        '''
        self.set_prop('show-password', value)

    @property
    def disabled(self):
        '''
        可选值：text，textarea 和其他原生 input 的 type 值 \n
        是否禁用
        '''

        
        p = self.get_prop('disabled')
        return BoolTypePropInfo(p)

        


    @disabled.setter
    def disabled(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：text，textarea 和其他原生 input 的 type 值 \n
        是否禁用
        '''
        self.set_prop('disabled', value)

    @property
    def size(self):
        '''
        可选值：large / default / small \n
        输入框尺寸，只在 type !="textarea" 时有效
        '''

        
        p = self.get_prop('size')
        return StrTypePropInfo(p)

        


    @size.setter
    def size(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：large / default / small \n
        输入框尺寸，只在 type !="textarea" 时有效
        '''
        self.set_prop('size', value)

    @property
    def rows(self):
        '''
        可选值：large / default / small \n
        输入框行数，只对 type="textarea" 有效
        '''

        
        p = self.get_prop('rows')
        return NumberTypePropInfo(p)

        


    @rows.setter
    def rows(self, value: Union[NumberTypePropInfo,float]):
        '''
        可选值：large / default / small \n
        输入框行数，只对 type="textarea" 有效
        '''
        self.set_prop('rows', value)

    @property
    def autosize(self):
        '''
        可选值：large / default / small \n
        textarea高度是否自适应，只在 type="textarea" 时生效。 可以接受一个对象，比如: { minRows: 2, maxRows: 6 }
        '''

        
        p = self.get_prop('autosize')
        return BoolTypePropInfo(p)

        


    @autosize.setter
    def autosize(self, value: Union[BoolTypePropInfo,Union[bool,Dict]]):
        '''
        可选值：large / default / small \n
        textarea高度是否自适应，只在 type="textarea" 时生效。 可以接受一个对象，比如: { minRows: 2, maxRows: 6 }
        '''
        self.set_prop('autosize', value)

    @property
    def autocomplete(self):
        '''
        可选值：large / default / small \n
        原生属性，自动补全
        '''

        
        p = self.get_prop('autocomplete')
        return StrTypePropInfo(p)

        


    @autocomplete.setter
    def autocomplete(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：large / default / small \n
        原生属性，自动补全
        '''
        self.set_prop('autocomplete', value)

    @property
    def name(self):
        '''
        可选值：large / default / small \n
        原生属性
        '''

        
        p = self.get_prop('name')
        return StrTypePropInfo(p)

        


    @name.setter
    def name(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：large / default / small \n
        原生属性
        '''
        self.set_prop('name', value)

    @property
    def readonly(self):
        '''
        可选值：large / default / small \n
        原生属性，是否只读
        '''

        
        p = self.get_prop('readonly')
        return BoolTypePropInfo(p)

        


    @readonly.setter
    def readonly(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：large / default / small \n
        原生属性，是否只读
        '''
        self.set_prop('readonly', value)

    @property
    def max(self):
        '''
        可选值：large / default / small \n
        原生属性，设置最大值
        '''

        
        p = self.get_prop('max')
        return NumberTypePropInfo(p)

        


    @max.setter
    def max(self, value: Union[NumberTypePropInfo,int]):
        '''
        可选值：large / default / small \n
        原生属性，设置最大值
        '''
        self.set_prop('max', value)

    @property
    def min(self):
        '''
        可选值：large / default / small \n
        原生属性，设置最小值
        '''

        
        p = self.get_prop('min')
        return NumberTypePropInfo(p)

        


    @min.setter
    def min(self, value: Union[NumberTypePropInfo,int]):
        '''
        可选值：large / default / small \n
        原生属性，设置最小值
        '''
        self.set_prop('min', value)

    @property
    def step(self):
        '''
        可选值：large / default / small \n
        原生属性，设置输入字段的合法数字间隔
        '''

        
        p = self.get_prop('step')
        return NumberTypePropInfo(p)

        


    @step.setter
    def step(self, value: Union[NumberTypePropInfo,int]):
        '''
        可选值：large / default / small \n
        原生属性，设置输入字段的合法数字间隔
        '''
        self.set_prop('step', value)

    @property
    def resize(self):
        '''
        可选值：none / both / horizontal / vertical \n
        控制是否能被用户缩放
        '''

        
        p = self.get_prop('resize')
        return StrTypePropInfo(p)

        


    @resize.setter
    def resize(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：none / both / horizontal / vertical \n
        控制是否能被用户缩放
        '''
        self.set_prop('resize', value)

    @property
    def autofocus(self):
        '''
        可选值：none / both / horizontal / vertical \n
        原生属性，自动获取焦点
        '''

        
        p = self.get_prop('autofocus')
        return BoolTypePropInfo(p)

        


    @autofocus.setter
    def autofocus(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：none / both / horizontal / vertical \n
        原生属性，自动获取焦点
        '''
        self.set_prop('autofocus', value)

    @property
    def input_style(self):
        '''
        可选值：none / both / horizontal / vertical \n
        input 元素或 textarea 元素的 style
        '''

        
        return self.get_prop('input-style')
        


    @input_style.setter
    def input_style(self, value: Union[TypePropInfo,Dict]):
        '''
        可选值：none / both / horizontal / vertical \n
        input 元素或 textarea 元素的 style
        '''
        self.set_prop('input-style', value)
