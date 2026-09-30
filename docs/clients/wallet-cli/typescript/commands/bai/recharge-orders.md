# wallet-cli bai recharge-orders

列出 B.AI 的充值订单。

## 用法

```
wallet-cli bai recharge-orders [--limit <n>] [--offset <n>] [--sort <asc|desc>] [options]
```

## 说明

列出该 API key 所属 B.AI 账户的充值订单，包括由 [`bai recharge`](recharge.md) 创建的那些。不需要钱包，也不需要密码。

需要先用 [`config baiApiKey`](../config.md) 保存 B.AI API key；见 [`bai`](index.md#the-api-key)。

## 选项

| 选项 | 说明 |
|---|---|
| `--limit <n>` | 每页行数，1–200（默认 `20`）；B.AI 最多返回 100 条，因此更大的值会被降到 `100` 并给出警告 |
| `--offset <n>` | 跳过的行数（默认 `0`） |
| `--sort <asc\|desc>` | 按创建时间排序（默认 `desc`） |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli bai recharge-orders --limit 2
```

```console
B.AI recharge orders
  orders:
    1.
      can Download Invoice: Yes
      chain Key: tron
      created At: 1,782,986,861
      currency: USDT
      id: 31,207
      payment Method: TRON
      points: 1,000,000
      quantity Display: 1
      recharge Type: crypto
      recipient Display Label: Not available
      recipient Relation: self
      status: success
      team Id: Not available
      transaction Id: 5d1e8f3a7c2b90e4f6a18d3c5b7e9f02a4c6e8b1d3f5a7c9e2b4d6f8a0c1e3b5
      type: purchase
    2.
      bonus Type: rebate
      chain Key: Not available
      created At: 1,782,986,861
      currency: -
      id: 351,872
      payment Method: -
      points: 500,000
      quantity Display: -
      recharge Type: bonus
      status: expired
      transaction Id: -
      type: bonus
  pagination:
    offset: 0
    limit: 2
    total: 6
```

```bash
wallet-cli bai recharge-orders --limit 2 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"bai.recharge-orders","data":{"orders":[{"canDownloadInvoice":true,"chainKey":"tron","createdAt":1782986861,"currency":"USDT","id":31207,"paymentMethod":"TRON","points":1000000,"quantityDisplay":"1","rechargeType":"crypto","recipientDisplayLabel":null,"recipientRelation":"self","status":"success","teamId":null,"transactionId":"5d1e8f3a7c2b90e4f6a18d3c5b7e9f02a4c6e8b1d3f5a7c9e2b4d6f8a0c1e3b5","type":"purchase"},{"bonusType":"rebate","chainKey":null,"createdAt":1782986861,"currency":"-","id":351872,"paymentMethod":"-","points":500000,"quantityDisplay":"-","rechargeType":"bonus","status":"expired","transactionId":"-","type":"bonus"}]},"meta":{"durationMs":2456,"warnings":[],"pagination":{"offset":0,"limit":2,"total":6}}}
```

第一条订单是在 TRON 上支付的 1 USDT 充值：`points` 是它增加的额度，`transactionId` 是付款交易。第二条是随之产生的返利赠送，创建于同一时刻。`createdAt`（文本中为 `created At`）是以秒计的 Unix 时间戳，`total` 统计的是全部订单，含赠送在内。JSON 输出中，分页信息在 `meta.pagination` 里。

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `orders[]` | array | B.AI 返回的订单原样给出，默认按时间倒序——其中包括 `id`、`type`（充值为 `purchase`，随充值产生的返利为 `bonus`）、`status`、`currency`、`quantityDisplay`（支付金额）、`points`（增加的额度）、`chainKey`、`transactionId`、`createdAt`（Unix 秒） |

分页信息在 `meta.pagination` 中：`offset`、`limit`（若被降到 `100`，这里是降后的值），以及 `total`（全部订单，含赠送）。`--offset` 超过最后一条订单时返回空列表。

## 退出码

`0` 成功 · `1` 执行失败（`bai_auth_failed`；`bai_rejected`；`provider_error`；`timeout`） · `2` 用法错误（`bai_credentials_missing`；`invalid_value`——`--limit` 或 `--offset` 越界）。

## 另请参见

[`bai recharge`](recharge.md) · [`bai usage-records`](usage-records.md)
