<script setup lang="ts">
import { computed, ref, toRaw, watch } from 'vue'
import { TComponent } from "~/shares/typing";
import { getStates } from "~/shares";
import { useDisplayData, type TData } from "./dataTableUse";
import { getEvents } from "./dataTableEvents";
import { TEventContext, TSortContext } from './dataTableTyping';

const props = defineProps<{ id: string, children: TComponent[] }>()
const states = getStates()
const getReactData = states.methods.getReactData

const reactData = getReactData(props.id) as TData


const tableSortContext = ref({ prop: null, order: null } as unknown as TSortContext)
const displayData = useDisplayData(props.id, states, tableSortContext)

watch([() => reactData.pageSize, () => reactData.dataframe.infos.rows], _ => {
    reactData.currentPage = 1
})


const columns = computed(() => reactData.columnsSetting.showColumns || reactData.dataframe.infos.columns)

const columnSortStaue = computed(() => {
    const res = new Map(columns.value.map(v => ([v, false])))

    if (!reactData.columnsSetting.sortableColumns) {
        return res
    }

    if (typeof reactData.columnsSetting.sortableColumns === 'boolean') {
        res.forEach((v, k) => {
            res.set(k, reactData.columnsSetting.sortableColumns as boolean)
        })

        return res
    }

    reactData.columnsSetting.sortableColumns.forEach(col => {
        res.set(col, true)
    })

    return res

})


const eventContext: TEventContext = {
    sortContext: tableSortContext
}
const events = getEvents(reactData, eventContext)


</script>

<template>
    <div class="pvf-table" style="display: flex;" :style="reactData.styles">
        <div class="table-fix">
            <el-table @sort-change="events.onSortChange" @row-click="events.onRowClick"
                @cell-mouse-enter="events.onCellMouseEnter" v-bind="reactData" :data="displayData">
                <el-table-column :formatter="events.columnsFormatter" v-for="col in columns" :prop="col" :label="col"
                    :sortable="columnSortStaue.get(col)" />
            </el-table>
            <el-pagination v-if="reactData.dataframe.infos.rows > reactData.pageSize" background
                layout="prev, pager, next" :total="reactData.dataframe.infos.rows" :current-page="reactData.currentPage"
                :page-size="reactData.pageSize" @current-change="events.onCurrentChange"
                @size-change="events.onSizeChange">
            </el-pagination>
        </div>
    </div>
</template>

<style scoped >
.table-fix {
    flex: 1;
    width: 0;
}
</style>