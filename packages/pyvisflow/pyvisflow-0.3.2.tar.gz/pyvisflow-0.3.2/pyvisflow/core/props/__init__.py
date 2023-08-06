from .absProp import *
from .methodProp import *
from .typeProp import *
from .valueProp import *

from typing import Union

TTypePropInfo = AbsPropInfo

def create_getby_logic(id:str,logic:AbsPropInfo):
    idv = ConstantsPropInfo(id)
    getby = MethodPropInfo('getby',[idv,logic])
    return getby

def create_getby_prop(id:str,prop:str):
    lamb = LambdaPropInfo(['v'],ObjectPropCallPropInfo('v',prop))
    return create_getby_logic(id,lamb)

