import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def load_data(csv_file):
    """
    加载 CSV 数据，并进行必要的数据清洗和类型转换。

    Parameters:
    - csv_file: str，CSV 文件路径

    Returns:
    - DataFrame 或 None
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


def plot_price_distribution_scatter(data, output_image, hue="房型"):
    """
    绘制楼盘价格分布的散点图，并保存为图片文件。

    Parameters:
    - data: DataFrame，已清洗的数据
    - output_image: str，输出图片文件路径
    - hue: str，用于颜色编码的类别，可以是 '房型' 或其他
    """
    plt.figure(figsize=(14, 10))
    sns.set_theme(style="whitegrid")
    plt.rcParams["font.sans-serif"] = ["STHeiti"]

    # 创建散点图
    scatter = sns.scatterplot(data=data, x="均价", y="总价", hue=hue, palette="viridis", alpha=0.7, edgecolor="k")

    # 设置标题和标签
    plt.title("楼盘单价与总价分布散点图（按房型区分）", fontsize=20)
    plt.xlabel("均价 (元/㎡)", fontsize=16)
    plt.ylabel("总价 (万元)", fontsize=16)

    # 设置图例
    plt.legend(title="房型", title_fontsize=14, fontsize=12, loc="upper left", bbox_to_anchor=(1, 1))

    # 添加回归线（可选）
    sns.regplot(data=data, x="均价", y="总价", scatter=False, ax=scatter.axes, color="gray", line_kws={"linewidth": 1})

    # 调整布局
    plt.tight_layout()

    # 保存图表
    plt.savefig(output_image, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"价格分布散点图已保存为 {output_image}")


def main():
    input_csv = "../new_house_data.csv"  # 输入的 CSV 文件路径
    output_image_scatter = "../figire/price_distribution_type_scatter.png"  # 输出的散点图路径

    # 检查输入文件是否存在
    if not os.path.exists(input_csv):
        print(f"输入文件 {input_csv} 不存在。请确保文件路径正确。")
        return

    # 加载和处理数据
    data = load_data(input_csv)
    if data is None or data.empty:
        print("数据加载失败或数据为空。")
        return

    # 绘制散点图
    plot_price_distribution_scatter(data, output_image_scatter, hue="房型")


if __name__ == "__main__":
    main()
