# wallet-cli x402 pay

请求某个 HTTP 端点并支付它的 x402 挑战。

## 用法

```
wallet-cli x402 pay <url> [--method <m>] [--header "Name: value"]... [--body <s> | --body-file <path>]
                          [--max-amount <n> | --max-raw-amount <n>] [--token <symbol>] [--asset <address> [--decimals <n>]]
                          [--scheme <exact|exact_gasfree>] [--gasfree-relay <official|gasfree|url>]
                          [--max-gasfree-fee <n> | --max-gasfree-fee-raw <n>]
                          [--out <path>] [--dry-run] [--password-stdin] [options]
```

## 说明

发出请求。如果端点返回成功状态（2xx），该响应原样返回，不会付任何钱；除 `402` 之外的其他状态都会以 `provider_error` 失败，并带上 `httpStatus` 和 `phase: "request"`。如果端点返回 `402 Payment Required`，`pay` 会读取它给出的支付路由，挑选一条与所选 `--network` 及你的筛选条件相匹配的路由，用当前账户（或 `--account`）对支付授权签名，然后带着它重新发起请求。端点的 facilitator 负责在链上结算这笔付款。

**在匹配到路由之前不会签任何名。** 其他网络上的路由会被忽略；`--token`、`--asset` 和 `--scheme` 会进一步缩小选择范围，而 `--max-amount`（以 token 为单位，可含小数）或 `--max-raw-amount`（最小单位）会排除定价高于该值的路由。若没有任何路由匹配，命令以 `no_matching_requirement` 失败；若匹配到的路由定价超过限额，则以 `amount_exceeds_limit` 失败。两者都在签名之前抛出，带 `paymentStatus: "not_sent"`，并且不会索要密码——无论是否加了 `--dry-run`。如果你没有自行设定限额，对已知的稳定币会套用一个内置上限 **每笔 $1**；定价高于它的路由同样以 `amount_exceeds_limit` 失败，而传入 `--max-amount` 或 `--max-raw-amount` 会用你的限额取代这个内置上限。

**两种支付方案：**

- `exact`——从账户自己的 token 余额付款。
- `exact_gasfree`——从账户的 GasFree 账户付款（TRON）。GasFree 余额必须同时覆盖价格**和**最高服务费，否则在发出任何东西之前就以 `gasfree_insufficient_balance` 失败；它不会回退到普通余额。`--gasfree-relay` 决定 GasFree 账户数据的来源：`official`（默认，不需要凭据）、`gasfree`（GasFree Open API，需要在 [`config`](../config.md) 中配置 `gasfreeApiKey` / `gasfreeApiSecret`），或者你自己的 HTTPS URL。`--max-gasfree-fee` 用来限制你授权的服务费上限。

`--dry-run` 在读完挑战后就停下：它报告将要支付的那条路由，但不签名。

运行期间，`pay` 会在 stderr 上打印以 `⏳` 开头的进度行（JSON 模式下是 `{"type":"activity",...}` 行）；stdout 只承载最终结果。

响应体会放在 `data.response` 中返回——端点声明是 JSON 时会被解析——或者用 `--out` 写入一个新文件。响应大小上限为 10 MB。

**付款失败时，再次尝试之前请先读 `error.details`。** `paymentStatus: "not_sent"` 表示钱没有离开账户；`"unknown"` 表示 CLI 无法判断，此时应当视为**可能已付**并先行对账；`retryPayment: false` 表示不要靠再付一次来补救。参见 [x402 与 B.AI 的支付细节](../../machine-interface.md#x402-and-bai-payment-details)。

需要一个账户，即便最终发现该端点是免费的也一样。只有在确实要为付款签名时，才需要通过 `--password-stdin` 提供 master password。

## 参数

- `url`——端点 URL

## 选项

| 选项 | 说明 |
|---|---|
| `--method <GET\|POST\|PUT\|PATCH\|DELETE>` | HTTP 方法（默认 `GET`） |
| `--header <"Name: value">` | 形如 `Name: value` 的请求头；可重复传入多个 |
| `--body <string>` | 请求体；与 `--body-file` 互斥 |
| `--body-file <path>` | 从文件读取请求体，传 `-` 则从 stdin 读取；与 `--body` 互斥 |
| `--max-amount <n>` | 拒绝定价高于此值的路由，以 token 为单位（可含小数）；与 `--max-raw-amount` 互斥 |
| `--max-raw-amount <n>` | 同一限额，以最小单位计 |
| `--token <symbol>` | 只接受以该 token 付款的路由 |
| `--asset <address>` | 只接受以该 token 合约付款的路由 |
| `--decimals <n>` | `--asset` 所指 token 的精度；必须与 `--asset` 同用 |
| `--scheme <exact\|exact_gasfree>` | 只接受使用该方案的路由 |
| `--gasfree-relay <official\|gasfree\|url>` | `exact_gasfree` 下 GasFree 账户数据的来源（默认 `official`）；若给 URL，必须是 HTTPS 且不带凭据、查询串和片段 |
| `--max-gasfree-fee <n>` | 授权的最高 GasFree 服务费，以 token 为单位（可含小数）；与 `--max-gasfree-fee-raw` 互斥 |
| `--max-gasfree-fee-raw <n>` | 同一上限，以最小单位计 |
| `--out <path>` | 把响应体写入一个新文件，而不是放进 `data.response`；若文件已存在，会在发出任何请求**之前**就以 `output_exists` 拒绝，因此既不会被覆盖，也不会为它付钱 |
| `--dry-run` | 只读取挑战并报告选中的路由，不签名 |
| `--password-stdin` | 从 stdin 读取 master password |

此外还有[全局选项](../index.md#global-options-every-command)。`--timeout` 限制的是每一次 HTTP 请求。

## 示例 {#examples}

为一个 x402 端点付款分两步：先看它收多少，再付。示例用的是 x402 目录中 DIA 的 BTC 报价接口（见 [`x402 endpoint-list`](endpoint-list.md)），它在 TRON 主网上收款。

**1. 先看端点收多少。** `--dry-run` 只读价格、不签任何名，因此不会付钱：

```bash
wallet-cli x402 pay https://x402-gateway.bankofai.io/providers/dia-price-tron/v1/quotation/BTC --network tron --dry-run
```

```console
Payment preview — no payment sent
URL        https://x402-gateway.bankofai.io/providers/dia-price-tron/v1/quotation/BTC
Status     402
Settled    No
Delivered  No
Payment requirements:
  scheme: exact
  network: tron:728126428
  amount: 1
  asset: TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t
  pay To: TLXPgJVJFgL97gc49j8w8kC22mDTpH9EGa
  max Timeout Seconds: 300
  extra:
    asset Transfer Method: permit2
```

```bash
wallet-cli x402 pay https://x402-gateway.bankofai.io/providers/dia-price-tron/v1/quotation/BTC --network tron --dry-run -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"x402.pay","data":{"url":"https://x402-gateway.bankofai.io/providers/dia-price-tron/v1/quotation/BTC","status":402,"delivered":false,"settled":false,"dryRun":true,"paymentRequired":true,"selected":{"scheme":"exact","network":"tron:728126428","amount":"1","asset":"TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t","payTo":"TLXPgJVJFgL97gc49j8w8kC22mDTpH9EGa","maxTimeoutSeconds":300,"extra":{"assetTransferMethod":"permit2"}}},"meta":{"durationMs":900,"warnings":[]},"chain":{"family":"tron","network":"tron:728126428","chainId":"728126428"}}
```

`status: 402` 表示该端点要求付款。`selected`（文本中是 `Payment requirements`）就是将要支付的那条路由：`amount` 以该 token 的最小单位计，因此 `"1"` 是 0.000001 USDT（6 位精度）；`asset` 是 TRON 主网上的 USDT 合约；`payTo` 是收款方。

**2. 付款。** 这一步会在主网上花掉真实的 USDT。`--max-amount 0.001` 会拒绝任何高于 0.001 USDT 的价格，`--out` 把响应保存到 `btc-quote.json`。`$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入：

```bash
printf '%s' "$PW" | wallet-cli x402 pay https://x402-gateway.bankofai.io/providers/dia-price-tron/v1/quotation/BTC --network tron --max-amount 0.001 --out btc-quote.json --password-stdin
```

```console
URL          https://x402-gateway.bankofai.io/providers/dia-price-tron/v1/quotation/BTC
Status       200
Settled      Yes
Delivered    Yes
From         TWer2Ygk5TEheHp3TPuYeqxmB6SsGZmaL6
Transaction  9b41c7e2d05f83a6e1c4b8d27f9a03e5c6d8b1f4a2e7c9d0b3f5a8e1c6d2b7f4
Output       btc-quote.json
```

```bash
printf '%s' "$PW" | wallet-cli x402 pay https://x402-gateway.bankofai.io/providers/dia-price-tron/v1/quotation/BTC --network tron --max-amount 0.001 --out btc-quote.json --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"x402.pay","data":{"url":"https://x402-gateway.bankofai.io/providers/dia-price-tron/v1/quotation/BTC","status":200,"delivered":true,"settled":true,"payer":{"address":"TWer2Ygk5TEheHp3TPuYeqxmB6SsGZmaL6"},"paymentResponse":{"success":true,"transaction":"9b41c7e2d05f83a6e1c4b8d27f9a03e5c6d8b1f4a2e7c9d0b3f5a8e1c6d2b7f4","network":"tron:0x2b6653dc","payer":"0xe2e1a54926527fbb4e4420de4c6bab82beaee24d"},"output":{"path":"btc-quote.json","bytes":214}},"meta":{"durationMs":6412,"warnings":[]},"chain":{"family":"tron","network":"tron:728126428","chainId":"728126428"}}
```

`Settled Yes` 表示这笔付款已在链上完成；`Delivered Yes` 表示付费后的响应已经拿到，并写入了 `btc-quote.json`。`From` 是付款账户，`Transaction` 是该笔付款的交易 ID（JSON 中对应 `data.payer.address` 和 `data.paymentResponse.transaction`）。付款交易由 facilitator 提交并承担其能量开销，因此付款本身只花掉账户报价的那部分。例外是在 TRON 上首次用某个 token 进行 `exact` 付款：如果账户对该 token 尚无 Permit2 授权额度，且端点不代付这笔授权，账户会先自行广播 `approve(Permit2, MaxUint256)`——消耗自己的能量，不足时燃烧 TRX 抵扣——并授予 Permit2 **无上限**的额度。下文的 `approval` 字段会记录这笔授权。

## 输出 {#output}

| 字段 | 类型 | 含义 |
|---|---|---|
| `url` | string | 所请求的 URL |
| `status` | number | 最终响应的 HTTP 状态码 |
| `delivered` | boolean | 最终响应是否成功（2xx） |
| `settled` | boolean | 是否收到了所选网络上有效的结算回执 |
| `payer` | object | 付款账户的 `{address}`；在确实签署了付款时才有 |
| `paymentResponse` | object | 端点给出结算回执时的内容：`success`、`transaction`（付款的交易 ID）、`network` 和 `payer`——均按 facilitator 自己的写法给出，例如 `tron:0xcd8690dc` 和一个 hex 地址 |
| `approval` | object | 仅 TRON，且仅当该笔付款需要一次性的 Permit2 授权时：`{txId, token, spender, allowance: "unlimited", feeLimitSun, status}`。`status` 为 `confirmed`（在付款签名之前已广播并入块）或 `exported`（已签入付款包，由端点代为承担）。授权之后的任一步骤失败时，同样的对象会出现在 `error.details.approval` 中 |
| `response` | any | 响应体——解析后的 JSON，或文本；使用 `--out` 时没有该字段 |
| `output` | object | 使用 `--out` 时：写入的 `{path, bytes}` |
| `dryRun` / `paymentRequired` / `selected` | —— | 在 `402` 上使用 `--dry-run` 时：分别为 `true`、`true`，以及将要支付的那条路由（`scheme`、`network`、以最小单位计的 `amount`、`asset`、`payTo`、`maxTimeoutSeconds`、`extra`） |

## 退出码 {#exit-status}

`0` 成功，包括免费拿到响应的情形 · `1` 执行失败（`no_matching_requirement`、`amount_exceeds_limit`——两者都发生在签名之前，带 `paymentStatus: "not_sent"`；`gasfree_insufficient_balance` / `gasfree_not_activated`，`permit2_allowance_required` / `approval_reset_required`，`fee_cap_exceeded`，`payer_mismatch`，`invalid_settlement`，`invalid_x402_response`，`response_too_large`，`provider_rate_limited`——HTTP 429；`provider_error`——其他任何失败的请求或付款，带 `error.details.phase` 和 `httpStatus`；`missing_wallet_address`；`auth_required`——需要为付款签名却没有给出 `--password-stdin`；`auth_failed`，`timeout`） · `2` 用法错误（`output_exists`——`--out` 指定的文件已存在；`gasfree_credentials_missing`；`invalid_option`——同时给了两个互斥选项、`--decimals` 没有配 `--asset`，或者用了 `--wait` / `--wait-timeout`——本命令不接受它们，因为结算由 facilitator 完成；`invalid_amount`——限额不是一个正数金额；`invalid_value`——例如 `--header` 格式错误、`--method` 不受支持，或 `--gasfree-relay` 给的 URL 不是 HTTPS）。

## 另请参见

[`x402 serve`](serve.md) · [`x402 roundtrip`](roundtrip.md) · [`x402 endpoint-list`](endpoint-list.md) · [`gasfree info`](../gasfree/info.md)
