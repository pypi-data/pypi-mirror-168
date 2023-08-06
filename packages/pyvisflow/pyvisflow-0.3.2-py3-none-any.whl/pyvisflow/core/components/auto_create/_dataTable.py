from typing import Union,Dict,List
from pyvisflow.core.components.components import Component
from pyvisflow.core.props import StrTypePropInfo, NumberTypePropInfo, BoolTypePropInfo
from pyvisflow.models.TComponent import TComponentType
from pyvisflow.core.props import *

TypePropInfo=Union[StrTypePropInfo,NumberTypePropInfo,BoolTypePropInfo]

class _DataTable(Component):
    '''
    Input Number 数字输入框
仅允许输入标准的数字值，可定义范围
    '''

    def __init__(self) -> None:
        super().__init__('dataTable', TComponentType.builtIn)

    def _ex_get_react_data(self):
        return super()._ex_get_react_data()


    @property
    def current_page(self):
        '''
        可选值：nan \n
        分页时，当前页数
        '''

        
        p = self.get_prop('currentPage')
        return NumberTypePropInfo(p)

        


    @current_page.setter
    def current_page(self, value: Union[NumberTypePropInfo,int]):
        '''
        可选值：nan \n
        分页时，当前页数
        '''
        self.set_prop('currentPage', value)

    @property
    def page_size(self):
        '''
        可选值：nan \n
        分页时，每页的记录数
        '''

        
        p = self.get_prop('pageSize')
        return NumberTypePropInfo(p)

        


    @page_size.setter
    def page_size(self, value: Union[NumberTypePropInfo,int]):
        '''
        可选值：nan \n
        分页时，每页的记录数
        '''
        self.set_prop('pageSize', value)

    @property
    def height(self):
        '''
        可选值：nan \n
        Table 的高度， 默认为自动高度。 如果 height 为 number 类型，单位 px；如果 height 为 string 类型，则这个高度会设置为 Table 的 style.height 的值，Table 的高度会受控于外部样式。
        '''

        
        p = self.get_prop('height')
        return StrTypePropInfo(p)

        


    @height.setter
    def height(self, value: Union[StrTypePropInfo,Union[str,float]]):
        '''
        可选值：nan \n
        Table 的高度， 默认为自动高度。 如果 height 为 number 类型，单位 px；如果 height 为 string 类型，则这个高度会设置为 Table 的 style.height 的值，Table 的高度会受控于外部样式。
        '''
        self.set_prop('height', value)

    @property
    def max_height(self):
        '''
        可选值：nan \n
        Table 的最大高度。 合法的值为数字或者单位为 px 的高度。
        '''

        
        p = self.get_prop('max-height')
        return StrTypePropInfo(p)

        


    @max_height.setter
    def max_height(self, value: Union[StrTypePropInfo,Union[str,float]]):
        '''
        可选值：nan \n
        Table 的最大高度。 合法的值为数字或者单位为 px 的高度。
        '''
        self.set_prop('max-height', value)

    @property
    def stripe(self):
        '''
        可选值：nan \n
        是否为斑马纹 table
        '''

        
        p = self.get_prop('stripe')
        return BoolTypePropInfo(p)

        


    @stripe.setter
    def stripe(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：nan \n
        是否为斑马纹 table
        '''
        self.set_prop('stripe', value)

    @property
    def border(self):
        '''
        可选值：nan \n
        是否带有纵向边框
        '''

        
        p = self.get_prop('border')
        return BoolTypePropInfo(p)

        


    @border.setter
    def border(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：nan \n
        是否带有纵向边框
        '''
        self.set_prop('border', value)

    @property
    def size(self):
        '''
        可选值：large / default /small \n
        Table 的尺寸
        '''

        
        p = self.get_prop('size')
        return StrTypePropInfo(p)

        


    @size.setter
    def size(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：large / default /small \n
        Table 的尺寸
        '''
        self.set_prop('size', value)

    @property
    def fit(self):
        '''
        可选值：large / default /small \n
        列的宽度是否自撑开
        '''

        
        p = self.get_prop('fit')
        return BoolTypePropInfo(p)

        


    @fit.setter
    def fit(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：large / default /small \n
        列的宽度是否自撑开
        '''
        self.set_prop('fit', value)

    @property
    def show_header(self):
        '''
        可选值：large / default /small \n
        是否显示表头
        '''

        
        p = self.get_prop('show-header')
        return BoolTypePropInfo(p)

        


    @show_header.setter
    def show_header(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：large / default /small \n
        是否显示表头
        '''
        self.set_prop('show-header', value)

    @property
    def highlight_current_row(self):
        '''
        可选值：large / default /small \n
        是否要高亮当前行
        '''

        
        p = self.get_prop('highlight-current-row')
        return BoolTypePropInfo(p)

        


    @highlight_current_row.setter
    def highlight_current_row(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：large / default /small \n
        是否要高亮当前行
        '''
        self.set_prop('highlight-current-row', value)

    @property
    def empty_text(self):
        '''
        可选值：large / default /small \n
        空数据时显示的文本内容， 也可以通过 #empty 设置
        '''

        
        p = self.get_prop('empty-text')
        return StrTypePropInfo(p)

        


    @empty_text.setter
    def empty_text(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：large / default /small \n
        空数据时显示的文本内容， 也可以通过 #empty 设置
        '''
        self.set_prop('empty-text', value)

    @property
    def default_expand_all(self):
        '''
        可选值：large / default /small \n
        是否默认展开所有行，当 Table 包含展开行存在或者为树形表格时有效
        '''

        
        p = self.get_prop('default-expand-all')
        return BoolTypePropInfo(p)

        


    @default_expand_all.setter
    def default_expand_all(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：large / default /small \n
        是否默认展开所有行，当 Table 包含展开行存在或者为树形表格时有效
        '''
        self.set_prop('default-expand-all', value)

    @property
    def default_sort(self):
        '''
        可选值：order: ascending / descending \n
        默认的排序列的 prop 和顺序。 它的 prop 属性指定默认的排序的列，order 指定默认排序的顺序
        '''

        
        return self.get_prop('default-sort')
        


    @default_sort.setter
    def default_sort(self, value: Union[TypePropInfo,Dict]):
        '''
        可选值：order: ascending / descending \n
        默认的排序列的 prop 和顺序。 它的 prop 属性指定默认的排序的列，order 指定默认排序的顺序
        '''
        self.set_prop('default-sort', value)

    @property
    def tooltip_effect(self):
        '''
        可选值：dark / light \n
        tooltip effect 属性
        '''

        
        p = self.get_prop('tooltip-effect')
        return StrTypePropInfo(p)

        


    @tooltip_effect.setter
    def tooltip_effect(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：dark / light \n
        tooltip effect 属性
        '''
        self.set_prop('tooltip-effect', value)

    @property
    def show_summary(self):
        '''
        可选值：dark / light \n
        是否在表尾显示合计行
        '''

        
        p = self.get_prop('show-summary')
        return BoolTypePropInfo(p)

        


    @show_summary.setter
    def show_summary(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：dark / light \n
        是否在表尾显示合计行
        '''
        self.set_prop('show-summary', value)

    @property
    def sum_text(self):
        '''
        可选值：dark / light \n
        合计行第一列的文本
        '''

        
        p = self.get_prop('sum-text')
        return StrTypePropInfo(p)

        


    @sum_text.setter
    def sum_text(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：dark / light \n
        合计行第一列的文本
        '''
        self.set_prop('sum-text', value)

    @property
    def select_on_indeterminate(self):
        '''
        可选值：dark / light \n
        在多选表格中，当仅有部分行被选中时，点击表头的多选框时的行为。 若为 true，则选中所有行；若为 false，则取消选择所有行
        '''

        
        p = self.get_prop('select-on-indeterminate')
        return BoolTypePropInfo(p)

        


    @select_on_indeterminate.setter
    def select_on_indeterminate(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：dark / light \n
        在多选表格中，当仅有部分行被选中时，点击表头的多选框时的行为。 若为 true，则选中所有行；若为 false，则取消选择所有行
        '''
        self.set_prop('select-on-indeterminate', value)

    @property
    def indent(self):
        '''
        可选值：dark / light \n
        展示树形数据时，树节点的缩进
        '''

        
        p = self.get_prop('indent')
        return NumberTypePropInfo(p)

        


    @indent.setter
    def indent(self, value: Union[NumberTypePropInfo,float]):
        '''
        可选值：dark / light \n
        展示树形数据时，树节点的缩进
        '''
        self.set_prop('indent', value)

    @property
    def lazy(self):
        '''
        可选值：dark / light \n
        是否懒加载子节点数据
        '''

        
        p = self.get_prop('lazy')
        return BoolTypePropInfo(p)

        


    @lazy.setter
    def lazy(self, value: Union[BoolTypePropInfo,bool]):
        '''
        可选值：dark / light \n
        是否懒加载子节点数据
        '''
        self.set_prop('lazy', value)

    @property
    def tree_props(self):
        '''
        可选值：dark / light \n
        渲染嵌套数据的配置选项
        '''

        
        return self.get_prop('tree-props')
        


    @tree_props.setter
    def tree_props(self, value: Union[TypePropInfo,Dict]):
        '''
        可选值：dark / light \n
        渲染嵌套数据的配置选项
        '''
        self.set_prop('tree-props', value)

    @property
    def table_layout(self):
        '''
        可选值：fixed / auto \n
        Sets the algorithm used to lay out table cells, rows, and columns
        '''

        
        p = self.get_prop('table-layout')
        return StrTypePropInfo(p)

        


    @table_layout.setter
    def table_layout(self, value: Union[StrTypePropInfo,str]):
        '''
        可选值：fixed / auto \n
        Sets the algorithm used to lay out table cells, rows, and columns
        '''
        self.set_prop('table-layout', value)
