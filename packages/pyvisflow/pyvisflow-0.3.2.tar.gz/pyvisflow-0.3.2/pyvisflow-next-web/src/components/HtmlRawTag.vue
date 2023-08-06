<script setup lang="ts">
import { ref } from 'vue'
import { TComponent } from "~/shares/typing";
// import Dynamic from "./Dynamic.vue";


const props = defineProps<{ controler: TComponent }>()

</script>



<template>
    <!-- {{ props.controler }} -->
    <component class="pvf-raw-tag" v-if="props.controler.type === 'html-raw'" :is="props.controler.tag">
        <Dynamic v-for="(c, idx) in props.controler.children" :controler="c" :key="idx"></Dynamic>
    </component>

    <span v-if="props.controler.type === 'html-raw-string'">{{ props.controler.tag }}</span>
</template>

<style scoped lang="less">
</style>
