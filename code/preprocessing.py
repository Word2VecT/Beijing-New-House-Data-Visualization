import json
import csv
import re


def extract_number(text):
    """
    从字符串中提取所有数字，支持整数和小数
    """
    return re.findall(r"\d+\.?\d*", text)


def safe_get_str(record, key):
    """
    安全地获取字符串值，如果值为 None 或非字符串，则返回空字符串
    """
    value = record.get(key, "")
    return value.strip() if isinstance(value, str) else ""


def process_record(record):
    """
    处理单个 JSON 记录，返回一个字典符合 CSV 结构
    """
    processed = {}

    # 1. 楼盘名称
    processed["楼盘名称"] = safe_get_str(record, "name")

    # 2. 类型
    processed["类型"] = safe_get_str(record, "type")

    # 3. 地理位置（分为行政区、街道、具体位置）
    locations = record.get("location", [])
    if not isinstance(locations, list):
        locations = []
    location_fields = ["行政区", "街道", "具体位置"]
    for i, field in enumerate(location_fields):
        if i < len(locations) and isinstance(locations[i], str):
            processed[field] = locations[i].strip()
        else:
            processed[field] = ""

    # 4. 房型（取平均值）
    rooms = record.get("room", [])
    if not isinstance(rooms, list):
        rooms = []
    room_numbers = []
    for room in rooms:
        if isinstance(room, str):
            nums = extract_number(room)
            if nums:
                room_numbers.extend([float(num) for num in nums])
    if room_numbers:
        avg_room = sum(room_numbers) / len(room_numbers)
        processed["房型"] = round(avg_room)
    else:
        processed["房型"] = ""

    # 5. 面积（取平均值）
    area_text = safe_get_str(record, "area")
    area_numbers = extract_number(area_text)
    if len(area_numbers) >= 2:
        lower = float(area_numbers[0])
        upper = float(area_numbers[1])
        avg_area = (lower + upper) / 2
        processed["面积"] = round(avg_area)
    elif len(area_numbers) == 1:
        processed["面积"] = round(float(area_numbers[0]))
    else:
        processed["面积"] = ""

    # 6. 总价（万元，整数）
    total_price_text = safe_get_str(record, "total_price")
    total_price_nums = extract_number(total_price_text)
    if total_price_nums:
        processed["总价"] = int(float(total_price_nums[0]))
    else:
        processed["总价"] = ""

    # 7. 均价（元，整数）
    unit_price_text = safe_get_str(record, "unit_price")
    unit_price_nums = extract_number(unit_price_text)
    if unit_price_nums:
        processed["均价"] = int(float(unit_price_nums[0]))
    else:
        processed["均价"] = ""

    return processed


def json_to_csv(json_file, csv_file):
    """
    将 JSON 文件转换为 CSV 文件，按照指定的预处理规则
    """
    with open(json_file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"JSON 解码错误: {e}")
            return

    # 确保数据是一个列表
    if not isinstance(data, list):
        data = [data]

    # 定义 CSV 的字段名
    fieldnames = ["楼盘名称", "类型", "行政区", "街道", "具体位置", "房型", "面积", "总价", "均价"]

    with open(csv_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for record in data:
            if not isinstance(record, dict):
                print(f"跳过非字典类型的记录: {record}")
                continue
            processed = process_record(record)
            writer.writerow(processed)


if __name__ == "__main__":
    input_json = "./new_house_data.json"  # 输入的 JSON 文件路径
    output_csv = "./new_house_data.csv"  # 输出的 CSV 文件路径
    json_to_csv(input_json, output_csv)
    print(f"数据已成功从 {input_json} 转换为 {output_csv}")
