from typing import Dict, List, Optional
from enum import Enum

from pyvisflow.utils.jsonable import Jsonable




class TComponentType(str, Enum):
    htmlRaw = 'html-raw'
    htmlRawString = 'html-raw-string'
    mdRawString = 'markdown-raw-string'
    builtIn = 'built-in'

class TComponent(Jsonable):

    __slot__='id','tag','type','attrs','styles','children'

    def __init__(self,
                id: str,
                tag: str,
                type: TComponentType,
                attrs: Optional[Dict] ,
                styles: Optional[Dict] ,
                children: Optional[List['TComponent']]
        ) -> None:
        super().__init__()
        self.id=id
        self.tag=tag
        self.type=type
        self.attrs=attrs or {}
        self.styles=styles or {}
        self.children=children or []


