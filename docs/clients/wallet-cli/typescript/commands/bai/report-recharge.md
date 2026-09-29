# wallet-cli bai report-recharge

把一笔已有的充值交易重新上报给 B.AI，不再付款。

## 用法

```
wallet-cli bai report-recharge <txHash> --chain <tron|bnb|base> [--amount <n>] [--to <identifier> --target-id <id>] [options]
```

## 说明

这是 [`bai recharge`](recharge.md) 已经付款、但以 `creditStatus: "unconfirmed"` 结束之后的补救步骤。它把交易哈希再次发给 B.AI，以便加上额度。它不创建订单、不签名、也不付款；交易能否入账由 B.AI 判定。不需要钱包，也不需要密码。

请给出原始充值时的各项值：

- 同一个 API key；
- `--chain`——付款所在的链（BSC 用 `bnb`）；
- `--amount`，如果你还留着的话；
- 如果当初是给他人充值，需**同时**给出原始的 `--to` 和其 `rechargeTarget` 中的 `targetId`。本命令不会重新解析收款方。为自己的账户充值时，两者都不用给。

哈希在 TRON 上必须是 64 个 hex 字符，在 BSC 和 Base 上必须是 `0x` 加 64 个 hex 字符。

交易只上报一次；CLI 不会重试。当 B.AI 还找不到该交易、或正在对客户端限流时，命令仍然成功，返回 `creditStatus: "unconfirmed"` 和一个 `code` / `warning`（限流时若 B.AI 发来 `Retry-After`，还会带上 `error.details.retryAfterMs`）；稍后再执行一次即可。不要再充一次。重复上报一笔已经入账的交易是安全的：它会再次返回 `credited`，不会重复加额度。

需要先用 [`config baiApiKey`](../config.md) 保存 B.AI API key；见 [`bai`](index.md#the-api-key)。

## 参数

- `txHash`——原始充值的付款交易

## 选项

| 选项 | 说明 |
|---|---|
| `--chain <tron\|bnb\|base>` | **必填。** 原始充值所在的链 |
| `--amount <n>` | 原始金额，以 token 为单位（可含小数） |
| `--to <identifier>` | 原始收款方的邮箱或地址；必须与 `--target-id` 同用 |
| `--target-id <id>` | 原始的 `rechargeTarget.confirmedTarget.targetId`；必须与 `--to` 同用 |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

上报一笔在 TRON 上支付的 1 USDT 充值：

```bash
wallet-cli bai report-recharge 3f7a9c2e1b8d4f60a5c3e7b9d1f2a4c6e8b0d3f5a7c9e1b2d4f6a8c0e2b4d6f8 --chain tron --amount 1
```

```console
✅ B.AI recharge credited
  chain: tron
  tx Hash: 3f7a9c2e1b8d4f60a5c3e7b9d1f2a4c6e8b0d3f5a7c9e1b2d4f6a8c0e2b4d6f8
  amount: 1
  retry Payment: No
  credit Status: credited
  order:
    can Download Invoice: No
    chain Key: tron
    created At: 1,789,569,840
    currency: USDT
    id: 31,215
    payment Method: TRON
    points: 1,000,000
    quantity Display: 1
    recharge Type: crypto
    recipient Display Label: Not available
    recipient Relation: self
    status: success
    team Id: Not available
    transaction Id: 3f7a9c2e1b8d4f60a5c3e7b9d1f2a4c6e8b0d3f5a7c9e1b2d4f6a8c0e2b4d6f8
    type: purchase
```

```bash
wallet-cli bai report-recharge 3f7a9c2e1b8d4f60a5c3e7b9d1f2a4c6e8b0d3f5a7c9e1b2d4f6a8c0e2b4d6f8 --chain tron --amount 1 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"bai.report-recharge","data":{"chain":"tron","txHash":"3f7a9c2e1b8d4f60a5c3e7b9d1f2a4c6e8b0d3f5a7c9e1b2d4f6a8c0e2b4d6f8","amount":"1","retryPayment":false,"creditStatus":"credited","order":{"canDownloadInvoice":false,"chainKey":"tron","createdAt":1789569840,"currency":"USDT","id":31215,"paymentMethod":"TRON","points":1000000,"quantityDisplay":"1","rechargeType":"crypto","recipientDisplayLabel":null,"recipientRelation":"self","status":"success","teamId":null,"transactionId":"3f7a9c2e1b8d4f60a5c3e7b9d1f2a4c6e8b0d3f5a7c9e1b2d4f6a8c0e2b4d6f8","type":"purchase"}},"meta":{"durationMs":972,"warnings":[]}}
```

`credited`（标题为 `B.AI recharge credited`）表示 B.AI 已把该交易与它的订单对上，订单内容见 `order`。重复上报一笔已经入账的交易会返回同样的结果，不会重复加额度。

上报一笔 B.AI 无法核验的交易——这里是一笔从来就不是 B.AI 充值的普通 TRX 转账——同样以 `0` 退出。它返回 `creditStatus: unconfirmed`（标题为 `B.AI credit not confirmed`）并给出原因：

```bash
wallet-cli bai report-recharge 54a7315953ded3b8565cf36973cb56fa3d65f63eccb86aaf1033f28d2bdea01a --chain tron
```

```console
⚠️ B.AI credit not confirmed — reconcile before paying again
  chain: tron
  tx Hash: 54a7315953ded3b8565cf36973cb56fa3d65f63eccb86aaf1033f28d2bdea01a
  retry Payment: No
  credit Status: unconfirmed
  code: TX_NOT_FOUND_OR_INVALID
  warning: B.AI could not verify the transaction. Check confirmation, chain, recipient and sender; do not pay again
```

```bash
wallet-cli bai report-recharge 54a7315953ded3b8565cf36973cb56fa3d65f63eccb86aaf1033f28d2bdea01a --chain tron -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"bai.report-recharge","data":{"chain":"tron","txHash":"54a7315953ded3b8565cf36973cb56fa3d65f63eccb86aaf1033f28d2bdea01a","retryPayment":false,"creditStatus":"unconfirmed","code":"TX_NOT_FOUND_OR_INVALID","warning":"B.AI could not verify the transaction. Check confirmation, chain, recipient and sender; do not pay again"},"meta":{"durationMs":69635,"warnings":[]}}
```

请核对交易哈希和 `--chain`，稍后再上报一次。不要重复付款。

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `creditStatus` | string | `credited` 或 `unconfirmed` |
| `txHash` / `chain` / `amount` | string | 所上报的内容；`amount` 仅在给出时才有 |
| `rechargeTarget` | object | 使用 `--to` / `--target-id` 时：所上报的收款方 |
| `retryPayment` | boolean | 恒为 `false` |
| `order` | object | `credited` 时：B.AI 返回的订单原样给出 |
| `code` / `warning` / `error` | string / string / object | `unconfirmed` 时：未能确认的原因，例如 `code: TX_NOT_FOUND_OR_INVALID` |

## 退出码

`0` 已上报——**请检查 `creditStatus`**：上报失败（包括 key 被拒或 B.AI 不可达）同样以 `0` 退出，返回 `unconfirmed`，失败原因在 `code` / `error` 中 · `2` 用法错误（`bai_credentials_missing`；`invalid_value`——哈希与该链的格式不符，或 `--to` 与 `--target-id` 只给了一个；`invalid_amount`——`--amount` 不是正数金额）。

## 另请参见

[`bai recharge`](recharge.md) · [`bai recharge-orders`](recharge-orders.md)
