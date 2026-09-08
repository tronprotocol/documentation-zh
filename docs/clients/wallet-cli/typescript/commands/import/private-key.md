# wallet-cli import private-key

导入一个原始私钥。**仅交互式。**

> **注意**：这里没有 `--private-key-stdin` / `--password-stdin` 选项。私钥和 master password **只能**通过隐藏的 TTY 提示输入——私钥与助记词一样敏感，因此适用同样的限制。

## 用法

```
wallet-cli import private-key [--label <name>]
```

## 说明

从一个原始私钥导入单个账户，并用你的 master password 加密保存。与助记词导入不同，私钥账户没有 seed——无法从中派生出任何东西。导入的钱包会成为当前账户。

交互流程与 [`import mnemonic`](mnemonic.md) 一致：master password（隐藏）→ 标签 → 私钥（隐藏，绝不回显）→ 校验（不合法则报 `invalid_private_key` 并重新提示）并加密保存。没有 TTY 时，命令会以 `tty_required` 失败——本命令没有非交互式的路径。

## 选项

| 选项 | 说明 |
|---|---|
| `--label <string>` | 便于识别的唯一账户标签，1–64 个字符；省略则自动生成 |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli import private-key --label hot
```

```console
? Set master password (hidden):
? Confirm master password:
? Paste private key (hidden):
✅ Imported wallet "hot"
  Account ID    wlt_2qnr6j1f
  Type          private key
  TRON address  TMVQGm1qAQYVdetCeGRRkTWYYrLXuHK2HC
  EVM address   0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC
  Active        yes

⚠️ Private key was read from hidden input and was not printed.
```

```bash
wallet-cli import private-key --label hot -o json
```

```console
? Set master password (hidden):
? Confirm master password:
? Paste private key (hidden):
{"schema":"wallet-cli.result.v1","success":true,"command":"import.private-key","data":{"status":"created","accountId":"wlt_2qnr6j1f","label":"hot","type":"privateKey","index":null,"active":true,"addresses":{"tron":"TMVQGm1qAQYVdetCeGRRkTWYYrLXuHK2HC","evm":"0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC"},"derivationPath":null},"meta":{"durationMs":38,"warnings":[]}}
```

## 输出

`data` 携带导入的账户——只有地址，绝不含任何密钥。本地命令——没有 `chain` 块。

| 字段 | 类型 | 含义 |
|---|---|---|
| `status` | string | `"created"`；若同一把密钥已经存在，则为 `"existing"`（此时选中的是已有的那个账户） |
| `accountId` | string | 稳定的账户 id |
| `label` | string | 账户标签 |
| `type` | string | `"privateKey"`（独立私钥，没有 seed） |
| `index` | number \| null | 非 HD 账户，恒为 `null` |
| `active` | boolean | 是否成为当前账户 |
| `addresses` | object | 所导入密钥的两种编码形式：`tron`（base58）和 `evm`（EIP-55） |
| `derivationPath` | null | 原始私钥没有派生路径 |

## 退出码

`0` 导入成功 · `1` 执行失败（`auth_failed`——输入的 master password 与已有 keystore 不匹配；`invalid_private_key`——存储层校验拒绝了该私钥；`io_error`） · `2` 用法错误（`tty_required`——没有可用于隐藏输入的 TTY；`invalid_value`——标签非法或重复）。在 TTY 提示处输入的非法私钥或强度不足的新密码，会当场被拒绝并重新提示，而不会作为终止性错误返回。

## 另请参见

[`import mnemonic`](mnemonic.md) · [`backup`](../backup.md) · [`change-password`](../change-password.md) · [machine-interface → 敏感信息处理](../../machine-interface.md#secret-handling)
