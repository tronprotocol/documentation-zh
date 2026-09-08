# wallet-cli asset participate

用 TRX 参与某个 TRC10 的 ICO。

## 用法

```
wallet-cli asset participate <asset> --pay <trx>
                             [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]]
                             [--permission-id <n>] [options]
```

## 说明

在募集窗口内，按 token 发行时设定的固定比率从其发行中买入。这是参与 ICO，而不是市场交易——token 出自发行方的剩余供应量，价格没有商量余地。发行方地址由 token 自动解析得到，因此无需另行传入。

**`--pay` 表示支付的 TRX，而不是收到的 token 数量。** 收到的数量按 `floor(pay × tokens ÷ trx)` 计算，其中 `trx:tokens` 是 token 发行时设定的比率。链上采用整数先乘后除，因此结果会向下取整。支付的 TRX 会全额转出，取整产生的余数不会退还。

取整损失小于一个 **token 最小单位**。链上使用 `trxNum:num` 数对记录最小单位的价格，即 `trxNum` SUN 可购买 `num` 个最小单位，因此舍去的金额小于 `trxNum ÷ num` SUN。对于 `--price 1:100 --precision 6`，上限仅为 0.01 SUN；对于 `--price 1:100 --precision 0`，数对会约分为 `10000:1`，最坏情况下会舍去 9,999 SUN。如果 `--pay` 小到无法购买一个最小单位，命令会在本地报错，不会广播交易。

执行操作的账户不能是该 token 自己的发行方。

**该命令默认在交易提交后返回**（`stage: "submitted"`），不会等待确认。使用 `--wait` 可阻塞至交易确认或失败。命令需要一个账户；仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回 `watch_only_no_signer`。

Ledger 的 TRON 应用无法对 TRC10 发行类合约签名。Ledger 账户可以做试运行或构建未签名的 hex，但签名模式会在与设备交互之前就以 `ledger_unsupported` 失败。

## 选项

| 选项 | 说明 |
|---|---|
| `<asset>` | **必填。** token id 或名称；全数字的值按 id 解析 |
| `--pay <trx>` | **必填。** 要花费的 TRX（不是 token 数量），> 0 |
| `--dry-run` | 只构建和估算，不签名/不广播；与 `--sign-only` / `--build-only` 互斥 |
| `--sign-only` | 只签名不广播，输出已签名的 hex；与 `--dry-run` / `--build-only` 互斥；配合 `--expiration` 使用 |
| `--build-only` | 构建并估算，输出**未签名**的 hex；与 `--dry-run` / `--sign-only` 互斥；配合 `--expiration` 使用 |
| `--expiration <ms>` | 交易过期时间（毫秒），最大 `86400000`（24 小时）；仅可与 `--sign-only` 或 `--build-only` 同用；省略时使用节点默认值（约 60 秒） |
| `--permission-id <n>` | 用于签名的权限组（0=owner，1=witness，2-9=active）；默认 `0` |
| `--wait` / `--wait-timeout <ms>` | 广播后轮询直到已确认/失败（上限默认取配置 `waitTimeoutMs`，内置 60000） |
| `--password-stdin` | 从 stdin（fd 0）读取 master password |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

示例中的 `$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入。

在一个按 `1:100` 发行的 token 上花费 100 TRX：

```bash
echo "$PW" | wallet-cli asset participate 1000124 --pay 100 --network tron:3448148188 --wait --password-stdin
```

```console
✅ Participated in ICO
  Asset        BetaToken  (id 1000124)
  Issuer       TBeta9mR...8pLx
  Participant  TQkXm4vN...5Zt7Uw
  Paid         100 TRX
  Received     10,000 BetaToken
  TxID         4c8...
  Block        #57,883,402
  Fee          0 TRX
  Status       success
```

```bash
echo "$PW" | wallet-cli asset participate 1000124 --pay 100 --network tron:3448148188 --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"asset.participate","data":{"kind":"asset-participate","stage":"confirmed","txId":"4c8...","confirmed":true,"blockNumber":57883402,"feeSun":0,"netUsed":301,"netFeeSun":0,"failed":false,"assetId":"1000124","name":"BetaToken","issuerAddress":"TBeta9mR...","participantAddress":"TQkXm4vN...","paidSun":"100000000","receivedAmount":"10000000000","precision":6},"meta":{"durationMs":6450,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交） | `kind: "asset-participate"`、`stage: "submitted"`、`txId`、`assetId`、`name`、`issuerAddress`、`participantAddress`、`paidSun`、`receivedAmount` |
| `--wait`（已确认） | 以上内容，外加 `stage: "confirmed"`、`confirmed`（boolean）、`blockNumber`、返回时的扁平结算字段（`feeSun`、`energyUsed`、`netUsed`、`energyFeeSun`、`netFeeSun`）、`failed` |

`paidSun` 是花费的 TRX，以 sun 计；`receivedAmount` 是 token 数量，以其最小单位计。两者都是十进制字符串；结果中还包含 `precision`，供 text 输出和程序消费方换算 token 数量。

## 退出码

`0` 已提交（早退模式下为已构建/已签名） · `1` 执行失败（`asset_not_found`——没有这个 token；`not_in_ico_window`——不在募集窗口内；`self_participation`——这个 token 是你自己发行的；`transaction_rejected`——节点拒绝了它，例如余额不足以支付 `--pay`；`watch_only_no_signer`；`ledger_unsupported`；`auth_failed`） · `2` 用法错误（`missing_option`——没有给 `--pay`；`invalid_amount`——`--pay` 不是十进制数，或小数位超过 6 位；`invalid_value`——`--pay` ≤ 0，或小到买不了一个最小单位）。

## 另请参见

[`asset info`](info.md) · [`tx send`](../tx/send.md) · [`exchange trade`](../exchange/trade.md) · [脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)
