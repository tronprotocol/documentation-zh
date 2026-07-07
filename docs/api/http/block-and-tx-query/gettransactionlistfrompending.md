# /wallet/gettransactionlistfrompending

返回待打包池（pending）中所有交易的 ID 列表。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetTransactionListFromPendingServlet.java`
- Method：`GET` / `POST`
- Response：`api.TransactionIdList`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `visible` | bool | 否 | 无影响（响应无 bytes 字段） |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/gettransactionlistfrompending \
     --header 'accept: application/json'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `txId` | repeated string | 交易 ID hex 列表 |

响应示例：

```json
{
  "txId": [
    "7a265c89822d2dd9ee2187a728db3f273784943d588fd7b79ce972fc14a3f1de",
    "93347d947c339a2a7df588d3a96a003ec8745a4e0ee93a8074db3f1a754f21b5"
  ]
}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize`（POST） | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 节点内部异常（读取 pending 池失败） | `{"Error": "<exceptionClass> : <message>"}` |
