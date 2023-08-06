from typing import Dict, Hashable, Any, Optional, Union
from pyvisflow.core.reactive import Reactive
from pyvisflow.core.props import TTypePropInfo


class Structure(Reactive):
    def __init__(self) -> None:
        super().__init__()


class Mapping(Structure):
    def __init__(self,
                 mapping: Optional[Dict[str, Dict[str, Any]]] = None) -> None:
        super().__init__()
        self._mapping = mapping or {}
        self.key = ''

    def add_item(self, key: str, datas: Union[Dict[str, Any], Any]):
        if not isinstance(datas, dict):
            datas = {'__value__': datas}

        self._mapping.update({key: datas})

        return self

    @property
    def value(self):
        return self['__value__']

    @property
    def key(self):
        return self.get_prop('key')

    @key.setter
    def key(self, value: Union[TTypePropInfo, str]):
        self.set_prop('key', value)

    # def __getitem__(self, item: str):
    #     return (ExPropInfo(
    #         self, f'key').set_watchingPath(f"`mapping['${{change}}'].{item}`"))

    def _ex_get_react_data(self) -> Dict[str, Any]:
        data = super()._ex_get_react_data()
        data.update({'mapping': self._mapping})
        return data
