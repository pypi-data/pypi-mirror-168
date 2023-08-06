import { computed, ComputedRef, reactive, UnwrapNestedRefs } from "vue"
import { getDatasetFns } from "./datasetFns"
import { TComponent, TConfig, TDataframe, TDataset } from "./typing"
import { createReactiveDataMapping } from "./reactiveData";


type TReactDataFns = ReturnType<typeof createReactiveDataMapping>

export function createMapping(config: TConfig) {


    const dfMapping = new Map<TDataframe['id'], TDataframe>(
    )

    config.staticData.dataframes.forEach(df => {
        dfMapping.set(df.id, df)
    })

    function getDataframe(id: TDataframe['id']) {
        return dfMapping.get(id)!
    }


    // const datasetMapping = new Map<TDataset['id'], ComputedRef<TDataframe>>(
    // )

    // const dsFns = getDatasetFns()

    // function createComputed(ds: TDataset) {
    //     const df = getDataframe(ds.src)
    //     return computed(() => {
    //         let data = df
    //         if (ds.srcType === 'react') {
    //             data = reactDataFns.getData(ds.src) as TDataframe
    //         }

    //         ds.exec.map(logic => {
    //             const dsTransformer: (ds: TDataframe) => TDataframe = new Function('ds', 'getby', `return ${logic}`)(dsFns, reactDataFns.getby)
    //             data = dsTransformer(data)
    //         })

    //         return data
    //     })
    // }


    // config.dataset.forEach(ds => {


    //     const dsComputed = createComputed(ds)

    //     datasetMapping.set(ds.id, dsComputed)

    // })

    // function getDataset(id: TDataset['id']) {
    //     return datasetMapping.get(id)!
    // }

    return {
        mapping: dfMapping,
        getDataframe,
    }
}


