# /wallet/getReward

查询账户可领取的投票分红（未提取）。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetRewardServlet.java`
- Method：`GET` / `POST`
- 支持固化接口：`/walletsolidity/getReward`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `address` | string | 是 | 投票账户地址 |
| `visible` | bool | 否 | 无效果（servlet 通过 `41` 前缀自动识别地址格式，响应无 bytes 字段） |

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

提取使用 [`/wallet/withdrawbalance`](withdrawbalance.md)。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| `address` 解析失败（非法 hex / base58） | `{"Error": "INVALID address, <details>"}` |
| 请求体不是合法 JSON（POST） | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
