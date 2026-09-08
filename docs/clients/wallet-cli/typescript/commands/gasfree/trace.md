# wallet-cli gasfree trace

用 `traceId` 跟踪一笔已提交的 GasFree 转账。

## 用法

```
wallet-cli gasfree trace <traceId> [options]
```

## 说明

用 [`gasfree transfer`](transfer.md) 返回的 `traceId` 查询一笔 GasFree 转账，报告它当前的状态。转账一旦上链，响应中还会包含交易 id 和实际扣除的费用。

服务方定义的状态依次是：`WAITING`（已受理，排队中）→ `INPROGRESS`（已在链上提交）→ `CONFIRMING`（等待固化）→ `SUCCEED` / `FAILED`。文本输出的 `Status` 行用小写显示状态（与其他命令保持一致）；原始的大写枚举值保留在 JSON 的 `state` 中。状态为 `FAILED` 时，会原样带上 API 返回的失败原因。

需要服务方的 API 凭据（`gasfreeApiKey` / `gasfreeApiSecret`，用 [`config`](../config.md) 设置）。

## 选项

没有命令级选项；`traceId` 是位置参数，此外还有[全局选项](../index.md#global-options-every-command)（`--network`）。

## 示例

```bash
wallet-cli gasfree trace 7f3e9a02-58c1-4d2e-b6a4-91d0c3f8e527 --network tron:3448148188
```

```console
Trace ID        7f3e9a02-58c1-4d2e-b6a4-91d0c3f8e527
Status          succeed
TxID            d2e...
Token           USDT
Amount          25 USDT
Service fee     0.5 USDT
Activation fee  0 USDT
Total           25.5 USDT
To              TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub
```

```bash
wallet-cli gasfree trace 7f3e9a02-58c1-4d2e-b6a4-91d0c3f8e527 --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"gasfree.trace","data":{"traceId":"7f3e9a02-58c1-4d2e-b6a4-91d0c3f8e527","state":"SUCCEED","txId":"d2e...","token":"USDT","tokenAddress":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf","decimals":6,"amount":"25000000","serviceFee":"500000","activateFee":"0","totalDeducted":"25500000","from":"TNER12mMVWruqopsW9FQtKxCGfZcEtb3ER","owner":"TMVQGm1qAQYVdetCeGRRkTWYYrLXuHK2HC","to":"TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub","nonce":"8"},"meta":{"durationMs":290,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `traceId` | string | 服务方的受理 id |
| `state` | string | 原始状态枚举：`WAITING` / `INPROGRESS` / `CONFIRMING` / `SUCCEED` / `FAILED` |
| `txId` | string | 链上交易 id（提交上链后才有） |
| `token` | string | Token 符号 |
| `tokenAddress` | string | TRC20 合约地址 |
| `decimals` | number | 用于渲染金额的 token 精度 |
| `amount` | string | 金额，以 token 的最小单位计 |
| `serviceFee` / `activateFee` | string | 扣除的费用，以 token 的最小单位计 |
| `totalDeducted` | string | 转账金额加上已结算的服务费与激活费，以 token 的最小单位计 |
| `from` / `owner` | string | GasFree 托管地址 / 所属账户地址 |
| `to` | string | 接收方地址 |
| `nonce` | string | 授权 nonce |
| `failureReason` | string | 服务方给出的说明，仅在转账失败且服务方提供时出现 |

## 退出码

`0` 成功 · `1` 执行失败（`not_found`——`traceId` 不存在；`gasfree_integrity`；`provider_error`——服务出错、返回了格式错误或过大的 JSON、返回了本 CLI 不会据以行事的字段，或返回了任何非 429 的错误状态码；`provider_rate_limited`——服务返回了 429） · `2` 用法错误（`gasfree_credentials_missing`、`unsupported_network`、`invalid_value`）。

转账结果为 `FAILED` 时，查询命令本身仍然执行成功：响应中的 `success` 保持为 `true`，退出码为 `0`，
`data.failureReason` 提供服务方返回的失败原因。

## 另请参见

[`gasfree transfer`](transfer.md) · [`gasfree info`](info.md) · [`config`](../config.md)
