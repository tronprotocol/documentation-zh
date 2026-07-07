# /wallet/getReward

查询账户可领取的投票分红（未提取）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetRewardServlet.java`
- Method：`GET` / `POST`
- 支持固化接口：`/walletsolidity/getReward`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `address` | string | 否 | 投票账户地址；省略或为空时返回 `reward: 0` |
| `visible` | bool | 否 | 无影响（servlet 通过 `41` 前缀自动识别地址格式，响应无 bytes 字段） |
| `int64_as_string` | bool | 否 | 仅 GET；为 `true` 时将 `reward` 作为 JSON 字符串返回 |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getReward \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1"
}
'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `reward` | int64 | 单位 sun（1 TRX = 1e6 sun） |

响应示例（Nile，sr-15 当前累积分红，约 29994831 TRX）：

```json
{ "reward": 29994831460307 }
```

> 注意：`address` 缺失或为空时不会报错；`reward` 为 `0`（GET 使用 `int64_as_string=true` 时为 `"0"`）。

使用 GET 请求并添加 `?int64_as_string=true` 时：

```json
{ "reward": "29994831460307" }
```

提取使用 [`/wallet/withdrawbalance`](withdrawbalance.md)。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize`（POST） | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| `address` 解析失败（非法 hex / base58） | `{"Error": "INVALID address, <details>"}` |
| 请求体不是合法 JSON（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
