from __future__ import annotations

from typing import Any, Dict, List,TYPE_CHECKING, Union
from pyvisflow.core.reactive import Reactive
from pyvisflow.utils.data_gen import get_global_id
import pandas as pd

from pyvisflow.core.props import ConstantsPropInfo, create_getby_prop
from pyvisflow.core.props.methodProp import  LambdaPropInfo, MethodPropInfo, VarPropInfo


class Dataset():
    def __init__(self) -> None:
        self.id=get_global_id()

class StaticDataset(Dataset):

    def __init__(self,dataframe:pd.DataFrame) -> None:
        super().__init__()
        self._dataframe=dataframe

    def create_reactive_dataset(self):
        lamb = LambdaPropInfo(['v'],VarPropInfo('v'))
        getDf=MethodPropInfo('getDf',[ConstantsPropInfo(self.id),lamb])

        reactDs = ReactiveDataset()
        reactDs.set_prop('dataframe',getDf)

        return reactDs 


class ReactiveDataset(Reactive):

    def __init__(self) -> None:
        super().__init__()

    def _ex_get_react_data(self) -> Dict[str, Any]:
        data= super()._ex_get_react_data()

        data.update({
            'dataframe':{
                'infos':{
                    "columns": [],
                    "rows": 0
                },
                "columnsType": [],
                "data": []
            }
        })

        return data