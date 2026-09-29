# wallet-cli x402 serve

在本地运行一个受 x402 保护的端点。

## 用法

```
wallet-cli x402 serve --pay-to <address> [--amount <n> | --raw-amount <n>] [--token <symbol> | --asset <address> [--decimals <n>]]
                      [--scheme <exact|exact_gasfree>] [--valid-for-seconds <n>] [--resource-url <url>]
                      [--host <127.0.0.1|::1>] [--port <n>] [--facilitator-url <url>] [--daemon] [options]
```

## 说明

在回环接口上启动一个小型 HTTP 服务器，在所选网络上售卖唯一一项资源 `/pay`，收款方为 `--pay-to`。它会打印一次端点与价格，然后持续运行，直到你用 Ctrl-C 停止。加上 `--daemon` 则改为后台运行：命令在服务器开始监听后即返回，给出它的进程 ID 和日志文件路径，之后用 `kill <PID>` 停止。它的用途是试用 [`x402 pay`](pay.md)；[`x402 roundtrip`](roundtrip.md) 会启动同样的服务器、付一次款，然后退出。

服务器的应答规则：

| 请求 | 响应 |
|---|---|
| 未带付款访问 `/pay`（任意方法） | `402 Payment Required`，在响应体和 `payment-required` 头中给出支付要求 |
| 带付款访问 `/pay` | 服务器交由 `--facilitator-url` 校验并结算。成功时：`200`，带 `{"success":true,"network":…,"scheme":…,"transaction":…}` 和 `payment-response` 头。失败时：`400` 或 `502`，带 `code`、`error`、`phase` 和 `paymentStatus` |
| `GET /.well-known/x402` | `200`，返回同样的支付要求，用于能力发现 |
| `/health` | `200`，返回 `{"ok":true}` |
| 其他任何请求 | `404` |

**价格**由 `--amount`（以 token 为单位，可含小数；默认 `0.0001`）或 `--raw-amount`（该 token 的最小单位）给出。**token** 由 `--token` 指定，取地址簿在所选网络上已知的符号（默认 `USDT`；例如 Base Sepolia 上用 `USDC`），或由 `--asset` 指定 token 合约地址；若该合约不在地址簿中，还需同时给出 `--decimals`。`--amount` 的小数位不能超过该 token 的精度。`exact_gasfree` 仅在 TRON 上提供。

`--resource-url` 设置支付要求中对外声明的资源 URL（默认就是 `/pay` 这个 URL 本身）。服务器只绑定到 `127.0.0.1` 或 `::1`。不需要钱包，也不需要密码。

**在 TRON 上会先询问 facilitator。** 开始监听之前，服务器会读取 `--facilitator-url` 的 `/supported` 列表，并按 facilitator 对 x402 v2 及所选方案的写法来声明网络——支持时用十进制 id（`tron:3448148188`），否则用 facilitator 的 hex 形式（例如 `tron:0xcd8690dc`）。若该列表读不到、或其中没有匹配条目，服务器不会启动。[`x402 roundtrip`](roundtrip.md) 和 [`bai recharge`](../bai/recharge.md) 会做同样的检查。

**访问日志。** 每个请求都会记录状态和耗时——绝不记录其 URL 查询串、请求头、请求体或支付签名。前台运行时这些行输出到 stderr，text 模式下形如 `Payment required: HTTP 402 (1 ms)`，JSON 模式下形如 `{"event":"x402.request","method":"GET","route":"/pay","status":402,"durationMs":1}`；使用 `--daemon` 时则写入日志文件。

## 选项

| 选项 | 说明 |
|---|---|
| `--pay-to <address>` | **必填。** 所选网络上的收款地址 |
| `--amount <n>` | 价格，以 token 为单位（可含小数），小数位不得超过该 token 的精度（默认 `0.0001`）；与 `--raw-amount` 互斥 |
| `--raw-amount <n>` | 价格，以该 token 的最小单位计 |
| `--token <symbol>` | 地址簿在该网络上已知的支付 token（默认 `USDT`）；与 `--asset` 互斥 |
| `--asset <address>` | 用合约地址而非符号指定支付 token；若该合约不在地址簿中，还需给出 `--decimals` |
| `--decimals <n>` | `--asset` 所指 token 的精度，0–18；必须与 `--asset` 同用，且若该 token 在地址簿中已知，必须与之一致 |
| `--scheme <exact\|exact_gasfree>` | 提供的支付方案（默认 `exact`）；`exact_gasfree` 仅限 TRON |
| `--valid-for-seconds <n>` | 支付授权的有效时长，1–86400（默认 `300`） |
| `--resource-url <url>` | 支付要求中声明的资源 URL，`http://` 或 `https://`（默认为 `/pay` 的 URL） |
| `--host <127.0.0.1\|::1>` | 绑定的回环地址（默认 `127.0.0.1`） |
| `--port <n>` | 端口，1–65535（默认 `4020`） |
| `--facilitator-url <url>` | 负责校验并结算付款的 HTTPS facilitator（默认 `https://facilitator.bankofai.io`） |
| `--daemon` | 后台运行，并返回其 PID 与日志文件 |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

在 Nile 上以 0.0001 USDT 售卖一项资源：

```bash
wallet-cli x402 serve --pay-to TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ --network nile
```

```console
✅ Payment endpoint ready (Ctrl+C to stop)
  URL      http://127.0.0.1:4020/pay
  Network  nile
  Scheme   exact
  Amount   0.0001 USDT
  Pay to   TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ
```

```bash
wallet-cli x402 serve --pay-to TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ --network nile -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"x402.serve","data":{"payUrl":"http://127.0.0.1:4020/pay","network":"tron:3448148188","scheme":"exact","token":"USDT","asset":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf","decimals":6,"validForSeconds":300,"resourceUrl":"http://127.0.0.1:4020/pay","rawAmount":"100","payTo":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ"},"meta":{"durationMs":981,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

同样的服务器放到后台运行，适合需要腾出终端的脚本：

```bash
wallet-cli x402 serve --pay-to TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ --network nile --daemon
```

```console
✅ Payment endpoint running in background
  URL      http://127.0.0.1:4020/pay
  Network  nile
  Scheme   exact
  Amount   0.0001 USDT
  Pay to   TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ
  PID      15076
  Log      /var/folders/pz/jfbc2kzs54bfwtphmkj5zzlc0000gn/T/wallet-cli-x402-BRIQLn/access.log
```

```bash
wallet-cli x402 serve --pay-to TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ --network nile --daemon -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"x402.serve","data":{"payUrl":"http://127.0.0.1:4020/pay","network":"tron:3448148188","scheme":"exact","token":"USDT","asset":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf","decimals":6,"validForSeconds":300,"resourceUrl":"http://127.0.0.1:4020/pay","rawAmount":"100","payTo":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ","daemon":true,"pid":15598,"logFile":"/var/folders/pz/jfbc2kzs54bfwtphmkj5zzlc0000gn/T/wallet-cli-x402-dhxHjU/access.log"},"meta":{"durationMs":1282,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

用 `kill 15076`（也就是 `PID`）停止它。想查看价格并付款，见 [`x402 pay`](pay.md)。

## 输出 {#output}

启动时打印一次：

| 字段 | 类型 | 含义 |
|---|---|---|
| `payUrl` | string | 付费端点 |
| `network` | string | 该价格所在的网络 |
| `scheme` | string | 提供的支付方案 |
| `token` | string | 支付 token 的符号；用 `--asset` 指定 token 时没有该字段 |
| `asset` | string | 支付 token 的合约 |
| `decimals` | number | 支付 token 的精度 |
| `validForSeconds` | number | 支付授权的有效时长 |
| `resourceUrl` | string | 支付要求中声明的资源 URL |
| `rawAmount` | string | 价格，以该 token 的最小单位计 |
| `payTo` | string | 收款方 |
| `daemon` / `pid` / `logFile` | boolean / number / string | 使用 `--daemon` 时：`true`、后台进程 ID，以及它的日志文件 |

## 退出码 {#exit-status}

`0` 以 Ctrl-C 停止，或使用 `--daemon` 时服务器已启动 · `1` 执行失败（`port_in_use`——端口被占用；`provider_error`——facilitator 的 `/supported` 列表读取失败，或使用 `--daemon` 时后台服务器启动失败（含端口被占用的情形），其日志文件在 `error.details.logFile` 中；`provider_rate_limited`——facilitator 返回 429；`invalid_x402_response`——它的 `/supported` 列表格式有误） · `2` 用法错误（`unsupported_network_capability`——在 TRON 上，facilitator 不支持该网络与方案的组合；`missing_option`——未给出 `--pay-to`；`invalid_address`——`--pay-to` 或 `--asset` 不是合法地址；`family_mismatch`——`--pay-to` 属于另一个链家族；`invalid_option`——`--amount` 与 `--raw-amount` 同用、`--token` 与 `--asset` 同用、`--decimals` 没有配 `--asset`，或 `--decimals` 与已知 token 的精度不一致；`invalid_amount`——价格不是正数，或小数位超过该 token 的精度；`invalid_value`——该 token 未在该网络上注册且没有给出带 `--decimals` 的 `--asset`、在 EVM 网络上使用了 `exact_gasfree`、`--facilitator-url` 不是 HTTPS、`--resource-url` 不是 HTTP(S)、`--host` 不是回环地址、`--port` 超出 1–65535，或 `--valid-for-seconds` 超出 1–86400）。

## 另请参见

[`x402 pay`](pay.md) · [`x402 roundtrip`](roundtrip.md)
