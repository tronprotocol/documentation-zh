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

## OpenRPC 错误目录扩展

顶层 `x-tron-error-model` 与每个 method 的 `x-tron-error-catalog` 在不改变 JSON-RPC 线上格式及源码派生 OpenRPC `errors` 数组的前提下，补充稳定的错误分类和重试指引。

每个 method catalog 链接都包含 `errorIndex`。它是该 method `errors` 数组的从零开始的索引；关联的 `catalogId` 指向 `x-tron-error-model.catalog` 中的对应条目。method catalog 为空表示该 method 没有源码声明的错误，但 `sharedCatalogIds` 中与 method 无关的失败仍然适用。

按以下顺序对响应分类：

1. 先评估 `sharedCatalogIds` 引用的可执行匹配，包括协议/servlet 失败以及普通 JSON-RPC envelope 之外的传输响应。
2. 如果已知调用的 method，则通过其 `x-tron-error-catalog` 链接限定候选项，并匹配 `code` 或已记录的 message 前缀等可观测线上字段。
3. 如果同一线上响应仍匹配多个候选项——尤其是重用的 `-32000` 和 `-32005` 错误码——则使用 `ambiguousCodeFallback`：`retryable: false` 且 `retryClass: UNKNOWN`。

`sourceException` 和 `sourceMessage` 是从 java-tron 源码声明派生的解释性元数据。它们不保证出现在 `error.message`、`error.data` 或其它任何线上字段中，不得作为运行时匹配条件。其中 `<underlying exception message>` 是源码描述占位符，不是字面响应值。

`retryable: true` 特指允许自动重试同一逻辑操作。`AFTER_STATE_CHANGE`、`AFTER_REQUEST_REBUILD` 或 `VERIFY_BEFORE_RETRY` 等有条件的重试类别仍为 `retryable: false`；客户端只能在满足该类别声明的前置条件后再次尝试。`UNKNOWN` 同样禁止自动重试。

该目录包含 java-tron 生成的稳定协议、servlet 和 HTTP 响应。连接失败、超时以及没有稳定响应契约的通用 I/O 失败，仍属于客户端传输错误。
