from typing import Any, Dict
from pyvisflow.models.TComponent import TComponentType
from .components import Component
from bs4 import BeautifulSoup


class Icon(Component):
    def __init__(self, svg: str, size: str) -> None:
        super().__init__('icon', TComponentType.builtIn)

        s = BeautifulSoup(svg, 'html.parser')

        del s.find('svg')['width']
        del s.find('svg')['height']
        self._svg = str(s)
        self._size = size

    def _ex_get_react_data(self) -> Dict[str, Any]:
        data = super()._ex_get_react_data()
        data.update({'svg': self._svg, 'size': self._size})
        return data