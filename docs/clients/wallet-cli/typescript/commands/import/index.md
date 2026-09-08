# wallet-cli import

从已有的密钥或硬件设备导入钱包。

## 用法

```
wallet-cli import COMMAND
```

## 子命令

| 命令 | 说明 | 该账户会拥有的链家族 |
|---|---|---|
| [`import mnemonic`](mnemonic.md) | 导入一段 BIP39 助记词 | TRON **与** EVM |
| [`import private-key`](private-key.md) | 导入一个原始私钥 | TRON **与** EVM |
| [`import keystore`](keystore.md) | 导入一个 Web3 keystore 文件 | TRON **与** EVM |
| [`import ledger`](ledger.md) | 注册一个 Ledger 账户（本地仅观察；在设备上签名） | 由 `--app` 决定 |
| [`import watch`](watch.md) | 注册一个仅观察地址（不含任何密钥） | 由地址本身决定 |

密钥——无论是助记词、私钥还是 keystore——本身并不绑定某一条链：**同一把密钥**既能产生 TRON 地址，也能产生 EVM 地址，因此上面这三种导入方式得到的账户在两个家族上都可用。而 Ledger 账户和仅观察账户是单家族的，因为设备上的 app 和你粘贴的地址各自都只对应一个家族。

涉及密钥的三个子命令——`import mnemonic`、`import private-key`、`import keystore`——都是**仅交互式**的：每一项敏感信息都通过隐藏的 TTY 提示读取。没有 `--mnemonic-stdin` / `--private-key-stdin` 这类参数，`--password-stdin` 也会以 `invalid_option` 被拒绝；没有终端时命令会以 `tty_required` 失败。敏感信息绝不会经过命令行参数或环境变量。参见[machine-interface → 敏感信息处理](../../machine-interface.md#secret-handling)。

## 另请参见

[`create`](../create.md) · [`list`](../list.md) · [快速上手](../../guide/getting-started.md)
