# /wallet/listnodes

列出节点已发现的对等节点。

- 源码：`framework/src/main/java/org/tron/core/services/http/ListNodesServlet.java`
- Method：`GET` / `POST`
- 别名路径：`/net/listnodes`
- Response：`api.NodeList`

## 请求参数

GET 和 POST 都从 URL 查询参数读取以下字段；servlet 不解析 POST 请求体。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `visible` | GET / POST | bool | 否 | 文本字段格式（仅影响 `Address.host`：`true` 输出 UTF-8 IP 字符串，默认/`false` 输出 hex 字节） |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/listnodes \
     --header 'accept: application/json'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `nodes` | repeated Node | 已知节点 |
| `nodes[].address.host` | string | IP 地址；`visible=true` 为 UTF-8 文本（如 `"176.9.148.236"`），否则为对应字节的 hex（如 `"3137362e392e3134382e323336"`） |
| `nodes[].address.port` | int32 | 端口 |

响应示例（默认；以下截取前 3 项，实际响应包含数十个节点）：

```json
{
  "nodes": [
    { "address": { "host": "3137362e392e3134382e323336", "port": 18888 } },
    { "address": { "host": "35382e3133362e3130332e3833", "port": 18889 } },
    { "address": { "host": "31352e3233352e3233332e313239", "port": 18888 } }
  ]
}
```

响应示例（`visible=true`，相同节点对应的 UTF-8 输出）：

```json
{
  "nodes": [
    { "address": { "host": "176.9.148.236", "port": 18888 } },
    { "address": { "host": "58.136.103.83", "port": 18889 } },
    { "address": { "host": "15.235.233.129", "port": 18888 } }
  ]
}
```

> 公共网关（`nile.trongrid.io`）不会透传 POST body 中的 `visible` 字段，因此通过它请求时 `host` 始终为 hex；如需 UTF-8 形式，需在自有节点直接访问。

无节点时返回 `{}`。

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET / POST | 节点内部异常（拉取节点列表或序列化失败） | `{"Error": "<exceptionClass> : <message>"}` |
