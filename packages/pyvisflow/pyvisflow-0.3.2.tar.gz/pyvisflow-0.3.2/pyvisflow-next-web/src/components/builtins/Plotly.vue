<script setup lang="ts">
import { computed, onMounted, Ref, ref, toRaw, watch, watchEffect } from 'vue'
import { getStates } from "~/shares";
import { TComponent } from '~/shares/typing';
// import * as Plotly from "plotly.js-dist";
import { useEventListener } from '@vueuse/core';
import { execDataFilterLogic } from '~/shares/watchChange';
import { set, zipObject } from 'lodash';

const props = defineProps<{ id: string, children: TComponent[] }>()
const states = getStates()
const getReactData = states.methods.getReactData

type TData = {
    data: {}[]
    layout: {}
    config: {}
    dataPropsReplace: {
        path: string
        column: string
    }[]
    clickInfo: {}
    hoverInfo: {}
}

const reactData = getReactData(props.id) as TData


const div$ = ref(null as unknown as HTMLDivElement)

type TClickData = {
    points: [{
        curveNumber: 1,  // index in data of the trace associated with the selected point
        pointNumber: 1,  // index of the selected point
        x: 1,        // x value
        y: 1,      // y value
        data: {/* */ },       // ref to the trace as sent to Plotly.newPlot associated with the selected point
        fullData: {/* */ },   // ref to the trace including all of the default attributes
        xaxis: {/* */ },   // ref to x-axis object (i.e layout.xaxis) associated with the selected point
        yaxis: {/* */ }    // ref to y-axis object " "
    }]
}

onMounted(() => {

    watchEffect(() => {

        try {
            Plotly.newPlot(div$.value, reactData.data, reactData.layout, reactData.config);
        } catch (error) {
            console.log('error');

        }

    })


    // watchEffect(() => {
    //     Plotly.react(div$.value, plotlyData.value, reactData.layout, reactData.config);

    // })

    useEventListener('resize', () => {
        Plotly.Plots.resize(div$.value)
    })


    div$.value.on('plotly_click', (e: TClickData) => {
        reactData.clickInfo = {
            infos: e.points.map(p => ({ x: p.x, y: p.y }))[0]
        }
    })

    div$.value.on('plotly_hover', (e: TClickData) => {
        reactData.hoverInfo = {
            infos: e.points.map(p => ({ x: p.x, y: p.y }))[0]
        }
    })
})

</script>

<template>
    <div class="pvf-plotly" ref="div$"></div>
</template>

<style scoped >
.pvf-plotly {
    width: inherit;
    height: fit-content;
    position: relative;
}
</style>