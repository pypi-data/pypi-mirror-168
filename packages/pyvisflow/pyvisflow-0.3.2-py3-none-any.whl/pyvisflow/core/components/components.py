from abc import abstractmethod
from typing import Any, Dict, List, Tuple, Union

from pyvisflow.core.props.typeProp import StrTypePropInfo
from pyvisflow.models.TComponent import TComponent, TComponentType
import re

from pyvisflow.core.reactive import Reactive

RE_match_array = re.compile(r'(?P<name>.+)(\[(?P<num>\d+)\])')


class Component(Reactive):
    def __init__(self, tag: str, type: TComponentType) -> None:
        super().__init__()
        self._tag = tag
        self._type = type
        self._attrs = {}
        self._styles = {}
        self._children: List[Component] = []
        self._stylesProp = StyleProp(self)

    @property
    def styles(self):
        return self._stylesProp

    def update_attrs(self, **kws):
        self._attrs.update(kws)
        return self

    def update_styles(self, **kws):

        for key, value in kws.items():
            self.set_prop(f'styles.{key}', value)

        return self

    def _ex_get_react_data(self) -> Dict[str, Any]:
        if self._type == TComponentType.builtIn:
            data = {
                'attrs': self._attrs,
                'styles': self._styles,
            }

            return data

        return {}

    def to_model(self) -> TComponent:
        children = [c.to_model() for c in self._children]
        return TComponent(id=self._id,
                          type=self._type,
                          tag=self._tag,
                          attrs=self._attrs,
                          styles=self._styles,
                          children=children)


class StyleProp():
    def __init__(self, cp: Component) -> None:
        self.__cp = cp

    def set(self, name: str, value: Union[StrTypePropInfo, str]):
        self.__cp.set_prop(f'styles.{name}', value)
        return self

    @property
    def width(self):
        '''
        width 属性用于设置元素的宽度
        /* <length> values */
        width: 300px;
        width: 25em;

        /* <percentage> value */
        width: 75%;

        /* Keyword values */
        width: max-content;
        width: min-content;
        width: fit-content(20em);
        width: auto;

        /* Global values */
        width: inherit;
        width: initial;
        width: unset;
        '''
        p = self.__cp.get_prop('styles.width')
        return StrTypePropInfo(p)

    def make_center(self):
        self.set('display', 'flex').set('justify-content',
                                        'center').set('align-items', 'center')
        return self

    def set_width(self, value: Union[StrTypePropInfo, str]):
        self.__cp.set_prop('styles.width', value)
        return self

    def set_height(self, value: Union[StrTypePropInfo, str]):
        self.__cp.set_prop('styles.height', value)
        return self

    def set_fixed(
            self,
            top: Union[StrTypePropInfo, str] = 'unset',
            right: Union[StrTypePropInfo, str] = 'unset',
            bottom: Union[StrTypePropInfo, str] = 'unset',
            left: Union[StrTypePropInfo, str] = 'unset',
    ):
        '''
        元素的位置在屏幕滚动时不会改变。打印时，元素会出现在的每页的固定位置
        '''
        self.__cp.set_prop('styles.position', 'fixed')
        self.__cp.set_prop('styles.top', top)
        self.__cp.set_prop('styles.right', right)
        self.__cp.set_prop('styles.bottom', bottom)
        self.__cp.set_prop('styles.left', left)

        from pyvisflow.core.components.containers import BoxContainer
        if isinstance(self.__cp,BoxContainer):
            self.__cp._teleportTarget='body'

        return self

    def set_absolute(
            self,
            top: Union[StrTypePropInfo, str] = '0',
            right: Union[StrTypePropInfo, str] = 'unset',
            bottom: Union[StrTypePropInfo, str] = 'unset',
            left: Union[StrTypePropInfo, str] = '0',
    ):
        '''
        元素会被移出正常文档流，并不为元素预留空间，通过指定元素相对于最近的非 static 定位祖先元素的偏移，来确定元素位置。绝对定位的元素可以设置外边距（margins），且不会与其他边距合并
        '''
        self.__cp.set_prop('styles.position', 'absolute')
        self.__cp.set_prop('styles.top', top)
        self.__cp.set_prop('styles.right', right)
        self.__cp.set_prop('styles.bottom', bottom)
        self.__cp.set_prop('styles.left', left)

        self.set_height('100%')
        return self

    def set_absolute_center(self):
        '''
        justify-content: center;
        align-items: center;
        left: 50%;
        top: 50%;
        transform: translateX(-50%) translateY(-50%);
        '''
        self.set('display', 'flex').set('justify-content', 'center').set(
            'align-items',
            'center').set('transform',
                          'translateX(-50%) translateY(-50%)').set(
                              'left', '50%').set('top', '50%')
        return self

    def set_absolute_left(self):
        '''
        justify-content: center;
        align-items: center;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        '''
        self.set('display', 'flex').set('justify-content', 'center').set(
            'align-items', 'center').set('transform',
                                         'translateX(0) translateY(-50%)').set(
                                             'top', '50%').set('left', '0')
        return self

    def set_border(self,
                   value: Union[StrTypePropInfo, str] = '1px solid black'):
        '''
        border属性是一个用于设置各种单独的边界属性的简写属性。border可以用于设置一个或多个以下属性的值： border-width, border-style, border-color。
        '''
        self.__cp.set_prop('styles.border', value)
        return self

    def set_margin(self, value: Union[StrTypePropInfo, str] = '1rem'):
        '''
        margin 属性为给定元素设置所有四个（上下左右）方向的外边距属性。也就是 margin-top，margin-right，margin-bottom，和 margin-left 四个外边距属性设置的简写
        '''
        self.__cp.set_prop('styles.margin', value)
        return self

    def set_background(self, value: Union[StrTypePropInfo, str] = 'unset'):
        '''
        background 是一种 CSS 简写属性，用于一次性集中定义各种背景属性，包括 color, image, origin 与 size, repeat 方式等等。
        '''
        self.__cp.set_prop('styles.background', value)
        return self

    def set_border_radius(self, value: Union[StrTypePropInfo, str] = '2rem'):
        '''
        border-radius 允许你设置元素的外边框圆角。当使用一个半径时确定一个圆形，当使用两个半径时确定一个椭圆。这个(椭)圆与边框的交集形成圆角效果
        '''
        self.__cp.set_prop('styles.border-radius', value)
        return self

    def set_transition(self, value: Union[StrTypePropInfo, str] = '0.6s'):
        '''
        transition CSS 属性是 transition-property，transition-duration，transition-timing-function 和 transition-delay 的一个简写属性。        '''
        self.__cp.set_prop('styles.transition', value)
        return self