# wallet-cli x402 provider-list

列出 x402 目录中的服务方。

## 用法

```
wallet-cli x402 provider-list [--network <id>] [--category <c>] [--capability <c>]
                              [--include-blocked] [--limit <n>] [--offset <n>] [options]
```

## 说明

列出 x402 目录（`https://x402-catalog.bankofai.io/api/catalog.json`）中的服务方——也就是你可以用 [`x402 pay`](pay.md) 调用的付费 API。每个服务方以其 `fqn` 命名，[`x402 provider-show`](provider-show.md) 和 [`x402 endpoint-list`](endpoint-list.md) 接收的就是它。

当 [`x402 update-catalog`](update-catalog.md) 写下的本地缓存有效时，它从缓存读取；只有缓存缺失、或缓存里没有所需内容时，才从目录下载。它从不写入缓存。

筛选条件：

- `--network` 与别处一样接收网络 id 或别名，保留在该链上收款的服务方——目前是主网 `tron:728126428`、`eip155:56` 和 `eip155:8453`。若某个网络上没有任何服务方收款（例如 Nile 测试网 `tron:3448148188`），返回空列表；未知网络则以 `unsupported_network` 失败。
- `--category` 接收分类 id，目前为 `finance`。
- `--capability` 匹配服务方的 `featuredTags`，例如 `security` 或 `defi`。

若 `--category` 或 `--capability` 的取值不在目录使用的范围内，会以 `invalid_value` 失败，并在 `error.details.matches` 中列出可接受的取值。

不需要钱包，也不需要密码。

## 选项

| 选项 | 说明 |
|---|---|
| `--network <id>` | 只列出在该链上有支付路由的服务方（网络 id 或别名） |
| `--category <c>` | 只列出该分类，例如 `finance` |
| `--capability <c>` | 只列出 `featuredTags` 中含有该标签的服务方 |
| `--include-blocked` | 把标记为已屏蔽的服务方也包含进来 |
| `--limit <n>` | 最大行数，1–200（默认 `20`） |
| `--offset <n>` | 跳过的行数（默认 `0`） |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli x402 provider-list
```

```console
| Provider             | Title       | Type | Category | Endpoints | Networks        | Tags                                                      |
| -------------------- | ----------- | ---- | -------- | --------- | --------------- | --------------------------------------------------------- |
| sunpump-token-launch | SunPump     |      | finance  | 1         | tron, bsc, base | sunpump, token-launch, agent-token, tron, bsc, base       |
| defillama            | DefiLlama   |      | finance  | 9         | tron, bsc, base | defillama, defi, tvl, paid                                |
| dexscreener          | DexScreener |      | finance  | 3         | tron, bsc, base | dexscreener, dex, new-pairs, meme, liquidity, price, paid |
| dia                  | DIA         |      | finance  | 2         | tron, bsc, base | dia, price, oracle, quotation, multi-source, paid         |
| goplus               | GoPlus      |      | finance  | 3         | tron, bsc, base | goplus, security, honeypot, risk, token-security, paid    |
```

`Provider` 就是要传给 [`x402 endpoint-list`](endpoint-list.md) 的名称。`Networks` 是接受付款的链，`Tags` 则是 `--capability` 所匹配的取值。`Type` 一列为空，因为目录并不发布服务方类型。

只看带 `security` 标签的服务方——这里是 GoPlus，它负责检查 token 和地址的风险：

```bash
wallet-cli x402 provider-list --capability security
```

```console
| Provider | Title  | Type | Category | Endpoints | Networks        | Tags                                                   |
| -------- | ------ | ---- | -------- | --------- | --------------- | ------------------------------------------------------ |
| goplus   | GoPlus |      | finance  | 3         | tron, bsc, base | goplus, security, honeypot, risk, token-security, paid |
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `catalog` | string | 目录 URL |
| `generatedAt` | string | 目录的生成时间 |
| `count` | number | 本页返回的服务方数量 |
| `filters` | object | 实际生效的筛选条件 |
| `results[]` | array | 目录发布的服务方记录原样返回——其中包括 `fqn`、`title`、`category`、`chains`、`endpointCount`、`minPriceUsd` / `maxPriceUsd`、`serviceUrl`、`featuredTags` 等。端点列表本身不含在内，请用 [`x402 endpoint-list`](endpoint-list.md) |

`meta.pagination` 中带有 `offset`、`limit` 和 `total`（全部匹配的服务方数）。文本输出只显示表格。

## 退出码

`0` 成功 · `1` 执行失败（`provider_error`——目录不可达或不合法；`catalog_schema_unsupported`；`response_too_large`；`timeout`） · `2` 用法错误（`unsupported_network`——`--network` 未知；`invalid_value`——`--category` / `--capability` 的取值不在目录使用范围内，或 `--limit` 越界）。

## 另请参见

[`x402 provider-show`](provider-show.md) · [`x402 endpoint-list`](endpoint-list.md) · [`x402 update-catalog`](update-catalog.md)
