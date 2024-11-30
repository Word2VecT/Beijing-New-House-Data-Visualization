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

    # 选择需要的列
    required_columns = ["均价", "总价", "类型"]
    for col in required_columns:
        if col not in data.columns:
            print(f"缺少必要的列: {col}")
            return None

    # 处理数据类型
    # 将 '均价' 和 '总价' 转换为数值类型，处理缺失或非数值的数据
    data["均价"] = pd.to_numeric(data["均价"], errors="coerce")
    data["总价"] = pd.to_numeric(data["总价"], errors="coerce")
    data["类型"] = data["类型"].astype(str)

    # 删除含有缺失值的行
    data = data.dropna(subset=["均价", "总价", "类型"])

    return data


def visualize_data(data, output_image):
    """
    绘制楼盘价格分布的散点图，并保存为图片文件。
    """
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    plt.rcParams["font.sans-serif"] = ["STHeiti"]

    # 创建散点图
    sns.scatterplot(data=data, x="均价", y="总价", hue="类型", palette="viridis", s=100, alpha=0.7, edgecolor="k")

    # 设置图表标题和标签
    plt.title("楼盘价格分布散点图", fontsize=16)
    plt.xlabel("均价 (元/㎡)", fontsize=14)
    plt.ylabel("总价 (万元)", fontsize=14)

    # 设置图例标题
    plt.legend(title="类型", title_fontsize=12, fontsize=10)

    # 调整布局
    plt.tight_layout()

    # 保存图表
    plt.savefig(output_image, dpi=300)
    plt.close()
    print(f"散点图已保存为 {output_image}")


def main():
    input_csv = "../new_house_data.csv"  # 输入的 CSV 文件路径
    output_image = "../figire/price_distribution.png"  # 输出的图片文件路径

    # 检查输入文件是否存在
    if not os.path.exists(input_csv):
        print(f"输入文件 {input_csv} 不存在。请确保文件路径正确。")
        return

    # 加载和处理数据
    data = load_data(input_csv)
    if data is None or data.empty:
        print("数据加载失败或数据为空。")
        return

    # 可视化数据
    visualize_data(data, output_image)


if __name__ == "__main__":
    main()
