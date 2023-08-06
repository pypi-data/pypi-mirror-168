<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: 'DynamicCP'
})

</script>

<script setup lang="ts">
import { ref } from 'vue'
import { TComponent } from "~/shares/typing";
import BuiltIn from "./BuiltIn.vue";

const props = defineProps<{ component: TComponent }>()


</script>

<template>
    <span
        v-if="props.component.type === 'html-raw-string'"
    >{{ props.component.tag }}</span>

    <component
        v-if="props.component.type === 'html-raw'"
        :is="props.component.tag"
        v-bind="props.component.attrs"
    >
        <DynamicCP
            v-for="c in props.component.children"
            :component="c"
        ></DynamicCP>
    </component>

    <BuiltIn
        v-if="props.component.type === 'built-in'"
        :component="props.component"
        v-bind="props.component.attrs"
    ></BuiltIn>
</template>

<style scoped>
</style>