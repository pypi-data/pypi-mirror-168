<script setup lang="ts">
import { computed, ref } from 'vue'
import { getStates } from "~/shares";
import { TComponent } from '~/shares/typing';


const props = defineProps<{ id: string, children: TComponent[] }>()
const states = getStates()
const data = states.methods.getReactData(props.id) as { isWrap: boolean, styles: {} }

const styles = computed(() => {
    return {
        ...data.styles,
        'flex-wrap': data.isWrap ? 'wrap' : 'nowrap'
    }
})


</script>

<template>
    <div class="pvf-row" :style="styles">
        <Dynamic v-for="(c, idx) in props.children" :component="c" :key="idx"></Dynamic>
    </div>
</template>

<style scoped>
.pvf-row {
    display: flex;
    align-items: center;
}
</style>