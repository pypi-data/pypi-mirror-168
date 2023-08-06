from typing import Any, Dict
from pyvisflow.models.TComponent import TComponentType
from .components import Component


class Image(Component):
    def __init__(self, value:str) -> None:
        super().__init__('image', TComponentType.builtIn)
        self.value=value
        self.styles.set('display','block').set('object-fit','contain')

    def _ex_get_react_data(self) -> Dict[str, Any]:
        data = super()._ex_get_react_data()
        data.update({'value': self.value})
        return data