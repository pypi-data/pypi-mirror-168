import { ref, Ref, InjectionKey, inject, provide, reactive, UnwrapNestedRefs } from "vue";
import { TComponent, TConfig, TDataframe } from "./typing";
import { createReactiveDataMapping } from "./reactiveData";
import { createMapping as createStaticData } from "./staticData";
import configData from "~/tempData/configFromPy.json";
import { getDatasetFns } from "./datasetFns";

export type TStates = ReturnType<typeof useStates>

const key = Symbol() as InjectionKey<TStates>



export function useStates() {
    const init = useInit()

    provide(key, init)
    return init
}

export function getStates() {
    return inject(key)!
}



export function useInit() {

    let config: TConfig = null

    if (import.meta.env.PROD) {
        config = "__{{__config_data__}}___";
    } else {
        config = configData as TConfig
    }


    const { getData: getReactData } = createReactiveDataMapping(config)
    const { getDataframe } = createStaticData(config)



    function getby(id: string, func: (data: {}) => any) {
        return func(getReactData(id))
    }

    function getDf(id: string, func: (df: TDataframe) => any) {
        return func(getDataframe(id))
    }

    const dsFns = getDatasetFns()


    return {
        config,
        methods: {
            getReactData
        },
        loginExecContext: {
            getby,
            dsFns,
            getDf,
        }
    }
}