# /wallet/getenergyprices

获取历史能量单价（每次提案变更后追加）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetEnergyPricesServlet.java`
- Method：`GET` / `POST`
- Response：`api.PricesResponseMessage`
- 支持固化接口：`/walletsolidity/getenergyprices`

## 请求参数

无。

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getenergyprices \
     --header 'accept: application/json'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `prices` | string | 由 `,` 分隔的多条 `<生效时间戳>:<单价 sun>` 记录，如 `0:100,1572597600000:10` |

响应示例：

```json
{
  "prices": "0:100,1572597600000:10,1606282800000:40,1612768800000:140,1612769400000:140,1612778400000:140,1628674200000:420,1635143400000:280,1669603800000:420,1726283400000:210,1754644200000:100"
}
```

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET / POST | 节点内部异常（读取价格历史或序列化失败） | `{"Error": "<exceptionClass> : <message>"}` |
