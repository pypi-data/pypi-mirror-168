<script setup lang="ts">
import { computed, ref } from 'vue'
import { getStates } from "~/shares";
import { TComponent } from '~/shares/typing';


const props = defineProps<{ id: string, children: TComponent[] }>()
const states = getStates()
const data = states.methods.getReactData(props.id) as { svg: string, size: string, styles: {} }

const styles = computed(() => {
    return {
        ...data.styles,
        width: data.size,
        height: data.size,
    }
})


</script>

<template>
    <div class="pvf-icon" v-html="data.svg" :style="styles"></div>
</template>

<style scoped>
.pvf-icon {
    display: inline-flex;
    justify-content: center;
    align-items: center;
}
</style>