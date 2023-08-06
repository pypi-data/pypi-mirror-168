from typing import TYPE_CHECKING, Any, Dict, List, Union
from pyvisflow.core.props.typeProp import BoolTypePropInfo, StrTypePropInfo, SubscriptableTypePropInfo
from pyvisflow.models.TComponent import TComponentType
from .components import Component
from pyvisflow.utils.data_gen import get_global_id
from pyvisflow.core.reactive import Reactive
from pyvisflow.core.props.absProp import AbsPropInfo
# if TYPE_CHECKING:
    

class File(Component):
    def __init__(self) -> None:
        super().__init__('file', TComponentType.builtIn)
        self.__info_id=f'data-{get_global_id()}'

    @property
    def columns(self):
        p = self.get_prop('details.columns')
        return SubscriptableTypePropInfo(p)

    @property
    def data(self):
        return FileData(self,self.get_prop('details'))



    def _ex_get_react_data(self) -> Dict[str, Any]:
        data= super()._ex_get_react_data()
        data.update({
            'infoID':self.__info_id,
            'details':{
                'columns':[],
                'data':list(list())
            },
        })
        return data



class FileData(Reactive):

    def __init__(self,file:File,details_binding:AbsPropInfo) -> None:
        super().__init__()
        self.__file=file
        self.details_binding=details_binding
        self.set_prop('details',details_binding)

    def _ex_get_react_data(self) -> Dict[str, Any]:
        data =  super()._ex_get_react_data()
        data.update({
            'details':{
                'columns':[],
                'data':list(list())
            }
        })
        return data

  