from typing import Union,Dict,List
from pyvisflow.core.components.components import Component
from pyvisflow.core.props import StrTypePropInfo, NumberTypePropInfo, BoolTypePropInfo
from pyvisflow.models.TComponent import TComponentType
from pyvisflow.core.props import *

TypePropInfo=Union[StrTypePropInfo,NumberTypePropInfo,BoolTypePropInfo]

class _Select(Component):
    '''
    Select 选择器
当选项过多时，使用下拉菜单展示并选择内容
    '''

    def __init__(self) -> None:
        super().__init__('select', TComponentType.builtIn)

    def _ex_get_react_data(self):
        return super()._ex_get_react_data()


    @property
    def multiple(self):
        '''
        可选值：— \n
        是否多选
        '''

        
        p = self.get_prop('multiple')
        return BoolTypePropInfo(p)

        


    @multiple.setter
    def multiple(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：— \n
        是否多选
        '''
        self.set_prop('multiple', value)

    @property
    def disabled(self):
        '''
        可选值：— \n
        是否禁用
        '''

        
        p = self.get_prop('disabled')
        return BoolTypePropInfo(p)

        


    @disabled.setter
    def disabled(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：— \n
        是否禁用
        '''
        self.set_prop('disabled', value)

    @property
    def value_key(self):
        '''
        可选值：— \n
        作为 value 唯一标识的键名，绑定值为对象类型时必填
        '''

        
        p = self.get_prop('value-key')
        return StrTypePropInfo(p)

        


    @value_key.setter
    def value_key(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：— \n
        作为 value 唯一标识的键名，绑定值为对象类型时必填
        '''
        self.set_prop('value-key', value)

    @property
    def size(self):
        '''
        可选值：large/default/small \n
        输入框尺寸
        '''

        
        p = self.get_prop('size')
        return StrTypePropInfo(p)

        


    @size.setter
    def size(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：large/default/small \n
        输入框尺寸
        '''
        self.set_prop('size', value)

    @property
    def clearable(self):
        '''
        可选值：large/default/small \n
        是否可以清空选项
        '''

        
        p = self.get_prop('clearable')
        return BoolTypePropInfo(p)

        


    @clearable.setter
    def clearable(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：large/default/small \n
        是否可以清空选项
        '''
        self.set_prop('clearable', value)

    @property
    def collapse_tags(self):
        '''
        可选值：large/default/small \n
        多选时是否将选中值按文字的形式展示
        '''

        
        p = self.get_prop('collapse-tags')
        return BoolTypePropInfo(p)

        


    @collapse_tags.setter
    def collapse_tags(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：large/default/small \n
        多选时是否将选中值按文字的形式展示
        '''
        self.set_prop('collapse-tags', value)

    @property
    def multiple_limit(self):
        '''
        可选值：large/default/small \n
        多选时用户最多可以选择的项目数， 为 0 则不限制
        '''

        
        p = self.get_prop('multiple-limit')
        return NumberTypePropInfo(p)

        


    @multiple_limit.setter
    def multiple_limit(self, value: Union[NumberTypePropInfo,int]):
        '''
        可选值：large/default/small \n
        多选时用户最多可以选择的项目数， 为 0 则不限制
        '''
        self.set_prop('multiple-limit', value)

    @property
    def name(self):
        '''
        可选值：large/default/small \n
        多选框的输入框的原生 name 属性
        '''

        
        p = self.get_prop('name')
        return StrTypePropInfo(p)

        


    @name.setter
    def name(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：large/default/small \n
        多选框的输入框的原生 name 属性
        '''
        self.set_prop('name', value)

    @property
    def effect(self):
        '''
        可选值：string \n
        Tooltip theme, built-in theme: dark / light
        '''

        
        p = self.get_prop('effect')
        return StrTypePropInfo(p)

        


    @effect.setter
    def effect(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：string \n
        Tooltip theme, built-in theme: dark / light
        '''
        self.set_prop('effect', value)

    @property
    def autocomplete(self):
        '''
        可选值：string \n
        ‎选择输入的自动完成属性‎
        '''

        
        p = self.get_prop('autocomplete')
        return StrTypePropInfo(p)

        


    @autocomplete.setter
    def autocomplete(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：string \n
        ‎选择输入的自动完成属性‎
        '''
        self.set_prop('autocomplete', value)

    @property
    def placeholder(self):
        '''
        可选值：string \n
        ‎占 位 符‎
        '''

        
        p = self.get_prop('placeholder')
        return StrTypePropInfo(p)

        


    @placeholder.setter
    def placeholder(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：string \n
        ‎占 位 符‎
        '''
        self.set_prop('placeholder', value)

    @property
    def filterable(self):
        '''
        可选值：string \n
        ‎选择是否可过滤‎
        '''

        
        p = self.get_prop('filterable')
        return BoolTypePropInfo(p)

        


    @filterable.setter
    def filterable(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：string \n
        ‎选择是否可过滤‎
        '''
        self.set_prop('filterable', value)

    @property
    def allow_create(self):
        '''
        可选值：string \n
        ‎是否允许创建新项目。要使用此，必须为 true‎filterable
        '''

        
        p = self.get_prop('allow-create')
        return BoolTypePropInfo(p)

        


    @allow_create.setter
    def allow_create(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：string \n
        ‎是否允许创建新项目。要使用此，必须为 true‎filterable
        '''
        self.set_prop('allow-create', value)

    @property
    def remote(self):
        '''
        可选值：string \n
        ‎是否从服务器加载选项‎
        '''

        
        p = self.get_prop('remote')
        return BoolTypePropInfo(p)

        


    @remote.setter
    def remote(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：string \n
        ‎是否从服务器加载选项‎
        '''
        self.set_prop('remote', value)

    @property
    def loading(self):
        '''
        可选值：string \n
        ‎选择是否正在从服务器加载数据‎
        '''

        
        p = self.get_prop('loading')
        return BoolTypePropInfo(p)

        


    @loading.setter
    def loading(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：string \n
        ‎选择是否正在从服务器加载数据‎
        '''
        self.set_prop('loading', value)

    @property
    def loading_text(self):
        '''
        可选值：string \n
        ‎从服务器加载数据时显示的文本‎
        '''

        
        p = self.get_prop('loading-text')
        return StrTypePropInfo(p)

        


    @loading_text.setter
    def loading_text(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：string \n
        ‎从服务器加载数据时显示的文本‎
        '''
        self.set_prop('loading-text', value)

    @property
    def no_match_text(self):
        '''
        可选值：string \n
        ‎当没有数据与过滤查询匹配时显示的文本，也可以使用 slot‎empty
        '''

        
        p = self.get_prop('no-match-text')
        return StrTypePropInfo(p)

        


    @no_match_text.setter
    def no_match_text(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：string \n
        ‎当没有数据与过滤查询匹配时显示的文本，也可以使用 slot‎empty
        '''
        self.set_prop('no-match-text', value)

    @property
    def no_data_text(self):
        '''
        可选值：string \n
        ‎显示文本时没有选项，也可以使用插槽‎empty
        '''

        
        p = self.get_prop('no-data-text')
        return StrTypePropInfo(p)

        


    @no_data_text.setter
    def no_data_text(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：string \n
        ‎显示文本时没有选项，也可以使用插槽‎empty
        '''
        self.set_prop('no-data-text', value)

    @property
    def popper_class(self):
        '''
        可选值：string \n
        ‎"选择"下拉列表的自定义类名‎
        '''

        
        p = self.get_prop('popper-class')
        return StrTypePropInfo(p)

        


    @popper_class.setter
    def popper_class(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：string \n
        ‎"选择"下拉列表的自定义类名‎
        '''
        self.set_prop('popper-class', value)

    @property
    def reserve_keyword(self):
        '''
        可选值：string \n
        ‎何时 为 true，是否在选择选项后保留当前关键字‎multiplefilter
        '''

        
        p = self.get_prop('reserve-keyword')
        return BoolTypePropInfo(p)

        


    @reserve_keyword.setter
    def reserve_keyword(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：string \n
        ‎何时 为 true，是否在选择选项后保留当前关键字‎multiplefilter
        '''
        self.set_prop('reserve-keyword', value)

    @property
    def default_first_option(self):
        '''
        可选值：string \n
        ‎在输入键上选择第一个匹配选项。与 或 一起使用‎filterableremote
        '''

        
        p = self.get_prop('default-first-option')
        return BoolTypePropInfo(p)

        


    @default_first_option.setter
    def default_first_option(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：string \n
        ‎在输入键上选择第一个匹配选项。与 或 一起使用‎filterableremote
        '''
        self.set_prop('default-first-option', value)

    @property
    def teleported(self):
        '''
        可选值：true / false \n
        ‎选择下拉列表是否传送到正文‎
        '''

        
        p = self.get_prop('teleported')
        return BoolTypePropInfo(p)

        


    @teleported.setter
    def teleported(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：true / false \n
        ‎选择下拉列表是否传送到正文‎
        '''
        self.set_prop('teleported', value)

    @property
    def persistent(self):
        '''
        可选值：true / false \n
        ‎当选择下拉列表处于非活动状态并且是 时，选择下拉列表将被销毁‎persistentfalse
        '''

        
        p = self.get_prop('persistent')
        return BoolTypePropInfo(p)

        


    @persistent.setter
    def persistent(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：true / false \n
        ‎当选择下拉列表处于非活动状态并且是 时，选择下拉列表将被销毁‎persistentfalse
        '''
        self.set_prop('persistent', value)

    @property
    def automatic_dropdown(self):
        '''
        可选值：true / false \n
        ‎对于不可过滤的 Select，此属性决定在输入聚焦时是否弹出选项菜单‎
        '''

        
        p = self.get_prop('automatic-dropdown')
        return BoolTypePropInfo(p)

        


    @automatic_dropdown.setter
    def automatic_dropdown(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：true / false \n
        ‎对于不可过滤的 Select，此属性决定在输入聚焦时是否弹出选项菜单‎
        '''
        self.set_prop('automatic-dropdown', value)

    @property
    def fit_input_width(self):
        '''
        可选值：true / false \n
        ‎下拉列表的宽度是否与输入相同‎
        '''

        
        p = self.get_prop('fit-input-width')
        return BoolTypePropInfo(p)

        


    @fit_input_width.setter
    def fit_input_width(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：true / false \n
        ‎下拉列表的宽度是否与输入相同‎
        '''
        self.set_prop('fit-input-width', value)

    @property
    def tag_type(self):
        '''
        可选值：success/info/warning/danger \n
        ‎标记类型‎
        '''

        
        p = self.get_prop('tag-type')
        return StrTypePropInfo(p)

        


    @tag_type.setter
    def tag_type(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：success/info/warning/danger \n
        ‎标记类型‎
        '''
        self.set_prop('tag-type', value)
