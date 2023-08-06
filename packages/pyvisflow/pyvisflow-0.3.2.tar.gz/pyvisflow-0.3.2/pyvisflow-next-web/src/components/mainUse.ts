import { useStates } from "~/shares/index";
import { execValueLogic } from "~/shares/watchChange";

import { get, set, zipWith } from "lodash";
import { watchEffect } from "vue";
import { useEventListener } from "@vueuse/core";


export function init() {
    scalePage()
}

function scalePage() {

    function handler() {
        if (document.body.clientWidth < 1000 && document.body.clientWidth >= 300) {
            const value = 1 - ((document.body.clientWidth - 300) / 700)
            const scale = 1 - value * 0.7
            document.documentElement.style.fontSize = `${scale * 100}%`

            return
        }

        if (document.body.clientWidth < 300) {
            return
        }

        document.documentElement.style.fontSize = '100%'
    }

    useEventListener('resize', handler)
    handler()
}


export function watchValueTypeInfo(states: ReturnType<typeof useStates>) {

    const getReactData = states.methods.getReactData

    states.config.watchInfo.values.forEach(info => {
        const targetData = getReactData(info.target.id)

        watchEffect(() => {
            const cal = execValueLogic(states.loginExecContext, info.target.logic)
            set(targetData, info.target.path, cal)
        })

        // const cal = computed(() => {
        //     const cal = execValueLogic(states.loginExecContext, info.target.logic)
        //     return cal
        // })

        // watch(cal, change => {
        //     set(targetData, info.target.path, change)
        // })

        // const defaultValue = get(targetData, info.target.path)
        // set(targetData, info.target.path, defaultValue)
    })
}