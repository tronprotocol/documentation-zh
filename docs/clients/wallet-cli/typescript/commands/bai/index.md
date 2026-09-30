# wallet-cli bai

查询 B.AI 的额度与用量，并用稳定币为 B.AI 账户充值。

## 用法

```
wallet-cli bai COMMAND
```

## 子命令

| 命令 | 页面 | 说明 |
|---|---|---|
| `bai usage-summary` | [usage-summary.md](usage-summary.md) | 额度余额、本月消耗与逐月趋势 |
| `bai usage-records` | [usage-records.md](usage-records.md) | 单条用量记录 |
| `bai recharge-orders` | [recharge-orders.md](recharge-orders.md) | 充值订单 |
| `bai recharge` | [recharge.md](recharge.md) | 为自己或他人的 B.AI 账户充值 |
| `bai report-recharge` | [report-recharge.md](report-recharge.md) | 重新上报一笔已有的充值交易，不再付款 |

## API key {#the-api-key}

每条命令都需要你个人的 B.AI API key。用 [`config`](../config.md) 保存一次即可，它从 stdin 读取该 key——这里取自 `$BAI_KEY` 环境变量：

```bash
printf '%s\n' "$BAI_KEY" | wallet-cli config baiApiKey --api-key-stdin
```

保存 key 只是写到本地：不需要网络、账户或 master password，也不会访问 B.AI，因此 key 是否正确要等到某条 `bai` 命令用到它时才会发现（`bai_auth_failed`）。

没有保存 key 时，所有 `bai` 命令都会以 `bai_credentials_missing` 停止（退出码 2）。

## 充值的过程

1. 可选地，`bai recharge --dry-run` 先预览这次充值：它会执行同样的检查（master password 除外），报告付款地址是否还需要绑定（`bindingRequired`），并显示将要支付的内容，但不做绑定、不创建订单、也不签名。
2. `bai recharge` 校验金额、网络、token、收款方和 master password，并向 B.AI 询问付款地址是否已绑定到你的 B.AI 账户。若尚未绑定，CLI 会用该账户对 B.AI 的绑定消息签名并完成绑定。其中任一步失败都会中止，不会产生订单，也不会付款。随后它创建订单，用你账户的一笔 x402 付款支付该订单，并把交易上报给 B.AI。
3. B.AI 确认后增加额度：`creditStatus: "credited"`。
4. 如果 B.AI 未能及时确认，命令仍然成功，返回 `creditStatus: "unconfirmed"` 和交易哈希。**款已经付出去了——不要再充一次。** 请改用 [`bai report-recharge`](report-recharge.md) 带上那个哈希重新上报。

## 另请参见

[`x402`](../x402/index.md) · [`config`](../config.md) · [x402 与 B.AI 的支付细节](../../machine-interface.md#x402-and-bai-payment-details)
