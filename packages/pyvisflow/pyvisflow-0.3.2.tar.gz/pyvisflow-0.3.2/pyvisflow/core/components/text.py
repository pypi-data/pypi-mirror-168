from typing import Union
from pyvisflow.core.props.typeProp import StrTypePropInfo
from pyvisflow.models.TComponent import TComponentType
from .components import Component


class Text(Component):
    def __init__(self, value:str) -> None:
        super().__init__('text', TComponentType.builtIn)
        self.set_prop('value',value)

    @property
    def value(self):
        '''
        文字内容
        '''

        p = self.get_prop('value')
        return StrTypePropInfo(p)

    @value.setter
    def value(self, value: Union[StrTypePropInfo, str]):
        '''
        文字内容
        '''
        self.set_prop('value', value)