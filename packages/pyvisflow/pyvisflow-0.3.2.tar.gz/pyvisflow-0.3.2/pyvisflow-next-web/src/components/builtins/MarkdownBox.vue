<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { getStates } from "~/shares";
import { TComponent } from '~/shares/typing';
// import Dynamic from "~/components/Dynamic.vue";

const props = defineProps<{ id: string, children: TComponent[] }>()
const states = getStates()
const data = states.methods.getReactData(props.id) as { spec: number, styles: {}, isHover: boolean }


function onmouseenter() {
    data.isHover = true
}

function onmouseleave() {
    data.isHover = false
}



</script>

<template>
    <div :id="props.id" class="pvf-md-box" :style="data.styles" @mouseenter="onmouseenter" @mouseleave="onmouseleave">
        <Dynamic v-for="(c, idx) in props.children" :component="c" :key="idx"></Dynamic>
    </div>
</template>

<style scoped >
.pvf-md-box {
    width: 100%;
    position: relative;
}
</style>