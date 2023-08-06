import { computed, Ref, ref, toRef, watch, watchEffect } from "vue";
import { TStates } from "~/shares";
import { TComponent, TDataframe } from "~/shares/typing";
import { zipObject, orderBy } from "lodash";
import { TData, TColumnFormatterType, TSortContext } from "./dataTableTyping";

/**
 * 用于页面显示的数据，这个数据是考虑到分页
 * @param id 
 * @param states 
 * @returns 
 */
export function useDisplayData(id: TComponent['id'], states: TStates, sortContext: Ref<TSortContext>) {
    const getReactData = states.methods.getReactData
    const data = getReactData(id) as TData

    const tableData = computed(() => {

        const start = (data.currentPage - 1) * data.pageSize
        const end = data.currentPage * data.pageSize

        let res = data.dataframe.data

        if (sortContext.value.prop) {
            const idx = data.dataframe.infos.columns.indexOf(sortContext.value.prop)
            const sort = sortContext.value.order === 'ascending' ? 'asc' : 'desc'
            res = orderBy(res, [idx], [sort])
        }

        return res.slice(start, end).map(row => zipObject(data.dataframe.infos.columns, row))

    })

    return tableData
}



class FormatterManager {
    private mapping

    constructor(private reactData: TData) {
        this.mapping = new Map(
            reactData.columnsSetting.formatters.map(r => {
                return [r.column, this.createFormatFn(r.formatType, r.args)]
            })
        )
    }


    private createFormatFn(type: TColumnFormatterType, args: object) {
        switch (type) {
            case 'percent':
                return {
                    format: (value: TDataframe['data'][0]) => {
                        if (typeof value === 'number') {
                            return new Intl.NumberFormat('en-IN', args).format(value)
                        }
                        return value
                    }
                }
                break;

            default:
                break;
        }
    }

    /**
     * format
columnName:string,     */
    public format(columnName: string, value: TDataframe['data'][0]) {
        if (!this.mapping.has(columnName)) {
            return value
        }

        return this.mapping.get(columnName)?.format(value)
    }
}





export function getFormatterManager(reactData: TData) {
    return new FormatterManager(reactData)
}


