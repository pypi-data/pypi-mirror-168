from pyvisflow.utils.jsonable import Jsonable

class JsCode(Jsonable):

    def __init__(self,code:str) -> None:
        self._code=code

    def _to_json_dict(self):
        return self._code

        