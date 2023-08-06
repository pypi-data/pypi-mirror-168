from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union,TYPE_CHECKING
from pyvisflow.core.components.containers import BoxContainer, Component
from pyvisflow.core.dataManager import DataFrameManager
from pyvisflow.core.dataset.dataset import ReactiveDataset
from pyvisflow.core.dataset.props import ReactiveDatasetPropInfo
from pyvisflow.core.optimizers import WatchValueOptimizer
from pyvisflow.core.props import create_getby_prop
from pyvisflow.core.props.fns import Fns
from pyvisflow.core.structure import Mapping
from pyvisflow.models.TConfig import TReactData, TConfig
from pyvisflow.models.TStaticData import TStaticData
from pyvisflow.models.TWatchInfo import TTargetWatchInfo, TValueWatch, TWatchInfo
from pyvisflow.models.TComponent import TComponentType
from pyvisflow.utils.data_gen import get_project_root, json_dumps_fn
from pyvisflow.utils.helper import flatten
import pandas as pd
import re
from pyvisflow.core.components.file import FileData
from pyvisflow.core.dataset import StaticDataset
if TYPE_CHECKING:
    from pyvisflow.core.reactive import Reactive
    

__scripts_mapping__ = {'plotly': 'plotly-2.9.0.min.js'}
__re_app_div__ = re.compile(r'<div\sid="app"></div>')


class App(BoxContainer):
    def __init__(self) -> None:
        super().__init__()
        self.structures: List[Reactive] = []
        self.df_manager = DataFrameManager()
        self.dataset_collector : List[ReactiveDataset] = []
        self._scripts: Set[str] = set()
        self.fns = Fns(self)

        def on_before_data_fn(data: Union[pd.DataFrame,FileData,StaticDataset,ReactiveDataset]):
            if isinstance(data, pd.DataFrame):
                return self.dataset(data)

            if isinstance(data, StaticDataset):
                self.df_manager.mark_dataset(data)

            if isinstance(data, ReactiveDataset):
                self.dataset_collector.append(data)

            if isinstance(data,FileData):
                self.structures.append(data)
                return self.df_manager.mark_fileData(data)

            return data

        self._on_before_data_fn = on_before_data_fn

        def on_before_add_child_fn(cp: Component):
            if cp._tag == 'plotly':
                self._scripts.add(cp._tag)

        self._on_before_add_child_fn = on_before_add_child_fn



    def dataset(self,df:pd.DataFrame):
        sd = StaticDataset(df)
        self._on_before_data_fn(sd)
        reactDs= sd.create_reactive_dataset()
        self._on_before_data_fn(reactDs)
        return ReactiveDatasetPropInfo(create_getby_prop(reactDs._id,'dataframe'))

    @property
    def Fns(self):
        return self.fns

    def mapping(self, mapping: Optional[Dict[str, Dict[str, Any]]] = None):
        m = Mapping(mapping)
        self.structures.append(m)
        return m

    def add_srcipt(self, *names: str):
        for n in names:
            assert n in __scripts_mapping__, f'not support {n} script'
        for n in names:
            self._scripts.add(n)

    def pretty_json(self):
        return json_dumps_fn(self.create_config(), indent=2)

    def config2file(self, file):
        return Path(file).write_text(self.pretty_json(), 'utf8')

    def create_config(self):
        cps = [self.to_model()]

        # reactData for each
        cps_flatten = list(flatten(self, lambda x: x._children))
        reactData = [
            TReactData(id=cp._id, data=cp._create_react_data())
            for cp in cps_flatten if cp._type not in
            {TComponentType.htmlRaw, TComponentType.htmlRawString}
        ]

        structure_data = [
            TReactData(id=s._id, data=s._create_react_data())
            for s in self.structures
        ]

        reactData.extend(structure_data)

        
        reactive_ds = [
            TReactData(id=ds._id,data = ds._create_react_data())
            for ds in self.dataset_collector
        ]
        reactData.extend(reactive_ds)


        vw_optimizer= WatchValueOptimizer()
        
        for cp in cps_flatten:
            vw_optimizer.preload(cp)

        for s in self.structures:
            vw_optimizer.preload(s)

        for ds in self.dataset_collector:
            vw_optimizer.preload(ds)

        opt_res= vw_optimizer.create_infos()

        reactData.extend(opt_res.tempReactiveDatas)

        watchInfo = TWatchInfo(values=opt_res.watchs)

        return TConfig(
            staticData=TStaticData(dataframes=self.df_manager.to_model()),
            cps=cps,
            reactDatas=reactData,
            watchInfo=watchInfo)

    def __reset_data(self):
        self._children.clear()
        self.df_manager.reset()

    def to_raw_html(self):
        symbol = '"__{{__config_data__}}___"'
        scripts_tag = '<!-- [__other_scripts__] -->'

        def script2module(name: str):
            file = get_project_root() / 'template' / __scripts_mapping__[name]
            return f'<script>{file.read_text()}</script>'

        script_codes = ' '.join(script2module(s) for s in self._scripts)

        config = self.create_config()
        self.__reset_data()
        config = json_dumps_fn(config)

        with open(get_project_root() / 'template/index.html',
                  mode='r',
                  encoding='utf8') as html:
            res = html.read().replace(symbol, config).replace(
                '<div id="app"></div>', f'<div id="app"></div> {script_codes}')
            return res

    def to_html(self, file):
        file = Path(file)
        raw = self.to_raw_html()
        Path(file).write_text(raw, 'utf8')

        print(f'to html:{file.absolute()}')


    def _repr_html_(self):
        return self.to_raw_html()