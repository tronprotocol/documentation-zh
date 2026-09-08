# wallet-cli tx multisig

通过 TronLink 服务创建 / 联署多签交易。仅限 TRON。

> `tx multisig` 仅限 TRON——在 EVM 网络上会以 `family_mismatch` 失败。它只能通过外部的 TronLink 多签服务工作，并且需要凭据（`tronlinkSecretId` / `tronlinkSecretKey` / `tronlinkChannel`）。它是一个可选的便利层——链上路径（[`tx sign`](sign.md) / [`tx approvals`](approvals.md) / [`tx broadcast`](broadcast.md)）不依赖任何服务就能完成同样的工作。没有凭据时该命令无法使用（`tronlink_credentials_missing`）。

## 用法

```
wallet-cli tx multisig [--create (--hex <unsigned-hex> | --file <path>) | --sign <txId> | --watch]
                       [options]
```

## 说明

链上路径是把 hex 在人与人之间传递，而服务路径则由 TronLink 服务**保管**交易、逐个**累计**签名，并通过 WebSocket 向联署人**推送**通知。该命令有四种互斥的模式：

- **默认（不带模式参数）**——列出服务上与该账户相关的多签交易及其进度。这是日常查看有哪些交易在等你处理的方式。
- **`--create`**——在本地对一笔**未签名**的交易签名并提交，从而开启一次签名收集。输入是未签名的 hex，由支持 `--build-only` 的交易构建命令生成（例如 `tx send … --build-only`）。软件账户需要 master password；Ledger 账户在设备上确认。
- **`--sign <txId>`**——联署某一笔交易：连同已收集到的签名一起取回，在本地签名，再把整笔交易提交回去交给服务累计。软件账户需要 master password；Ledger 账户在设备上确认。
- **`--watch`**——保持一条 WebSocket 连接，用等待你签名的交易**数量**来提醒你（不含任何详情）；要处理它们，请用默认模式把它们列出来。

### 创建签名收集时会添加发起方签名

签名收集不能以零个签名开始。服务根据提交交易中已有的签名计算初始权重，因此 `--create` 会先在本地
签名再提交，进度从 `1 / N` 开始。发起人之后无需重复签名，否则会返回 `already_signed`。

`--create` 会拒绝已经携带签名的交易（`invalid_value`）、已经过期的交易（`tx_expired`），以及权限组中不包含所选账户的交易（`not_authorized`）。

### 达到阈值之后

累计权重达到阈值后，**服务会自动广播交易**。因此 `--sign` 的输出会优先提示查询链上状态，只有服务
未完成广播时才需要手动提交。重复广播已上链的交易会返回 `transaction_rejected`
（`Transaction already exists.`）；这不会改变链上结果，但应通过查询确认交易状态。包含多个签名的
交易还会产生 1 TRX 的多签手续费。

`--watch` 只接收数量，绝不接收交易内容，因此监听不会泄露队列中有什么。它会一直运行到被中断（Ctrl-C、SIGINT/SIGTERM），然后报告一共收到了多少条通知。

凭据按环境（主网 / 测试网）分别配置；用 [`config`](../config.md) 设置。数据归服务所有；该命令不保留任何本地副本。

## 选项

| 选项 | 说明 |
|---|---|
| `--create` | 对 `--hex` / `--file` 传入的**未签名**交易签名，并以此开启一次签名收集；与 `--sign` / `--watch` 互斥 |
| `--hex <unsigned-hex>` / `--file <path>` | 未签名的交易（二选一，仅可与 `--create` 同用） |
| `--sign <txId>` | 按 32 字节 hex 形式的 txId 联署一笔待处理交易：取回 → 本地签名 → 提交回去；与 `--create` / `--watch` 互斥 |
| `--watch` | 保持一条 WebSocket 连接；用等待你签名的交易数量提醒你（不含详情）；与 `--create` / `--sign` 互斥 |

此外还有[全局选项](../index.md#global-options-every-command)，以及供软件账户使用的 `--password-stdin`（用于 `--create` 和 `--sign`）。

## 示例

示例中的 `$PW` 是某个软件账户的 master password，通过 `--password-stdin` 从 stdin 传入。

发起方先构建一笔**未签名**的交易（`--build-only`，并延长过期时间以便留出收集签名的余地），然后签名并提交，从而开启一次签名收集：

```bash
# --build-only 不签名，因此不需要 master password
wallet-cli tx send --to TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub --amount 1000 --permission-id 2 --build-only --expiration 86400000 --network tron:3448148188 > tx.unsigned.hex
```

```bash
echo "$PW" | wallet-cli tx multisig --create --file tx.unsigned.hex --network tron:3448148188 --password-stdin
```

```console
✅ Created on TronLink multi-sig service
  Signer  TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw  (weight 1)
  Hex     0a02...9f31

Transaction
  TxID        9c1...
  Type        Transfer TRX — 1,000 TRX
  From        TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw
  To          TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub
  Permission  active "finance" (id 2)  threshold 2
  Expires     2026-07-14 15:32 (in ~23h)

Progress  1 / 2 — 1 more weight needed
| Approved signer                    | Weight |
| ---------------------------------- | ------ |
| TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw | 1      |
! Each co-signer signs it with: wallet-cli tx multisig --sign 9c1...
```

联署人先列出在等自己处理的交易（默认模式），然后联署：

```bash
wallet-cli tx multisig --account cosigner --network tron:3448148188
```

```console
Multi-sig transactions — TronLink service (1 total)
| TxID   | Type             | Amount    | State        | Validation | Progress | Expires                    |
| ------ | ---------------- | --------- | ------------ | ---------- | -------- | -------------------------- |
| 9c1... | TransferContract | 1,000 TRX | awaiting you | verified   | 1 / 2    | 2026-07-14 15:32 (in ~22h) |
! Co-sign one with: wallet-cli tx multisig --sign <txId>
```

```bash
echo "$PW" | wallet-cli tx multisig --sign 9c1... --account cosigner --network tron:3448148188 --password-stdin
```

```console
✅ Signed & submitted
  Signer  TXe4Kd8nP2rF9gH5jL3mV6cW1bN7yS0aQz  (weight 1)
  Hex     0a02...9f31

Transaction
  TxID        9c1...
  Type        Transfer TRX — 1,000 TRX
  From        TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw
  To          TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub
  Permission  active "finance" (id 2)  threshold 2
  Expires     2026-07-14 15:32 (in ~22h)

Progress  2 / 2 — threshold reached
| Approved signer                    | Weight |
| ---------------------------------- | ------ |
| TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw | 1      |
| TXe4Kd8nP2rF9gH5jL3mV6cW1bN7yS0aQz | 1      |
! Threshold reached — the service broadcasts it. Confirm: wallet-cli tx info --txid 9c1...
  Not on chain: wallet-cli tx broadcast --hex 0a02...
```

列表模式的 JSON 输出：

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"tx.multisig","data":{"address":"TXe4Kd8nP2rF9gH5jL3mV6cW1bN7yS0aQz","total":1,"unreadable":0,"transactions":[{"verified":true,"txId":"9c1...","state":"pending","contractType":"TransferContract","originator":"TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw","owner":"TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw","permission":{"id":2,"name":"finance","threshold":2},"currentWeight":1,"missingWeight":1,"thresholdReached":false,"awaitingMySignature":true,"signedByCurrentAccount":false,"createdAt":1784385120000,"expiration":1784388720000,"expired":false,"signatures":1,"signatureProgress":[{"address":"TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw","weight":1,"signed":true,"signedAt":1784385130000},{"address":"TXe4Kd8nP2rF9gH5jL3mV6cW1bN7yS0aQz","weight":1,"signed":false,"signedAt":null}],"from":"TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw","to":"TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub","rawAmount":"1000000000"}]},"meta":{"durationMs":420,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

此外还可以用 WebSocket 接收提醒（只有数量——要看详情请把它们列出来）：

```bash
wallet-cli tx multisig --watch --account cosigner --network tron:3448148188
```

```console
Watching TronLink multi-sig service for tron:3448148188 … (Ctrl-C to stop)
🔔 You have 1 transaction(s) to sign — view them with: wallet-cli tx multisig

✅ Stopped watching TronLink multi-sig service
  Address        TXe4Kd8nP2rF9gH5jL3mV6cW1bN7yS0aQz
  Notifications  1
```

## 输出

`data` 的形态是有区分的：列表模式以 `transactions` 区分，其他模式以 `action` 区分。

**默认（列表）**

| 字段 | 类型 | 含义 |
|---|---|---|
| `address` | string | 读取该队列所针对的账户 |
| `total` | number | 服务报告的交易数量 |
| `unreadable` | number | 因本客户端无法解码而略去的记录数 |
| `transactions[].txId` | string | 交易 id |
| `transactions[].state` | string | `pending` \| `signed` \| `success` \| `failed` |
| `transactions[].verified` | boolean | 该记录是否与链上核对一致 |
| `transactions[].unverifiedReason` | string? | 仅当 `verified` 为 `false` 时才有 |
| `transactions[].contractType` | string | 服务方报告的合约类型 |
| `transactions[].from` / `to` | string? | 合约类型能给出时，解码得到的发送方与接收方 |
| `transactions[].rawAmount` | string? | 可用时解码得到的原始整数金额；单位取决于合约类型 |
| `transactions[].originator` / `owner` | string | 由谁创建 / 作用于谁的账户 |
| `transactions[].permission` | object | `id`、`name`、`threshold` |
| `transactions[].currentWeight` / `missingWeight` / `thresholdReached` | — | 批准进度 |
| `transactions[].awaitingMySignature` | boolean | 是否正在等待所选账户签名 |
| `transactions[].signedByCurrentAccount` | boolean | 该账户是否已经签过名 |
| `transactions[].createdAt` / `expiration` | number | 服务方的创建时间与交易过期时间，Unix 毫秒 |
| `transactions[].expired` | boolean | 该交易是否已经过期 |
| `transactions[].signatures` | number | 当前已附加的签名数量 |
| `transactions[].signatureProgress` | array | 每把密钥的 `address`、`weight`、`signed`，以及可为 null 的 `signedAt` |

客户端无法与链上核对一致的记录仍会显示出来并被标注，而不会让整页查询失败。

**`--create` / `--sign`**

| 字段 | 类型 | 含义 |
|---|---|---|
| `signer` / `signerWeight` | string / number | 刚刚完成签名的地址，及其权重 |
| `hex` | string | 包含目前已收集到的全部签名的交易 hex |
| `transaction` | object | 交易摘要 + 批准进度 |

`--watch` 会持续输出数量提醒。停止时，它在 JSON 模式下的终止结果是 `{action: "watch", address, notifications}`；text 模式下打印同样的地址和通知条数。

## 退出码

`0` 成功 · `1` 执行失败（`not_found`——服务上没有该 txId、`not_authorized`、`already_signed`、`tx_expired`、`auth_failed`、`provider_error`——服务出错 / 触发限流） · `2` 用法错误（`tronlink_credentials_missing`、`unsupported_network`、`invalid_value`——包括把已签名的交易传给 `--create`、模式冲突）。

## 另请参见

[`tx sign`](sign.md) · [`tx approvals`](approvals.md) · [`tx broadcast`](broadcast.md) · [`config`](../config.md) · [`permission show`](../permission/show.md)
