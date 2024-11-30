import pandas as pd
import matplotlib.pyplot as plt
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
    required_columns = ["均价", "总价", "行政区"]
    for col in required_columns:
        if col not in data.columns:
            print(f"缺少必要的列: {col}")
            return None

    # 处理数据类型
    # 将 '均价' 和 '总价' 转换为数值类型，处理缺失或非数值的数据
    data["均价"] = pd.to_numeric(data["均价"], errors="coerce")
    data["总价"] = pd.to_numeric(data["总价"], errors="coerce")
    data["行政区"] = data["行政区"].astype(str)

    # 删除含有缺失值的行
    data = data.dropna(subset=["均价", "总价", "行政区"])

    return data


def prepare_plot_data(data):
    """
    按行政区分组，计算每个行政区的平均单价、平均总价和楼盘数量。
    """
    grouped = (
        data.groupby("行政区")
        .agg(
            平均单价=("均价", "mean"),
            平均总价=("总价", "mean"),
            楼盘数量=("楼盘名称", "count"),  # 假设每个楼盘名称唯一
        )
        .reset_index()
    )

    # 排序（可选）
    grouped = grouped.sort_values(by="平均单价", ascending=False)

    return grouped


def plot_bar_chart(grouped_data, value_column, y_label, title, output_image):
    """
    绘制柱状图，柱子高度代表指定的值，柱子宽度代表楼盘数量。
    """
    # 获取数据
    districts = grouped_data["行政区"]
    values = grouped_data[value_column]
    counts = grouped_data["楼盘数量"]

    plt.rcParams["font.sans-serif"] = ["STHeiti"]

    # 设置柱子宽度的比例
    min_width = 0.3
    max_width = 1.0
    normalized_counts = (
        (counts - counts.min()) / (counts.max() - counts.min()) if counts.max() != counts.min() else [0.5] * len(counts)
    )
    widths = min_width + normalized_counts * (max_width - min_width)

    # 绘图
    plt.figure(figsize=(12, 8))
    ax = plt.gca()

    for idx, (district, value, width) in enumerate(zip(districts, values, widths)):
        ax.bar(idx, value, width=width, align="center", alpha=0.7, edgecolor="black")

    # 设置 x 轴
    ax.set_xticks(range(len(districts)))
    ax.set_xticklabels(districts, rotation=45, ha="right")

    # 设置标签和标题
    plt.xlabel("行政区", fontsize=14)
    plt.ylabel(y_label, fontsize=14)
    plt.title(title, fontsize=16)

    # 添加楼盘数量标签
    for idx, (value, count, width) in enumerate(zip(values, counts, widths)):
        plt.text(idx, value + (values.max() * 0.01), f"×{count}", ha="center", va="bottom", fontsize=10)

    plt.tight_layout()
    plt.savefig(output_image, dpi=300)
    plt.close()
    print(f"柱状图已保存为 {output_image}")


def main():
    input_csv = "../new_house_data.csv"  # 输入的 CSV 文件路径
    output_image_unit_price = "../figire/average_unit_price_per_district.png"  # 输出的平均单价柱状图路径
    output_image_total_price = "../figire/average_total_price_per_district.png"  # 输出的平均总价柱状图路径

    # 检查输入文件是否存在
    if not os.path.exists(input_csv):
        print(f"输入文件 {input_csv} 不存在。请确保文件路径正确。")
        return

    # 加载和处理数据
    data = load_data(input_csv)
    if data is None or data.empty:
        print("数据加载失败或数据为空。")
        return

    # 准备绘图数据
    grouped_data = prepare_plot_data(data)
    if grouped_data.empty:
        print("分组后的数据为空。")
        return

    # 绘制平均单价柱状图
    plot_bar_chart(
        grouped_data=grouped_data,
        value_column="平均单价",
        y_label="平均单价 (元/㎡)",
        title="各行政区楼盘平均单价分布",
        output_image=output_image_unit_price,
    )

    # 绘制平均总价柱状图
    plot_bar_chart(
        grouped_data=grouped_data,
        value_column="平均总价",
        y_label="平均总价 (万元)",
        title="各行政区楼盘平均总价分布",
        output_image=output_image_total_price,
    )


if __name__ == "__main__":
    main()
