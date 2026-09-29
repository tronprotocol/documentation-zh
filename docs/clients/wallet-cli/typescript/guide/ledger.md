# 使用 Ledger 硬件钱包

密钥始终留在设备上；wallet-cli 负责构建交易，由 Ledger 在屏幕上确认并签名。私钥从不接触你的电脑。

## 前置条件

- Ledger 已连接、已**解锁**，并在设备上打开了你要用的 app——**TRON** 或 **Ethereum**；
- 该 app 事先已通过 Ledger Live 安装。

## 1. 注册 Ledger 账户

```bash
wallet-cli import ledger --app tron --index 0 --label cold
```

在本地这只会创建一条**仅观察**记录——不保存任何密钥；签名在设备上完成。

`--app` 决定链家族，而 Ledger 账户是**单家族**的：`--app tron` 注册出 `tron` 账户，`--app ethereum` 注册出 `evm` 账户，各自只持有那一个地址。这与软件账户不同——软件账户从同一份种子同时派生出 TRON *和* EVM 地址——Ledger 账户只能在其所属家族的网络上使用，用在别处会以 `family_mismatch` 失败。想同时持有两个，就用两个 app 各导入这台设备一次。

指定账户的三种方式（互斥）：

| 参数 | 适用场景 |
|---|---|
| `--index <n>` | 你知道该账户在 Ledger Live 中的索引 |
| `--path <bip32>` | 你需要显式指定派生路径，例如 `m/44'/195'/0'/0/0`（TRON）或 `m/44'/60'/0'/0/0`（以太坊） |
| `--address <addr>` | 你知道地址；wallet-cli 会逐个扫描索引来找到它（`--scan-limit`，默认 20） |

三者都省略时，若挂载了 TTY，会打开一个分页的账户选择器；非交互式运行没有选择器，会回落到索引 0。`--index <n>`、选择器和 `--address` 扫描都遵循 Ledger Live 的模板：TRON 为 `m/44'/195'/<n>'/0/0`，以太坊为 `m/44'/60'/<n>'/0/0`。软件账户用的是 `m/44'/<coin>'/0'/0/<n>`，因此除了索引 0 之外，相同的索引数字对应的是不同的地址。其他方案请用 `--path`。

用 `wallet-cli list` 确认——该账户会与你的软件账户并列出现，并且可以配合 `use`、`--account` 以及全部查询命令使用。

## 2. 签名并发送

命令本身没有任何变化：

```bash
wallet-cli tx send --to T... --amount 1 --network nile --account cold
```

CLI 不会提示输入密码，而是将交易详情显示在 **Ledger 屏幕上**。请在设备上核对收款方和金额后批准。
交易随后会正常广播，可通过 [`tx status`](../commands/tx/status.md) 查询状态。

这是你对抗地址替换类恶意软件的最佳防线：设备屏幕上显示的内容就是被签名的内容，与主机显示什么无关。

## 3. 设备没有响应时

设备调用与 RPC 受同一个 `--timeout` 限制（默认 60000 毫秒），失败时返回 `error.code: "timeout"`。请依次检查：

1. Ledger 是否已解锁，并且打开的是正确的 app——也就是注册该账户时用的那个，而不是主界面？
2. 重新插拔数据线；避免使用 USB 集线器。
3. 用更长的 `--timeout` 重试——设备上的确认时间也算在其中，请给自己留出阅读和按键的时间。

更多处理办法：[故障排查](../troubleshooting.md#timeout-exit-1)。

## 离线模式

Ledger 本身已经隔离了密钥，但你仍然可以把构建、签名和广播拆开。对于一台不能联网的签名机：在联网机器上构建 TRON 的未签名 hex 并给出明确的签名时间窗（`--build-only --expiration 3600000`），在接着 Ledger 的机器上用 `tx sign --offline` 签名，然后回到联网机器广播这段已签名 hex。TRON 的默认过期时间约为 60 秒——对跨机器流程通常太短；最长可设为 24 小时。EVM 产物没有过期参数。参见[脚本编写 → 此处签名、彼处广播](scripting.md#sign-here-broadcast-there)。

## 另请参见

[`import ledger` 帮助](../commands/import/index.md) · [安全模型](../concepts/security.md) · [快速上手](getting-started.md)
