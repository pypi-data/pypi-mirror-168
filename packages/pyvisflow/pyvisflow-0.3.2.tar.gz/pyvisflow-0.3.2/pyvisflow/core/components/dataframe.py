from typing import Any, Dict
from pyvisflow.models.TComponent import TComponentType
from .components import Component
from pandas.io.formats.style import Styler

class Dataframe(Component):

    def __init__(self,styler:Styler) -> None:
        super().__init__('dataframe', TComponentType.builtIn)

        self.__styler=styler

    def _ex_get_react_data(self) -> Dict[str, Any]:
        data= super()._ex_get_react_data()
        data.update({
            'rawHtml':self.__styler.render()
        })
        return data