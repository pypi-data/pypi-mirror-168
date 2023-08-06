# pyvisflow

pyvisflow 是一个使用 Python 直观简洁声明语句的可视化报告库。使用 pyvison，你可以创建灵活强大的 BI 式交互报告。生成的报告只有一个 html 文件，用户只需要使用浏览器打开就能看到所有的交互效果，无须 Python 环境。



## 例子

下面是一个简单入门的联动示例：

```python
import pyvisflow as pvf

input=pvf.input()
pvf.markdown('''
# 第一个联动示例

上面输入框的内容是：{{text}}
''',text=input.value)
```



pyvisflow 的一个独特功能是，页面上创建的每个组件各种属性都可以互相设置关联，并且语句非常简单直观。

下面是另一个特别的联动示例：

```python

```



另一个特别强大的特性是，基于数据集的组件(table、图表等)，都能支持数据过滤联动。这意味着你能够随意设置表格与图表、图表与图表、甚至与页面上的文本内容做联动。

下面是一个展现 pyvisflow 强大联动能力的示例：

```python

```



具体能做到如何的效果，取决于你的想象力！



## 功能

- 简单直观的 api，任何联动设置就像任意对象赋值一样简单
- 所有组件的属性都有智能提示
- 零依赖。所有的交互效果都在一个 html 文件中，无须 Python 运行环境
- 超乎想象简单直观的数据过滤 api 设计



## 安装

```
pip install pyvisflow
```



pyvisflow 依赖 Python 这些第三方库(开发者需要安装)：

- [pandas](https://pandas.pydata.org/)



前端核心功能使用了这些库(开发者与用户都无须关心)：

- [echart]([Apache ECharts](https://echarts.apache.org/zh/index.html))
- [Vue.js - The Progressive JavaScript Framework | Vue.js (vuejs.org)](https://vuejs.org/)
- [A Vue 3 UI Framework | Element Plus (element-plus.org)](https://element-plus.org/zh-CN/)
- [plotly](https://plotly.com/javascript/)


- [python magic methods](extension://idghocbbahafpfhjnfhpbfbmpegphmmp/assets/pdf/web/viewer.html?file=https%3A%2F%2Fraw.githubusercontent.com%2FRafeKettler%2Fmagicmethods%2Fmaster%2Fmagicmethods.pdf)

- [移动端Web页面适配方案](https://www.jianshu.com/p/2c33921d5a68)
