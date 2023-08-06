<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getStates } from "~/shares";
import { TComponent } from '~/shares/typing';
import * as XLSX from "xlsx/dist/xlsx.core.min.js";
import _ from "lodash";
import { TData } from "./fileTyping";


const props = defineProps<{ id: string, children: TComponent[] }>()
const states = getStates()
const reactData = states.methods.getReactData(props.id) as TData

const div$ = ref(null as unknown as HTMLDivElement)

onMounted(() => {
    div$.value.addEventListener("dragover", function (event) {
        event.preventDefault();
    }, false);


    div$.value.addEventListener("drop", async function (event: DragEvent) {
        if (!event.dataTransfer) {
            return
        }

        event.preventDefault();
        const file = event.dataTransfer.files[0]
        const data = await file.arrayBuffer()
        const workbook = XLSX.read(data);
        const wrk = workbook.Sheets[workbook.SheetNames[0]]



        const dataJson = XLSX.utils.sheet_to_json(wrk, { header: 1 });

        reactData.details.columns = dataJson[0]
        reactData.details.data = _(dataJson).tail().value()
        // const res = _(dataJson).tail().filter(v => v[3] === 'male').groupBy(v => v[0]).map((items, key) => {
        //     return {
        //         key,
        //         total: _(items).sumBy(v => v[1])
        //     }
        // }).value()
        // console.log(res);


    }, false);
})

</script>

<template>
    <div ref="div$" class="pvf-file" :style="reactData.styles">把excel文件拖到这里</div>
</template>

<style  >
.pvf-file {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    min-height: 10vh;
    height: 100%;
    border: 1px dashed rgba(96, 143, 196, 0.445);
    border-radius: 2px;
}
</style>