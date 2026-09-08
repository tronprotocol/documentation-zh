# wallet-cli import ledger

注册一个 Ledger 账户。本地仅观察；在设备上签名。

## 用法

```
wallet-cli import ledger --app <tron|ethereum> [--index <n> | --path <bip32> | --address <addr>]
                         [--scan-limit <n>] [--label <l>] [options]
```

## 选项

| 选项 | 说明 |
|---|---|
| `--app <tron\|ethereum>` | **必填。** 要在设备上打开的 Ledger app；正是它决定了链家族和派生方案 |
| `--index <number>` | 在 wallet-cli 对应家族的路径模板下的账户索引。与 `--path` / `--address` 互斥 |
| `--path <string>` | 显式指定的派生路径，例如 `m/44'/195'/0'/0/0`（TRON）或 `m/44'/60'/0'/0/0`（以太坊） |
| `--address <string>` | 已知地址，通过有限范围扫描定位 |
| `--scan-limit <number>` | 配合 `--address` 时扫描的索引个数（默认 20） |
| `--label <string>` | 唯一的账户标签，1-64 个字符；省略则自动生成 |

此外还有[全局选项](../index.md)。

## 注意事项

该命令创建一条仅观察记录，不在本地保存任何密钥。执行前需解锁设备，并打开所选的 Ledger 应用。

三个定位参数都省略时，若挂载了 TTY，会打开一个分页的账户选择器（每次显示五个派生地址）。非交互式
场景不会显示选择器，而是默认使用索引 0；脚本中请显式传入 `--index`、`--path` 或 `--address`。

对以太坊来说，`--index <n>` 使用的是 wallet-cli 的 MetaMask 风格路径 `m/44'/60'/0'/0/<n>`。Ledger Live 常用的则是 `m/44'/60'/<n>'/0/0`；导入按那套方案创建的账户时，请显式指定 `--path`。

`--app` 决定 Ledger 账户所属的**单一链家族**：TRON 应用注册 `tron` 账户，以太坊应用注册 `evm`
账户，每个导入记录只包含一个地址。如需同时使用两个链家族，请分别打开对应应用并各导入一次。参见
[Ledger 指南](../../guide/ledger.md)。

## 示例

```bash
wallet-cli import ledger --app tron --index 0 --label cold
```

```console
✅ Registered Ledger account "cold"
  Account ID    wlt_7h2k9d3m
  App           tron
  Path          m/44'/195'/0'/0/0
  TRON address  TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ

⚠️ No private key is stored locally. Signing requires device confirmation.
```

以太坊 app 会从同一台设备注册出一个 EVM 账户：

```bash
wallet-cli import ledger --app ethereum --index 0 --label cold-evm
```

```bash
wallet-cli import ledger --app tron --index 0 --label cold -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"import.ledger","data":{"status":"created","accountId":"wlt_7h2k9d3m","label":"cold","type":"ledger","index":null,"active":true,"addresses":{"tron":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ"},"family":"tron","path":"m/44'/195'/0'/0/0"},"meta":{"durationMs":812,"warnings":[]}}
```

## 输出

`data` 携带新注册的 Ledger 账户——只有地址和派生路径，不含任何密钥。本地命令——没有 `chain` 块。

| 字段 | 类型 | 含义 |
|---|---|---|
| `status` | string | `"created"`；若该账户此前已注册，则为 `"existing"` |
| `accountId` | string | 稳定的账户 id |
| `label` | string | 账户标签 |
| `type` | string | `"ledger"`（在设备上签名） |
| `index` | number \| null | 非 HD 账户，恒为 `null`（设备上的索引体现在 `path` 中） |
| `active` | boolean | 是否成为当前账户 |
| `addresses` | object | 唯一的那个地址，以其家族为键——TRON app 为 `{"tron":"T…"}`，以太坊 app 为 `{"evm":"0x…"}` |
| `family` | string | 由 `--app` 选定的链家族——`tron` 或 `evm` |
| `path` | string | 设备上的派生路径 |

## 退出码

`0` 成功 · `1` 执行失败 · `2` 用法错误。参见 [machine-interface](../../machine-interface.md)。

## 另请参见

[Ledger 指南](../../guide/ledger.md) · [`import watch`](watch.md)
