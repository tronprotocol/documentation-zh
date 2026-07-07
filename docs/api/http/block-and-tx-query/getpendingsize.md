# /wallet/getpendingsize

返回当前节点 pending 池中的交易数量。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetPendingSizeServlet.java`
- Method：`GET` / `POST`

## 请求参数

无。

GET 请求可在 URL 查询参数中添加 `int64_as_string=true`，使 `pendingSize` 以 JSON 字符串返回。

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

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize`（POST） | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 节点内部异常（读取 pending 池失败） | `{"Error": "<exceptionClass> : <message>"}` |
