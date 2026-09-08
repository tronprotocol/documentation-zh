# 快速上手

创建钱包、在 Nile 测试网上充值、查看余额、发送第一笔交易——整个流程大约 10 分钟。这里的所有操作都在 **Nile** 上运行（测试 TRX，没有真实价值）。

前置条件：已安装 wallet-cli——`wallet-cli --version` 能打印出版本号。如果不能，请见[安装](../index.md#install)。

## 1. 创建钱包

```bash
wallet-cli create --label main
```

命令会提示设置 **master password**，用于加密本地保存的所有密钥材料。该密码无法找回，必须至少包含
8 个字符，并同时包含大写字母、小写字母、数字和特殊字符。

**建议使用密码管理器。** 它可以生成高强度的唯一密码，并避免密码出现在 shell 历史、进程列表或明文文件中。任何提供命令行工具的密码管理器都可以；以下仅以 1Password 的 `op` 为例（请先安装并登录，参见[文档](https://developer.1password.com/docs/cli/)）。将 master password 保存为一个条目，然后读取它来创建钱包：

```bash
op read "op://Private/wallet-cli/password" | wallet-cli create --label main --password-stdin
```

`create` **不会**显示助记词，种子会以加密形式保存在本地。要创建恢复备份，请运行
[`backup`](../commands/backup.md)。该命令会生成一个权限为 `0600`、包含明文 BIP39 助记词的文件；
请将其离线保存。需要在其他机器上恢复钱包时，必须使用这份助记词备份。

已经有助记词或私钥了？改用 [`import mnemonic`](../commands/import/mnemonic.md) 或 [`import private-key`](../commands/import/private-key.md)。

确认新账户已经存在：

```bash
wallet-cli list
```

```console
HD  wlt_4473p34m
└─ [0] main  TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ  (active)
```

其中的 `T…` 是 TRON 地址，在所有 TRON 网络上都相同。`(active)` 表示命令默认使用的账户；可通过 `wallet-cli use <label>` 切换。

你的账户还有一个**EVM 地址**，由同一份种子派生而来——`list` 一次只显示一个链家族，因此传 `--network` 才能看到另一个：

```bash
wallet-cli list --network sepolia
```

```console
HD  wlt_4473p34m
└─ [0] main  0x3f9A1C74E5B2d80Af6C31e97b45D2a08c7E6F193  (active)
```

这两个是互相独立的地址，余额也互相独立；给其中一个充值不会让另一个多出一分。下面所有内容在两边的用法完全一样——把 `--network tron:3448148188` 换成 `--network sepolia`，金额单位就从 TRX 变成 ETH。参见[网络](../concepts/networks.md)。

## 2. 领取测试 TRX

打开 Nile 水龙头 [nileex.io/join/getJoinPage](https://nileex.io/join/getJoinPage)，找到 "Get 2000 test coins" 一节，粘贴你的 `T…` 地址，通过验证码并提交（每天一次；一分钟内到账）。然后确认已经到账：

```bash
wallet-cli account balance --network tron:3448148188
```

```console
Label    main
Balance  1,976.489 TRX
```

提示：把 Nile 设为默认网络，学习阶段就可以省略 `--network`：

```bash
wallet-cli config defaultNetwork tron:3448148188
```

## 3. 发送第一笔交易 {#3-send-your-first-transaction}

发送交易需要通过 `--password-stdin` 从 stdin 传入 master password：

```bash
printf '%s' "$MY_PASSWORD" | wallet-cli tx send --to TSx72ViULFepRGCS4PM5dP4FqD1d8qggCc --amount 1 --network tron:3448148188 --password-stdin
```

**提示——更推荐使用密码管理器**（第 1 步中已配置）。直接把密码从它管道传入：

```bash
op read "op://Private/wallet-cli/password" | wallet-cli tx send --to TSx72ViULFepRGCS4PM5dP4FqD1d8qggCc --amount 1 --network tron:3448148188 --password-stdin
```

交易会被签名并**提交**。提交不等于确认，请继续查询交易状态：

```bash
wallet-cli tx status --txid <the txid you got back> --network tron:3448148188
```

```console
TxID           7d9b6a08505537f7fd51ed4fb4223ce89098403d26e8d3fe07bdb3d625a46364
Status         confirmed ✅
Block          #70,433,563
Confirmations  1
```

`pending` 表示交易仍在处理中，应稍后再次查询；`failed` 表示交易已经入块，但链上执行失败（见[故障排查](../troubleshooting.md)）。想让 `tx send` 等待交易结果，请加上 `--wait`。

对某笔交易没把握？先演练一次——`--dry-run` 只构建交易并估算费用，不签名也不广播：

```bash
wallet-cli tx send --to TSx72ViULFepRGCS4PM5dP4FqD1d8qggCc --amount 1 --network tron:3448148188 --dry-run
```

## 4. 接下来看什么

- 发送 TRC20/TRC10 token（例如 USDT）：[发送 token](send-tokens.md)
- 不再为手续费燃烧 TRX：[质押与资源](stake-and-resources.md)
- 质押之后为超级代表投票并领取投票奖励：[`vote`](../commands/vote/index.md)、[`reward`](../commands/reward/index.md)
- 硬件钱包签名：[Ledger 指南](ledger.md)
- 完整的交易详情和交易回执：[`tx info`](../commands/tx/info.md)
- 你的历史记录和持仓：[`account history`](../commands/account/history.md)、[`account portfolio`](../commands/account/portfolio.md)
- 把这些操作自动化：[脚本编写指南](scripting.md)
- `tron:3448148188` / `eip155:11155111` 究竟是什么，以及哪些命令能在哪里运行：[网络](../concepts/networks.md)

> **主网操作提示**：主网 TRX 具有真实价值。请仔细核对收款地址，并优先执行 `--dry-run`；交易一旦
> 广播，发送方无法主动撤销，是否达到最终性仍取决于链上固化状态。
