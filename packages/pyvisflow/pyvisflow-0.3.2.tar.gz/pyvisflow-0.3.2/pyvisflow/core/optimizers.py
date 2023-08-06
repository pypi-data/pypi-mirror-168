from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List, Tuple, Any
from collections import defaultdict


from pyvisflow.core.reactive import Reactive
from pyvisflow.models.TConfig import TReactData
from pyvisflow.models.TWatchInfo import TTargetWatchInfo, TValueWatch

class WatchValueOptimizer():

    def __init__(self) -> None:
        self.collects:defaultdict[str, list[TValueWatch]] = defaultdict(lambda:[])


    def preload(self,reactive: Reactive):
        pass


        for (targetPath, logic),propInfo in reactive._watch_infos_map.items():
            target = TTargetWatchInfo(id=reactive._id,
                                    path=targetPath,
                                    logic=logic)
            self.collects[logic].append(TValueWatch(target=target))

    def create_infos(self):
        res_watchs:List[TValueWatch]=[]
        res_tempWatchReactiveDatas:List[TReactData]=[]

        # 以logic 为 key，发现2个以上
        for logic,watchs in self.collects.items():
            if len(watchs)>1:
                # 生成一个新的 临时监控 tempWatchReactive
                tempWatchReactive = TempWatchReactive()
                res_tempWatchReactiveDatas.append(TReactData(tempWatchReactive._id,tempWatchReactive._create_react_data()))

                # 创建一个watch，目标是 tempwatch，logic是共有的
                target = TTargetWatchInfo(id=tempWatchReactive._id,
                                        path='temp',
                                        logic=logic)
                
                res_watchs.append(TValueWatch(target=target))

                # 把这些 组合的 watch 的 logic 修改成指向 tempWatch
                for watch in watchs:
                    watch.target.logic=f"getby('{tempWatchReactive._id}',v=>v.temp)"

            res_watchs.extend(watchs)

        return WatchValueOptimizerResult(res_watchs,res_tempWatchReactiveDatas)


class WatchValueOptimizerResult():

    __slot__='watchs','tempReactiveDatas'

    def __init__(self,watchs:List[TValueWatch],tempReactiveDatas:List[TReactData]) -> None:
        self.watchs=watchs
        self.tempReactiveDatas=tempReactiveDatas

        

class TempWatchReactive(Reactive):

    def __init__(self) -> None:
        super().__init__()

    @property
    def tempData(self):
        self.get_prop('temp')

    @tempData.setter
    def tempData(self,value):
        self.set_prop('temp',value)


    def _ex_get_react_data(self) -> Dict[str, Any]:
        data= super()._ex_get_react_data()    
        data.update({
            'temp':None
        })
        return data
            