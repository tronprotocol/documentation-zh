# /wallet/validateaddress

校验地址格式合法性（hex / base58check / base64 自动识别）。**不查链**，只做编码 + checksum 校验。

- 源码：`framework/src/main/java/org/tron/core/services/http/ValidateAddressServlet.java`
- Method：`GET` / `POST`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `address` | string | 是 | 待校验地址，自动按长度判断格式：42 字符 hex / 34 字符 base58check / 28 字符 base64 |

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

但 `doPost` 在 `validAddress` **之前**还有两步会抛异常，且 servlet 的外层 `catch (Exception e)` 只 `logger.debug` 不写响应体——客户端会收到 **HTTP 200 + 空 body**：

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.http.maxMessageSize`（POST） | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| 请求体不是合法 JSON（POST） | 空响应（`JSON.parseObject` 抛 `org.tron.json.JSONException`，被 catch 后丢弃） |

GET 路径不读 body，上面两种情况只在 POST 触发。
