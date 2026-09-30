# wallet-cli x402 endpoint-list

列出某个服务方的端点与价格。

## 用法

```
wallet-cli x402 endpoint-list <provider> [options]
```

## 说明

列出目录中某个服务方的付费端点，给出每个端点的价格以及它接受付款的网络。表格中，价格区间显示为 `min–max`，缺失的值显示为 `——`，而不是零价格。

表格中不含 URL。**每个网络都有各自的付款 URL**——请在 JSON 的 `x402Routes[].url` 中查找，填好路径里的 `{placeholders}`，再连同匹配的 `--network` 一起传给 [`x402 pay`](pay.md)。端点顶层的 `url` 只是其中之一。

与 [`x402 provider-list`](provider-list.md) 一样，它优先读本地缓存，只下载缓存中没有的部分。不需要钱包，也不需要密码。

## 参数

- `provider`——服务方的 `fqn`，可由 [`x402 provider-list`](provider-list.md) 列出

## 选项

没有本命令特有的选项；仅[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli x402 endpoint-list dia
```

```console
| Method | Path                                      | Price (USD) | Networks        | Description                                                 |
| ------ | ----------------------------------------- | ----------- | --------------- | ----------------------------------------------------------- |
| GET    | /v1/quotation/{symbol}                    | 0.000001    | tron, bsc, base | Aggregated price quotation by asset symbol                  |
| GET    | /v1/assetQuotation/{blockchain}/{address} | 0.000001    | tron, bsc, base | Aggregated price quotation by blockchain + contract address |
```

表格里没有 URL：每个网络的付款 URL 都在 JSON 的 `x402Routes[].url` 下。以 DIA 的第一个端点在 TRON 上为例，它是 `https://x402-gateway.bankofai.io/providers/dia-price-tron/v1/quotation/{symbol}`——把 `{symbol}` 换成 `BTC`，再用 `--network tron` 付款，做法见 [`x402 pay`](pay.md#examples) 的示例。

## 输出 {#output}

| 字段 | 类型 | 含义 |
|---|---|---|
| `fqn` | string | 服务方名称 |
| `endpoints[]` | array | 每个端点一条记录，按目录发布的原样给出 |

端点记录的主要字段：

| 字段 | 类型 | 含义 |
|---|---|---|
| `method` / `path` | string | HTTP 方法与路径 |
| `url` | string | 它其中一条路由的 URL（第一个网络的）；请按你要付款的网络改用 `x402Routes[].url` |
| `title` / `description` | string | 它返回什么 |
| `minPriceUsd` / `maxPriceUsd` | number | 每次调用的价格，以 USD 计 |
| `metered` | boolean | 是否按用量计费 |
| `x402Routes[]` | array | 每种付款方式一条：`network`、`scheme`（`exact` / `exact_gasfree`）、`assetTransferMethod`（例如 `permit2`、`eip3009`；`exact_gasfree` 下没有该字段）、`provider`，以及在该网络上付款所用的 `url` |

## 退出码

`0` 成功 · `1` 执行失败（`provider_not_found`——没有该名称的服务方；`provider_error`；`catalog_schema_unsupported`；`timeout`） · `2` 用法错误（`missing_option`——未给出服务方；`invalid_value`——名称中含有服务方名称不允许的字符）。

## 另请参见

[`x402 provider-show`](provider-show.md) · [`x402 pay`](pay.md)
