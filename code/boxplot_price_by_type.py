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


def plot_boxplot(data, value_column, y_label, title, output_image):
    """
    绘制楼盘类型的单价或总价分布箱线图，并保存为图片文件。
    """
    plt.figure(figsize=(12, 8))
    sns.set_theme(style="whitegrid")
    plt.rcParams["font.sans-serif"] = ["STHeiti"]

    # 创建箱线图
    sns.boxplot(
        x="类型",
        y=value_column,
        data=data,
        palette="Set3",
        showfliers=True,  # 显示异常值
    )

    # 设置图表标题和标签
    plt.title(title, fontsize=16)
    plt.xlabel("楼盘类型", fontsize=14)
    plt.ylabel(y_label, fontsize=14)

    # 添加数值标签（中位数）
    medians = data.groupby(["类型"])[value_column].median().values
    for i, median in enumerate(medians):
        plt.text(i, median, f"{median:.0f}", horizontalalignment="center", color="black", weight="semibold")

    plt.tight_layout()
    plt.savefig(output_image, dpi=300)
    plt.close()
    print(f"箱线图已保存为 {output_image}")


def main():
    input_csv = "../new_house_data.csv"  # 输入的 CSV 文件路径
    output_image_unit_price = "../figire/boxplot_unit_price_by_type.png"  # 输出的单价箱线图路径
    output_image_total_price = "../figire/boxplot_total_price_by_type.png"  # 输出的总价箱线图路径

    # 检查输入文件是否存在
    if not os.path.exists(input_csv):
        print(f"输入文件 {input_csv} 不存在。请确保文件路径正确。")
        return

    # 加载和处理数据
    data = load_data(input_csv)
    if data is None or data.empty:
        print("数据加载失败或数据为空。")
        return

    # 绘制平均单价箱线图
    plot_boxplot(
        data=data,
        value_column="均价",
        y_label="均价 (元/㎡)",
        title="各楼盘类型均价分布箱线图",
        output_image=output_image_unit_price,
    )

    # 绘制平均总价箱线图
    plot_boxplot(
        data=data,
        value_column="总价",
        y_label="总价 (万元)",
        title="各楼盘类型总价分布箱线图",
        output_image=output_image_total_price,
    )


if __name__ == "__main__":
    main()
