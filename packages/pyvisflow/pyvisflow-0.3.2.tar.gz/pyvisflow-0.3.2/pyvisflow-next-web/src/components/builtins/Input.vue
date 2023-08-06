<script setup lang="ts">
import { ref } from 'vue'
import { getStates } from "~/shares";
import { TComponent } from '~/shares/typing';

const props = defineProps<{ id: string, children: TComponent[] }>()
const states = getStates()
const data = states.methods.getReactData(props.id) as { value: string, styles: {} }

</script>

<template>
    <div :style="data.styles">
        <el-input class="pvf-input" :id="props.id" v-bind="data" v-model="data.value"></el-input>
    </div>
</template>

<style  >
.pvf-input {
    height: 100%;
}

/* .pvf-input > .el-input__inner {
    height: 100%;
} */
</style>