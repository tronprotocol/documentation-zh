# /wallet/getaccount

查询账户信息。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetAccountServlet.java`
- Method：`GET` / `POST`
- 支持固化接口：`/walletsolidity/getaccount`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `address` | string | 是 | 账户地址；`visible=false` 为 hex（21 字节，0x41 前缀），`visible=true` 为 base58check |
| `visible` | bool | 否 | 地址、文本字段格式 |

POST 示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getaccount \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
}
'
```

## 响应

返回 `protocol.Account`（见 `protocol/src/main/protos/core/Tron.proto:132`）。常用字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `address` | bytes | 账户地址 |
| `account_name` | bytes | 账户昵称 |
| `type` | enum | `Normal` / `AssetIssue` / `Contract` |
| `balance` | int64 | TRX 余额（sun，1 TRX = 1e6 sun） |
| `create_time` | int64 | 创建时间，毫秒 |
| `votes` | repeated Vote | 投票记录 |
| `frozen` | repeated Frozen | Stake 1.0 冻结（带宽） |
| `frozenV2` | repeated FreezeV2 | Stake 2.0 冻结 |
| `unfrozenV2` | repeated UnFreezeV2 | Stake 2.0 解冻中 |
| `account_resource` | AccountResource | 能量相关 |
| `asset` / `assetV2` | map\<string,int64\> | 持有的 TRC10 |
| `allowance` | int64 | 见证人未提取奖励 |
| `latest_opration_time` | int64 | 最近一次操作时间 |
| `owner_permission` / `witness_permission` / `active_permission` | Permission | 权限配置 |

响应示例：

```json
{
  "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "balance": 1793227200,
  "create_time": 1776933207000,
  "latest_opration_time": 1777444809000,
  "free_net_usage": 441,
  "latest_consume_free_time": 1777431471000,
  "net_window_size": 28800000,
  "net_window_optimized": true,
  "account_resource": {
    "latest_consume_time_for_energy": 1777444809000,
    "energy_window_size": 28800000,
    "energy_window_optimized": true
  },
  "owner_permission": {
    "permission_name": "owner",
    "threshold": 1,
    "keys": [
      { "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9", "weight": 1 }
    ]
  },
  "active_permission": [
    {
      "type": "Active",
      "id": 2,
      "permission_name": "active",
      "threshold": 1,
      "operations": "7fff1fc0033efb0f000000000000000000000000000000000000000000000000",
      "keys": [
        { "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9", "weight": 1 }
      ]
    }
  ],
  "frozenV2": [
    {},
    { "type": "ENERGY" },
    { "type": "TRON_POWER" }
  ],
  "assetV2": [
    { "key": "1005416", "value": 100000000 }
  ],
  "free_asset_net_usageV2": [
    { "key": "1005416", "value": 0 }
  ],
  "asset_optimized": true
}
```

账户不存在返回 `{}`。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize`（POST） | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `address` 缺失 | `{"Error": "class java.lang.NullPointerException : <message>"}` |
| `address` 不是合法 base58check（`visible=true`） | `{"Error": "class java.lang.IllegalArgumentException : <message>"}`（GET）；`{"Error": "class java.lang.NullPointerException : <message>"}`（POST） |
| `address` 不是合法 hex（`visible=false`） | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}`（GET）；`{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}`（POST） |
| 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
