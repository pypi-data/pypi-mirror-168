from typing import Any, Dict, Iterable, List, Tuple, Union
from pyvisflow.core.props import SubscriptableTypePropInfo, StrTypePropInfo, NumberTypePropInfo
from pyvisflow.core.props.absProp import AbsPropInfo

from .auto_create._select import _Select



class Select(_Select):
    def __init__(self, options: Iterable[str], multiple=False) -> None:
        super().__init__()

        self._options=[]

        if isinstance(options,AbsPropInfo):
            self.set_prop('options',options)
        else:
            options = list(options)
            self._options = options

        self.multiple = multiple

    @property
    def options(self):
        '''
        '''

        p = self.get_prop('options')
        return SubscriptableTypePropInfo[str,StrTypePropInfo](p)

    @options.setter
    def options(self, value: Union[SubscriptableTypePropInfo[str,StrTypePropInfo], bool]):
        '''
        '''
        self.set_prop('options', value)

    @property
    def currentLabels(self):
        p = self.get_prop('currentLabels')
        return SubscriptableTypePropInfo[int, StrTypePropInfo](p)

    def _ex_get_react_data(self):
        data = super()._ex_get_react_data()
        data.update({'options': self._options, 'currentLabels': []})
        return data
