# wallet-cli x402 provider-show

显示 x402 目录中的单个服务方。

## 用法

```
wallet-cli x402 provider-show <provider> [options]
```

## 说明

显示某个服务方在目录中的记录。文本输出给出它的名称、网站、端点数量、简介、分类和支付网络；JSON 则返回完整记录，包含全部端点。与 [`x402 provider-list`](provider-list.md) 一样，它优先读本地缓存，只下载缓存中没有的部分。

不需要钱包，也不需要密码。

## 参数

- `provider`——服务方的 `fqn`，可由 [`x402 provider-list`](provider-list.md) 列出

## 选项

没有本命令特有的选项；仅[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli x402 provider-show dia
```

```console
Provider   dia
Name       DIA
Service    https://www.diadata.org
Endpoints  2
Summary    What it does  DIA oracle price feeds over x402: transparent,
           multi-source aggregated token quotations across 80+ CEX/DEX markets
           for 3,000+ assets, through one provider with TRON, BSC and Base
           Mainnet payment routes.
Category   finance
Networks   tron, bsc, base
```

`Endpoints` 是该服务方提供的付费 API 数量——用 [`x402 endpoint-list`](endpoint-list.md) 可以列出它们及其 URL 和价格。`Networks` 是它接受付款的链。JSON 输出会返回该服务方的完整目录记录，包含全部端点。

## 输出

目录发布的服务方记录原样返回。主要字段：

| 字段 | 类型 | 含义 |
|---|---|---|
| `fqn` | string | 服务方名称 |
| `title` / `subtitle` / `description` | string | 展示名称与描述 |
| `serviceUrl` | string | 该服务方的网站 |
| `category` | string | 分类 id |
| `chains` | string[] | 它接受付款的链的 CAIP-2 id |
| `endpointCount` / `endpoints` | number / array | 它的端点——参见 [`x402 endpoint-list`](endpoint-list.md#output) |
| `minPriceUsd` / `maxPriceUsd` | number | 每次调用的价格区间，以 USD 计 |
| `status` | object | 目录、网关、支付和上游的状态 |

## 退出码

`0` 成功 · `1` 执行失败（`provider_not_found`——没有该名称的服务方；`provider_error`；`catalog_schema_unsupported`；`timeout`） · `2` 用法错误（`missing_option`——未给出服务方；`invalid_value`——名称中含有服务方名称不允许的字符，例如空格或 `..`）。

## 另请参见

[`x402 provider-list`](provider-list.md) · [`x402 endpoint-list`](endpoint-list.md)
