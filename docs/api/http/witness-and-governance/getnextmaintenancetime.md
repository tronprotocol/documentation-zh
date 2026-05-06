# /wallet/getnextmaintenancetime

获取下次 SR 维护期开始时间。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetNextMaintenanceTimeServlet.java`
- Method：`GET` / `POST`

## 请求参数

无（仅 `visible`）。

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getnextmaintenancetime \
     --header 'accept: application/json'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `num` | int64 | 下次维护时间（毫秒时间戳） |

响应示例（`num` 随每个维护期结束而推进）：

```json
{ "num": 1777446600000 }
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 节点内部异常 | `{"Error": "<exceptionClass> : <message>"}` |
