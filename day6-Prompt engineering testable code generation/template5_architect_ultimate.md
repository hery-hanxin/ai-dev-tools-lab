# 模板 5: "架构师"终极模板 (The "Architect's" Ultimate Template)

## 英文指令 (给 AI):

```
You are an expert Python developer following best practices. Write a Python script that converts a given CSV file to a JSON file.
Your code MUST adhere to the following principles:
1. **Separation of Concerns**: The core data transformation logic must be in pure functions, completely separate from file I/O, printing, or argument parsing.
2. **Type Safety**: All function signatures, including arguments and return values, must have precise Python type hints.
3. **Self-Documenting**: Every function must include a Google-style docstring explaining its purpose, arguments (`Args:`), and return value (`Returns:`).
4. **Robust I/O**: Any function performing file I/O must handle potential exceptions (e.g., `FileNotFoundError`) gracefully.
5. **CLI Interface**: The script should be runnable from the command line, using the `argparse` library to handle input and output file paths.
```

## 中文翻译 (助你理解):

"你是一位遵循最佳实践的资深 Python 开发者。请编写一个 Python 脚本，用于将一个给定的 CSV 文件转换为 JSON 文件。
你的代码**必须**遵循以下原则：

1. **关注点分离**: 核心的数据转换逻辑必须封装在**纯函数**中，与文件I/O、打印或参数解析完全分离。
2. **类型安全**: 所有的函数签名，包括参数和返回值，都必须有精确的 Python **类型提示**。
3. **自文档化**: 每个函数都必须包含一个 Google 风格的**文档字符串 (docstring)**，解释其用途、参数 (`Args:`) 和返回值 (`Returns:`)。
4. **健壮的 I/O**: 任何执行文件 I/O 的函数都必须优雅地处理潜在的异常（如 `FileNotFoundError`）。
5. **命令行接口**: 脚本应可从命令行运行，使用 `argparse` 库来处理输入和输出的文件路径。"

## 适用场景:
- 企业级项目开发
- 高质量代码要求
- 完整功能实现

## 核心特点:
- 综合所有最佳实践
- 可直接用于生产环境
- 完整的错误处理和用户界面
- 高度可测试和可维护