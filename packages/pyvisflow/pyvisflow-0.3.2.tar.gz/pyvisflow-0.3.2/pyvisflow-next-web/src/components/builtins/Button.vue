<script setup lang="ts">
import { computed, nextTick, ref } from 'vue'
import { getStates } from "~/shares";
import { TComponent } from '~/shares/typing';

const props = defineProps<{ id: string, children: TComponent[] }>()
const states = getStates()
const data = states.methods.getReactData(props.id) as { text: string, click: boolean, styles: {} }



function onclick() {
    console.log('click');

    data.click = true
    nextTick(() => {
        data.click = false
    })
}

</script>

<template>
    <div class="pvf-link" :id="props.id" v-bind="data" @click="onclick" :style="data.styles">
        {{ data.text }}
        <Dynamic v-for="(c, idx) in props.children" :component="c" :key="idx"></Dynamic>
    </div>
</template>

<style scoped >
</style>