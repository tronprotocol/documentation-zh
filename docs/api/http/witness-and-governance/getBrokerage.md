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

> 地址缺失或为空，以及 Base58Check 地址因长度、校验和或解码后地址不合法而被拒绝时，均返回 `{"brokerage": 0}`。这与合法地址的佣金比例为零时的响应无法区分。使用结果前请先验证地址；解析器异常见下方错误表。

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET / POST | `address` 以 `41` 开头但不是合法 hex | `{"Error": "INVALID address, <hex 解析器信息>"}` |
| GET / POST | Base58 解码抛出异常（例如长度符合要求的地址中含有非法字符） | `{"Error": "INVALID address, <base58 解析器信息>"}` |
| GET / POST | Base58Check 地址长度或校验和错误，或解码后的地址不合法 | `{"brokerage": 0}` |
| POST | POST 体不是合法 JSON | `{"Error": "class org.tron.json.JSONException : <解析器信息>"}` |
| GET / POST | 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
