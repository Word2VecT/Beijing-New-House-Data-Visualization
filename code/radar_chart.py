import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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


def prepare_radar_data(data, group_by="行政区"):
    """
    按指定类别分组，计算各组的关键指标平均值。

    Parameters:
    - data: DataFrame，已清洗的数据
    - group_by: str，用于分组的列名，如 '行政区' 或 '类型'

    Returns:
    - DataFrame，包含分组后的平均指标
    """
    grouped = (
        data.groupby(group_by)
        .agg(
            平均面积=("面积", "mean"),
            平均房型=("房型", "mean"),
            平均单价=("均价", "mean"),
            平均总价=("总价", "mean"),
            楼盘数量=("楼盘名称", "count"),
        )
        .reset_index()
    )

    return grouped


def normalize_data(df, metrics):
    """
    对指定的指标进行归一化处理，使其值介于0和1之间。

    Parameters:
    - df: DataFrame，需要归一化的数据
    - metrics: list of str，需要归一化的列名

    Returns:
    - DataFrame，包含归一化后的指标
    """
    df_norm = df.copy()
    for metric in metrics:
        min_val = df[metric].min()
        max_val = df[metric].max()
        if max_val - min_val == 0:
            df_norm[metric] = 0
        else:
            df_norm[metric] = (df[metric] - min_val) / (max_val - min_val)
    return df_norm


def plot_radar_chart(grouped_data, output_image, group_by="行政区", max_vars=20):
    """
    绘制雷达图，并保存为图片文件。

    Parameters:
    - grouped_data: DataFrame，包含分组后的平均指标
    - output_image: str，输出图片文件路径
    - group_by: str，用于分组的列名，如 '行政区' 或 '类型'
    - max_vars: int，雷达图显示的最大类别数量
    """
    # 选择前max_vars个类别
    if len(grouped_data) > max_vars:
        grouped_data = grouped_data.head(max_vars)
        print(f"数据量较大，已选择前 {max_vars} 个 {group_by} 进行绘制。")

    categories = ["平均面积", "平均房型", "平均单价", "平均总价", "楼盘数量"]
    N = len(categories)

    # 计算角度
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # 完成闭环

    # 设置雷达图
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    plt.rcParams["font.sans-serif"] = ["STHeiti"]

    # 绘制每个类别
    for idx, row in grouped_data.iterrows():
        values = row[categories].tolist()
        values += values[:1]  # 完成闭环
        ax.plot(angles, values, label=row[group_by], linewidth=2)
        ax.fill(angles, values, alpha=0.25)

    # 设置类别标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12)

    # 设置 Y 轴
    ax.set_rlabel_position(30)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8])
    ax.set_yticklabels(["20%", "40%", "60%", "80%"], fontsize=10)
    ax.set_ylim(0, 1)

    # 添加标题和图例
    plt.title(f"{group_by}的楼盘综合指标雷达图", fontsize=16, y=1.08)
    plt.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

    # 保存图表
    plt.tight_layout()
    plt.savefig(output_image, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"雷达图已保存为 {output_image}")


def main():
    input_csv = "../new_house_data.csv"  # 输入的 CSV 文件路径
    output_image_radar_admin = "../figure/radar_chart_administrative_district.png"  # 输出的雷达图路径（按行政区）
    output_image_radar_type = "../figure/radar_chart_property_type.png"  # 输出的雷达图路径（按楼盘类型）

    # 检查输入文件是否存在
    if not os.path.exists(input_csv):
        print(f"输入文件 {input_csv} 不存在。请确保文件路径正确。")
        return

    # 加载和处理数据
    data = load_data(input_csv)
    if data is None or data.empty:
        print("数据加载失败或数据为空。")
        return

    # 准备按行政区分组的数据
    grouped_admin = prepare_radar_data(data, group_by="行政区")
    if grouped_admin.empty:
        print("按行政区分组后的数据为空。")
        return

    # 归一化指标
    metrics = ["平均面积", "平均房型", "平均单价", "平均总价", "楼盘数量"]
    grouped_admin_norm = normalize_data(grouped_admin, metrics)

    # 绘制按行政区分组的雷达图
    plot_radar_chart(grouped_admin_norm, output_image_radar_admin, group_by="行政区", max_vars=20)

    # 准备按楼盘类型分组的数据
    grouped_type = prepare_radar_data(data, group_by="类型")
    if grouped_type.empty:
        print("按楼盘类型分组后的数据为空。")
        return

    # 归一化指标
    grouped_type_norm = normalize_data(grouped_type, metrics)

    # 绘制按楼盘类型分组的雷达图
    plot_radar_chart(grouped_type_norm, output_image_radar_type, group_by="类型", max_vars=20)


if __name__ == "__main__":
    main()
