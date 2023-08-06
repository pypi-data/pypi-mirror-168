<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { getStates } from "~/shares";
import { TComponent } from '~/shares/typing';


const props = defineProps<{ id: string, children: TComponent[] }>()
const states = getStates()


const data = states.methods.getReactData(props.id) as {
    options: string[],
    currentLabels: string[],
    multiple: false, styles: {}
}

const id = ref(props.id)

const value = ref<string | string[]>(null)
const optionsMapping = computed(() => {
    const res = new Map<string, string>()
    data.options.forEach((v, idx) => {
        res.set(idx.toString(), v)
    })
    return res
})


watch(value, v => {
    if (typeof v === 'string') {
        v = [v]
    }

    data.currentLabels = v.map(change => optionsMapping.value.get(change)!)
})

watch(() => data.options, () => {
    value.value = ''
})

</script>

<template>
    <el-select class="pvf-select" :id="id" v-model="value" v-bind="data" size="large" :style="data.styles">
        <el-option v-for="(item, idx) in data.options" :key="idx" :label="item" :value="idx.toString()"></el-option>
    </el-select>
</template>

<style scoped >
.pvf-select {
    width: 100%;
}
</style>