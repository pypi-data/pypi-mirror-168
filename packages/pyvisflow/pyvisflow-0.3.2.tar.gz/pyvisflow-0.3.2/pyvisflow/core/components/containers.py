from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, List, TYPE_CHECKING, Optional, Union

import pandas as pd
from pandas.io.formats.style import Styler as pdStyler
from pyvisflow.core.components.components import Component
from pyvisflow.core.components.dataTable import DataTable
from pyvisflow.core.components.dataframe import Dataframe
from pyvisflow.core.components.echart import EChart
from pyvisflow.core.components.icon import Icon
from pyvisflow.core.components.input import Input
from pyvisflow.core.components.inputNumber import InputNumber
from pyvisflow.core.components.plotly import Plotly
from pyvisflow.core.components.select import Select
from pyvisflow.core.components.text import Text
from pyvisflow.core.components.file import File
from pyvisflow.core.components.image import Image
from pyvisflow.core.components.button import Button
from pyvisflow.core.dataset.props import DatasetSeriesArrayPropInfo, DatasetSeriesPropInfo, ReactiveDatasetPropInfo

from pyvisflow.core.layout import MarkdownLayout
from pyvisflow.core.props import BoolTypePropInfo

from io import BytesIO

from pyvisflow.models.TComponent import TComponentType
from pyvisflow.utils.data_gen import data2html_img_src

if TYPE_CHECKING:
    from pyvisflow.core.components.file import FileData
    from pyvisflow.core.props import TTypePropInfo

class Container(Component):
    def __init__(self, tag: str, type=TComponentType.builtIn) -> None:
        super().__init__(tag, type)

    def add_child(self, cp: Component):
        self._children.append(cp)
        return cp


class MarkdownBoxContainer(Container):
    def __init__(self) -> None:
        super().__init__('markdown-box')


class BoxContainer(Container):
    def __init__(self, sepc=0) -> None:
        super().__init__('box')
        self._spec = sepc
        self._on_before_data_fn = lambda data: data
        self._on_before_add_child_fn = BoxContainer.__default_on_before_add_child_fn
        self._teleportTarget=''

    @staticmethod
    def __default_on_before_add_child_fn(cp: Component):
        pass


    def file(self):
        cp = File()
        self._on_before_add_child_fn(cp)
        self.add_child(cp)
        return cp

    def __image(self,value:str):
        cp = Image(value)
        self._on_before_add_child_fn(cp)
        self.add_child(cp)
        return cp

    def dataframe(self,styler:pd.DataFrame | pdStyler):
        if isinstance(styler,pd.DataFrame):
            styler = styler.style

        cp = Dataframe(styler)
        self._on_before_add_child_fn(cp)
        self.add_child(cp)
        return cp

    def image_from_url(self,url:str):
        return self.__image(url)
    
    def button(self,text:str):
        cp = Button(text)
        self._on_before_add_child_fn(cp)
        self.add_child(cp)
        return cp

    def image_from_file(self,path:str):
        with open(path,'rb') as f:
            value = data2html_img_src(f.read())
            return self.__image(value)

    def image_from_mpl(self,fig):
        png = None
        with BytesIO() as buf:
            fig.savefig(buf, format='png')
            buf.seek(0)
            png=buf.getvalue()
        
        value = data2html_img_src(png)
        return self.__image(value)

    def box(self, ):
        cp = BoxContainer()
        cp._on_before_data_fn = self._on_before_data_fn
        cp._on_before_add_child_fn = self._on_before_add_child_fn

        self._on_before_add_child_fn(cp)
        self.add_child(cp)
        return cp

    def row(self, ):
        cp = Row()
        cp._on_before_data_fn = self._on_before_data_fn
        self._on_before_add_child_fn(cp)
        self.add_child(cp)
        return cp

    def icon(self, svg: str, size: str):
        cp = Icon(svg, size)
        self._on_before_add_child_fn(cp)
        self.add_child(cp)
        return cp

    def icon_fromfile(self, file: str, size: str):
        with open(file, 'r', encoding='utf8') as f:
            return self.icon(f.read(), size)

    def text(self, value: str):
        cp = Text(value)
        self._on_before_add_child_fn(cp)
        self.add_child(cp)
        return cp

    def dataTable(self, reactDataset: pd.DataFrame | ReactiveDatasetPropInfo | DatasetSeriesPropInfo, page_size=5):

        if isinstance(reactDataset,pd.DataFrame):
            reactDataset = self._on_before_data_fn(reactDataset)


        cp = DataTable(reactDataset)
        cp.page_size = page_size
        self._on_before_add_child_fn(cp)
        self.add_child(cp)
        return cp

    def tabs(self, names: Union[Iterable[str], Dict[str, str]]):
        cp = tabs.Tabs(names)
        self._on_before_add_child_fn(cp)
        self.add_child(cp)

        for box in cp.boxes:
            box._on_before_data_fn = self._on_before_data_fn
            box._on_before_add_child_fn = self._on_before_add_child_fn

        return cp

    def plotly(self):
        cp = Plotly()
        self._on_before_add_child_fn(cp)
        self.add_child(cp)
        return cp

    def cols(self, spec: Union[int, List[int]]):
        cp = ColumnsContainer(spec)
        self._on_before_add_child_fn(cp)
        self.add_child(cp)

        for box in cp.boxes:
            box._on_before_data_fn = self._on_before_data_fn
            box._on_before_add_child_fn = self._on_before_add_child_fn

        return cp

    def input(self, value=''):
        cp = Input(value)
        self._on_before_add_child_fn(cp)
        self.add_child(cp)
        return cp

    def inputNumber(self, value=0):
        cp = InputNumber(value)
        self._on_before_add_child_fn(cp)
        self.add_child(cp)
        return cp

    def select(self, options: Iterable[str] | DatasetSeriesArrayPropInfo | ReactiveDatasetPropInfo | DatasetSeriesPropInfo):
        cp = Select(options)
        self._on_before_add_child_fn(cp)
        self.add_child(cp)
        return cp

    def echart(self):
        cp = EChart()
        self._on_before_add_child_fn(cp)
        self.add_child(cp)
        return cp

    def markdown(self, md: str, **prop_mapping: TTypePropInfo):
        layout = MarkdownLayout(md, prop_mapping)

        box = self.__markdown_box()

        for cp in layout.parse_markdown():
            self._on_before_add_child_fn(cp)
            box.add_child(cp)
        return layout

    def __markdown_box(self):
        cp = MarkdownBoxContainer()
        self._on_before_add_child_fn(cp)
        self.add_child(cp)
        return cp

    @property
    def isHover(self):
        p = self.get_prop('isHover')
        return BoolTypePropInfo(p)

    def _ex_get_react_data(self) -> Dict[str, Any]:
        data = super()._ex_get_react_data()
        data.update({'spec': self._spec, 'isHover': False,'teleportTarget':self._teleportTarget})
        return data


class ColumnsContainer(Container):
    def __init__(
            self,
            spec: Union[int, List[int]]) -> None:
        super().__init__('columns-container')

        self._is_grid = not isinstance(spec, int)

        __spec = spec
        if isinstance(spec, int):
            __spec = [spec for _ in range(spec)]
        self._spec = __spec
        self._boxes = tuple([BoxContainer(s) for s in __spec])
        for box in self._boxes:
            self.add_child(box)

    @property
    def boxes(self):
        return self._boxes

    def __iter__(self):
        return iter(self.boxes)

    def __getitem__(self, index: int):
        return self._boxes[index]


    def _ex_get_react_data(self) -> Dict[str, Any]:
        data = super()._ex_get_react_data()
        data.update({'spec': self._spec, 'isGrid': self._is_grid})
        return data


class Row(BoxContainer):
    def __init__(self) -> None:
        super().__init__()
        self._tag='row'

    @property
    def isWrap(self):
        '''

        '''

        p = self.get_prop('isWrap')
        return BoolTypePropInfo(p)

    @isWrap.setter
    def isWrap(self, value: Union[BoolTypePropInfo, bool]):
        '''
        '''
        self.set_prop('isWrap', value)


import pyvisflow.core.components.tabs as tabs