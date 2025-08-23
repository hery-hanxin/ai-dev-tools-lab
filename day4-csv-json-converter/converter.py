import csv
import json
from typing import List, Dict, Any, Optional
from pathlib import Path


def read_csv_file(csv_path: str) -> List[Dict[str, Any]]:
    """
    读取CSV文件并返回字典列表
    
    Args:
        csv_path: CSV文件的路径
        
    Returns:
        包含CSV数据的字典列表，每个字典代表一行数据
        
    Raises:
        FileNotFoundError: 当CSV文件不存在时
        UnicodeDecodeError: 当文件编码有问题时
    """
    try:
        # 使用 utf-8-sig 兼容含 BOM 的 CSV（常见于 Windows）
        with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        return rows
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV文件未找到: {csv_path}")
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"文件编码错误: {e}")


def convert_csv_to_json_data(csv_data: List[Dict[str, Any]]) -> str:
    """
    将CSV数据转换为JSON格式的字符串
    
    Args:
        csv_data: CSV数据字典列表
        
    Returns:
        JSON格式的字符串
    """
    return json.dumps(csv_data, ensure_ascii=False, indent=2)


def write_json_to_file(json_data: str, output_path: Optional[str] = None) -> None:
    """
    将JSON数据写入文件
    
    Args:
        json_data: 要写入的JSON字符串
        output_path: 输出文件路径，如果为None则打印到控制台
    """
    if output_path:
        try:
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(json_data)
            print(f"JSON数据已成功写入: {output_path}")
        except IOError as e:
            print(f"写入文件时出错: {e}")
    else:
        print(json_data)


def convert_csv_to_json(csv_path: str, output_path: Optional[str] = None) -> None:
    """
    主要的转换函数：读取CSV文件，转换为JSON，并输出
    
    Args:
        csv_path: 输入CSV文件的路径
        output_path: 输出JSON文件的路径，如果为None则打印到控制台
    """
    try:
        # 读取CSV文件
        csv_data = read_csv_file(csv_path)
        
        # 转换为JSON格式
        json_data = convert_csv_to_json_data(csv_data)
        
        # 输出结果
        write_json_to_file(json_data, output_path)
        
    except Exception as e:
        print(f"转换过程中出错: {e}")


def print_csv_as_json(csv_path: str) -> None:
    """
    兼容性函数：保持原有接口不变
    
    Args:
        csv_path: CSV文件的路径
    """
    convert_csv_to_json(csv_path)


# 主程序示例
if __name__ == "__main__":
    # 示例用法
    sample_csv = "test_data/sample.csv"
    
    # 打印到控制台
    print("=== 转换结果（打印到控制台）===")
    convert_csv_to_json(sample_csv)
    
    # 保存到文件
    print("\n=== 转换结果（保存到文件）===")
    output_file = "test_data/output.json"
    convert_csv_to_json(sample_csv, output_file)
