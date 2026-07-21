# /wallet/getBrokerage

查询 SR 当前周期的分红比例（佣金）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetBrokerageServlet.java`
- Method：`GET` / `POST`
- 支持固化接口：`/walletsolidity/getBrokerage`

## 请求参数

GET 从 URL 查询读取 `address`；POST 从 JSON 请求体读取。`visible` 被忽略。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `address` | GET / POST | string | 否 | SR 地址；省略或为空时返回 `brokerage: 0` |
| `visible` | GET / POST | bool | 否 | 无影响（servlet 通过 `41` 前缀自动识别地址格式，响应无 bytes 字段） |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getBrokerage \
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
| `brokerage` | int | 百分比（0–100），默认 20 |

响应示例（Nile，sr-15）：

```json
{ "brokerage": 100 }
```

> 注意：`address` 字段缺失或为空时不报错，直接返回 `{"brokerage": 0}`——与"该 SR 当前佣金为 0"响应完全一致，调用方需自行区分。

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET / POST | `address` 以 `41` 开头但不是合法 hex | `{"Error": "INVALID address, <hex 解析器信息>"}` |
| GET / POST | `address` 不是合法 base58check | `{"Error": "INVALID address, <base58 校验信息>"}` |
| POST | POST 体不是合法 JSON | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
