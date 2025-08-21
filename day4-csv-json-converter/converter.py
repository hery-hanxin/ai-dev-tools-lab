import csv
import json

def print_csv_as_json(csv_path: str) -> None:
    # 使用 utf-8-sig 兼容含 BOM 的 CSV（常见于 Windows）
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    print(json.dumps(rows, ensure_ascii=False, indent=2))


# 示例
if __name__ == "__main__":
    print_csv_as_json("test_data/sample.csv")
