# wallet-cli tx approvals

查看一笔多签交易上已收集的签名。仅限 TRON。

## 用法

```
wallet-cli tx approvals (--hex <hex> | --file <path>) [options]
```

## 说明

以只读方式查看交易 hex 的联署进度：它使用的权限组和阈值、目前已累计的权重、已经批准的签名者列表、还差多少权重，以及过期时间。它是 [`tx sign`](sign.md) 的“先看后签”搭档——信息完全相同，但不会产生签名，也不需要账户或密码。

仅限 TRON——多签批准是 TRON 权限模型里的概念，因此在 EVM 网络上，本命令会在任何节点调用之前就以 `family_mismatch` 失败。

它需要节点（`--network`），因为批准状态——哪些签名有效、各自计多少权重——是由链给出的答案，无法仅凭交易本身推导出来。读取文件时有略大于 1 MiB 的大小上限，且必须是常规文件，不能是符号链接。

已过期的交易仍然可以查询（不会报错）：文本输出的 `Expires` 行会显示时间，后面跟上 ` [EXPIRED]`，并附带一条 `!` 提示要求重新发起；JSON 中的 `expired` 字段为 `true`。

## 选项

| 选项 | 说明 |
|---|---|
| `--hex <hex>` | **必填**（二选一）。`protocol.Transaction` hex 字符串 |
| `--file <path>` | **必填**（二选一）。包含交易 hex 的文件 |

此外还有[全局选项](../index.md#global-options-every-command)（`--network`）。

## 示例

```bash
wallet-cli tx approvals --file tx.hex --network tron:3448148188
```

```console
Transaction
  TxID        9c1...
  Type        Transfer TRX — 1,000 TRX
  From        TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw
  To          TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub
  Permission  active "finance" (id 2)  threshold 2
  Expires     2026-07-14 15:32 (in ~22h)

Progress  1 / 2 — 1 more weight needed
| Approved signer                    | Weight |
| ---------------------------------- | ------ |
| TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw | 1      |
```

```bash
wallet-cli tx approvals --file tx.hex --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"tx.approvals","data":{"txId":"9c1...","contractType":"TransferContract","operation":"Transfer TRX","from":"TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw","to":"TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub","rawAmount":"1000000000","permission":{"id":2,"name":"finance","threshold":2},"currentWeight":1,"missingWeight":1,"thresholdReached":false,"approved":[{"address":"TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw","weight":1}],"expiration":1784388720000,"expired":false,"signatures":1},"meta":{"durationMs":45,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `txId` | string | 交易 id |
| `contractType` | string | 原始合约类型枚举（例如 `TransferContract`） |
| `from` / `to` | string | 发送方 / 接收方 |
| `rawAmount` | string | 原始整数金额；单位取决于合约类型（TRX 为 SUN，TRC20/TRC10 为 token 最小单位） |
| `operation` | string | 人类可读的操作名，例如 `Transfer TRX` |
| `signatures` | number | 该交易当前携带的签名数量 |
| `permission` | object | 签名所用的权限组：`{id, name, threshold}` |
| `currentWeight` / `missingWeight` | number | 目前已累计的权重 / 还需要的权重 |
| `thresholdReached` | boolean | 是否已达到阈值 |
| `approved[]` | array | 已批准的签名者：`{address, weight}` |
| `expiration` | number | 过期时间（epoch 毫秒） |
| `expired` | boolean | 是否已经过期 |

## 退出码

`0` 成功 · `1` 执行失败（`invalid_transaction`、`rpc_error`） · `2` 用法错误（`invalid_value`）。

## 另请参见

[`tx sign`](sign.md) · [`tx broadcast`](broadcast.md) · [`permission show`](../permission/show.md)
