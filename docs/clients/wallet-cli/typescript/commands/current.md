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

## 说明

一个账户在每个链家族下各有一个地址，文本输出会把它拥有的地址全部列出。`--network` 只决定 `--qr` 编码的是哪一个；它不会过滤这个列表，而且整个过程不访问任何节点。

## 示例

```bash
wallet-cli current
```

```console
Active account: main-1
  TRON address  TVz38F2QmQf53g7QVATBbsZ6JkHKccJFAQ
  EVM address   0xEA4A61822322c695F5A9eB7920b843054CbDaA83
```

```bash
wallet-cli current -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"current","data":{"accountId":"wlt_kwyjcwdh.1","label":"main-1","type":"seed","index":1,"active":true,"addresses":{"tron":"TVz38F2QmQf53g7QVATBbsZ6JkHKccJFAQ","evm":"0xEA4A61822322c695F5A9eB7920b843054CbDaA83"},"seedId":"wlt_kwyjcwdh","derivationPath":null},"meta":{"durationMs":18,"warnings":[]},"chain":{"family":"tron","network":"tron:728126428","chainId":"728126428"}}
```

加上 `--qr` 还会把所选网络的收款地址画成二维码，随后是一行带完整地址的 `Receive address`；`--network sepolia` 取的就是 EVM 地址：

```bash
wallet-cli current --qr
```

```console
Active account: main-1
  TRON address  TVz38F2QmQf53g7QVATBbsZ6JkHKccJFAQ
  EVM address   0xEA4A61822322c695F5A9eB7920b843054CbDaA83

[ QR code of the TRON address, drawn with block characters ]

Receive address  TVz38F2QmQf53g7QVATBbsZ6JkHKccJFAQ
```

绘制二维码需要一个足够宽的交互式终端；否则命令会打印 `warning: terminal is non-interactive or too narrow for a complete QR code; showing the full address only`，并只显示地址。

## 输出

`data` 是一条账户记录，形状与 [`list`](list.md#output) 返回的一致。

| 字段 | 类型 | 含义 |
|---|---|---|
| `accountId` | string | 账户 id |
| `label` | string | 账户标签 |
| `type` | string | `seed` / `privateKey` / `watch` / `ledger` |
| `index` | number \| null | HD 派生索引；非 HD 账户为 `null` |
| `active` | boolean | 当前账户为 `true`；`--account` 选中了其他账户时为 `false` |
| `addresses` | object | 该账户能产生的每个家族各一项：`tron`（base58）和/或 `evm`（`0x`，EIP-55 校验和格式） |
| `seedId` | string | 所属种子钱包 id（仅 `seed` 账户） |
| `derivationPath` | null | 恒为 `null`，这是刻意为之——`current` 不接收 master password，因此在不打开种子的情况下无法分辨旧 TRON 路径与当前路径；`derive` 和 `backup` 会报告经过校验的路径 |
| `receiveAddress` | string | 仅在给出 `--qr` 时才出现在 JSON 中；即 `--network` 所选的那个地址 |
| `family` | string | 该账户绑定的链家族——仅单家族账户（`watch`、`ledger`）有此字段 |
| `path` | string | 该账户在设备上的派生路径（仅 `ledger` 账户） |

`chain` 块回显的是用于显示的所选网络；本命令不访问任何节点。

## 退出码

`0` 成功 · `1` 执行失败 · `2` 用法错误。参见 [machine-interface](../machine-interface.md)。

## 另请参见

[`use`](use.md) · [`list`](list.md)
