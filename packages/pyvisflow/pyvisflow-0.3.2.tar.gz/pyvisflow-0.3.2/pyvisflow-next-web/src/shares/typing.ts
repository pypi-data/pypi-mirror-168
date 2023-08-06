
export type TComponentType = 'html-raw' | 'html-raw-string' | 'built-in'

export type TComponent = {
    id: string
    tag: string
    type: TComponentType
    attrs: {}
    styles: {}
    children: TComponent[]
}

export type TValueWatch = {
    target: {
        id: string
        path: string
        logic: string
    }
}


export type TDataframe = {
    id: string
    infos: {
        columns: string[]
        rows: number
    },
    columnsType: {
        name: string
        type: string
    }[],
    data: (string | number | Date | null)[][]
}

export type TDatasetSrcType = 'static' | 'react'



export type TConfig = {
    staticData: {
        dataframes: TDataframe[]
    }
    cps: TComponent[]
    reactDatas: {
        id: string
        data: {}
    }[]
    watchInfo: {
        values: TValueWatch[]
    }
}