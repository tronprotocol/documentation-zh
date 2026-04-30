# /wallet/getaccountresource

查询账户的带宽（Net）+ 能量（Energy）+ TronPower 资源使用情况。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetAccountResourceServlet.java`
- Method：`GET` / `POST`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `address` | string | 是 | 账户地址 |
| `visible` | bool | 否 | 地址格式 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getaccountresource \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
}
'
```

## 响应

返回 `api.AccountResourceMessage`（`api.proto`）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `freeNetUsed` / `freeNetLimit` | int64 | 免费带宽（每 24h 重置） |
| `NetUsed` / `NetLimit` | int64 | 质押带宽 |
| `assetNetUsed` / `assetNetLimit` | map | TRC10 各自带宽 |
| `TotalNetLimit` / `TotalNetWeight` | int64 | 全网带宽配额、全网质押 |
| `EnergyUsed` / `EnergyLimit` | int64 | 能量 |
| `TotalEnergyLimit` / `TotalEnergyWeight` | int64 | 全网能量配额、全网质押 |
| `tronPowerUsed` / `tronPowerLimit` | int64 | 投票权 |
| `TotalTronPowerWeight` | int64 | 全网投票权总量 |
| `storageUsed` / `storageLimit` | int64 | 存储（已不使用） |

响应示例：

```json
{
  "freeNetUsed": 441,
  "freeNetLimit": 600,
  "assetNetUsed": [
    { "key": "1005416", "value": 0 }
  ],
  "assetNetLimit": [
    { "key": "1005416", "value": 10000 }
  ],
  "TotalNetLimit": 43200000000,
  "TotalNetWeight": 68305209098,
  "TotalEnergyLimit": 180000000000,
  "TotalEnergyWeight": 2411528185
}
```

`address` 缺失或对应账户不存在均返回 `{}`。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize`（POST） | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `address` 不是合法 hex（`visible=false`） | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : exception decoding Hex string: <详情>"}` |
| `address` 不是合法 base58check（`visible=true`） | `{"Error": "class java.lang.IllegalArgumentException : <详情>"}` |
| 请求体不是合法 JSON / 字段类型不符（POST） | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
