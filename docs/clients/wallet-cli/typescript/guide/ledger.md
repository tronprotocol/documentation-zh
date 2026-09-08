# 使用 Ledger 硬件钱包

密钥始终留在设备上；wallet-cli 负责构建交易，由 Ledger 在屏幕上确认并签名。私钥从不接触你的电脑。

## 前置条件

- Ledger 已连接、已**解锁**，并且设备上已打开对应的 app——TRON 账户用 **TRON app**，EVM 账户用**以太坊 app**；
- 该 app 事先已通过 Ledger Live 安装。

## 1. 注册 Ledger 账户

```bash
wallet-cli import ledger --app tron --index 0 --label cold
wallet-cli import ledger --app ethereum --index 0 --label cold-evm
```

该操作会在本地创建一条**仅观察**记录，不保存任何密钥材料；签名在设备上完成。有三种互斥的账户指定方式：

| 参数 | 适用场景 |
|---|---|
| `--index <n>` | 你知道该账户在 wallet-cli 对应家族路径模板下的索引 |
| `--path <bip32>` | 你需要一个明确的派生路径，例如 `m/44'/195'/0'/0/0`（TRON）或 `m/44'/60'/0'/0/0`（以太坊） |
| `--address <addr>` | 你知道地址；wallet-cli 会扫描索引来找到它（`--scan-limit`，默认 20） |

**`--app` 会把该账户限定在一个链家族上。** 软件账户可由同一份种子同时派生 TRON 和 EVM 地址，而 Ledger 账户只保存所选 app 派生出的地址，也只能用于对应家族的网络。在其他家族的网络上使用该账户会返回 `family_mismatch`。如果需要同时使用两个家族，请分别通过两个 app 导入一次设备。

未提供这三个定位参数时，如果挂载了 TTY，CLI 会显示分页的账户选择器；非交互式调用则默认使用索引 0。对于以太坊，wallet-cli 的 `--index <n>` 路径模板是 `m/44'/60'/0'/0/<n>`（MetaMask 风格），而 Ledger Live 常用 `m/44'/60'/<n>'/0/0`。请使用 `--path` 精确注册目标 Ledger Live 账户，不要假设两种路径的索引可以直接互换。

使用 `wallet-cli list` 确认导入结果：该账户会与软件账户并列显示，并且可以配合 `use`、`--account` 以及所有查询命令使用。`list` 一次只显示一个家族，因此 TRON app 的账户不会出现在 `--network sepolia` 的文本输出中，反之亦然；`-o json` 则会列出全部账户，不受此限制。

## 2. 签名并发送

命令本身没有任何变化：

```bash
wallet-cli tx send --to T... --amount 1 --network tron:3448148188 --account cold
```

CLI 不会提示输入密码，而是将交易详情显示在 **Ledger 屏幕上**。请在设备上核对收款方和金额后批准。
交易随后会正常广播，可通过 [`tx status`](../commands/tx/status.md) 查询状态。

这是你对抗地址替换类恶意软件的最佳防线：设备屏幕上显示的内容就是被签名的内容，与主机显示什么无关。

## 3. 设备没有响应时

设备调用与 RPC 受同一个 `--timeout` 限制（默认 60000 毫秒），失败时返回 `error.code: "timeout"`。请依次检查：

1. Ledger 是否已解锁，对应的 app 是否已打开（而不是停在主界面）？
2. 重新插拔数据线；不要使用 USB hub。
3. 用更长的 `--timeout` 重试——设备上的确认时间也计入其中，所以要给自己留出阅读和按键的时间。

更多处理办法：[故障排查](../troubleshooting.md#timeout-exit-1)。

## 离线模式

Ledger 已将密钥与主机隔离，但你仍然可以把构建、签名、广播三步拆开。如果连接设备的那台机器没有链访问权限，就在联网机器上构建 TRON 的未签名 hex，并显式给出签名窗口，例如 `--build-only --expiration 3600000`；再在插着 Ledger 的机器上用 `tx sign --offline` 签名；最后在联网机器上广播已签名的 hex。TRON 的默认过期时间约 60 秒，对跨机器流程来说通常太短；上限是 24 小时。EVM 的产物没有过期时间这个参数。参见[脚本编写 → 分离签名与广播](scripting.md#sign-here-broadcast-there)。

## 另请参见

[`import ledger` 帮助](../commands/import/index.md) · [安全模型](../concepts/security.md) · [快速上手](getting-started.md)
