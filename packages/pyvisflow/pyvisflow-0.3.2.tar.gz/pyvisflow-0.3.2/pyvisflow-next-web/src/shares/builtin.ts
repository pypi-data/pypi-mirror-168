import { Component } from "vue";
import Input from "~/components/builtins/Input.vue";
import InputNumber from "~/components/builtins/InputNumber.vue";
import Select from "~/components/builtins/Select.vue";
import Dataframe from "~/components/builtins/Dataframe.vue";
import DataTable from "~/components/builtins/DataTable.vue";
import EChart from "~/components/builtins/EChart.vue";
import Plotly from "~/components/builtins/Plotly.vue";
import MarkdownValue from "~/components/builtins/MarkdownValue.vue";
import Box from "~/components/builtins/Box.vue";
import MarkdownBox from "~/components/builtins/MarkdownBox.vue";
import Row from "~/components/builtins/Row.vue";
import Tabs from "~/components/builtins/Tabs.vue";
import Text from "~/components/builtins/Text.vue";
import Icon from "~/components/builtins/Icon.vue";
import Image from "~/components/builtins/Image.vue";
import File from "~/components/builtins/File.vue";
import Button from "~/components/builtins/Button.vue";
import ColumnsContainer from "~/components/builtins/ColumnsContainer.vue";


const component_mapping = new Map<string, Component>(
    [
        ['input', Input],
        ['button', Button],
        ['image', Image],
        ['markdown-box', MarkdownBox],
        ['file', File],
        ['input-number', InputNumber],
        ['select', Select],
        ['dataframe', Dataframe],
        ['dataTable', DataTable],
        ['echart', EChart],
        ['plotly', Plotly],
        ['markdown-value', MarkdownValue],
        ['box', Box],
        ['row', Row],
        ['tabs', Tabs],
        ['text', Text],
        ['icon', Icon],
        ['columns-container', ColumnsContainer]
    ]
)


export function get_builtin_component(tag: string) {
    return component_mapping.get(tag)
}