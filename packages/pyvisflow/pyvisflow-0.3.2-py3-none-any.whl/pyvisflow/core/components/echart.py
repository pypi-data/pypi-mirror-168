from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from pyvisflow.core.dataset.props import DatasetSeriesPropInfo, ReactiveDatasetPropInfo
from pyvisflow.core.props import SubscriptableTypePropInfo, StrTypePropInfo
from pyvisflow.core.props.absProp import AbsPropInfo
import json


from .auto_create._echart import _EChart
from pyvisflow.core.jsCode import JsCode
from pyvisflow.core.user_utils.common import js_code

class EChart(_EChart):
    def __init__(
            self,
    ) -> None:
        super().__init__()
        self._series = []
        (
            self
            .set_option('series',[])
        )
        self._functionSettings=[]

    @property
    def utils(self, ):
        return Helper(self)

    def mark_json_code(self,option_path:str):
        self._functionSettings.append(option_path)
        return self

    def set_option(self, prop: str, data: Any or JsCode):
        if not prop.startswith('option.'):
            prop = f'option.{prop}'
        self.set_prop(prop, data)

        if isinstance(data,JsCode):
            self.mark_json_code(prop)
        return self

    def set_series(self, idx: int, prop: str, data: Any):
        self.set_option(f'series[{idx}].{prop}', data)
        return self

    @property
    def clickInfo(self):
        """点击联动属性
        可以获取用户点击图表上的图形时的相关信息，比如点击柱状图的某个柱子的数据，系列名等信息

        Returns:
            EventInfoWrapper: 属性包装器
        """
        return EventInfoWrapper(self,'clickInfo')

    @property
    def hoverInfo(self):
        """悬停联动属性
        可以获取 鼠标经过图表上的图形时的相关信息，比如经过柱状图的某个柱子的数据，系列名等信息

        Returns:
            EventInfoWrapper: 属性包装器
        """
        return EventInfoWrapper(self,'hoverInfo')


    def _ex_get_react_data(self):
        data = super()._ex_get_react_data()

        data.update({
            'option':{

            },
            'clickInfo': {},
            'hoverInfo':{},
            'functionSettings':self._functionSettings
        })
        return data


class EventInfoWrapper():

    def __init__(self,echart:EChart,info_name:str) -> None:
        self.__echart=echart
        self.__clickInfo_prop=self.__echart.get_prop(info_name)

    def __get_click_prop_info(self):
        return SubscriptableTypePropInfo[str, StrTypePropInfo](self.__clickInfo_prop) 

    @property
    def name(self):
        """ 数据名，类目名

        Returns:
            StrTypePropInfo: value of name
        """
        return self.__get_click_prop_info()['name']

    @property
    def data(self):
        """传入的原始数据项

        Returns:
            object: Data Objects
        """
        return self.__get_click_prop_info()['data']


class Helper():
    def __init__(self, echart: EChart) -> None:
        self._echart = echart

    def use_from_option_dict(self,option:Dict):
        for key,value in option.items():
            self._echart.set_option(key,value)
        return self

    def use_from_json_file(self,path:str):
        with open('fig.json',encoding='utf8') as f:
            opts = json.load(f)
            self.use_from_option_dict(opts)
            return self



    def setLastSymbol(self,series_index:int,last:str,others:str):
        echart = self._echart
        echart.set_option(f'series[{series_index}].symbol',js_code(f'''
            (value,p,opt)=>{{
                const len = opt.series[p.seriesIndex].data.length
                const lastPoint = p.dataIndex===len-1
                if(lastPoint){{
                    return '{last}'
                }}else{{
                    return '{others}'
                }}
            }}
        '''))

        echart.set_option('series[0].symbolRotate',js_code('''
            (value,p,opt,chart)=>{
                
                const len = opt.series[p.seriesIndex].data.length
                const lastPoint = p.dataIndex===len-1
                if(lastPoint){
                    const yData = opt.series[p.seriesIndex].data
                    const xData = opt.xAxis.data
                    let point1 = chart.convertToPixel({seriesIndex:p.seriesIndex},[xData[len-2],yData[len-2]])
                    let point2 = chart.convertToPixel({seriesIndex:p.seriesIndex},[xData[len-1],yData[len-1]])

                    /*
                    point2=[2,yData[len-1]]
                    point1=[1,yData[len-2]]
                    */

                    const dist = Math.sqrt(Math.pow(point2[0]-point1[0],2)+Math.pow(point2[1]-point1[1],2))

                    const deg = Math.round(Math.asin((point2[0]-point1[0])/dist) * 180 / Math.PI)

                    if(yData[len-1]>yData[len-2]){
                        return -deg
                    }

                    return deg +180
                    
                }else{
                    return 0
                }
            }
        '''))

        return echart
  


    def use_pie(self, dataset: ReactiveDatasetPropInfo):

        dataset = dataset.rename({0:'name',1:'value'})[['name','value']]

      
        self._echart.set_option('series', [{
            'type': 'pie',
            'id': self._echart._id,
            "universalTransition": True,
        }]) \
        .set_option('legend', {
                                'top': '5%',
                                'left': 'center'
                            },) \
        .set_option('series[0].data',dataset.to_jsObject())
        return PieHelper(self._echart)

    def use_bar(self, x: AbsPropInfo, y: AbsPropInfo):
        self._echart.set_option('xAxis',{}).set_option('yAxis',{})
        self._echart.set_option('series', [{
            'type': 'bar',
            'showBackground': True,
            'backgroundStyle': {
                'color': 'rgba(180, 180, 180, 0.2)'
            },
            'encode': {
                'x': x,
                'y': y
            },
            'id': self._echart._id,
            "universalTransition": True,
        }]).set_option('xAxis', {'type': 'category'}).set_prop(
        'option.xAxis.data',x).set_prop(
        'option.series[0].data',y
        )



        return BarHelper(self._echart)

    def use_line(self, x: AbsPropInfo, y: AbsPropInfo, color: Optional[str] = None):
        self._echart.set_option('xAxis',{}).set_option('yAxis',{})
        self._echart.set_option('series', [{
            'type': 'line',
            'encode': {
                'x': x,
                'y': y,
                'color' :color
            },
            'id': self._echart._id,
            "universalTransition": True,
        }]) \
        .set_option('xAxis', {'type': 'category'}) \
        .set_option('yAxis', {'type': 'value'}) \
        .set_option('tooltip', {'trigger': 'axis'}) \
        .set_option('xAxis.data',x) \
        .set_option('series[0].data',y)
        return LineHelper(self._echart)


class AbsHelper():

    def __init__(self, echart: EChart) -> None:
        self._echart = echart

    def set_prop(self, prop: str, value: Union[AbsPropInfo, Any]):
        self._echart.set_prop(prop,value)
        return self

class LineHelper(AbsHelper):
    def __init__(self, echart: EChart) -> None:
        super().__init__(echart)

    def area_chart(self):
        '''
        基础面积图
        '''
        self._echart \
                    .set_series(0, 'areaStyle', {}) \
                    .set_series(0,'symbol','none') \
                    .set_series(0,'sampling','lttb') \
                    .set_series(0,  "lineStyle",{"width": 0}) \
                    .set_option('xAxis', {'type': 'category'})

        return self

    def smooth(self):
        '''
        平滑化
        '''
        self._echart \
                    .set_series(0, 'smooth', True) \

        return self


class BarHelper(AbsHelper):
    def __init__(self, echart: EChart) -> None:
        super().__init__(echart)

    def showBackground(self, color: str = 'rgba(180, 180, 180, 0.2)'):
        '''
        显示柱子背景
        '''
        self._echart \
                    .set_series(0, 'showBackground', True) \
                    .set_series(0, 'backgroundStyle',  {
                        'color': color
                    }) \

        return self


class PieHelper(AbsHelper):
    def __init__(self, echart: EChart) -> None:
        super().__init__(echart)

    def circle_chart(self):
        '''
        圆环图
        '''
        self._echart.set_series(0, 'labelLine', {
            'show': False
        }).set_series(0, 'emphasis', {
            'label': {
                'show': True,
                'fontSize': '40',
                'fontWeight': 'bold'
            }
        }).set_series(0, 'label', {
            'show': False,
            'position': 'center'
        }).set_series(0, 'itemStyle', {
            'borderRadius': 10,
            'borderColor': '#fff',
            'borderWidth': 2
        }).set_series(0, 'avoidLabelOverlap', False).set_series(
            0, 'radius', ['40%', '70%']).set_series(0, 'type', 'pie')

        return self

    def nightingale_rose_chart(self):
        '''
        南丁格尔玫瑰图
        '''
        self._echart \
                    .set_series(0, 'type', 'pie') \
                    .set_series(0, 'center',  ['50%', '50%']) \
                    .set_series(0, 'roseType', 'area') \
                    .set_series(0, 'itemStyle', {
                                                'borderRadius': 8
                                            }) \

        return self