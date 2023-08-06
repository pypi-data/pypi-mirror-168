<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { getStates } from "~/shares";
import { TComponent } from '~/shares/typing';
// import Dynamic from "~/components/Dynamic.vue";

const props = defineProps<{ id: string, children: TComponent[] }>()
const states = getStates()
const data = states.methods.getReactData(props.id) as { teleportTarget: string, spec: number, styles: {}, isHover: boolean }

const hasTable = computed(() => props.children.some(v => v.tag === 'dataTable'))

function onmouseenter() {
    data.isHover = true
}

function onmouseleave() {
    data.isHover = false
}



</script>

<template>
    <template v-if="data.teleportTarget">
        <Teleport :to="data.teleportTarget">
            <div :id="props.id" class="pvf-box" :class="{ 'table-fix': hasTable }" :style="data.styles"
                @mouseenter="onmouseenter" @mouseleave="onmouseleave">
                <Dynamic v-for="(c, idx) in props.children" :component="c" :key="idx"></Dynamic>
            </div>
        </Teleport>
    </template>

    <template v-else>
        <div :id="props.id" class="pvf-box" :class="{ 'table-fix': hasTable }" :style="data.styles"
            @mouseenter="onmouseenter" @mouseleave="onmouseleave">
            <Dynamic v-for="(c, idx) in props.children" :component="c" :key="idx"></Dynamic>
        </div>
    </template>
</template>

<style scoped >
.pvf-box {
    width: 100%;
    position: relative;

    display: grid;
    gap: 1rem;
    grid-template-columns: repeat(1, minmax(0px, 1fr));
}
</style>