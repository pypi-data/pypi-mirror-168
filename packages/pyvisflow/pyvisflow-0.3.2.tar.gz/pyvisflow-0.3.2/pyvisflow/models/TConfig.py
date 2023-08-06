from typing import Dict, List, Optional

from pyvisflow.models.TWatchInfo import TWatchInfo
from pyvisflow.utils.jsonable import Jsonable
from .TComponent import TComponent
from .TStaticData import TStaticData


class TReactData(Jsonable):

    __slot__='id','data'

    def __init__(self,id: str,data: Dict) -> None:
        super().__init__()
        self.id=id
        self.data=data


class TConfig(Jsonable):

    __slot__='staticData','dataset','cps','reactDatas','watchInfo'

    def __init__(self,
        staticData: TStaticData,
        cps: List[TComponent],
        reactDatas: Optional[List[TReactData]],
        watchInfo: TWatchInfo
    ) -> None:
        super().__init__()
        self.staticData=staticData
        self.cps=cps
        self.reactDatas=reactDatas or []
        self.watchInfo=watchInfo


