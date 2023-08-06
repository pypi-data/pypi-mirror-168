<script setup lang="ts">
import { computed, isRef, ref, watch } from 'vue'
import { getStates } from '~/shares';
import { isArray } from "lodash";
import { TComponent } from '~/shares/typing';

const props = defineProps<{ id: string, children: TComponent[] }>()

const states = getStates()
const data = states.methods.getReactData(props.id) as {
    value: any
}



const display = computed(() => {
    if (!data.value && typeof (data.value) != 'undefined' && data.value != 0) {
        return null
    }

    if (isArray(data.value) && data.value.length === 0) {
        return null
    }

    return data.value
})

</script>

<template>
    <span class="pvf-md-value">{{ display }}</span>
</template>

<style scoped lang="less">
</style>