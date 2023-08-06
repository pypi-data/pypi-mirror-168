<script setup lang="ts">
import { ref, watch } from 'vue'
import { getStates } from "~/shares";
import { TComponent } from '~/shares/typing';

const props = defineProps<{ id: string, children: TComponent[] }>()
const states = getStates()
const data = states.methods.getReactData(props.id) as { value: number, styles: {} }



</script>

<template>
    <el-input-number class="pvf-input-number" :id="props.id" v-bind="data" v-model="data.value" :style="data.styles">
    </el-input-number>
</template>

<style scoped >
</style>