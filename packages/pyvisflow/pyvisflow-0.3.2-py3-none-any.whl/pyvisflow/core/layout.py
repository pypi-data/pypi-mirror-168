from __future__ import annotations

from typing import Dict, Generator, Iterable, TYPE_CHECKING, Optional
from pyvisflow.models.TComponent import TComponentType
from pyvisflow.utils.markdown2 import markdown

from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag
import re
from pyvisflow.core.components import Component
from pyvisflow.core.components.markdownValue import MarkdownValue

if TYPE_CHECKING:
    from pyvisflow.core.props import TypePropInfo

RE_CONTROLER = re.compile('{{.+?}}')


class MarkdownLayout():
    def __init__(self,
                 md: str,
                 props_mapping: Optional[Dict[str, TypePropInfo]] = None
                 ) -> None:
        self._md = md
        self._props_mapping = props_mapping or {}
        self._component_mapping: Dict[str, MarkdownValue] = {}

    def __update_prop2cp(self, cp_name: str, prop: TypePropInfo):
        assert cp_name in self._component_mapping, f'not found name[{cp_name}] in markdown'
        # self._component_mapping[cp_name].update_attrs(**{
        #     'id': prop.reactive._id, 'path': prop.get_trigger_path(), 'logic': prop.get_post_change_logic('return change')
        # })
        self._component_mapping[cp_name].set_value(prop)

    def parse_markdown(self, ):
        def _gen_from_string(s: str) -> Generator[Component, None, None]:
            mats = list(RE_CONTROLER.finditer(s))

            start = 0
            for m in mats:
                if m.start() > start:
                    yield Component(tag=s[start:m.start()],
                                    type=TComponentType.htmlRawString)
                    # yield Controler(tag=s[start:m.start()], type=ControlerTypeEnum.htmlRawString, responsive=False, children=[])

                cp_name = m.group().replace('{{', '').replace('}}', '')
                self._component_mapping[cp_name] = MarkdownValue()

                if cp_name in self._props_mapping:
                    prop = self._props_mapping[cp_name]
                    self.__update_prop2cp(cp_name, prop)

                yield self._component_mapping[cp_name]

                start = m.end()

            if start == 0:
                yield Component(tag=s, type=TComponentType.htmlRawString)

        def _gen_nodes(tags: Iterable[PageElement] or str, ):
            for t in tags:
                if type(t) is Tag:
                    cp = Component(tag=t.name, type=TComponentType.htmlRaw)
                    cp._children = list(_gen_nodes(t.children))
                    yield cp
                else:
                    if t == '\n':
                        continue
                    yield from _gen_from_string(t)

        html = markdown(
            self._md, extras=['fenced-code-blocks', 'task_list', 'code-color'])
        soup = BeautifulSoup(html, 'html.parser')
        return _gen_nodes(soup.children)

    def set(self, **prop_mapping: TypePropInfo):
        for name, prop in prop_mapping.items():
            self.__update_prop2cp(name, prop)
