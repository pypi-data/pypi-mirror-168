from typing import Any, Dict, Union
from pyvisflow.core.props.typeProp import BoolTypePropInfo, StrTypePropInfo
from pyvisflow.models.TComponent import TComponentType
from .components import Component
from bs4 import BeautifulSoup


class Button(Component):
    def __init__(self,text:str) -> None:
        super().__init__('button', TComponentType.builtIn)
        self.text=text
        self.styles.set('cursor','pointer')
        
    @property
    def text(self):
        '''

        '''
        p = self.get_prop('text')
        return StrTypePropInfo(p)

    @text.setter
    def text(self, value: Union[StrTypePropInfo,str]):
        '''
        '''
        self.set_prop('text', value)


    @property
    def click(self):
        p= self.get_prop('click')
        return BoolTypePropInfo(p)

    def _ex_get_react_data(self) -> Dict[str, Any]:
        data = super()._ex_get_react_data()
        data.update({'click':False})
        return data