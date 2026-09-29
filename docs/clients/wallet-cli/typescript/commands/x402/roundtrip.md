# wallet-cli x402 roundtrip

启动本地付费墙、付一次款，然后退出。

## 用法

```
wallet-cli x402 roundtrip --pay-to <address> [--amount <n> | --raw-amount <n>] [--token <symbol> | --asset <address> [--decimals <n>]]
                          [--scheme <exact|exact_gasfree>] [--valid-for-seconds <n>] [--port <n>] [--facilitator-url <url>]
                          [--gasfree-relay <official|gasfree|url>] [--max-gasfree-fee <n> | --max-gasfree-fee-raw <n>]
                          [--password-stdin] [options]
```

## 说明

一步完成 [`x402 serve`](serve.md) 和 [`x402 pay`](pay.md)：启动同样的本地端点，用当前账户（或 `--account`）向它付一次款，然后关闭服务器。用它可以端到端地验证整条 x402 流程——支付要求、签名、facilitator 结算。

**这是一笔真实付款**，金额为设定的价格，收款方是 `--pay-to`；而且 `pay` 只接受服务器启动时设定的那条路由，因此不可能付到别处去。

服务器始终绑定到 `127.0.0.1`。价格、token、方案、端口和 facilitator 相关选项的校验规则与 `x402 serve` 完全相同。需要一个账户，以及通过 `--password-stdin` 提供的 master password。

## 选项

| 选项 | 说明 |
|---|---|
| `--pay-to <address>` | **必填。** 所选网络上的收款地址 |
| `--amount <n>` | 价格，以 token 为单位（可含小数），小数位不得超过该 token 的精度（默认 `0.0001`）；与 `--raw-amount` 互斥 |
| `--raw-amount <n>` | 价格，以该 token 的最小单位计 |
| `--token <symbol>` | 地址簿在该网络上已知的支付 token（默认 `USDT`）；与 `--asset` 互斥 |
| `--asset <address>` | 用合约地址而非符号指定支付 token；若该合约不在地址簿中，还需给出 `--decimals` |
| `--decimals <n>` | `--asset` 所指 token 的精度，0–18；必须与 `--asset` 同用 |
| `--scheme <exact\|exact_gasfree>` | 支付方案（默认 `exact`）；`exact_gasfree` 仅限 TRON |
| `--valid-for-seconds <n>` | 支付授权的有效时长，1–86400（默认 `300`） |
| `--port <n>` | 端口，1–65535（默认 `4020`） |
| `--facilitator-url <url>` | HTTPS facilitator（默认 `https://facilitator.bankofai.io`） |
| `--gasfree-relay <official\|gasfree\|url>` | `exact_gasfree` 下 GasFree 账户数据的来源；见 [`x402 pay`](pay.md) |
| `--max-gasfree-fee <n>` / `--max-gasfree-fee-raw <n>` | GasFree 服务费上限；两者互斥 |
| `--password-stdin` | 从 stdin 读取 master password |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

在 Nile 上通过本地付费墙向 `TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ` 支付 0.0001 USDT。`$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入：

```bash
printf '%s' "$PW" | wallet-cli x402 roundtrip --pay-to TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ --network nile --password-stdin
```

```console
✅ Payment settled
  Network      nile
  Scheme       exact
  Amount       0.0001 USDT
  From         TWer2Ygk5TEheHp3TPuYeqxmB6SsGZmaL6
  To           TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ
  Transaction  d6e0bb3015dce28ac9813f4d90be442d0f1ef61a6d4268cb023c5e8cfc09ef36
  Delivery     Delivered
```

```bash
printf '%s' "$PW" | wallet-cli x402 roundtrip --pay-to TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ --network nile --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"x402.roundtrip","data":{"serve":{"payUrl":"http://127.0.0.1:4020/pay","network":"tron:3448148188","scheme":"exact","token":"USDT","asset":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf","decimals":6,"validForSeconds":300,"resourceUrl":"http://127.0.0.1:4020/pay","rawAmount":"100","payTo":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ"},"pay":{"url":"http://127.0.0.1:4020/pay","status":200,"delivered":true,"settled":true,"payer":{"address":"TWer2Ygk5TEheHp3TPuYeqxmB6SsGZmaL6"},"paymentResponse":{"success":true,"transaction":"1ca932a4cda16fe9485689d6b7daa38ca34c601bbd970f609fb1c5a56b375438","network":"tron:0xcd8690dc","payer":"0xe2e1a54926527fbb4e4420de4c6bab82beaee24d"},"response":{"success":true,"network":"tron:3448148188","scheme":"exact","transaction":"1ca932a4cda16fe9485689d6b7daa38ca34c601bbd970f609fb1c5a56b375438"}}},"meta":{"durationMs":7594,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

`Payment settled` 加上 `Delivery Delivered`，表示这笔付款已在链上完成，且付费墙返回了它的响应。`From` 是付款账户，`Transaction` 是该笔付款的交易 ID。在 JSON 中，`serve` 是付费墙所收取的内容（`rawAmount` 以该 token 的最小单位计），`pay` 则是付款结果：`paymentResponse` 是 facilitator 的回执，其中的 `payer` 是你的地址的 hex 形式，`response` 是付款之后付费墙返回的内容。

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `serve` | object | 服务器所提供的内容——字段与 [`x402 serve`](serve.md#output) 相同 |
| `pay` | object | 付款结果——字段与 [`x402 pay`](pay.md#output) 相同 |

## 退出码

`0` 已付款 · `1` 执行失败（[`x402 pay`](pay.md#exit-status) 的各项付款错误；`auth_required`——未给出 `--password-stdin`；`missing_wallet_address`；`port_in_use`） · `2` 用法错误（[`x402 serve`](serve.md#exit-status) 的各项用法错误；`invalid_option`——同时给了两个互斥选项（`--amount` / `--raw-amount`、`--token` / `--asset`、两个 GasFree 费用上限）、`--decimals` 没有配 `--asset`，或使用了本命令不接受的 `--wait` / `--wait-timeout`；`gasfree_credentials_missing`）。

## 另请参见

[`x402 serve`](serve.md) · [`x402 pay`](pay.md)
