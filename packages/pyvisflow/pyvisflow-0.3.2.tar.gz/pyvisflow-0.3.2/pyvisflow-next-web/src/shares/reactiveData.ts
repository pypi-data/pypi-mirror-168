import { reactive, UnwrapNestedRefs } from "vue"
import { TComponent, TConfig } from "./typing"


type TID = TComponent['id']

export function createReactiveDataMapping(config: TConfig) {


    const reactDataMapping = new Map<TID, UnwrapNestedRefs<{}>>(
    )

    config.reactDatas.forEach(d => {
        reactDataMapping.set(d.id, reactive(d.data))
    })

    function getData(id: TID) {
        return reactDataMapping.get(id)!
    }


    return {
        mapping: reactDataMapping,
        getData,
    }
}
