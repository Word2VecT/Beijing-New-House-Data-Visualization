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
    required_columns = ["均价", "总价", "行政区", "类型"]
    for col in required_columns:
        if col not in data.columns:
            print(f"缺少必要的列: {col}")
            return None

    # 处理数据类型
    # 将 '均价' 和 '总价' 转换为数值类型，处理缺失或非数值的数据
    data["均价"] = pd.to_numeric(data["均价"], errors="coerce")
    data["总价"] = pd.to_numeric(data["总价"], errors="coerce")
    data["行政区"] = data["行政区"].astype(str)
    data["类型"] = data["类型"].astype(str)

    # 删除含有缺失值的行
    data = data.dropna(subset=["均价", "总价", "行政区", "类型"])

    return data


def compute_average_prices(data):
    """
    按行政区和楼盘类型分组，计算平均单价和平均总价。
    """
    grouped = data.groupby(["行政区", "类型"]).agg(平均单价=("均价", "mean"), 平均总价=("总价", "mean")).reset_index()

    # 创建透视表
    pivot_unit_price = grouped.pivot(index="行政区", columns="类型", values="平均单价")
    pivot_total_price = grouped.pivot(index="行政区", columns="类型", values="平均总价")

    return pivot_unit_price, pivot_total_price


def plot_heatmap(pivot_table, title, y_label, output_image, fmt=".0f", cmap="YlGnBu"):
    """
    绘制热力图，并保存为图片文件。
    """
    plt.figure(figsize=(12, 8))
    sns.set_theme(style="white")
    plt.rcParams["font.sans-serif"] = ["STHeiti"]

    # 创建热力图
    sns.heatmap(
        pivot_table, annot=True, fmt=fmt, cmap=cmap, linewidths=0.5, linecolor="gray", cbar_kws={"label": y_label}
    )

    # 设置标题和标签
    plt.title(title, fontsize=16, pad=20)
    plt.xlabel("楼盘类型", fontsize=14)
    plt.ylabel("行政区", fontsize=14)

    # 调整布局
    plt.tight_layout()

    # 保存图表
    plt.savefig(output_image, dpi=300)
    plt.close()
    print(f"热力图已保存为 {output_image}")


def main():
    input_csv = "../new_house_data.csv"  # 输入的 CSV 文件路径
    output_image_unit_price = "../figire/heatmap_average_unit_price_per_district_type.png"  # 输出的平均单价热力图路径
    output_image_total_price = "../figire/heatmap_average_total_price_per_district_type.png"  # 输出的平均总价热力图路径

    # 检查输入文件是否存在
    if not os.path.exists(input_csv):
        print(f"输入文件 {input_csv} 不存在。请确保文件路径正确。")
        return

    # 加载和处理数据
    data = load_data(input_csv)
    if data is None or data.empty:
        print("数据加载失败或数据为空。")
        return

    # 计算平均单价和总价
    pivot_unit_price, pivot_total_price = compute_average_prices(data)

    # 检查是否有数据
    if pivot_unit_price.empty or pivot_total_price.empty:
        print("分组后的数据为空。")
        return

    # 绘制平均单价热力图
    plot_heatmap(
        pivot_table=pivot_unit_price,
        title="各行政区与楼盘类型的平均单价热力图",
        y_label="平均单价 (元/㎡)",
        output_image=output_image_unit_price,
        fmt=".0f",
        cmap="YlGnBu",
    )

    # 绘制平均总价热力图
    plot_heatmap(
        pivot_table=pivot_total_price,
        title="各行政区与楼盘类型的平均总价热力图",
        y_label="平均总价 (万元)",
        output_image=output_image_total_price,
        fmt=".0f",
        cmap="YlOrRd",
    )


if __name__ == "__main__":
    main()
