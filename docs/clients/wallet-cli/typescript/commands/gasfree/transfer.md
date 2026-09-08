# wallet-cli gasfree transfer

签署一笔免 gas 转账并提交给 GasFree 服务方。

## 用法

```
wallet-cli gasfree transfer --to <address|contact> --amount <n> [--token <symbol>]
                            [--dry-run | --wait [--wait-timeout <ms>]] [options]
```

## 说明

用 TIP-712 结构化数据签名（TRON 版的 EIP-712）对转账签名，并提交给 GasFree 服务方，由它代你上链。不需要 TRX——每笔转账的服务费（首次转账再加一次性的激活费）在转账金额之外，从 GasFree 地址的 token 余额中扣除。

提交后会返回一个 **`traceId`**（服务方的受理 id）；此时转账只是被受理，**还没有上链**。加 `--wait` 可轮询服务方直到进入终态（`SUCCEED` / `FAILED`），也可以之后用 [`gasfree trace`](trace.md) 跟进。首次转账时 GasFree 地址尚未激活，这笔转账会自动带上激活动作，总扣除额 = 转账金额 + 服务费 + 激活费（回执和 `--dry-run` 中会分项列出）。

本命令没有 `--sign-only` / `--build-only`：签名负载与服务方的提交协议绑定，离线分发没有意义。需要一个账户和服务方凭据（`gasfreeApiKey` / `gasfreeApiSecret`，用 [`config`](../config.md) 设置）。只有在提交转账时才需要通过 `--password-stdin` 提供 master password；`--dry-run` 不解锁、也不签名。仅观察账户在提交时会以 `watch_only_no_signer` 失败。

## 选项

| 选项 | 说明 |
|---|---|
| `--to <address\|contact>` | **必填。** 收款地址，或[联系人簿](../contact/index.md)中的一个名称 |
| `--amount <n>` | **必填。** 以 token 单位计的金额（例如 `25` = 25 USDT）；费用在此之外另计 |
| `--token <symbol>` | 要转账的 token；必须是服务方支持的（见 `gasfree info`）——默认 `USDT` |
| `--dry-run` | 只做费用分项计算和余额检查；不签名、不提交、不需要密码 |
| `--wait` / `--wait-timeout <ms>` | 轮询服务方直到转账成功/失败（上限默认取配置 `waitTimeoutMs`，内置值 60000） |
| `--password-stdin` | 从 stdin 读取 master password |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

示例中的 `$PW` 是你的 master password，通过 `--password-stdin` 从 stdin 传入。

默认——提交并返回受理回执（一个 `traceId`，尚未上链）：

```bash
echo "$PW" | wallet-cli gasfree transfer --to TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub --amount 25 --network tron:3448148188 --password-stdin
```

```console
⏳ Submitted to GasFree — send 25 USDT
  Trace ID            7f3e9a02-58c1-4d2e-b6a4-91d0c3f8e527
  From                TNER12mMVWruqopsW9FQtKxCGfZcEtb3ER
  To                  TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub
  Service fee         0.5 USDT
  Activation fee      0 USDT
  Authorized max fee  1.5 USDT
  Total               25.5 USDT
  Status              waiting
! Track it: wallet-cli gasfree trace 7f3e9a02-58c1-4d2e-b6a4-91d0c3f8e527
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"gasfree.transfer","data":{"kind":"gasfree-transfer","stage":"submitted","traceId":"7f3e9a02-58c1-4d2e-b6a4-91d0c3f8e527","state":"WAITING","token":"USDT","tokenAddress":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf","decimals":6,"amount":"25000000","serviceFee":"500000","activateFee":"0","authorizedMaxFee":"1500000","totalDeducted":"25500000","owner":"TMVQGm1qAQYVdetCeGRRkTWYYrLXuHK2HC","from":"TNER12mMVWruqopsW9FQtKxCGfZcEtb3ER","to":"TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub","serviceProvider":"TKtWbdzEq5ss9vTS9kwRhBp5mXmBfBns3E","nonce":"8","deadline":"1700000060"},"meta":{"durationMs":650,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

加 `--wait` 可轮询至终态，输出链上 txid 和实际扣除额：

```bash
echo "$PW" | wallet-cli gasfree transfer --to TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub --amount 25 --network tron:3448148188 --wait --password-stdin
```

```console
✅ Sent 25 USDT via GasFree
  Trace ID            a41b6c88-0d2f-4e73-9a05-3c7d81f2b964
  TxID                d2e...
  From                TNER12mMVWruqopsW9FQtKxCGfZcEtb3ER
  To                  TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub
  Service fee         0.5 USDT
  Activation fee      0 USDT
  Authorized max fee  1.5 USDT
  Total               25.5 USDT
  Status              succeed
```

首次转账时 GasFree 地址还未激活，因此费用会分列服务费和一次性激活费，`Total` 也把激活费算在内：

```bash
wallet-cli gasfree transfer --to TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub --amount 25 --network tron:3448148188 --dry-run
```

```console
⏳ Dry run — GasFree transfer 25 USDT (not submitted)
  From                TNER12mMVWruqopsW9FQtKxCGfZcEtb3ER
  To                  TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub
  Service fee         0.5 USDT
  Activation fee      1 USDT
  Authorized max fee  1.5 USDT
  Total               26.5 USDT
  Status              not submitted
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"gasfree.transfer","data":{"kind":"gasfree-transfer","stage":"dry-run","token":"USDT","tokenAddress":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf","decimals":6,"amount":"25000000","serviceFee":"500000","activateFee":"1000000","authorizedMaxFee":"1500000","totalDeducted":"26500000","owner":"TMVQGm1qAQYVdetCeGRRkTWYYrLXuHK2HC","from":"TNER12mMVWruqopsW9FQtKxCGfZcEtb3ER","to":"TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub","serviceProvider":"TKtWbdzEq5ss9vTS9kwRhBp5mXmBfBns3E","nonce":"8","deadline":"1700000060"},"meta":{"durationMs":210,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 的内容随模式而变。金额和费用都是 token 的最小单位（字符串）：

| 模式 | 字段 |
|---|---|
| 默认（提交） | `kind: "gasfree-transfer"`、`stage: "submitted"`、`traceId`、服务方的 `state`、`token`、`tokenAddress`、`decimals`、`amount`、`serviceFee`、`activateFee`、`authorizedMaxFee`、`totalDeducted`、`owner`、`from`、`to`、`nonce`、`deadline`、`serviceProvider`；`--to` 传的是联系人名称时还有 `toContact` |
| `--wait`（已确认） | 同上，但 `stage: "confirmed"`、`state: "SUCCEED"`，服务方给出时还有 `txId` |
| `--wait`（失败） | 字段相同，但 `stage: "failed"`、`state: "FAILED"`，并可能带有服务方给出的 `failureReason` / `txId` |
| `--dry-run` | 与默认字段相同，但没有 `traceId` **和** `state`——这两项都来自服务方，而此模式根本不会调用它——且 `stage: "dry-run"`；不签名、不提交。文本输出会在缺失的 `state` 位置显示 `Status  not submitted` |

服务方返回失败状态时，CLI 命令本身仍可能执行成功，因此响应中的 `success` 为 `true`、退出码为 `0`。
这个视图里没有 `confirmed` 或 `failed` 布尔字段；程序应根据 `data.stage` / `data.state` 判断转账结果，而不是只检查退出码。参见
[脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)。

## 退出码

`0` 已提交（或试运行完成） · `1` 执行失败（`insufficient_token_balance`——token 余额 < 金额 + 服务费 [+ 激活费]；`gasfree_rejected`——服务方拒绝了该授权；`gasfree_integrity`——服务方给出的费用元数据自相矛盾；`watch_only_no_signer`；`auth_failed`；`signing_rejected`；`provider_error`——服务出错、返回了格式错误或过大的 JSON、返回了本 CLI 不会据以行事的字段，或返回了任何非 429 的错误状态码；`provider_rate_limited`——服务返回了 429） · `2` 用法错误（`gasfree_credentials_missing`、`unsupported_network`、`unsupported_token`、`invalid_value`、`invalid_amount`）。

## 另请参见

[`gasfree info`](info.md) · [`gasfree trace`](trace.md) · [`tx send`](../tx/send.md) · [`config`](../config.md)
