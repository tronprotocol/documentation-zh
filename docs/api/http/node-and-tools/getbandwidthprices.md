# /wallet/getbandwidthprices

获取历史带宽单价。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetBandwidthPricesServlet.java`
- Method：`GET` / `POST`
- Response：`api.PricesResponseMessage`
- 支持固化接口：`/walletsolidity/getbandwidthprices`

## 请求参数

无。

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getbandwidthprices \
     --header 'accept: application/json'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `prices` | string | 由 `,` 分隔的多条 `<生效时间戳>:<单价 sun>` 记录 |

响应示例：

```json
{
  "prices": "0:10,1606282800000:40,1612778400000:140,1625815200000:100,1626253800000:1000"
}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize`（POST） | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 节点内部异常（读取价格历史或序列化失败） | `{"Error": "<exceptionClass> : <message>"}` |
