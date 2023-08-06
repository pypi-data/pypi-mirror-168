from typing import Callable, Dict, Hashable, List, Optional, Set, Tuple, Union

from pyvisflow.utils.jsonable import Jsonable


class TTargetWatchInfo(Jsonable):

    __slot__='id','path','logic'

    def __init__(self,id: str,path: str,logic: str) -> None:
        super().__init__()
        self.id=id
        self.path=path
        self.logic=logic

class TLogic(Jsonable):

    __slot__='logic'

    def __init__(self,logic: str) -> None:
        super().__init__()
        self.logic=logic

class TChartFilterTarget(Jsonable):

    __slot__='id','logic'

    def __init__(self,id: str,logic: str) -> None:
        super().__init__()
        self.id=id
        self.logic=logic

class TTableFilterTarget(Jsonable):

    __slot__='id','logic'

    def __init__(self,id: str,logic: str) -> None:
        super().__init__()
        self.id=id
        self.logic=logic

class TValueWatch(Jsonable):

    __slot__='target'

    def __init__(self,target: TTargetWatchInfo) -> None:
        super().__init__()
        self.target=target

class TChartFilterWatch(Jsonable):

    __slot__='target'

    def __init__(self,target: TChartFilterTarget) -> None:
        super().__init__()
        self.target=target


class TTableFilterWatch(Jsonable):

    __slot__='target'

    def __init__(self,target: TTableFilterTarget) -> None:
        super().__init__()
        self.target=target


class TWatchInfo(Jsonable):

    __slot__='values'

    def __init__(self,
                values: Optional[List[TValueWatch]]=None
                ) -> None:
        super().__init__()
        self.values=values or []



