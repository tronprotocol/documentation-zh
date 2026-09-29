# wallet-cli import mnemonic

导入一段 BIP39 助记词。**仅交互式。**

> **注意**：这里没有 `--mnemonic-stdin` / `--password-stdin` 选项。助记词和 master password **只能**通过隐藏的 TTY 提示输入——一段助记词足以取走全部资金，而走 stdin 太容易泄漏到管道、shell 历史和进程列表里。导入本身并不频繁，强制人工输入的代价很小。

## 用法

```
wallet-cli import mnemonic [--label <name>]
```

## 说明

从已有的 BIP39 助记词恢复一个 HD 钱包：派生出 #0 号账户，并用你的 master password 加密保存 seed。导入的钱包会成为当前账户。

交互流程（所有密钥均隐藏输入，绝不回显，也绝不出现在 argv 中）：

1. **master password**——首次使用时设置（需确认一次），或输入以解锁。
2. **标签**——可选的显示名；留空则自动生成一个（例如 `wallet_ad8f21`）。
3. **助记词**——以隐藏方式粘贴输入；驱动 CLI 的 AI 或脚本绝不会看到它。
4. **校验并存储**——词数/校验和不对 → `invalid_mnemonic`，重新提示；成功则派生出各地址，并把种子加密写入，绝不明文保存。

没有 TTY 时，命令会以 `tty_required` 失败——本命令没有非交互式的路径。

## 选项

| 选项 | 说明 |
|---|---|
| `--label <string>` | 便于识别的唯一账户标签，1–64 个字符；省略则自动生成 |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli import mnemonic --label restored
```

```console
? Set master password (hidden):
? Confirm master password:
? Paste recovery phrase (hidden):
✅ Imported wallet "restored"
  Account ID    wlt_d66fvems.0
  Type          HD
  TRON address  TWer2Ygk5TEheHp3TPuYeqxmB6SsGZmaL6
  EVM address   0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
  Active        yes

⚠️ Recovery phrase was read from hidden input and was not printed.
```

```bash
wallet-cli import mnemonic --label restored -o json
```

```console
? Set master password (hidden):
? Confirm master password:
? Paste recovery phrase (hidden):
{"schema":"wallet-cli.result.v1","success":true,"command":"import.mnemonic","data":{"status":"created","accountId":"wlt_d66fvems.0","label":"restored","type":"seed","index":0,"active":true,"addresses":{"tron":"TWer2Ygk5TEheHp3TPuYeqxmB6SsGZmaL6","evm":"0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"},"seedId":"wlt_d66fvems","derivationPath":{"tron":"m/44'/195'/0'/0/0","evm":"m/44'/60'/0'/0/0"}},"meta":{"durationMs":38,"warnings":[]}}
```

## 输出

`data` 携带导入的账户——只有地址，绝不含任何密钥。本地命令——没有 `chain` 块。

| 字段 | 类型 | 含义 |
|---|---|---|
| `status` | string | `"created"`；若该助记词的 0 号账户此前已存在，则为 `"existing"`（并选中那个账户） |
| `accountId` | string | 稳定的 id，形如 `<seedId>.<index>` |
| `label` | string | 账户标签 |
| `type` | string | `"seed"`（HD 派生） |
| `index` | number | HD 派生索引（第一个账户为 0） |
| `active` | boolean | 是否成为当前账户 |
| `addresses` | object | 派生出的两个地址：`tron`（base58）和 `evm`（EIP-55） |
| `derivationPath` | object | 索引 0 账户按家族给出的 BIP44 路径 |
| `seedId` | string | 所属种子钱包 id |

## 退出码

`0` 导入成功 · `1` 执行失败（`auth_failed`——输入的 master password 与已有 keystore 不匹配；`invalid_mnemonic`——存储层校验拒绝了该助记词；`io_error`） · `2` 用法错误（`tty_required`——没有可用于隐藏输入的 TTY；`invalid_value`——标签非法或重复）。在提示处输入的无效助记词或过弱的新密码会当场被拒并要求重输，而不会作为终态错误返回。

## 另请参见

[`import private-key`](private-key.md) · [`create`](../create.md) · [`change-password`](../change-password.md) · [故障排查](../../troubleshooting.md)
