<script setup lang="ts">
import { computed, ref } from 'vue'
import { getStates } from "~/shares";
import { TComponent } from '~/shares/typing';
import { zipWith } from "lodash";

const props = defineProps<{ id: string, children: TComponent[] }>()
const states = getStates()
const data = states.methods.getReactData(props.id) as { value: string, styles: {} }


</script>

<template>
    <img
        :id="props.id"
        :style="data.styles"
        :src="data.value"
    />
</template>

<style scoped >
</style>