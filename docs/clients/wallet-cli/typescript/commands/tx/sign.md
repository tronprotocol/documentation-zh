# wallet-cli tx sign

对在别处构建好的交易签名。

## 用法

```
wallet-cli tx sign (--hex <hex> | --file <path> | --transaction <json>) [--offline] [--out <path>] [options]
```

## 说明

对在别处构建好的一笔交易签名——在 TRON 上，它把当前账户的签名追加到一段未签名或部分签名的 hex 上，并报告已累计的签名权重距离该权限组的阈值还差多少；在 EVM 上，它产生这笔交易所需的那唯一一个签名。

两种输入模式：用 `--hex` / `--file` 时，它对交易 hex 签名（TRON 上是 protobuf，EVM 上是 RLP `0x02…`）；用 `--transaction` 时，它接收未签名的 TRON 交易 JSON，保留原来直接单签的流程。`--transaction` 是一条 TRON 兼容路径，从不访问节点。

**EVM 上没有联署这回事。** EVM 交易只带一个签名，因此已经带有签名的 hex 会以 `invalid_transaction` 被拒绝，也没有任何阈值、权重或权限组可供报告。交易内部的链 id 会与 `--network` 比对，不一致即为 `chain_id_mismatch`。

在 TRON 上，这是链上的联署路径：发起方用 `tx send --sign-only`（或任何支持 `--sign-only` 模式的广播命令）生成一段部分签名的 hex，各位联署人依次运行 `tx sign`——把 hex 一个人一个人地传下去——一旦权重达到阈值，任何人都可以用 [`tx broadcast --hex`](broadcast.md) 广播最终的 hex。所有签名都必须在交易过期之前收集完毕（默认约 60 秒，通过 `--expiration` 最长可延至 24 小时）。

签名意味着用你的密钥为这笔交易背书：软件账户从 `--password-stdin` 读取 master password 后直接签名，CLI 不展示任何预览；Ledger 账户则不读取 master password，改为在设备上确认。若想在不签名的前提下查看交易，请用 [`tx approvals`](approvals.md)。它**不会**广播，也**没有 `--permission-id`**（权限组已经固定在交易体里，会显示在 `Permission` 行上）。仅观察账户会以 `watch_only_no_signer` 失败。

### 签名前会校验什么

**TRON。** 使用 `--hex` / `--file` 时，命令会连接节点。只有当前账户属于交易指定权限组（否则返回
`not_authorized`），且尚未签署该交易（否则返回 `already_signed`）时，CLI 才会签名。这两项检查均在
解密密钥前完成，避免使用不符合条件的账户签名。

`--offline` 会跳过这两项检查，且完全不访问节点——适用于没有网络的签名机。此时与签名资格有关的错误只有在广播时才会暴露出来，所以请事先确认签名账户确实在权限组内。

**EVM。** 交易的链 id 必须与所选网络一致（否则 `chain_id_mismatch`），并且它不能已经带有签名（否则 `invalid_transaction`）。这两项都是本地检查；签名过程不访问任何节点，因此 `--offline` 在这里不起任何作用。

所有模式都会校验载荷完整性，离线模式也不例外。这套三方校验是 TRON 独有的——EVM 交易的哈希由它自身的字节算出，因此不存在互相矛盾的可能。TRON 交易会把自己的内容表述三遍——`raw_data`（你读到的）、`raw_data_hex`（节点实际执行的）和 `txID`（签名真正覆盖的），而格式本身并不强制三者一致，因此一笔 `raw_data` 上写着「1 TRX」的交易，完全可以带着一笔 1000 TRX 转账的 `txID`。为此 `tx sign` 会拒绝签名（`tx_integrity`），除非 `txID` 等于 `raw_data_hex` 的 sha256，并且在合约类型可解码时，`raw_data` 重新编码后与那串字节完全一致。

有三种合约类型无法被内置的解码器逐字段重新编码——`ShieldedTransferContract`、`MarketSellAssetContract` 和 `MarketCancelOrderContract`。它们不会被拒绝：命令仍会校验 `txID = sha256(raw_data_hex)`，并把声明的合约类型与 protobuf 外层绑定核对，但它无法独立证明 `raw_data` 里那些人类可读的字段与实际执行的字段一致。请把这些字段视为未经验证，签名前用能理解该合约类型的工具检查这份产物。`UnfreezeAssetContract` 由内置的 TRC10 编解码器完整重新编码，不在此列。

## 选项

| 选项 | 说明 |
|---|---|
| `--hex <hex>` | **必填**（三选一）。交易 hex——TRON 上是 `protocol.Transaction` protobuf，EVM 上是 RLP |
| `--file <path>` | **必填**（三选一）。包含交易 hex 的文件（hex 较长时建议用它） |
| `--transaction <json>` | **必填**（三选一）。**仅限 TRON。** 未签名的 TRON 交易 JSON；兼容路径，从不做联网校验 |
| `--offline` | 在本地签名而不访问节点；跳过签名者权限检查和批准权重检查。只能与 `--hex` / `--file` 同用，且只有在 TRON 上才有意义——EVM 签名本来就不访问节点 |
| `--out <path>` | 把已签名的交易原子地写入一个权限 0644 的文件——TRON 上是联署后的 protobuf hex，EVM 上是已签名的 RLP。它只是**额外**写出一个文件；同样的 hex 仍保留在结果体中，因此只想要摘要的调用方需要自行丢弃该字段。不能与 `--transaction` 同用 |

此外还有[全局选项](../index.md#global-options-every-command)，以及供软件账户使用的 `--password-stdin`。

交易通过 argv 传入，而不是 stdin：它不是机密信息，这样也能把 fd 0 留给 `--password-stdin`。

## 示例

示例中的 `$PW` 是你的 master password，通过 `--password-stdin` 从 stdin 传入。

发起方先用 `tx send --sign-only` 生成一份部分签名的 `tx.hex`：

```bash
echo "$PW" | wallet-cli tx send --to TF9yB7bAL2oBbonYaMvGTqoXxExS14x73c --amount 1000 --sign-only --permission-id 2 --expiration 86400000 --network nile --password-stdin > tx.hex
```

第二位软件签名者追加自己的签名；回执中包含交易内容和进度两个区块：

```bash
echo "$PW" | wallet-cli tx sign --file tx.hex --account cosigner --out tx.signed.hex --network nile --password-stdin
```

```console
✅ Signature added
  Signer  TNDHPk1LMLZTap8tMWfxUBy4MgArnWeSVP  (weight 1)
  Hex     written to tx.signed.hex

Transaction
  TxID        9c1...
  Type        Transfer TRX — 1,000 TRX
  From        TP2Zs9qKScTMs8jDYV3SAHQ5pqgKY1NQ5V
  To          TF9yB7bAL2oBbonYaMvGTqoXxExS14x73c
  Permission  active "finance" (id 2)  threshold 2
  Expires     2026-07-18 15:32 (in ~23h)

Progress  2 / 2 — threshold reached
| Approved signer                    | Weight |
| ---------------------------------- | ------ |
| TP2Zs9qKScTMs8jDYV3SAHQ5pqgKY1NQ5V | 1      |
| TNDHPk1LMLZTap8tMWfxUBy4MgArnWeSVP | 1      |
! Broadcast it: wallet-cli tx broadcast --file tx.signed.hex
```

使用 `--offline` 时无法获取权限组名称、阈值和各签名者权重，因此回执只包含可在本地推导的字段，并会明确标注这一限制。`Signatures` 表示签名**数量**，不是累计权重：

```bash
echo "$PW" | wallet-cli tx sign --file tx.hex --account cosigner --offline --network nile --password-stdin
```

```console
✅ Signature added
  Signer  TNDHPk1LMLZTap8tMWfxUBy4MgArnWeSVP
  Hex     0a02...9f31

Transaction (local inspection)
  TxID        9c1...
  Type        Transfer TRX — 1,000 TRX
  From        TP2Zs9qKScTMs8jDYV3SAHQ5pqgKY1NQ5V
  To          TF9yB7bAL2oBbonYaMvGTqoXxExS14x73c
  Permission  active (id 2)
  Signatures  1
  Expires     2026-07-18 15:32 (in ~23h)
! Approval state was not checked online. Inspect it with: wallet-cli tx approvals --hex <hex-above>
```

```bash
echo "$PW" | wallet-cli tx sign --file tx.hex --account cosigner --out tx.signed.hex --network nile --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"tx.sign","data":{"kind":"tx-sign","signer":"TNDHPk1LMLZTap8tMWfxUBy4MgArnWeSVP","hex":"0a02...9f31","checked":true,"transaction":{"txId":"9c1...","contractType":"TransferContract","operation":"Transfer TRX","from":"TP2Zs9qKScTMs8jDYV3SAHQ5pqgKY1NQ5V","to":"TF9yB7bAL2oBbonYaMvGTqoXxExS14x73c","rawAmount":"1000000000","permissionId":2,"expiration":1784388720000,"expired":false,"signatures":2},"signerWeight":1,"approval":{"txId":"9c1...","contractType":"TransferContract","operation":"Transfer TRX","from":"TP2Zs9qKScTMs8jDYV3SAHQ5pqgKY1NQ5V","to":"TF9yB7bAL2oBbonYaMvGTqoXxExS14x73c","rawAmount":"1000000000","permission":{"id":2,"name":"finance","threshold":2},"currentWeight":2,"missingWeight":0,"thresholdReached":true,"approved":[{"address":"TP2Zs9qKScTMs8jDYV3SAHQ5pqgKY1NQ5V","weight":1},{"address":"TNDHPk1LMLZTap8tMWfxUBy4MgArnWeSVP","weight":1}],"expiration":1784388720000,"expired":false,"signatures":2},"out":"tx.signed.hex"},"meta":{"durationMs":310,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
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

对于 TRON 的 `--hex` / `--file` 结果，`transaction` 在联网和离线两种模式下都存在，因此使用方可以无条件读取；而在访问 `approval` 之前，请先检查 `checked`。EVM 的结果里既没有 `transaction`，也没有 `checked`。

在 EVM 上，结果改为单签形态——`kind: "sign"`、`mode: "sign-only"`、`signed`（`{raw, hash}`）、`address`、`txId`——也就是 `tx send --sign-only` 输出的那种形态，因为一个签名就让交易完整了。顶层没有 `hex`：已签名的原始交易在 `signed.raw` 里，`--out` 会把这个字符串原样写入文件，同时仍将其保留在结果中。

`--transaction` 是仅限 TRON 的直接 JSON 路径，返回的结构与 TRON 上 `tx send --sign-only` 输出的相同：

| 字段 | 类型 | 含义 |
|---|---|---|
| `kind` | string | `"sign"` |
| `mode` | string | `"sign-only"` |
| `address` | string | 产生该签名的地址 |
| `txId` | string | 交易 id |
| `signed` | object | 已签名的 TRON 交易对象——正是 TRON 的 [`tx broadcast`](broadcast.md) 通过 `--transaction` / `--tx-stdin` 所接受的形态 |

`--transaction` 模式不会报告 `fee`：交易不是在这里构建的，也就没有做过任何估算。

## 退出码

`0` 成功 · `1` 执行失败（`tx_integrity`——TRON 的三种载荷表述互相矛盾；`invalid_transaction`——载荷不可用，或在 EVM 上该载荷已经签过名；`chain_id_mismatch`——该 EVM 交易是为另一条链构建的；`tx_expired`、`not_authorized`——该账户不在权限组的密钥列表中、`already_signed`、`watch_only_no_signer`、`auth_failed`、`signing_rejected`、`rpc_error`） · `2` 用法错误（`invalid_value`、`missing_option`；`invalid_option`——在 EVM 网络上使用了 `--transaction`）。

## 另请参见

[`tx approvals`](approvals.md) · [`tx broadcast`](broadcast.md) · [`tx multisig`](multisig.md) · [`permission show`](../permission/show.md)
