import { zipObject, uniq, slice } from "lodash"
import { TDataframe, TDataset } from "./typing"


type TValue = (string | number | Date | null)
type TArray = TValue[]


function filter(df: TDataframe, condition: (r: Record<string, TValue>) => boolean): TDataframe {
    const data = df.data.filter(row => condition(zipObject(df.infos.columns, row)))
    return {
        id: df.id,
        data,
        infos: {
            columns: df.infos.columns,
            rows: data.length
        },
        columnsType: df.columnsType
    }
}

function getSeries(df: TDataframe, columnName: string): TArray {
    const idx = df.infos.columns.indexOf(columnName)
    return df.data.flatMap(v => v[idx])
}

function getbyColumns(df: TDataframe, columnNames: string[]): TDataframe {
    const columnsType = df.columnsType.filter(col => columnNames.includes(col.name))

    const idxes = columnNames.map(v => df.infos.columns.indexOf(v))

    const data = df.data.map(row => {

        return row.filter((value, idx) => idxes.includes(idx))

    })
    return {
        id: df.id,
        data,
        infos: {
            columns: columnNames,
            rows: data.length
        },
        columnsType
    }
}

function getValues(df: TDataframe): TDataframe['data'] {
    return df.data
}

function getColumns(df: TDataframe): string[] {
    return df.infos.columns
}

function recolumnName(df: TDataframe, mapping: [string | number, string][]): TDataframe {

    const map = new Map<string, string>(
    )

    mapping.forEach(([key, value]) => {
        if (typeof key === 'number') {
            map.set(df.infos.columns[key], value)
        } else {
            map.set(key, value)
        }
    })

    const columns = df.infos.columns.map(col => {
        if (map.has(col)) {
            return map.get(col)!
        }
        return col
    })

    return {
        ...df,
        infos: {
            ...df.infos,
            columns
        }
    }

}

function toJsObjects(df: TDataframe) {
    return df.data.map(row => zipObject(df.infos.columns, row))
}

function seriesDup(series: TArray): TArray {
    return uniq(series)
}

function seriesContains(series: TArray, values: TArray): TArray {
    const valuesSet = new Set<TValue>(values)
    return series.filter(v => valuesSet.has(v))
}

function seriesTakeSingle(series: TArray, idx: number): TValue {
    const values = slice(series, idx)
    if (values.length > 0) {
        return values[0]
    }
    return null
}

const dsFns = {
    filter,
    getSeries,
    getbyColumns,
    getValues,
    getColumns,
    recolumnName,
    toJsObjects,

    seriesDup,
    seriesContains,
    seriesTakeSingle,
}




export function getDatasetFns() {
    return dsFns
}