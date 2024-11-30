# Beijing New House Data Visualization

## 使用库

- `pandas` 2.2.3

- `matplotlib` 3.9.2

- `seaborn` 0.31.2

- `squarify` 0.4.4

## 快速开始

1. 克隆本项目到本地

    ```git
    git clone https://github.com/Word2VecT/Lianjia-Spider-Demo
    cd Lianjia-Spider-Demo
    ```

2. 安装 `uv` Python 项目管理器（需要 Python 环境以及 `pip`）

    ```bash
    pip install uv
    ```

3. 使用 `uv` 安装虚拟环境

    ```bash
    uv venv
    ```

4. 根据提示,激活虚拟环境 (以 `fish` 为例)

    ```bash
    source .venv/bin/activate.fish
    ```

5. 安装项目依赖

    ```bash
    uv pip install -r pyproject.toml
    ```

6. 进入 `code` 文件夹，运行你想生成对应图像的 `python` code

    ```bash
    cd code
    python price_distribution.py
    ```

7. 图像会生成在 `figure` 文件夹，Enjoy!

## 预处理

> - 最终的 csv 文件，应包括以下字段：楼盘名称，类型，地理位置（3 个字段分别存储），房型（只保留最小房型或平均值），面积（按照最小值或平均值），总价（万元， 整数），均价（元，整数
> - 对于所有字符串字段，去掉所有的前后空格
> - 如果有缺失数据，不填充

房型和面积的数值选取了平均值的数值，有助于简化数据，使其更易于分析和展示。平均值能够反映出楼盘的典型特征，便于在后续的数据分析中进行比较和统计

预处理 code：[`preprocessing.py`](code/preprocessing.py)

## 可视化结果

### 楼盘价格分布散点图

> 绘制楼盘价格分布的散点图，纵横轴分别代表单价和总价，楼盘类型通过散点的颜色区分

[`price_distribution.py`](code/price_distribution.py)

![price_distribution](figure/price_distribution.png)

### 各行政区楼盘直方图

> 绘制各行政区楼盘的直方图，每个行政区一个柱子，高度代表平均单价，宽度代表楼盘数量；将单价换为总价再绘制一张直方图

[`average_price_per_district.py`](code/average_price_per_district.py)

![average_unit_price_per_district](figure/average_unit_price_per_district.png)

![average_total_price_per_district](figure/average_total_price_per_district.png)

## 各行政区楼盘价格箱线图

> 能够有效展示数据的分布、集中趋势以及异常值，可以更深入地理解各行政区楼盘价格的变异性

[`boxplot_price_by_type.py`](code/boxplot_price_by_type.py)

![boxplot_unit_price_by_type](figure/boxplot_unit_price_by_type.png)

![boxplot_total_price_by_type](figure/boxplot_total_price_by_type.png)

## 各行政区与楼盘类型价格热力图

> 能够有效地展示不同行政区和楼盘类型之间在单价和总价上的差异和模式，可以直观地识别哪些行政区的某类楼盘价格较高或较低

[`heatmap_average_price_per_district_type.py`](code/heatmap_average_price_per_district_type.py)

![heatmap_average_unit_price_per_district_type](figure/heatmap_average_unit_price_per_district_type.png)

![heatmap_average_total_price_per_district_type](figure/heatmap_average_total_price_per_district_type.png)

## 楼盘面积与房型对价格多维散点图

> 展示楼盘面积（面积）、房型（房型）、单价（均价）和总价（总价）之间的关系，并通过颜色和大小编码不同的楼盘类型（类型）或行政区（行政区），从而揭示数据中的潜在模式和趋势

[`bubble_scatter.py`](code/bubble_scatter.py)

![bubble_scatter_district](figure/bubble_scatter_district.png)

![bubble_scatter_type](figure/bubble_scatter_type.png)

## 各行政区与楼盘类型树状图

> 展示不同行政区中各类楼盘的数量及其价格水平，通过图形大小和颜色的变化，直观地呈现数据的层次结构和分布情况

[`treemap_average_price.py`](code/treemap_average_price.py)

![treemap_average_unit_price](figure/treemap_average_unit_price.png)

![treemap_average_total_price](figure/treemap_average_total_price.png)

## 各行政区房型的平均价格分组柱状图

> 展示不同行政区内不同房型的平均单价和总价，便于比较和分析各行政区及房型之间的价格差异和趋势

[`grouped_bar_average_price.py`](code/grouped_bar_average_price.py)

![grouped_bar_average_unit_price](figure/grouped_bar_average_unit_price.png)

![grouped_bar_average_total_price](figure/grouped_bar_average_total_price.png)

## 楼盘价格分布房型分类散点图

> 直观地展示不同房型的楼盘在单价和总价上的分布情况，添加回归线，更好观察观察单价与总价之间的趋势关系

[`price_distribution_type.py`](code/price_distribution_type.py)

![price_distribution_type_scatter](figure/price_distribution_type_scatter.png)

## 综合信息雷达图

> 直观地比较多个类别在多个维度上的表现，展示多变量数据的综合特征

[`radar_chart.py`](code/radar_chart.py)

![radar_chart_administrative_district](figure/radar_chart_administrative_district.png)

![radar_chart_property_type](figure/radar_chart_property_type.png)