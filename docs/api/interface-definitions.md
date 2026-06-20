# 机器可读 API 定义

本仓库发布机器可读 API 定义，便于工具集成、SDK 生成和 AI agent 使用：

| API 类型 | 格式 | 文件 |
|---|---|---|
| HTTP API | OpenAPI 3.1 | [`openapi.yaml`](openapi.yaml) |
| JSON-RPC API | OpenRPC 1.2.6 | [`openrpc.json`](openrpc.json) |

每个接口对应的生成片段也会保留，方便审阅：

| API 类型 | 片段目录 |
|---|---|
| HTTP API | [`specs/http/`](specs/http/) |
| JSON-RPC API | [`specs/json-rpc/`](specs/json-rpc/) |

java-tron API 源码变更后，可执行以下命令重新生成：

```bash
python3 scripts/generate_api_specs.py
```

生成脚本需要本地存在一份 java-tron 代码仓库。默认会从当前文档仓库相邻的 `../java-tron` 查找，也可以显式设置 `JAVA_TRON_SOURCE`：

```bash
JAVA_TRON_SOURCE=/path/to/java-tron python3 scripts/generate_api_specs.py
```

生成的接口列表来自源码：

- HTTP 路径、HTTP 方法、servlet 类、Solidity 端点映射以及请求消息提示来自 java-tron 源码树。
- JSON-RPC 方法名、Java 参数名称/类型、返回类型以及声明的错误码来自 `TronJsonRpc.java`。
- Markdown API 页面仅用于读取面向人的摘要、说明和外部文档链接。

默认情况下，生成脚本会确保发布的定义与文档化 API 范围保持一致。如果文档中的 HTTP 路径或 JSON-RPC 方法已不存在于 java-tron 源码中，生成过程会失败，而不是静默产出过期定义。

顶层 `openapi.yaml` 和 `openrpc.json` 由各接口片段汇总生成，方便工具直接消费一个标准文件。
