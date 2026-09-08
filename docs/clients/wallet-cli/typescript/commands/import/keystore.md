# wallet-cli import keystore

导入一个 Web3 keystore 文件。**仅交互式。**

> **注意**：这里没有任何 stdin 选项。master password 和 keystore 文件自身的密码**只能**通过隐藏的 TTY 提示输入——文件密码同样属于敏感密钥材料。

## 用法

```
wallet-cli import keystore <path> [--label <name>]
```

## 说明

从标准的 Web3 keystore JSON 导入单个账户——即 TronLink 导出的格式，也是 [`backup --keystore`](../backup.md) 写出的格式——并用你的 master password 加密保存。导入的钱包会成为当前账户。

一个 keystore 只保存**一个私钥**，因此得到的账户没有 seed，也无法从中派生任何东西，与 [`import private-key`](private-key.md) 完全一样。它的 `type` 记为 `privateKey`。

这里涉及两个相互独立的密码：master password 用于加密本地账户，keystore 密码用于解密导入文件。
CLI 会先读取文件并完成结构检查，再依次提示输入这两个密码，因此路径错误时不会要求输入密码。

没有 TTY 时，命令会以 `tty_required` 失败，退出码为 `2`，而且这项检查**最先**执行，排在读文件之前。在非交互环境中，无论路径正确与否，每次调用都会以同样的方式失败；上面"先读文件再要密码"的顺序只在你有终端时才成立。

导入操作**绝不会覆盖**已有账户。重复导入同一把密钥是幂等操作：命令返回 `status: "existing"`，并将
已有账户设为当前账户。如果该地址已由**其他类型**的账户持有，例如 HD 种子派生账户、仅观察账户或
Ledger 账户，命令会为同一地址新增一个独立的 `privateKey` 账户，不会替换原账户。keystore 解密完成
后的处理逻辑与 [`import private-key`](private-key.md) 相同。

## 选项

| 选项 | 说明 |
|---|---|
| `<path>` | **必填。** keystore JSON 文件的路径 |
| `--label <string>` | 便于识别的唯一账户标签，1–64 个字符；省略则自动生成 |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli import keystore ./tronlink-export.json --label imported
```

```console
? Master password (hidden):
? Keystore file password (hidden):
✅ Imported wallet "imported"
  Account ID    wlt_7h2k9m1a
  Type          private key
  TRON address  TZx9kP2m...7bWq
  EVM address   0xe4aAd11792F7E74f1B5cbce65f9a1E207c952961
  Active        yes

⚠️ The keystore password was read from hidden input and was not printed.
```

```bash
wallet-cli import keystore ./tronlink-export.json --label imported -o json
```

```console
? Master password (hidden):
? Keystore file password (hidden):
{"schema":"wallet-cli.result.v1","success":true,"command":"import.keystore","data":{"status":"created","accountId":"wlt_7h2k9m1a","label":"imported","type":"privateKey","index":null,"active":true,"addresses":{"tron":"TZx9kP2m...7bWq","evm":"0xe4aAd11792F7E74f1B5cbce65f9a1E207c952961"},"derivationPath":null},"meta":{"durationMs":44,"warnings":[]}}
```

## 输出

`data` 携带导入的账户——只有地址，绝不含任何密钥。本地命令——没有 `chain` 块。

| 字段 | 类型 | 含义 |
|---|---|---|
| `status` | string | `"created"`；若同一把密钥已存在，则为 `"existing"`，并将已有账户设为当前账户 |
| `accountId` | string | 稳定的账户 ID |
| `label` | string | 账户标签 |
| `type` | string | `"privateKey"`（独立私钥，没有 seed） |
| `index` | number \| null | 非 HD 账户，恒为 `null` |
| `active` | boolean | 是否成为当前账户 |
| `addresses` | object | 所导入密钥的两种编码形式：`tron`（base58）和 `evm`（EIP-55） |
| `derivationPath` | null | Web3 keystore 只包含一把原始密钥，没有派生路径 |

## 退出码

`0` 导入成功 · `1` 执行失败（`wrong_keystore_password`；`auth_failed`；`io_error`） · `2` 用法错误（`tty_required`——没有可用于交互输入的 TTY，此项先于其他一切检查；`keystore_not_found`——文件不存在；`invalid_keystore`——不是合法的 keystore JSON；`invalid_value`——标签重复或非法）。

## 另请参见

[`backup`](../backup.md) · [`import private-key`](private-key.md) · [`delete`](../delete.md) · [machine-interface → 敏感信息处理](../../machine-interface.md#secret-handling)
