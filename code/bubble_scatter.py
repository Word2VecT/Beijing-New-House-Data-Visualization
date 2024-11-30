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
    required_columns = ["面积", "房型", "均价", "总价", "类型", "行政区"]
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
    data = data.dropna(subset=["面积", "房型", "均价", "总价", "类型", "行政区"])

    return data


def plot_bubble_scatter(data, output_image, color_by="类型"):
    """
    绘制楼盘面积与房型对价格的多维散点图，并保存为图片文件。

    Parameters:
    - data: DataFrame，已清洗的数据
    - output_image: str，输出图片文件路径
    - color_by: str，颜色编码的类别，可以是 '类型' 或 '行政区'
    """
    plt.figure(figsize=(14, 10))
    sns.set_theme(style="whitegrid")
    plt.rcParams["font.sans-serif"] = ["STHeiti"]

    # 选择调色板
    palette = sns.color_palette("Set2", n_colors=data[color_by].nunique())

    # 创建散点图
    scatter = sns.scatterplot(
        data=data,
        x="面积",
        y="均价",
        hue=color_by,
        size="总价",
        sizes=(100, 1000),
        alpha=0.6,
        palette=palette,
        edgecolor="w",
        linewidth=0.5,
    )

    # 设置标题和标签
    plt.title("楼盘面积与单价的关系（按{}区分）".format(color_by), fontsize=18)
    plt.xlabel("面积 (㎡)", fontsize=14)
    plt.ylabel("均价 (元/㎡)", fontsize=14)

    # 设置图例
    handles, labels = scatter.get_legend_handles_labels()
    # 移除 '总价' 的图例
    size_labels = handles[: data[color_by].nunique() + 1]
    size_labels_labels = labels[: data[color_by].nunique() + 1]
    plt.legend(
        handles=size_labels,
        labels=size_labels_labels,
        title=color_by,
        bbox_to_anchor=(1.05, 1),
        loc=2,
        borderaxespad=0.0,
    )

    # 添加色标说明
    plt.tight_layout()

    # 保存图表
    plt.savefig(output_image, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"多维散点图已保存为 {output_image}")


def main():
    input_csv = "../new_house_data.csv"  # 输入的 CSV 文件路径
    output_image_type = "../figire/bubble_scatter_type.png"  # 输出的按类型区分的散点图路径
    output_image_district = "../figire/bubble_scatter_district.png"  # 输出的按行政区区分的散点图路径

    # 检查输入文件是否存在
    if not os.path.exists(input_csv):
        print(f"输入文件 {input_csv} 不存在。请确保文件路径正确。")
        return

    # 加载和处理数据
    data = load_data(input_csv)
    if data is None or data.empty:
        print("数据加载失败或数据为空。")
        return

    # 绘制按楼盘类型区分的散点图
    plot_bubble_scatter(data, output_image_type, color_by="类型")

    # 绘制按行政区区分的散点图
    plot_bubble_scatter(data, output_image_district, color_by="行政区")


if __name__ == "__main__":
    main()
