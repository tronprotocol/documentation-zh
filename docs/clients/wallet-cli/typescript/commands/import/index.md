# wallet-cli import

从已有的密钥或硬件设备导入钱包。

## 用法

```
wallet-cli import COMMAND
```

## 子命令

| 命令 | 说明 |
|---|---|
| [`import mnemonic`](mnemonic.md) | 导入 BIP39 助记词 |
| [`import private-key`](private-key.md) | 导入原始私钥 |
| [`import keystore`](keystore.md) | 从 Web3 keystore 文件导入账户 |
| [`import ledger`](ledger.md) | 注册 Ledger 账户（本地仅观察，在设备上签名） |
| [`import watch`](watch.md) | 注册一个仅观察地址；不保存任何密钥 |

三个涉及密钥的变体——`import mnemonic`、`import private-key`、`import keystore`——**只能交互执行**：每一项敏感信息都从隐藏的 TTY 提示中读取。它们没有 `--mnemonic-stdin` / `--private-key-stdin` 之类的参数，`--password-stdin` 会以 `invalid_option` 被拒绝，而在没有终端时命令会以 `tty_required` 失败。敏感信息绝不经过命令行参数或环境变量。参见 [machine-interface → 敏感信息处理](../../machine-interface.md#secret-handling)。

导入**密钥**并不与某条链绑定：助记词、私钥或 keystore 都会让该账户同时拥有 TRON 和 EVM 地址。而导入**地址或设备 app** 则是绑定的：`import watch` 取你粘贴的那个地址所属的家族，`import ledger` 取它 `--app` 所选的家族，因此这类账户只能在一个家族上使用。参见[账户与 HD 钱包](../../concepts/accounts-and-hd.md)。

## 另请参见

[`create`](../create.md) · [`list`](../list.md) · [快速上手](../../guide/getting-started.md)
