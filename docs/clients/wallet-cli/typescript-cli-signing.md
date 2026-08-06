# TypeScript CLI 签名与安全

TypeScript CLI 支持软件 keystore、Ledger 账户和 watch-only 账户。软件私钥始终在本地加密保存，
Ledger 私钥绝不会离开设备，watch-only 账户可以查询状态，但不能签名。

## 签名现有交易 {#sign-an-existing-transaction}

`tx sign` 可以签名在 wallet-cli 之外构建的 TRON 交易，但不会广播：

```bash
printf '%s\n' "$WALLET_PASSWORD" |
  wallet-cli tx sign --transaction "$TX_JSON" --password-stdin --output json
```

对于软件账户，签名可以离线完成，`--network` 为可选项。该命令是一个纯签名器：它不会判断签名者
是否拥有该交易、合约调用是否符合预期，也不会判断应转移多少价值。调用方仍需负责策略检查。

### 交易完整性

TRON 交易通过三个相互关联的字段表示其内容：

| 字段 | 用途 |
|------|------|
| `raw_data` | 供用户和应用读取的交易内容。 |
| `raw_data_hex` | 节点实际执行的字节。 |
| `txID` | 签名覆盖的哈希。 |

签名前，wallet-cli 要求 `txID` 等于 `raw_data_hex` 的 SHA-256 哈希。它还会解码交易的外层封装，
并要求 `raw_data` 声明的合约类型与 `raw_data_hex` 中编码的类型一致。对于可以重新编码的合约类型，
它还要求 `raw_data` 的字段级内容重新编码后得到相同字节。任何不一致都会返回 `tx_integrity`，且不会
生成签名。

底层库无法重新编码 `MarketSellAssetContract`、`MarketCancelOrderContract` 和
`ShieldedTransferContract`。wallet-cli 仍会检查这类交易的哈希和合约类型，但无法将其 `raw_data`
字段值与 `raw_data_hex` 对照验证；调用方必须把显示的这些字段值视为未经验证的数据。

### 多签交易

如果输入已经包含 `signature` 数组，`tx sign` 会追加新签名，而不是替换已有签名。因此，同一笔部分
签名的交易可以依次传递给多个授权签名者，直到达到权限阈值。

提取已签名的载荷，稍后再广播：

```bash
printf '%s\n' "$WALLET_PASSWORD" |
  wallet-cli tx sign --transaction "$TX_JSON" --password-stdin --output json |
  jq -c '.data.signed' > signed.json

wallet-cli tx broadcast --network tron:nile --tx-stdin < signed.json
```

文本输出会打印完整签名，而不是缩写的交易标识符。

## 签名类型化数据

`typed-data sign` 用于签名 EIP-712/TIP-712 结构化数据，并返回签名者地址、推断或声明的主类型、
摘要和签名：

```bash
printf '%s\n' "$WALLET_PASSWORD" |
  wallet-cli typed-data sign \
    --typed-data "$TYPED_DATA_JSON" \
    --password-stdin \
    --output json
```

载荷采用常见的 `domain`、`types`、`primaryType` 和 `message` 结构。CLI 会：

- 忽略 `types` 中的 `EIP712Domain`；
- 接受 `value` 作为 `message` 的别名；
- 在 `address` 字段中接受 TRON Base58 地址；
- 在省略 `primaryType` 时进行推断，并报告最终解析出的类型；
- 拒绝不是消息根类型的已声明 `primaryType`。

`domain.chainId` 会严格按输入值参与签名，不会与 `--network` 比较。签名前请检查 domain 和 message。

## Ledger 行为

`tx sign` 和 `typed-data sign` 均支持 Ledger 账户。交易完整性检查同样会在软件签名和 Ledger
签名之前执行。

类型化数据签名使用 TRON 应用的哈希签名能力。请在设备上启用
**Settings > Sign by Hash > Allowed**，否则 CLI 会返回 `ledger_setting_required`。如果 TRON
应用版本不支持该指令，则返回 `ledger_unsupported`。

交易数据或自定义合约签名等其他 Ledger 应用设置，也会以可采取操作的
`ledger_setting_required` 错误报告，而不是返回含义不清的 APDU 错误。设备超时或取消操作后会关闭
传输连接，使后续尝试可以正常重新连接。

Ledger 屏幕无法显示类型化数据的全部字段，可能只显示哈希。批准操作前，请在主机上核对载荷。

## Secret 输入策略

Secret 绝不会通过命令行参数或环境配置接收。

支持的 stdin 通道如下：

| 标志 | 输入 |
|------|------|
| `--password-stdin` | 用于解锁软件 keystore 的 master password。 |
| `--tx-stdin` | `tx broadcast` 消费的已签名交易 JSON。 |
| `--message-stdin` | `message sign` 消费的消息。 |

单次调用中只能有一个 `*-stdin` 标志消费 stdin。

以下高敏感度的初始化操作只能交互执行，并要求从真实 TTY 隐藏输入：

- `import mnemonic`
- `import private-key`
- `change-password`

它们不接受 `--mnemonic-stdin`、`--private-key-stdin` 或 `--password-stdin`。没有 TTY 时，
命令会返回 `tty_required`。

## 失败行为

- watch-only 账户会在签名或写操作开始前返回 `watch_only_no_signer`。
- 无效的全局选项值会返回 `invalid_value`，而不是退回默认值。
- Ledger 设置和版本问题分别使用 `ledger_setting_required` 和 `ledger_unsupported`。
- 交易的多种表示不一致时返回 `tx_integrity`。
- 用户或设备拒绝签名时返回 `signing_rejected`。

JSON 模式会在单个 `wallet-cli.result.v1` 信封中返回这些错误码；执行失败使用退出码 1，无效用法
使用退出码 2。

完整的字段级命令参考，请参见
[`tx sign`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/tx/sign.md) 和
[`typed-data sign`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/typed-data/sign.md)。
