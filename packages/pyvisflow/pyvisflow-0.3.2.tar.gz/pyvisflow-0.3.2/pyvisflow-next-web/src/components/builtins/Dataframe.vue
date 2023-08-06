<script setup lang="ts">
import { computed, ref } from 'vue'
import { getStates } from "~/shares";
import { TComponent } from '~/shares/typing';

const props = defineProps<{ id: string, children: TComponent[] }>()
const states = getStates()
const data = states.methods.getReactData(props.id) as { rawHtml: string }


</script>

<template>
    <div class="pvf-dataframe">

        <span v-html="data.rawHtml"></span>

    </div>
</template>

<style scoped >
</style>