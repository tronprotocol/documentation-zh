# wallet-cli x402

为受 x402 保护的 HTTP 端点付费，并浏览 x402 服务方目录。

x402 端点在收到未付费请求时，会返回 HTTP `402 Payment Required`，并附上它接受的支付路由：网络、token、金额和收款方。[`x402 pay`](pay.md) 会挑选一条匹配的路由，用你的账户对支付授权签名，然后带着它重新发起请求。结算由 facilitator 服务在链上完成。

## 用法

```
wallet-cli x402 COMMAND
```

## 子命令

| 命令 | 页面 | 说明 |
|---|---|---|
| `x402 pay` | [pay.md](pay.md) | 请求某个端点并支付它的 x402 挑战 |
| `x402 serve` | [serve.md](serve.md) | 在本地运行一个受 x402 保护的端点 |
| `x402 roundtrip` | [roundtrip.md](roundtrip.md) | 启动本地付费墙、付一次款，然后退出 |
| `x402 provider-list` | [provider-list.md](provider-list.md) | 列出目录中的服务方 |
| `x402 provider-show` | [provider-show.md](provider-show.md) | 显示单个服务方 |
| `x402 endpoint-list` | [endpoint-list.md](endpoint-list.md) | 列出某个服务方的端点与价格 |
| `x402 update-catalog` | [update-catalog.md](update-catalog.md) | 把目录下载到本地缓存 |

## 工作方式

- **路由跟随 `--network`。** `pay` 只考虑所选网络上的路由，而目录服务对每个网络有各自独立的 URL——[`x402 endpoint-list`](endpoint-list.md) 会显示它们。目录中的服务目前在主网（`tron`、`bsc`、`base`）上收款；想在测试网上试用，请用 [`x402 serve`](serve.md) 跑一个自己的端点。
- **限额在签名之前生效。** `--max-amount` 会拒绝定价过高的路由，与你的筛选条件都不匹配的路由也会被拒绝——两者都发生在签名之前，错误中会带 `paymentStatus: "not_sent"`。
- **由 facilitator 结算，因此没有 `--wait`。** `pay` 和 `roundtrip` 在 facilitator 完成结算后才返回；它们不接受 `--wait` / `--wait-timeout`。
- **两种方案。** `exact` 从账户的 token 余额付款；`exact_gasfree` 从它的 [GasFree](../gasfree/index.md) 账户付款，两者之间不会互相回退。
- **付款失败并不代表钱没出去。** 再次付款前请先读 `error.details` 中的 `paymentStatus` 和 `retryPayment`——参见 [x402 与 B.AI 的支付细节](../../machine-interface.md#x402-and-bai-payment-details)。
- **目录类命令优先读本地缓存**（由 `update-catalog` 写入），只下载缓存中没有的部分。它们自己不会刷新缓存。

## 另请参见

[`bai`](../bai/index.md) · [`gasfree`](../gasfree/index.md) · [`config`](../config.md)
