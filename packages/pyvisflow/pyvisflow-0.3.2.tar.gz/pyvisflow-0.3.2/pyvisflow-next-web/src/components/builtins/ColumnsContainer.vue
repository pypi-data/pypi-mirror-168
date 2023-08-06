<script setup lang="ts">
import { computed, ref } from 'vue'
import { getStates } from "~/shares";
import { TComponent } from '~/shares/typing';

const props = defineProps<{ id: string, children: TComponent[] }>()
const states = getStates()
const data = states.methods.getReactData(props.id) as { isGrid: boolean, spec: number[], styles: {} }

const gridCols = computed(() => data.spec.map(v => `minmax(0px, ${v}fr)`).join(' '))

// const disGrid = computed(() => data.isGrid ? 'grid' : 'flex')


const styles = computed(() => {
    return {
        ...data.styles,
        ...{ 'grid-template-columns': gridCols.value }
    }
})

</script>

<template>
    <div class="pvf-col-container" :style="styles">
        <Dynamic v-for="(c, idx) in props.children" :component="c" :key="idx"></Dynamic>
    </div>
</template>

<style scoped >
.pvf-col-container {
    /* flex-wrap: wrap; */
    display: grid;
    gap: 1rem;

    padding-top: 1rem;
    padding-bottom: 1rem;
    align-items: center;
}
</style>