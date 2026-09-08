# wallet-cli gasfree info

显示你的 GasFree 地址、激活状态、`nonce` 与费率表。

## 用法

```
wallet-cli gasfree info [options]
```

## 说明

通过服务方的 API 只读查看：该账户的 GasFree 地址（确定性派生）、它的激活状态和当前 `nonce`，以及服务方支持的 token 及其激活费和每笔转账费（均以该 token 本身计费）。

**GasFree 地址**是资产收付所用的地址——要通过 GasFree 收取 USDT，把这个地址给付款方即可。首次向外转账时，服务方会在链上激活它并收取激活费。费率表和受支持的 token 取自服务方的实时配置，因此输出就是 API 返回的内容。

需要服务方的 API 凭据（`gasfreeApiKey` / `gasfreeApiSecret`，用 [`config`](../config.md) 设置）。

## 选项

没有命令级选项；仅[全局选项](../index.md#global-options-every-command)（`--network` 用于选择服务环境，以及 `--account`）。

## 示例

```bash
wallet-cli gasfree info --account main --network tron:3448148188
```

```console
Owner            TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw
GasFree address  TVjsyZ7fYF3qCcNaMxN5PMWmSgYcCyqZfw
Status           active
Nonce            4

| Token | Balance  | Activation fee | Transfer fee |
| ----- | -------- | -------------- | ------------ |
| USDT  | 125 USDT | 1 USDT         | 0.5 USDT     |
```

```bash
wallet-cli gasfree info --account main --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"gasfree.info","data":{"ownerAddress":"TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw","gasFreeAddress":"TVjsyZ7fYF3qCcNaMxN5PMWmSgYcCyqZfw","active":true,"nonce":"4","tokens":[{"symbol":"USDT","address":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf","decimals":6,"activateFee":"1000000","transferFee":"500000","balance":"125000000"}]},"meta":{"durationMs":380,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `ownerAddress` | string | 该账户自身的 TRON 地址 |
| `gasFreeAddress` | string | 派生出的 GasFree 地址（收付款都用它） |
| `active` | boolean | GasFree 地址是否已在链上激活 |
| `nonce` | string | 该地址当前的 `nonce`，以无符号十进制字符串给出 |
| `tokens[]` | array | 受支持的 token：`{symbol, address, decimals, activateFee, transferFee, balance}`——费用和余额都是以该 token 最小单位计的十进制字符串 |

## 退出码

`0` 成功 · `1` 执行失败（`gasfree_integrity`——服务方在 token 列表与地址响应中给出的费用元数据自相矛盾；`provider_error`——服务出错、返回了格式错误或过大的 JSON、返回了本 CLI 不会据以行事的字段，或返回了任何非 429 的错误状态码；`provider_rate_limited`——服务返回了 429，若它给出了 `Retry-After`，则在 `details.retryAfter` 中） · `2` 用法错误（`gasfree_credentials_missing`、`unsupported_network`、`invalid_value`）。

## 另请参见

[`gasfree transfer`](transfer.md) · [`gasfree trace`](trace.md) · [`config`](../config.md)
