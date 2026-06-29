# 机器可读 API 定义

本仓库发布机器可读 API 定义，便于工具集成、SDK 生成和 AI agent 使用：

| API 类型 | 格式 | 文件 |
|---|---|---|
| HTTP API | OpenAPI 3.1 | [`openapi.yaml`](openapi.yaml) |
| JSON-RPC API | OpenRPC 1.2.6 | [`openrpc.json`](openrpc.json) |

每个接口对应的片段也会保留，方便审阅：

| API 类型 | 片段目录 |
|---|---|
| HTTP API | [`specs/http/`](https://github.com/tronprotocol/documentation-zh/tree/master/docs/api/specs/http) |
| JSON-RPC API | [`specs/json-rpc/`](https://github.com/tronprotocol/documentation-zh/tree/master/docs/api/specs/json-rpc) |

发布的定义来自 java-tron API 行为，并附带指向相应人类可读 API 文档的链接。顶层 `openapi.yaml` 和 `openrpc.json` 由各接口片段汇总生成，方便工具直接消费一个标准文件。
