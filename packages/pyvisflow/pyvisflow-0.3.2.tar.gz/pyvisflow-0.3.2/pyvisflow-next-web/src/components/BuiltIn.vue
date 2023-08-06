<script setup lang="ts">
import { ref } from 'vue'
import { get_builtin_component } from '../shares/builtin';
import { TComponent } from '../shares/typing';


const props = defineProps<{ component: TComponent }>()
const tag = get_builtin_component(props.component.tag)

</script>

<template>
    <tag
        :id="props.component.id"
        class="target"
        :children="props.component.children"
    ></tag>
</template>

<style scoped >
/* .target {
    display: inline-block;
} */
</style>