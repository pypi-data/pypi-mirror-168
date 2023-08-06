<script setup lang="ts">
import { ref } from 'vue'
import { getStates } from "~/shares";
import { TComponent } from '~/shares/typing';
import { zipWith } from "lodash";

const props = defineProps<{ id: string, children: TComponent[] }>()
const states = getStates()
const data = states.methods.getReactData(props.id) as { pageMode: boolean, activeName: string, names: string[], labels: string[] }

const nameInfos = zipWith(data.names, data.labels, props.children,
    (name, label, children) => ({ name, label, tab: children })
)

data.activeName = data.names[0]




function onclick(name: string) {
    data.activeName = name
}

</script>

<template>
    <div class="pvf-tabs" v-bind="data" type="border-card">
        <div class="header" :class="{ 'page-mode': data.pageMode }">
            <div class="tab" :class="{ 'activate': info.label == data.activeName, 'page-mode': data.pageMode }"
                v-for="info in nameInfos" @click="onclick(info.label)">{{ info.label }}</div>
        </div>

        <div class="body">
            <template v-for="info in nameInfos">
                <div v-if="data.activeName == info.name" style="width: 100%;">
                    <Dynamic v-for="(c, idx) in info.tab.children" :component="c" :key="idx"></Dynamic>
                </div>
            </template>
        </div>
    </div>
</template>

<style scoped >
.body {
    display: flex;
    flex: 1 1 0%;
}

.body>div {
    width: 100%;
    position: relative;

    display: grid;
    gap: 1rem;
    grid-template-columns: repeat(1, minmax(0px, 1fr));
}

.header {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    margin-bottom: 0.5em;
}

.header.page-mode {
    justify-content: stretch;
}

.tab {
    font-size: 1.25em;
    margin: 0.2em 0.5em;
    padding: 0.2em 0.5em;
    border-radius: 0.25em;
    min-width: 3em;
    text-align: center;
    cursor: pointer;
}

.tab.activate {
    background: rgba(230, 229, 251);
    color: rgba(142, 70, 229);
}

.tab.page-mode {
    background: rgba(230, 229, 251, 0);
    border-bottom: 2px solid rgba(121, 121, 121, 0.397);
    color: rgb(0, 0, 0);
    border-radius: 0;
    margin: 0.2em 0;
    width: 100%;
}

.tab.page-mode.activate {
    color: rgba(142, 70, 229);
    border-bottom: 2px solid rgba(142, 70, 229);
}
</style>