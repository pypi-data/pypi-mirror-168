import { computed, Ref, ref, toRef, watch, watchEffect } from "vue";
import { TStates } from "~/shares";
import { TComponent, TDataframe } from "~/shares/typing";




export type TColumnFormatterType = 'percent'


export type TData = {
    dataframe: TDataframe
    columnsSetting: {
        showColumns: string[]
        sortableColumns: string[] | boolean
        formatters: {
            column: string
            formatType: TColumnFormatterType
            args: object
        }[]
    }
    pageSize: number
    currentPage: number
    rowClick: {}
    rowHover: {}
    styles: {}
}



export type TEventContext = {
    sortContext: Ref<TSortContext>
}

export type TSortContext = {
    prop: string | null
    order: 'descending' | 'ascending' | null
}