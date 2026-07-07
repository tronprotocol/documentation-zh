# /wallet/listwitnesses

获取所有 SR 候选人列表。

- 源码：`framework/src/main/java/org/tron/core/services/http/ListWitnessesServlet.java`
- Method：`GET` / `POST`
- Response：`api.WitnessList`
- 支持固化接口：`/walletsolidity/listwitnesses`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `visible` | bool | 否 | 地址格式（响应中 `url` 为 proto `string`，不受 `visible` 影响） |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/listwitnesses \
     --header 'accept: application/json'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `witnesses` | repeated Witness | 候选人列表 |

`Witness`（`Tron.proto`）字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `address` | string | 候选人地址 |
| `voteCount` | int64 | 当前票数 |
| `pubKey` | string(hex) | 公钥 |
| `url` | string | 候选人 URL |
| `totalProduced` | int64 | 累计出块数 |
| `totalMissed` | int64 | 累计漏块数 |
| `latestBlockNum` | int64 | 最近出块高度 |
| `latestSlotNum` | int64 | 最近 slot |
| `isJobs` | bool | 是否当前 SR（前 27） |

响应示例（Nile 候选人共 800+ 个，仅截首项；`voteCount`、`latestBlockNum`、`latestSlotNum` 等随时间变化）：

```json
{
  "witnesses": [
    {
      "address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
      "voteCount": 2320142029,
      "url": "http://sr-15.com",
      "totalProduced": 1897834,
      "totalMissed": 252,
      "latestBlockNum": 66987961,
      "latestSlotNum": 592482103,
      "isJobs": true
    }
    /* ... 其余候选人 */
  ]
}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize`（POST） | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 节点内部异常（读取 Witness 存储失败） | `{"Error": "<exceptionClass> : <message>"}` |
