


from abc import abstractmethod


class Jsonable():


    @abstractmethod
    def _to_json_dict(self):
        return self.__dict__