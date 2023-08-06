
import _, { get, zipObject } from "lodash";
import { TData as TFileData } from "~/components/builtins/fileTyping";
import { useInit } from "~/shares/index";



type TLogicExecContext = ReturnType<typeof useInit>['loginExecContext']

function ifelse(cond: boolean, v1: string, v2: string) {
    return cond ? v1 : v2
}

function toNumber(value: string) {
    return Number(value)
}



function map(key: string, obj: [][], defaultValue: any) {
    if (!key) {
        return null
    }
    const mapping = new Map<string | number, string | number | Function>(obj)

    if (mapping.has(key)) {
        if (typeof mapping.get(key) === 'function') {
            return mapping.get(key)()
        }

        return mapping.get(key)
    }
    return defaultValue
}

const __fns = {
    ifelse,
    toNumber,
    map,
}





function filter(details: TFileData['details'], condition: (row: {}) => boolean) {
    const data = _(details.data).filter(row => condition(zipObject(details.columns, row))).value()
    return {
        columns: details.columns,
        data
    }
}

function sort(details: TFileData['details'], columns: string[], orders: (boolean | "asc" | "desc")[]) {
    const idx = columns.map(col => details.columns.findIndex(v => v === col))
    const data = _(details.data).orderBy(idx, orders).value()
    return {
        columns: details.columns,
        data
    }
}

function groupby(details: TFileData['details'], keys: string[]) {
    const idx = keys.map(col => details.columns.findIndex(v => v === col))
    const data = _(details.data).groupBy(item => {
        return idx.map(i => item[i])
    }).map((items, key) => {
        return {
            key,
            'colx': _(items).map(t => t[4]).sum()
        }
    }).value()



    return {

    }
}

const __dataFns = {
    filter,
    sort,
    groupby,
}

export function execDataFilterLogic(row: any, getby: (id: string, func: (data: {}) => any) => any, logic: string) {
    return new Function('row', 'fns', 'getby', `return ${logic}`)(row, __fns, getby)
}


export function execValueLogic(context: TLogicExecContext, logic: string) {

    const { getby, getDf, dsFns } = context
    return new Function('dataFns', 'fns', 'getby', 'getDf', 'ds', `return ${logic}`)
        (__dataFns, __fns, getby, getDf, dsFns)
}












