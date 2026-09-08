# /wallet/validateaddress

校验地址格式合法性（hex / base58check / base64 自动识别）。**不查链**，只做编码 + checksum 校验。

- 源码：`framework/src/main/java/org/tron/core/services/http/ValidateAddressServlet.java`
- Method：`GET` / `POST`

## 请求参数

GET 从 URL 查询参数读取以下字段；POST 从 JSON 请求体读取。

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `address` | GET | string | 是 | 待校验地址，自动按长度判断格式：42 字符 hex / 34 字符 base58check / 28 字符 base64 |
| `address` | POST | string | 否 | 待校验地址；省略时返回 `result=false` 及异常信息（旧版 JVM 上该信息可能为 null） |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/validateaddress \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{ "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9" }
'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `result` | bool | 是否合法 |
| `message` | string | `Hex string format` / `Base58check format` / `Base64 format` / `Length error` / `Invalid address` |

响应示例：

```json
{ "result": true, "message": "Hex string format" }
```

### 异常响应

地址解析层错误（长度不符、checksum 错误、base58/base64 解码失败等）通过 `result=false` + `message` 表达，**不会**返回 `{"Error": ...}` 形态。

有两类失败不会进入常规的 `result=false` 响应：超限请求体可能在 servlet 运行前被共享 HTTP 层拒绝，而非法 JSON 会在 `doPost` 内失败。后者的异常只会被捕获并记录日志，因此客户端收到 **HTTP 200 + 空 body**：

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| POST | 请求体不是合法 JSON（POST） | 空响应（`JSON.parseObject` 抛 `org.tron.json.JSONException`，被 catch 后丢弃） |
