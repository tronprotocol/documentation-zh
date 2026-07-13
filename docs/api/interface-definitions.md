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

## HTTP 带内错误扩展

HTTP 接口可能以状态码 200 返回成功对象或错误对象。JSON 响应 schema 使用 `x-tron-in-band-error` 描述消费者如何区分这两种情况。

如果存在 `errors` 数组，它就是描述接口特定业务错误的规范结构。如果该数组不存在，消费者必须回退使用 `errorSchema`、`discriminatorField` 和顶层 `sources`。业务错误条目包含 `responsePath`、`discriminatorPath`、`failureCondition` 和 `sources`。Java 错误条目标识 `JavaTronError` schema，并使用 `$.Error` 作为判别路径。当任意业务错误条目匹配时，该操作即视为业务失败。

支持以下 `failureCondition` 形式：

- `equals <value>`：判别字段存在，并且等于指定的 JSON 标量值或枚举标记。
- `missing or equals <value>`：字段不存在，或者字段存在且等于指定值。JSON `null` 不视为字段不存在。
- `field exists and is not <value>`：字段存在，并且不等于指定值。缺失的 proto3 默认值字段不会匹配。

判别路径使用 JSONPath 子集：`$`、以点分隔的对象成员，以及 `[0]` 形式的从零开始的数组索引。

当前所有 `x-tron-in-band-error` 条目都保留 `errorSchema`、`discriminatorField` 和顶层 `sources`。具有接口特定业务错误的操作还会提供 `errors`。这些旧字段仅描述 `JavaTronError` 分支；接口特定业务失败仅通过 `errors` 表示。
