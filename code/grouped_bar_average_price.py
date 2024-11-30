import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
    required_columns = ["楼盘名称", "类型", "行政区", "房型", "面积", "均价", "总价"]
    for col in required_columns:
        if col not in data.columns:
            print(f"缺少必要的列: {col}")
            return None

    # 处理数据类型
    data["房型"] = pd.to_numeric(data["房型"], errors="coerce")
    data["均价"] = pd.to_numeric(data["均价"], errors="coerce")
    data["总价"] = pd.to_numeric(data["总价"], errors="coerce")
    data["类型"] = data["类型"].astype(str)
    data["行政区"] = data["行政区"].astype(str)

    # 删除含有缺失值的行
    data = data.dropna(subset=["楼盘名称", "类型", "行政区", "房型", "面积", "均价", "总价"])

    return data


def prepare_grouped_data(data):
    """
    按行政区和房型分组，计算每组的平均单价和平均总价。
    """
    grouped = data.groupby(["行政区", "房型"]).agg(平均单价=("均价", "mean"), 平均总价=("总价", "mean")).reset_index()

    return grouped


def plot_grouped_bar_chart(grouped_data, output_image, metric="平均单价"):
    """
    绘制各行政区房型的平均单价或总价的分组柱状图，并保存为图片文件。

    Parameters:
    - grouped_data: DataFrame，包含行政区、房型、平均单价和平均总价
    - output_image: str，输出图片文件路径
    - metric: str，用于展示的指标，可以是 '平均单价' 或 '平均总价'
    """
    plt.figure(figsize=(16, 10))
    sns.set_theme(style="whitegrid")
    plt.rcParams["font.sans-serif"] = ["STHeiti"]

    # 确定绘图的指标
    y = metric

    # 创建分组柱状图
    sns.barplot(data=grouped_data, x="行政区", y=y, hue="房型", palette="Set2")

    # 设置标题和标签
    plt.title(f"各行政区房型的{metric}分布", fontsize=20)
    plt.xlabel("行政区", fontsize=16)
    plt.ylabel(metric, fontsize=16)

    # 设置图例标题
    plt.legend(title="房型", title_fontsize=14, fontsize=12)

    # 添加数据标签
    for container in plt.gca().containers:
        plt.gca().bar_label(container, fmt="%.0f", padding=3, fontsize=10)

    # 调整布局
    plt.tight_layout()

    # 保存图表
    plt.savefig(output_image, dpi=300)
    plt.close()
    print(f"分组柱状图已保存为 {output_image}")


def main():
    input_csv = "../new_house_data.csv"  # 输入的 CSV 文件路径
    output_image_unit_price = "../figire/grouped_bar_average_unit_price.png"  # 输出的按平均单价的分组柱状图路径
    output_image_total_price = "../figire/grouped_bar_average_total_price.png"  # 输出的按平均总价的分组柱状图路径

    # 检查输入文件是否存在
    if not os.path.exists(input_csv):
        print(f"输入文件 {input_csv} 不存在。请确保文件路径正确。")
        return

    # 加载和处理数据
    data = load_data(input_csv)
    if data is None or data.empty:
        print("数据加载失败或数据为空。")
        return

    # 准备分组数据
    grouped_data = prepare_grouped_data(data)
    if grouped_data.empty:
        print("分组后的数据为空。")
        return

    # 绘制按平均单价的分组柱状图
    plot_grouped_bar_chart(grouped_data=grouped_data, output_image=output_image_unit_price, metric="平均单价")

    # 绘制按平均总价的分组柱状图
    plot_grouped_bar_chart(grouped_data=grouped_data, output_image=output_image_total_price, metric="平均总价")


if __name__ == "__main__":
    main()
