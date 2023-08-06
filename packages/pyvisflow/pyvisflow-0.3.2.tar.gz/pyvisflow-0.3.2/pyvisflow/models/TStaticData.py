from typing import Any, Dict, List, Optional


from pyvisflow.utils.jsonable import Jsonable

class TInfo(Jsonable):

    __slot__='columns','rows'

    def __init__(self,columns:List[str],rows:int) -> None:
        super().__init__()
        self.columns=columns
        self.rows=rows


class TColumnsType(Jsonable):

    __slot__='name','type'

    def __init__(self,name:str,type:str) -> None:
        super().__init__()
        self.name=name
        self.type=type



class TDataframe(Jsonable):

    __slot__='id','infos','columnsType','data'

    def __init__(self,id:str,infos:TInfo,columnsType: List[TColumnsType],data: List[List[Any]]) -> None:
        super().__init__()
        self.id=id
        self.infos=infos
        self.columnsType=columnsType
        self.data=data


class TStaticData(Jsonable):

    __slot__='dataframes'

    def __init__(self,dataframes:List[TDataframe]) -> None:
        super().__init__()
        self.dataframes=dataframes

