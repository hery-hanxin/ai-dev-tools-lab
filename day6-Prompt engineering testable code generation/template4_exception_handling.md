# 模板 4: 指导异常处理 (Guiding Exception Handling)

## 英文指令 (给 AI):

```
Write a Python script for [your task description here].
When performing side effects like file reading, you must handle potential exceptions such as `FileNotFoundError` and `PermissionError` explicitly using try-except blocks. Do not use a generic `except Exception`. The core logic inside pure functions should not handle exceptions, but assume valid input.
```

## 中文翻译 (助你理解):

"请为 [此处描述你的任务] 编写一个 Python 脚本。
在执行文件读取等副作用时，你必须使用 try-except 块显式地处理潜在的异常，例如 `FileNotFoundError` 和 `PermissionError`。不要使用宽泛的 `except Exception`。纯函数内的核心逻辑不应处理异常，而应假定输入是有效的。"

## 适用场景:
- 涉及文件操作的脚本
- 网络请求相关代码
- 生产环境部署的应用

## 异常处理原则:
- 具体异常具体处理
- 纯函数不处理异常
- 副作用操作必须处理异常
- 提供有意义的错误信息