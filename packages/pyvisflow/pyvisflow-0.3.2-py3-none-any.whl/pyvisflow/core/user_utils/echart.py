from pyvisflow.core.components.echart import EChart
from .common import js_code






def setLastSymbol(echart:EChart,series_index:int,last:str,others:str):

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
  