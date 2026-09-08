# wallet-cli current

显示当前（活跃）账户。

## 用法

```
wallet-cli current [options]
```

## 选项

| 选项 | 说明 |
|---|---|
| `--qr` | 额外在终端中把**所选网络**的收款地址渲染成可扫描的 QR 码，下方打印完整地址以便人工核对；仅对文本输出有效 |

此外还有[全局选项](index.md)（`--account` 可覆盖显示哪个账户）。

一个账户在每个链家族下各有一个地址，文本输出会把它拥有的地址全部列出。`--network` 只决定 `--qr` 编码的是哪一个；它不会过滤这个列表，而且整个过程不访问任何节点。

## 示例

```bash
wallet-cli current
```

```console
Active account: main
  TRON address  TE9kPMtaMjfZN95CuPRsCHUQGWwx9EcJW8
  EVM address   0x7B28FE10FBccE88c3967ff0Fd64f1ffB46b46C9C
```

标题由 `data.active` 决定，而不是由是否传入 `--account` 决定。`--account` 指向非当前账户时显示
`Selected account:`；其他情况均显示 `Active account:`，包括显式指定当前账户时。

添加 `--qr` 后，命令会在地址列表下方用块状字符绘制可扫描的收款 QR 码，并在 `Receive address` 行
显示完整地址以供核对。该过程完全在本地完成，地址来自 keystore 元数据，不会访问节点：

```bash
wallet-cli current --qr
```

```console
Active account: main
  TRON address  TE9kPMtaMjfZN95CuPRsCHUQGWwx9EcJW8
  EVM address   0x7B28FE10FBccE88c3967ff0Fd64f1ffB46b46C9C

[ scannable QR code of the TRON address, drawn in the terminal ]
Receive address  TE9kPMtaMjfZN95CuPRsCHUQGWwx9EcJW8
```

QR 码编码的只有**一个**地址——所选网络对应的收款地址。用 `--network` 来选择是哪一个：

```bash
wallet-cli current --qr --network eip155:11155111
```

QR 码仅在能够正确对齐块状字符的终端中渲染。JSON 模式不会生成 QR 图案；此时 `--qr` 只用于确认
所选账户在该网络上存在地址，并将其写入 `data.receiveAddress`。如果文本终端为非交互式，或宽度不足以
显示完整 QR 码，命令会改为只输出地址并给出警告：

```console
warning: terminal is non-interactive or too narrow for a complete QR code; showing the full address only
```

```bash
wallet-cli current -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"current","data":{"accountId":"wlt_z259a1hq.0","label":"main","type":"seed","index":0,"active":true,"addresses":{"tron":"TE9kPMtaMjfZN95CuPRsCHUQGWwx9EcJW8","evm":"0x7B28FE10FBccE88c3967ff0Fd64f1ffB46b46C9C"},"seedId":"wlt_z259a1hq","derivationPath":{"tron":"m/44'/195'/0'/0/0","evm":"m/44'/60'/0'/0/0"}},"meta":{"durationMs":14,"warnings":[]},"chain":{"family":"tron","network":"tron:728126428","chainId":"728126428"}}
```

尚无当前账户时，命令会以 `missing_wallet_address` 失败（退出码 1）：

```bash
wallet-cli current
```

```console
error [missing_wallet_address]: no active account; import one first
```

## 输出

`data` 是一条账户记录，形状与 [`list`](list.md#output) 返回的一致。

| 字段 | 类型 | 含义 |
|---|---|---|
| `accountId` | string | 账户 ID |
| `label` | string | 账户标签 |
| `type` | string | `seed` / `privateKey` / `watch` / `ledger` |
| `index` | number \| null | HD 派生索引；非 HD 账户为 `null` |
| `active` | boolean | 当前账户为 `true`；`--account` 选中的是别的账户时为 `false` |
| `addresses` | object | 该账户能产生的每个家族各一项：`tron`（base58）和/或 `evm`（`0x`，EIP-55 校验和格式） |
| `derivationPath` | object \| null | 每个地址背后的 BIP32 路径：`seed` 账户是全部家族，`ledger` 账户是所选的那一条路径；`privateKey` 和 `watch` 从未派生过，因此为 `null` |
| `seedId` | string | 所属种子钱包 ID（仅 `seed` 账户） |
| `family` | string | 该账户绑定的链家族——仅单家族账户（`watch`、`ledger`）有此字段 |
| `receiveAddress` | string | 仅在请求了 `--qr` 时出现在 JSON 中；由 `--network` 选定的地址 |

`chain` 块回显的是用于显示的所选网络；本命令不访问任何节点。

## 退出码

`0` 成功 · `1` 执行失败 · `2` 用法错误。参见 [machine-interface](../machine-interface.md)。

## 另请参见

[`use`](use.md) · [`list`](list.md)
