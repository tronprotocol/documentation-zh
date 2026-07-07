# /wallet/getchainparameters

获取所有链参数当前值。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetChainParametersServlet.java`
- Method：`GET` / `POST`
- Response：`protocol.ChainParameters`

## 请求参数

无（仅 `visible`）。

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getchainparameters \
     --header 'accept: application/json'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `chainParameter` | repeated {key, value} | 链参数键值列表 |

参数 key 对应提案中可设置的参数编号（如 `getMaintenanceTimeInterval`、`getEnergyFee` 等）。

响应示例（Nile，节选前 8 项；完整列表共 75 项）：

```json
{
  "chainParameter": [
    { "key": "getMaintenanceTimeInterval",        "value": 1800000 },
    { "key": "getAccountUpgradeCost",             "value": 9999000000 },
    { "key": "getCreateAccountFee",               "value": 100000 },
    { "key": "getTransactionFee",                 "value": 1000 },
    { "key": "getAssetIssueFee",                  "value": 1024000000 },
    { "key": "getWitnessPayPerBlock",             "value": 8000000 },
    { "key": "getWitnessStandbyAllowance",        "value": 100000000 },
    { "key": "getCreateNewAccountFeeInSystemContract", "value": 1000000 }
    /* ... 其余参数 */
  ]
}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize`（POST） | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 节点内部异常（读取 DynamicProperties 失败） | `{"Error": "<exceptionClass> : <message>"}` |
