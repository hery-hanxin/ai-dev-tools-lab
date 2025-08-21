# CSV → JSON 转换器（标准库版）

功能：
- 读取CSV文件并进行健壮错误处理
- 字段类型自动推断（int/float/bool），其余保持为字符串
- 对缺失值/空值友好处理：空字符串与缺失单元格输出为 `null`
- 支持自定义分隔符
- 提供命令行接口与清晰错误信息
- 仅依赖 Python 标准库（csv、json、argparse、sys）

## 环境
- Python 3.8+
- 无需安装第三方库

## 使用
```bash
# 基本用法：从文件读，输出到标准输出
python converter.py test_data/sample.csv

# 指定输出文件
python converter.py test_data/sample.csv -o out.json

# 自定义分隔符（例如分号）
python converter.py test_data/sample.csv -o out.json -d ";"

# 自定义缩进（<=0 表示紧凑JSON）
python converter.py test_data/sample.csv -o out.json --indent 2

# 从标准输入读取，并写到标准输出（Windows PowerShell 示例）
Get-Content test_data/sample.csv | python converter.py - -o -

# 移除为 null 的字段
python converter.py test_data/sample.csv -o out.json --drop-null
```

## 参数说明
- `input`：输入CSV路径；`-` 表示从标准输入读取
- `-o, --output`：输出JSON路径；`-` 表示写到标准输出（默认）
- `-d, --delimiter`：分隔符，默认 `,`（必须为单字符）
- `--encoding`：输入与输出文件编码（默认 `utf-8`）
- `--indent`：JSON缩进空格数；`<=0` 则输出紧凑JSON（默认 2）
- `--drop-null`：移除值为 `null` 的字段

## 类型推断规则
1. 空/全空白字符串 → `null`
2. 不区分大小写的 `true`/`false` → 布尔值
3. 整数（含可选正负号）→ `int`
4. 其余可解析的数字 → `float`
5. 无法解析 → 原样字符串

## 错误信息示例（前缀统一为 `Error:`）
- 找不到输入文件: `<path>`
- 没有权限读取输入文件: `<path>`
- CSV 看起来为空或缺少表头行。请确保文件首行是列名。
- 分隔符 --delimiter 必须是单个字符
- JSON 写出失败: `<原因>`

## 示例
`test_data/sample.csv` 内容：
```csv
name,age,city,is_student,salary
Alice,25,New York,false,50000.5
Bob,30,,true,
Charlie,35,London,false,75000
Diana,28,Paris,true,45000.0
```

运行：
```bash
python converter.py test_data/sample.csv -o out.json --indent 2
```
输出：
```json
[
  {"name": "Alice", "age": 25, "city": "New York", "is_student": false, "salary": 50000.5},
  {"name": "Bob", "age": 30, "city": null, "is_student": true, "salary": null},
  {"name": "Charlie", "age": 35, "city": "London", "is_student": false, "salary": 75000},
  {"name": "Diana", "age": 28, "city": "Paris", "is_student": true, "salary": 45000.0}
]
```
