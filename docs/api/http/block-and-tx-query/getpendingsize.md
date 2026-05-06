# /wallet/getpendingsize

返回当前节点 pending 池中的交易数量。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetPendingSizeServlet.java`
- Method：`GET` / `POST`

## 请求参数

无。

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

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 节点内部异常（读取 pending 池失败） | `{"Error": "<exceptionClass> : <message>"}` |
