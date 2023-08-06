<script setup lang="ts">
import { computed, nextTick, ref, toRaw, watch } from 'vue'

import { TValueWatch } from "~/shares/typing";
import { useStates } from "~/shares/index";
import { watchValueTypeInfo, init } from "./mainUse";

// import Dynamic from "./Dynamic.vue";

// init()

const states = useStates()
watchValueTypeInfo(states)




</script>

<template>
  <div style="display: flex;flex: 1 1 auto;justify-content: center; margin: 1rem 2rem;">
    <div class="ct">
      <Dynamic v-for="(c, idx) in states.config.cps" :component="c" :key="idx"></Dynamic>
    </div>
  </div>
</template>


<style scoped>
.ct {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(1, minmax(0px, 1fr));
  padding-top: 1rem;
  width: 100%;
}
</style>
