# wallet-cli tx sign

对在别处构建好的交易签名。

## 用法

```
wallet-cli tx sign (--hex <hex> | --file <path> | --transaction <json>) [--offline] [--out <path>] [options]
```

## 说明

对在别处构建好的一笔交易签名——在 TRON 上，它把当前账户的签名追加到一段未签名或部分签名的 hex 上，并报告已累计的签名权重距离该权限组的阈值还差多少；在 EVM 上，它产生这笔交易所需的那唯一一个签名。

两种输入模式：用 `--hex` / `--file` 时，它对交易 hex 签名（TRON 上是 protobuf，EVM 上是 RLP `0x02…`）；用 `--transaction` 时，它接收未签名的 TRON 交易 JSON，保留原来直接单签的流程。`--transaction` 是一条 TRON 兼容路径，从不访问节点。

**EVM 上没有联署这回事。** EVM 交易只带一个签名，因此已经带有签名的 hex 会以 `invalid_transaction` 被拒绝，也没有任何阈值、权重或权限组可供报告。交易内部的链 id 会在签名**之前**与 `--network` 比对（`chain_id_mismatch`）——否则一笔主网交易被交给 `--network sepolia` 后，会返回一个对主网有效的合法签名，而下游没有任何环节能发现这一点。

在 TRON 上，该命令用于链上联署流程：发起方通过 `tx send --sign-only`（或其他支持 `--sign-only` 的交易构建命令）生成部分签名的 hex，各联署人依次接收该 hex 并运行 `tx sign` 添加签名。累计权重达到阈值后，任何人都可以使用 [`tx broadcast --hex`](broadcast.md) 广播最终交易。所有签名必须在交易过期前收集完毕；默认有效期约为 60 秒，可通过 `--expiration` 延长，最长为 24 小时。

签名意味着用你的密钥为这笔交易背书：软件账户从 `--password-stdin` 读取 master password 后直接签名，CLI 不展示任何预览；Ledger 账户则不读取 master password，改为在设备上确认。若想在不签名的前提下查看交易，请用 [`tx approvals`](approvals.md)。它**不会**广播，也**没有 `--permission-id`**（权限组已经固定在交易体里，会显示在 `Permission` 行上）。仅观察账户会以 `watch_only_no_signer` 失败。

### 签名前会校验什么

**TRON。** 使用 `--hex` / `--file` 时，命令会连接节点。只有当前账户属于交易指定权限组（否则返回
`not_authorized`），且尚未签署该交易（否则返回 `already_signed`）时，CLI 才会签名。这两项检查均在
解密密钥前完成，避免使用不符合条件的账户签名。

`--offline` 会跳过这两项检查，且完全不访问节点——适用于没有网络的签名机。此时与签名资格有关的错误只有在广播时才会暴露出来，所以请事先确认签名账户确实在权限组内。

**EVM。** 交易的链 id 必须与所选网络一致（`chain_id_mismatch`），并且它不能已经带有签名（`invalid_transaction`）。这两项都是本地检查；签名过程不访问任何节点。

所有模式都会校验交易数据完整性，离线模式也不例外。TRON 交易包含三种相关表示：`raw_data` 是可读的
交易内容，`raw_data_hex` 是节点实际执行的编码，`txID` 则是签名覆盖的哈希。格式本身不能保证三者
一致，因此攻击者可能让 `raw_data` 显示 1 TRX，却让实际签名内容对应 1000 TRX。为防止此类篡改，
`tx sign` 要求 `txID` 等于 `raw_data_hex` 的 SHA-256；对于可解码的合约类型，还要求 `raw_data`
重新编码后与 `raw_data_hex` 完全一致，否则返回 `tx_integrity` 并拒绝签名。

上面这套三方校验是 TRON 独有的；EVM 交易的哈希由它自身的字节算出，因此不存在互相矛盾的可能。

内置解码器无法对三种合约类型逐字段重新编码：`ShieldedTransferContract`、`MarketSellAssetContract` 和 `MarketCancelOrderContract`。命令不会直接拒绝这些交易：它仍会校验 `txID = sha256(raw_data_hex)`，并核对声明的合约类型与 protobuf 外层结构，但无法独立证明 `raw_data` 中的可读字段与实际执行字段一致。请将这些字段视为未经验证，并在签名前使用能够解析对应合约类型的工具检查交易产物。`UnfreezeAssetContract` 可由内置 TRC10 编解码器完整重新编码，不受此限制。

## 选项

| 选项 | 说明 |
|---|---|
| `--hex <hex>` | **必填**（三选一）。交易 hex——TRON 上是 `protocol.Transaction` protobuf，EVM 上是 RLP |
| `--file <path>` | **必填**（三选一）。包含交易 hex 的文件（hex 较长时建议用它） |
| `--transaction <json>` | **必填**（三选一）。**仅限 TRON。** 未签名的 TRON 交易 JSON；兼容路径，从不做联网校验 |
| `--offline` | 在本地签名而不访问节点；跳过签名者权限检查和批准权重检查。只有在 TRON 上才有意义——EVM 签名本来就不访问节点 |
| `--out <path>` | 将已签名交易以原子方式写入权限为 0644 的文件——TRON 写入联署后的 protobuf hex，EVM 写入已签名的 RLP。该选项只额外生成文件，同一 hex 仍保留在结果中；只需摘要的调用方应自行忽略该字段。不能与 `--transaction` 同用 |

此外还有[全局选项](../index.md#global-options-every-command)，以及供软件账户使用的 `--password-stdin`。

交易通过 argv 传入，而不是 stdin：它不是机密信息，这样也能把 fd 0 留给 `--password-stdin`。

## 示例

示例中的 `$PW` 是你的 master password，通过 `--password-stdin` 从 stdin 传入。

发起方先用 `tx send --sign-only` 生成一份部分签名的 `tx.hex`：

```bash
echo "$PW" | wallet-cli tx send --to TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub --amount 1000 --sign-only --permission-id 2 --expiration 86400000 --network tron:3448148188 --password-stdin > tx.hex
```

第二位软件签名者追加自己的签名；回执中包含交易内容和进度两个区块：

```bash
echo "$PW" | wallet-cli tx sign --file tx.hex --account cosigner --out tx.signed.hex --network tron:3448148188 --password-stdin
```

```console
✅ Signature added
  Signer  TXe4Kd8nP2rF9gH5jL3mV6cW1bN7yS0aQz  (weight 1)
  Hex     written to tx.signed.hex

Transaction
  TxID        9c1...
  Type        Transfer TRX — 1,000 TRX
  From        TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw
  To          TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub
  Permission  active "finance" (id 2)  threshold 2
  Expires     2026-07-14 15:32 (in ~23h)

Progress  2 / 2 — threshold reached
| Approved signer                    | Weight |
| ---------------------------------- | ------ |
| TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw | 1      |
| TXe4Kd8nP2rF9gH5jL3mV6cW1bN7yS0aQz | 1      |
! Broadcast it: wallet-cli tx broadcast --file tx.signed.hex
```

使用 `--offline` 时无法获取权限组名称、阈值和各签名者权重，因此回执只包含可在本地推导的字段，并会明确标注这一限制。`Signatures` 表示签名**数量**，不是累计权重：

```bash
echo "$PW" | wallet-cli tx sign --file tx.hex --account cosigner --offline --network tron:3448148188 --password-stdin
```

```console
✅ Signature added
  Signer  TXe4Kd8nP2rF9gH5jL3mV6cW1bN7yS0aQz
  Hex     0a02...9f31

Transaction (local inspection)
  TxID        9c1...
  Type        Transfer TRX — 1,000 TRX
  From        TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw
  To          TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub
  Permission  active (id 2)
  Signatures  1
  Expires     2026-07-14 15:32 (in ~23h)
! Approval state was not checked online. Inspect it with: wallet-cli tx approvals --hex <hex-above>
```

```bash
echo "$PW" | wallet-cli tx sign --file tx.hex --account cosigner --out tx.signed.hex --network tron:3448148188 --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"tx.sign","data":{"kind":"tx-sign","signer":"TXe4Kd8nP2rF9gH5jL3mV6cW1bN7yS0aQz","hex":"0a02...9f31","checked":true,"transaction":{"txId":"9c1...","contractType":"TransferContract","operation":"Transfer TRX","from":"TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw","to":"TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub","rawAmount":"1000000000","permissionId":2,"expiration":1784388720000,"expired":false,"signatures":2},"signerWeight":1,"approval":{"txId":"9c1...","contractType":"TransferContract","operation":"Transfer TRX","from":"TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw","to":"TBy6mQ7Y3nJ8sD2fWpXk4LhVc9Ra1Zt5Ub","rawAmount":"1000000000","permission":{"id":2,"name":"finance","threshold":2},"currentWeight":2,"missingWeight":0,"thresholdReached":true,"approved":[{"address":"TQkXm4vN8pR2sD6fWbYc3LhJa9Ee5Zt7Uw","weight":1},{"address":"TXe4Kd8nP2rF9gH5jL3mV6cW1bN7yS0aQz","weight":1}],"expiration":1784388720000,"expired":false,"signatures":2},"out":"tx.signed.hex"},"meta":{"durationMs":310,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

EVM 上对产物签名的结果则是单签形态：

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"tx.sign","data":{"kind":"sign","mode":"sign-only","signed":{"raw":"0x02f86b...","hash":"0x55b0068ef31bce39bbf5b06d456eaef307fd77f96d85ea291f48c1ae4b900d80"},"address":"0x88878d9250e68C574912f5618ad3b43f675B8888","txId":"0x55b0068ef31bce39bbf5b06d456eaef307fd77f96d85ea291f48c1ae4b900d80"},"meta":{"durationMs":84,"warnings":[]},"chain":{"family":"evm","network":"eip155:11155111","chainId":"11155111"}}
```

## 输出

两种输入模式返回的结构不同。

`--hex` / `--file`（对交易 hex 签名）：

| 字段 | 类型 | 含义 |
|---|---|---|
| `kind` | string | `"tx-sign"` |
| `signer` | string | 刚刚完成签名的地址 |
| `hex` | string | 追加了新签名之后的交易 hex |
| `checked` | boolean | 是否执行了联网的权限/批准校验——`--offline` 下为 `false` |
| `transaction` | object | 本地解码出的摘要：`txId`、`contractType`、`operation`、`from`、`to`、`rawAmount`、`permissionId`（只是一个标量——不含权限组名称和阈值）、`expiration`、`expired`、`signatures`（数量） |
| `signerWeight` | number | 该签名者在权限组中的权重。仅 TRON，且仅当 `checked` 为 `true` 时才有 |
| `approval` | object | 联网获取的权威批准状态，结构与 [`tx approvals`](approvals.md) 的 `data` 相同。仅 TRON，且仅当 `checked` 为 `true` 时才有 |
| `out` | string | 已签名 hex 的写入路径。仅在指定 `--out` 时出现；生成文件不会移除结果中的 hex |

EVM 使用单签结果结构：`kind: "sign"`、`mode: "sign-only"`、`signed`（`{raw, hash}`）、`address` 和 `txId`。顶层不含 `hex`，已签名的原始交易位于 `signed.raw`。指定 `--out` 时，该字符串会原样写入文件，并继续保留在结果中。

对于 TRON 的 `--hex` / `--file` 结果，`transaction` 在联网和离线两种模式下都存在，因此使用方可以无条件读取；而在访问 `approval` 之前，请先检查 `checked`。EVM 的结果里不含 `transaction` 和 `checked`。

`--transaction` 是仅限 TRON 的直接 JSON 路径，返回的结构与 TRON 上 `tx send --sign-only` 输出的完全一致：

| 字段 | 类型 | 含义 |
|---|---|---|
| `kind` | string | `"sign"` |
| `mode` | string | `"sign-only"` |
| `address` | string | 产生该签名的地址 |
| `txId` | string | 交易 id |
| `signed` | object | 已签名的 TRON 交易对象——正是 TRON 上 [`tx broadcast`](broadcast.md) 通过 `--transaction` / `--tx-stdin` 所接受的形式 |

`--transaction` 模式不会报告 `fee`：交易不是在这里构建的，也就没有做过任何估算。

## 退出码

`0` 成功 · `1` 执行失败（`tx_integrity`——TRON 交易数据的三种表示不一致、`invalid_transaction`——载荷不可用，或在 EVM 上这笔交易已经签过名、`chain_id_mismatch`——该 EVM 交易是为另一条链构建的、`tx_expired`、`not_authorized`——该账户不在权限组的密钥列表中、`already_signed`、`watch_only_no_signer`、`auth_failed`、`signing_rejected`、`rpc_error`） · `2` 用法错误（`invalid_value`、`missing_option`）。

## 另请参见

[`tx approvals`](approvals.md) · [`tx broadcast`](broadcast.md) · [`tx multisig`](multisig.md) · [`permission show`](../permission/show.md)
