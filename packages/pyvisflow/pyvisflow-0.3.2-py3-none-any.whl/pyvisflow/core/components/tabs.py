from typing import Dict, List, Iterable, Union

import pyvisflow.core.components.containers as containers
from .auto_create._tabs import _Tabs


class Tabs(_Tabs):
    def __init__(self, names: Union[Iterable[str], Dict[str, str]]) -> None:
        super().__init__()
        labels = []
        if isinstance(names, Iterable):
            names = [str(n) for n in names]
            labels = names

        if isinstance(names, Dict):
            labels = list(str(n) for n in names.values())
            names = list(str(n) for n in names.keys())

        self._labels = labels
        self.names = names

        self._boxes = tuple(
            [containers.BoxContainer() for _ in range(len(names))])

        self._mapping = {name: box for name, box in zip(names, self._boxes)}
        for box in self._boxes:
            self.add_child(box)

    @property
    def boxes(self):
        return self._boxes

    def __iter__(self):
        return iter(self.boxes)

    def __getitem__(self, key: Union[str, int]):
        if isinstance(key, int):
            return self._boxes[key]
        return self._mapping[key]

    def _ex_get_react_data(self):
        data = super()._ex_get_react_data()
        data.update({
            'labels': self._labels,
        })
        return data
