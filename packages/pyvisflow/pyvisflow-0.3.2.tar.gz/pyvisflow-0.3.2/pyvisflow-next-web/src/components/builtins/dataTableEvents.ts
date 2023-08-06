import { TableColumnCtx } from "element-plus/es/components/table/src/table-column/defaults"
import { toRaw } from "vue"
import { TData, TSortContext, TEventContext } from "./dataTableTyping"
import { getFormatterManager } from "./dataTableUse"


export function getEvents(reactData: TData, context: TEventContext) {

    const formatterManager = getFormatterManager(reactData)

    function columnsFormatter(row: any, column: TableColumnCtx<any>, cellValue: any, index: number) {
        return formatterManager.format(column.property, cellValue)
    }


    function onRowClick(row, column: TableColumnCtx<any>, event) {
        reactData.rowClick = toRaw(row)
    }

    function onCellMouseEnter(row, column: TableColumnCtx<any>, event) {
        reactData.rowHover = toRaw(row)
    }

    function onCurrentChange(value: number) {
        reactData.currentPage = value
    }

    function onSizeChange(size: number) {
        reactData.pageSize = size
    }

    function onSortChange(args: { column, prop: TSortContext['prop'], order: TSortContext['order'] }) {
        console.log(args);
        context.sortContext.value = {
            prop: args.prop, order: args.order
        }
    }

    return {
        columnsFormatter,
        onRowClick,
        onCellMouseEnter,
        onCurrentChange,
        onSizeChange,
        onSortChange,
    }
}
