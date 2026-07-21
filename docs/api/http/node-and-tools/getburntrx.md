# /wallet/getburntrx

查询累计销毁的 TRX 数量（包括手续费、合约销毁等）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetBurnTrxServlet.java`
- Method：`GET` / `POST`
- 支持固化接口：`/walletsolidity/getburntrx`

## 请求参数

POST 没有请求参数，也不解析请求体。GET 接受以下 URL 查询参数：

| 字段 | 方法 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| `int64_as_string` | GET | bool | 否 | 为 `true` 时，以 JSON 字符串返回 `burnTrxAmount` |

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getburntrx \
     --header 'accept: application/json'
```

## 响应

`burnTrxAmount` 单位为 sun。

响应示例：

```json
{ "burnTrxAmount": 153731208869910 }
```

使用 GET 请求并添加 `?int64_as_string=true` 时：

```json
{ "burnTrxAmount": "153731208869910" }
```

### 异常响应

| 方法 | 触发条件 | 响应 |
|---|---|---|
| GET / POST | 请求体超过 `node.http.maxMessageSize` | 通常由 `SizeLimitHandler` 返回 HTTP 413 `Payload Too Large` |
| GET / POST | 节点内部异常（读取动态属性失败） | `{"Error": "<exceptionClass> : <message>"}` |
