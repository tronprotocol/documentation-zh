# /wallet/getburntrx

查询累计销毁的 TRX 数量（包括手续费、合约销毁等）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetBurnTrxServlet.java`
- Method：`GET` / `POST`
- 支持固化接口：`/walletsolidity/getburntrx`

## 请求参数

无。

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

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 节点内部异常（读取动态属性失败） | `{"Error": "<exceptionClass> : <message>"}` |
