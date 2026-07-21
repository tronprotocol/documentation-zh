# /wallet/getnextmaintenancetime

获取下次 SR 维护期开始时间。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetNextMaintenanceTimeServlet.java`
- Method：`GET` / `POST`

## 请求参数

GET 和 POST 都从 URL 查询参数读取 `visible`；servlet 不解析 POST 请求体。`int64_as_string` 仅由 `RateLimiterServlet` 在 GET 请求中处理。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `visible` | GET / POST | bool | 否 | 输出格式；默认值为 `false` |
| `int64_as_string` | GET | bool | 否 | 为 `true` 时，以 JSON 字符串返回 `num` |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getnextmaintenancetime \
     --header 'accept: application/json'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `num` | int64 | 下次维护时间（毫秒时间戳） |

响应示例（`num` 随每个维护期结束而推进）：

```json
{ "num": 1777446600000 }
```

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET / POST | 节点内部异常 | `{"Error": "<exceptionClass> : <message>"}` |
