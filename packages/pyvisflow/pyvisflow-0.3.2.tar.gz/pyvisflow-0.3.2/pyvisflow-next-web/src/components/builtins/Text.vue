<script setup lang="ts">
import { ref } from 'vue'
import { getStates } from "~/shares";
import { TComponent } from '~/shares/typing';
import { zipWith } from "lodash";

const props = defineProps<{ id: string, children: TComponent[] }>()
const states = getStates()
const data = states.methods.getReactData(props.id) as { value: string, styles: {} }




</script>

<template>
    <span
        :id="props.id"
        :style="data.styles"
    >{{ data.value }}</span>
</template>

<style scoped >
</style>