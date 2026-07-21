# /wallet/getpendingsize

返回当前节点 pending 池中的交易数量。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetPendingSizeServlet.java`
- Method：`GET` / `POST`

## 请求参数

POST 没有请求参数，也不解析请求体。GET 接受以下 URL 查询参数：

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `int64_as_string` | GET | bool | 否 | 为 `true` 时，以 JSON 字符串返回 `pendingSize` |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getpendingsize \
     --header 'accept: application/json'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `pendingSize` | int64 | pending 池交易数 |

响应示例：

```json
{ "pendingSize": 2 }
```

使用 GET 请求并添加 `?int64_as_string=true` 时：

```json
{ "pendingSize": "2" }
```

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET / POST | 节点内部异常（读取 pending 池失败） | `{"Error": "<exceptionClass> : <message>"}` |
