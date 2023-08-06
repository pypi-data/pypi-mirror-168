<script setup lang="ts">
import { computed, onMounted, onUnmounted, Ref, ref, toRaw, watch, watchEffect } from 'vue'
import { TChartFilterWatch, TComponent } from "~/shares/typing";
import { getStates } from "~/shares";
import * as echarts from 'echarts';
import { set, get } from "lodash";
import { useEventListener } from "@vueuse/core";
import { execDataFilterLogic } from "~/shares/watchChange";
import { useResizeObserver } from "@vueuse/core";


type TChartData = {
    option: {

        xAxis: {}
        yAxis: {}

        series: {
            type: string
            encode?: {
                x: string
                y: string
            }
        }[]
    }
    styles: {}
    clickInfo: {}
    hoverInfo: {},
    functionSettings: string[]
}

const props = defineProps<{ id: string, children: TComponent[] }>()
const states = getStates()
const getReactData = states.methods.getReactData
const reactData = getReactData(props.id) as TChartData
const chartDiv = ref(null as unknown as HTMLDivElement)


type EventParams = {
    // 当前点击的图形元素所属的组件名称，
    // 其值如 'series'、'markLine'、'markPoint'、'timeLine' 等。
    componentType: string;
    // 系列类型。值可能为：'line'、'bar'、'pie' 等。当 componentType 为 'series' 时有意义。
    seriesType: string;
    // 系列在传入的 option.series 中的 index。当 componentType 为 'series' 时有意义。
    seriesIndex: number;
    // 系列名称。当 componentType 为 'series' 时有意义。
    seriesName: string;
    // 数据名，类目名
    name: string;
    // 数据在传入的 data 数组中的 index
    dataIndex: number;
    // 传入的原始数据项
    data: Object;
    // sankey、graph 等图表同时含有 nodeData 和 edgeData 两种 data，
    // dataType 的值会是 'node' 或者 'edge'，表示当前点击在 node 还是 edge 上。
    // 其他大部分图表中只有一种 data，dataType 无意义。
    dataType: string;
    // 传入的数据值
    value: number | Array<any>;
    // 数据图形的颜色。当 componentType 为 'series' 时有意义。
    color: string;
};

function onClick(params: EventParams) {

    reactData.clickInfo = {
        componentType: params.componentType,
        seriesName: params.seriesName,
        data: params.data,
        name: params.name,
        dataIndex: params.dataIndex
    }
}

function onMouseover(params: EventParams) {

    reactData.hoverInfo = {
        componentType: params.componentType,
        seriesName: params.seriesName,
        data: params.data,
        name: params.name,
        dataIndex: params.dataIndex
    }
}


onMounted(() => {
    const myChart = echarts.init(chartDiv.value)

    reactData.functionSettings.forEach(path => {
        // debugger
        const optPath = `${path}`
        const funStr = get(reactData, optPath)

        const funs = eval(funStr)

        const warpFun = (value, params) => {
            return funs(value, params, reactData.option, myChart)
        }

        set(reactData, optPath, warpFun)
    })


    useEventListener('resize', () => {
        myChart.resize()
    })

    useResizeObserver(chartDiv, () => {
        myChart.resize()
    })

    myChart.on('click', onClick)
    myChart.on('mouseover', onMouseover)

    watchEffect(() => {
        myChart.setOption(reactData.option)
    })

    onUnmounted(() => {
        myChart.dispose()
    })
})




</script>

<template>
    <div class="pvf-echart" ref="chartDiv"
        :style="reactData.styles"></div>
</template>

<style scoped >
.pvf-echart {
    width: inherit;
    height: 40vh;
}
</style>