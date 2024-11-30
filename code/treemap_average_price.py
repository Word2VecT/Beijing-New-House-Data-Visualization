import pandas as pd
import matplotlib.pyplot as plt
import squarify
import os


def load_data(csv_file):
    """
    加载 CSV 数据，并进行必要的数据清洗和类型转换。
    """
    try:
        data = pd.read_csv(csv_file, encoding="utf-8-sig")
    except FileNotFoundError:
        print(f"文件 {csv_file} 未找到。请确保文件路径正确。")
        return None
    except pd.errors.EmptyDataError:
        print(f"文件 {csv_file} 是空的。")
        return None
    except pd.errors.ParserError as e:
        print(f"解析 CSV 文件时出错: {e}")
        return None

    # 检查必要的列
    required_columns = ["楼盘名称", "类型", "行政区", "面积", "均价", "总价"]
    for col in required_columns:
        if col not in data.columns:
            print(f"缺少必要的列: {col}")
            return None

    # 处理数据类型
    data["面积"] = pd.to_numeric(data["面积"], errors="coerce")
    data["房型"] = pd.to_numeric(data["房型"], errors="coerce")
    data["均价"] = pd.to_numeric(data["均价"], errors="coerce")
    data["总价"] = pd.to_numeric(data["总价"], errors="coerce")
    data["类型"] = data["类型"].astype(str)
    data["行政区"] = data["行政区"].astype(str)

    # 删除含有缺失值的行
    data = data.dropna(subset=["楼盘名称", "类型", "行政区", "面积", "均价", "总价"])

    return data


def prepare_treemap_data(data):
    """
    按行政区和楼盘类型分组，计算每组的楼盘数量、平均单价和平均总价。
    """
    grouped = (
        data.groupby(["行政区", "类型"])
        .agg(
            楼盘数量=("楼盘名称", "count"),
            平均单价=("均价", "mean"),
            平均总价=("总价", "mean"),  # 计算平均总价
        )
        .reset_index()
    )

    return grouped


def plot_treemap(grouped_data, output_image, color_metric="平均单价"):
    """
    绘制树状图，并保存为图片文件。

    Parameters:
    - grouped_data: DataFrame，包含行政区、类型、楼盘数量、平均单价和平均总价
    - output_image: str，输出图片文件路径
    - color_metric: str，用于颜色编码的指标，可以是 '平均单价' 或 '平均总价'
    """
    # 创建标签
    grouped_data["标签"] = grouped_data.apply(
        lambda row: f"{row['行政区']}\n{row['类型']}\n数量: {row['楼盘数量']}\n{color_metric}: {int(row[color_metric])}",
        axis=1,
    )

    # 设置颜色范围
    norm = plt.Normalize(grouped_data[color_metric].min(), grouped_data[color_metric].max())
    cmap = plt.cm.Blues if color_metric == "平均单价" else plt.cm.Oranges
    colors = cmap(norm(grouped_data[color_metric]))

    # 创建图形和树状图的绘图区
    plt.figure(figsize=(16, 12))
    plt.rcParams["font.sans-serif"] = ["STHeiti"]

    # 绘制树状图
    squarify.plot(
        sizes=grouped_data["楼盘数量"], label=grouped_data["标签"], color=colors, alpha=0.8, edgecolor="white"
    )

    # 设置标题
    plt.title(f"各行政区与楼盘类型的树状图（按{color_metric}）", fontsize=20)

    # 关闭坐标轴
    plt.axis("off")

    # 创建一个新的轴，用于颜色条
    cax = plt.axes([0.92, 0.1, 0.02, 0.8])  # [left, bottom, width, height]
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, cax=cax)
    cbar.set_label(color_metric, fontsize=14)

    # 调整布局
    plt.tight_layout(rect=[0, 0, 0.9, 1])  # 留出右侧空间给颜色条

    # 保存图表
    plt.savefig(output_image, dpi=300)
    plt.close()
    print(f"树状图已保存为 {output_image}")


def main():
    input_csv = "../new_house_data.csv"  # 输入的 CSV 文件路径
    output_image_unit_price = "../figire/treemap_average_unit_price.png"  # 输出的按平均单价的树状图路径
    output_image_total_price = "../figire/treemap_average_total_price.png"  # 输出的按平均总价的树状图路径

    # 检查输入文件是否存在
    if not os.path.exists(input_csv):
        print(f"输入文件 {input_csv} 不存在。请确保文件路径正确。")
        return

    # 加载和处理数据
    data = load_data(input_csv)
    if data is None or data.empty:
        print("数据加载失败或数据为空。")
        return

    # 准备树状图数据
    grouped_data = prepare_treemap_data(data)
    if grouped_data.empty:
        print("分组后的数据为空。")
        return

    # 绘制按平均单价的树状图
    plot_treemap(grouped_data=grouped_data, output_image=output_image_unit_price, color_metric="平均单价")

    # 绘制按平均总价的树状图
    plot_treemap(grouped_data=grouped_data, output_image=output_image_total_price, color_metric="平均总价")


if __name__ == "__main__":
    main()
