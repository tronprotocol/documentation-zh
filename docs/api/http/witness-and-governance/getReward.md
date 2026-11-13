# /wallet/getReward

查询账户可领取的奖励总额，单位为 sun。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetRewardServlet.java`
- Method：`GET` / `POST`
- 支持固化接口：`/walletsolidity/getReward`

## 请求参数

GET 从 URL 查询读取 `address`；POST 从 JSON 请求体读取。`visible` 被忽略。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `address` | GET / POST | string | 否 | 账户地址（投票者或 SR）；省略或为空时返回 `reward: 0` |
| `visible` | GET / POST | bool | 否 | 无影响（servlet 通过 `41` 前缀自动识别地址格式，响应无 bytes 字段） |
| `int64_as_string` | GET | bool | 否 | 仅 GET；为 `true` 时将 `reward` 作为 JSON 字符串返回 |

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
| `reward` | int64 | 可领取的奖励总额；单位 sun（1 TRX = 1e6 sun） |

响应示例（Nile，sr-15 当前累计奖励，约 29994831 TRX）：

```json
{ "reward": 29994831460307 }
```

> 地址缺失或为空，以及 Base58Check 地址因长度、校验和或解码后地址不合法而被拒绝时，均返回零奖励。这与账户没有可领取奖励时的响应无法区分。使用结果前请先验证地址；解析器异常见下方错误表。

使用 GET 请求并添加 `?int64_as_string=true` 时：

```json
{ "reward": "29994831460307" }
```

提取使用 [`/wallet/withdrawbalance`](withdrawbalance.md)。

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET / POST | Hex 解码抛出异常，或 Base58 解码抛出异常（例如长度符合要求的地址中含有非法字符） | `{"Error": "INVALID address, <详情>"}` |
| GET / POST | Base58Check 地址长度或校验和错误，或解码后的地址不合法 | `{"reward": 0}`（GET 使用 `int64_as_string=true` 时为 `{"reward": "0"}`） |
| POST | 请求体不是合法 JSON（POST） | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
