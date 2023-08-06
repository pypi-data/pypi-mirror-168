from abc import abstractmethod
from typing import Any, Dict, Tuple, Union
from pyvisflow.core.props import  AbsPropInfo, create_getby_prop
from pyvisflow.models.TWatchInfo import TValueWatch, TTargetWatchInfo
from pyvisflow.utils.data_gen import get_global_id
import re


RE_match_array = re.compile(r'(?P<name>.+)(\[(?P<num>\d+)\])')


class Reactive():
    def __init__(self) -> None:
        self._id = get_global_id()
        self._watch_infos_map: Dict[Tuple[str,str], AbsPropInfo] = {}
        self._free_data: Dict[str, Any] = {}

    def _add_watch_info(self, targetPath: str, value: AbsPropInfo):
        # key = (self._id, targetPath)
        logic = value.gen_expr()
        key = (targetPath, logic)
        if not key in self._watch_infos_map:
            self._watch_infos_map[key] = value
            # target = TTargetWatchInfo(id=self._id,
            #                           path=targetPath,
            #                           logic=logic)
            # self._watch_infos_map[key] = TValueWatch(target=target)


    def get_prop(self, prop: str):
        return create_getby_prop(self._id,prop)

    def set_prop(self, prop: str, value: Union[AbsPropInfo, Any]):
        if isinstance(value, AbsPropInfo):
            self._add_watch_info(prop, value)

            if not prop in self._free_data:
                self._free_data[prop] = None
        else:
            self._free_data[prop] = value
        return self

    def __update_by_path(self, data: Dict, path: str, value: Any):
        paths = path.split('.')
        start = data
        for key in paths[:-1]:

            array = RE_match_array.match(key)
            if array:
                # is array like 'series[0]'
                name, idx = array.group('name'), array.group('num')
                start = start[name][int(idx)]
                continue

            if not key in start:
                start[key] = {}

            start = start[key]

        if paths[-1] in start and (value is
                                   None) and (not start[paths[-1]] is None):
            return

        start.update({paths[-1]: value})

    def _get_WatchInfos(self):
        return list(self._watch_infos_map.values())

    @abstractmethod
    def _ex_get_react_data(self) -> Dict[str, Any]:
        return {}

    def _create_react_data(self) -> Dict[str, Any]:
        data = self._ex_get_react_data()

        for prop, value in self._free_data.items():
            self.__update_by_path(data, prop, value)
        return data
