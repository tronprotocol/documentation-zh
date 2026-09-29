# wallet-cli bai recharge

用稳定币为 B.AI 账户充值。

## 用法

```
wallet-cli bai recharge <amount> [--token <symbol>] [--to <email|address>] [--network <tron|bsc|base>]
                         [--scheme <exact|exact_gasfree>] [--gasfree-relay <official|gasfree|url>]
                         [--max-gasfree-fee <n> | --max-gasfree-fee-raw <n>] [--dry-run] [--password-stdin] [options]
```

## 说明

在 B.AI 创建一笔充值订单，用当前账户（或 `--account`）以 x402 付款支付它——默认是 `exact`，TRON 上也可用 `exact_gasfree`——然后把交易上报给 B.AI，由它增加额度。**这会花掉真实的 token**——充值只在主网上可用：

| `--network` | 可用 token | 默认 `--token` |
|---|---|---|
| `tron` (`tron:728126428`) | `USDT`, `USDD` | `USDT` |
| `bsc` (`eip155:56`) | `USDT` | `USDT` |
| `base` (`eip155:8453`) | `USDC` | `USDC` |

USDT 和 USDC 的最小充值额为 1；USDD 没有下限。

**额度加给谁。** 不传 `--to` 时，加给该 API key 所属的账户。传了 `--to` 时，加给该邮箱或钱包地址（EVM、TRON 或 Solana）背后的 B.AI 账户；B.AI 会在创建订单之前完成解析。

**创建订单之前会校验：**

- 金额必须是满足最小额的正数（`invalid_amount`）。
- 网络：除 `tron`、`bsc` 和 `base` 之外都会以 `unsupported_network_capability` 失败。
- 付款地址必须已绑定到该 API key 所属的 B.AI 账户。CLI 每次都会向 B.AI 询问；若尚未绑定，它会（在校验 master password 之后）用付款账户对 B.AI 的绑定消息签名并完成绑定。绑定失败会中止命令。绑定一旦成功就会保留，即使后续步骤失败也不会撤销。
- token 必须是该网络接受的（否则 `invalid_value`），金额最多 6 位小数（否则 `invalid_amount`）。在 TRON 之外使用 `exact_gasfree` 会被拒绝（`invalid_value`）。
- 传了 `--to` 时，B.AI 必须能识别该收款方；否则以 `provider_error` 失败。
- master password：未给出 `--password-stdin` 时，命令以 `auth_required` 停止。

以上任一项失败时都不会产生订单、也不会付款。只有全部通过之后才会创建订单。

**用 `--dry-run` 预览。** 它执行同样的校验（密码除外），然后读取支付要求，但不做绑定、不创建订单、不解锁钱包、也不签名。`bindingRequired` 说明真正充值时是否需要先绑定付款地址（需要时会给出警告）。它会报告谁付给谁、以最小单位计的价格、支付路由，以及付款方当前的余额。手续费在付款前无法得知，因此 `estimatedFee` 为 `null`。不需要密码。

**`exact_gasfree`** 从账户的 [GasFree](../gasfree/index.md) 账户付款，而不是它自己的 token 余额，做法与 [`x402 pay`](../x402/pay.md) 相同：`--gasfree-relay` 决定 GasFree 账户数据的来源，`--max-gasfree-fee` 限制你授权的服务费上限。`--dry-run` 预览中显示的余额是付款钱包的余额，而不是它的 GasFree 账户余额。

**如果付款之后上报失败**，命令并不会失败。它返回 `creditStatus: "unconfirmed"`，带上交易哈希和 `retryPayment: false`——款已经付出去了，因此**不要再充一次**。请用 [`bai report-recharge`](report-recharge.md) 上报同一笔交易。CLI 会等待约 15 秒让交易被索引，然后上报一次；它不会重试。返回 `unconfirmed` 且 `code: "TX_NOT_FOUND_OR_INVALID"`（警告为 `B.AI has not indexed the transaction yet; report it again in a minute with \`bai report-recharge\``）或 `provider_rate_limited` 时，通常只是说明 B.AI 还需要一点时间。

如果是付款本身失败，错误中会带上付款细节（`paymentStatus`、`retryPayment: false`，以及已知时的交易哈希），外加 `chain`、`amount`，使用 `--to` 时还有解析出的 `rechargeTarget`。参见 [x402 与 B.AI 的支付细节](../../machine-interface.md#x402-and-bai-payment-details)。

需要一个账户、通过 `--password-stdin` 提供的 master password，以及已保存的 B.AI API key。

## 参数

- `amount`——以 token 为单位的金额（可含小数），例如 `10`

## 选项

| 选项 | 说明 |
|---|---|
| `--token <symbol>` | 用于付款的 token（默认：Base 上为 `USDC`，其他网络为 `USDT`） |
| `--to <email\|address>` | 为他人的 B.AI 账户充值；省略则为自己充值 |
| `--scheme <exact\|exact_gasfree>` | 支付方案（默认 `exact`）；`exact_gasfree` 仅限 TRON |
| `--gasfree-relay <official\|gasfree\|url>` | `exact_gasfree` 下 GasFree 账户数据的来源（默认 `official`）；见 [`x402 pay`](../x402/pay.md) |
| `--max-gasfree-fee <n>` | 授权的最高 GasFree 服务费，以 token 为单位（可含小数）；与 `--max-gasfree-fee-raw` 互斥 |
| `--max-gasfree-fee-raw <n>` | 同一上限，以最小单位计 |
| `--dry-run` | 执行校验并预览付款，但不创建订单、不付款 |
| `--password-stdin` | 从 stdin 读取 master password |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

充值分两步：先预览，再付款。

**1. 预览这次充值。** `--dry-run` 会完成全部校验并显示将要支付的内容，但不创建订单、也不签任何名：

```bash
wallet-cli bai recharge 1 --network tron --dry-run
```

```console
✅ B.AI recharge preview — no order or payment created
  dry Run: Yes
  binding Required: No
  network: tron:728126428
  token: USDT
  amount: 1
  payer: TWer2Ygk5TEheHp3TPuYeqxmB6SsGZmaL6
  pay To: TSNEPtuCagKEgF2EU4pAKWLzXLz1bekfTE
  scheme: exact
  raw Amount: 1000000
  recharge Target:
    type: self
    wallet Address: TWer2Ygk5TEheHp3TPuYeqxmB6SsGZmaL6
  payment:
    url: http://127.0.0.1:60758/pay
    status: 402
    delivered: No
    settled: No
    dry Run: Yes
    payment Required: Yes
    selected:
      scheme: exact
      network: tron:728126428
      amount: 1000000
      asset: TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t
      pay To: TSNEPtuCagKEgF2EU4pAKWLzXLz1bekfTE
      max Timeout Seconds: 300
      extra:
        asset Transfer Method: permit2
  balance:
    token Raw: 2500000
    native Raw: 7000006
  estimated Fee: Not available
  fee Limit:
    amount: Not available
    raw Amount: Not available
  warning: Preview only; final network/relay fee is unavailable until payment authorization. Balance refers to the payer wallet, not its GasFree account. No order or payment was created.
```

```bash
wallet-cli bai recharge 1 --network tron --dry-run -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"bai.recharge","data":{"dryRun":true,"bindingRequired":false,"network":"tron:728126428","token":"USDT","amount":"1","payer":"TWer2Ygk5TEheHp3TPuYeqxmB6SsGZmaL6","payTo":"TSNEPtuCagKEgF2EU4pAKWLzXLz1bekfTE","scheme":"exact","rawAmount":"1000000","rechargeTarget":{"type":"self","walletAddress":"TWer2Ygk5TEheHp3TPuYeqxmB6SsGZmaL6"},"payment":{"url":"http://127.0.0.1:60779/pay","status":402,"delivered":false,"settled":false,"dryRun":true,"paymentRequired":true,"selected":{"scheme":"exact","network":"tron:728126428","amount":"1000000","asset":"TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t","payTo":"TSNEPtuCagKEgF2EU4pAKWLzXLz1bekfTE","maxTimeoutSeconds":300,"extra":{"assetTransferMethod":"permit2"}}},"balance":{"tokenRaw":"2500000","nativeRaw":"7000006"},"estimatedFee":null,"feeLimit":{},"warning":"Preview only; final network/relay fee is unavailable until payment authorization. Balance refers to the payer wallet, not its GasFree account. No order or payment was created."},"meta":{"durationMs":1851,"warnings":[]},"chain":{"family":"tron","network":"tron:728126428","chainId":"728126428"}}
```

`payer` 向 B.AI 的收款地址 `payTo` 支付 1 USDT（`rawAmount` 为 `1000000`，6 位精度）。`balance` 是付款方当前的余额，以最小单位计：`tokenRaw` 对应 USDT，`nativeRaw` 对应 TRX（以 SUN 计）。

**2. 充值。** 这一步会花掉真实的 USDT。`$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入：

```bash
printf '%s' "$PW" | wallet-cli bai recharge 1 --network tron --password-stdin
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
  network: tron:728126428
  token: USDT
  payer: TWer2Ygk5TEheHp3TPuYeqxmB6SsGZmaL6
```

```bash
printf '%s' "$PW" | wallet-cli bai recharge 1 --network tron --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"bai.recharge","data":{"chain":"tron","txHash":"3f7a9c2e1b8d4f60a5c3e7b9d1f2a4c6e8b0d3f5a7c9e1b2d4f6a8c0e2b4d6f8","amount":"1","retryPayment":false,"creditStatus":"credited","order":{"canDownloadInvoice":false,"chainKey":"tron","createdAt":1789569840,"currency":"USDT","id":31215,"paymentMethod":"TRON","points":1000000,"quantityDisplay":"1","rechargeType":"crypto","recipientDisplayLabel":null,"recipientRelation":"self","status":"success","teamId":null,"transactionId":"3f7a9c2e1b8d4f60a5c3e7b9d1f2a4c6e8b0d3f5a7c9e1b2d4f6a8c0e2b4d6f8","type":"purchase"},"network":"tron:728126428","token":"USDT","payer":"TWer2Ygk5TEheHp3TPuYeqxmB6SsGZmaL6"},"meta":{"durationMs":14385,"warnings":[]},"chain":{"family":"tron","network":"tron:728126428","chainId":"728126428"}}
```

`credited`（标题为 `B.AI recharge credited`）表示 B.AI 已经把额度加上了——`order.points` 是加了多少。`txHash` 是付款交易，`payer` 是付款地址。

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `creditStatus` | string | `credited`——B.AI 已确认加上额度；`unconfirmed`——已付款，但尚未确认 |
| `txHash` | string | 付款交易 |
| `chain` | string | `tron`、`bnb` 或 `base` |
| `network` | string | 规范网络 id |
| `token` | string | 支付所用的 token |
| `amount` | string | 支付金额，以 token 为单位（可含小数） |
| `payer` | string | 付款地址 |
| `rechargeTarget` | object | 使用 `--to` 时：你给出的标识，以及 B.AI 解析出的 `targetId`——请保留它，`report-recharge` 会用到 |
| `retryPayment` | boolean | 恒为 `false` |
| `order` | object | `credited` 时：B.AI 返回的订单原样给出 |
| `code` / `warning` / `error` | string / string / object | `unconfirmed` 时：上报未能确认的原因 |

使用 `--dry-run` 时：

| 字段 | 类型 | 含义 |
|---|---|---|
| `dryRun` | boolean | `true` |
| `bindingRequired` | boolean | 付款地址尚未绑定到该 key 的 B.AI 账户时为 `true`，表示真正充值会先签名并完成绑定 |
| `network` / `token` / `amount` | string | 将要支付的内容 |
| `payer` / `payTo` | string | 付款地址，以及 B.AI 的收款地址 |
| `scheme` | string | `exact` 或 `exact_gasfree` |
| `rawAmount` | string | 金额，以该 token 的最小单位计 |
| `rechargeTarget` | object | 额度加给谁：`{type: "self", walletAddress}`，或解析后的 `--to` 收款方 |
| `payment` | object | 将要使用的支付路由——字段与 [`x402 pay --dry-run`](../x402/pay.md#output) 的结果相同 |
| `balance` | object \| null | 付款方以最小单位计的 `tokenRaw` 和 `nativeRaw` 余额；读取失败时为 `null`（并给出警告） |
| `estimatedFee` | null | 付款之前无法得知手续费 |
| `feeLimit` | object | 若给出了 `--max-gasfree-fee` / `--max-gasfree-fee-raw`，此处为其值 |
| `warning` | string | 提示：没有创建任何订单，也没有付款 |

## 退出码

`0` 已付款（请检查 `creditStatus`），或以 `--dry-run` 完成预览 · `1` 执行失败（[`x402 pay`](../x402/pay.md#exit-status) 的各项付款错误；`auth_required`——未给出 `--password-stdin`，发生在创建订单之前；`provider_error`——包括 B.AI 无法识别的 `--to` 收款方，或 B.AI 返回了对应其他地址或其他链的绑定；`bai_auth_failed`——B.AI 拒绝了已保存的 key；`bai_rejected`——带 `error.details.reason`） · `2` 用法错误（`bai_credentials_missing`；`unsupported_network_capability`；`invalid_value`——该网络不接受的 token，或在 TRON 之外使用 `exact_gasfree`；`invalid_amount`——不是正数金额、低于最小额，或小数位超过 6 位；`invalid_option`——同时给了两个 GasFree 费用上限，或使用了本命令不接受的 `--wait` / `--wait-timeout`）。

## 另请参见

[`bai report-recharge`](report-recharge.md) · [`bai recharge-orders`](recharge-orders.md) · [`config`](../config.md)
