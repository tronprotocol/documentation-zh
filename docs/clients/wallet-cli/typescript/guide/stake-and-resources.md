# 质押与资源

质押 TRX 可以获得能量和带宽资源，从而减少交易需要燃烧的 TRX。本文以 Nile 测试网为例说明 `stake`
命令的完整流程。**仅限 TRON**：EVM 网络使用 gas 为交易计价，不提供对应的资源质押机制，因此本页命令在 EVM 网络上都会返回 `family_mismatch`。背景知识见[能量与带宽](../concepts/energy-bandwidth.md)。

> **密码**：stake 写操作仅在需要签名的模式下使用 master password。为突出资源相关参数，以下示例省略了密码输入。使用软件账户签名时，请在命令前加上 `printf '%s' "$PW" |`，并在末尾添加 `--password-stdin`；也可以从密码管理器通过管道传入。`--dry-run`、`--build-only`、`stake info` 和 `stake delegated` 均无需密码。

## 1. 查看当前资源状态

先执行只读查询。[`stake info`](../commands/stake/info.md) 汇总质押数量、各类资源上限、待解质押和
TRON Power；如需查看资源的 `used / limit` 明细，请使用 `account info`：

```bash
wallet-cli account info --network tron:3448148188
```

```console
Label        main
Address      TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ
Balance      1,976.489 TRX
Staked       12 TRX (energy 12 + bandwidth 0)
Energy       used 0 / 888
Bandwidth    used 0 / 600
Created      2026-06-30
Permissions  owner 1-of-1, 1 active group
```

普通 TRX 转账消耗**带宽**，智能合约调用（包括 TRC20 转账）消耗**能量**。每个已激活账户都有少量免费带宽额度，示例中为 `0 / 600`。能量则只能通过质押获得；示例账户为能量质押了 12 TRX，因此显示 `0 / 888`（见 `Staked` 行），未质押时能量上限为 `0`。资源不足时，节点会从账户余额中燃烧 TRX 补足差额；质押可以减少这部分支出。

## 2. 质押并选择资源类型

`--amount-sun` 使用原始 SUN（1 TRX = 1,000,000 SUN）。为能量质押 100 TRX：

```bash
wallet-cli stake freeze --amount-sun 100000000 --resource energy --network tron:3448148188
```

`--resource` 决定质押所产生的资源类型，默认值为 `bandwidth`。发送 TRC20 token 或调用合约会消耗能量，因此这类用途应选择 `energy`（见第 1 步）。质押的 TRX 仍归账户所有，只是暂时锁定；同时还会获得 TRON Power（治理投票权）。与 stake 组的其他写操作一样，`stake freeze` 支持 `--dry-run`、`--sign-only`、`--build-only` 和 `--wait`，默认在交易提交后返回。

再次运行 `account info` 验证结果，`Energy` 上限会反映新增的质押：

```bash
wallet-cli account info --network tron:3448148188
```

## 3. 把资源代理给另一个地址

可以把质押产生的资源代理给其他地址。例如，将资源代理给热钱包后，热钱包无需自行质押 TRX 也能发起交易：

```bash
wallet-cli stake delegate --amount-sun 50000000 --resource energy --receiver TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH --network tron:3448148188
```

默认情况下，代理资源可以随时收回。添加 `--lock` 后，在锁定期结束前无法收回；锁定时长通过 `--lock-period <blocks>` 设置，每个区块约 3 秒。完成代理后，可以使用 [`stake delegated`](../commands/stake/delegated.md) 查看当前代理关系和最大可代理量。收回资源时使用 `stake undelegate`，并指定相同的数量、接收方和资源类型：

```bash
wallet-cli stake undelegate --amount-sun 50000000 --resource energy --receiver TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH --network tron:3448148188
```

## 4. 解质押、提取与取消

解质押不是即时的；链上规定了等待期——主网为 14 天（其他网络可能不同）：

```bash
# 第 1 步：申请解质押——资源立即失效，TRX 进入等待队列
wallet-cli stake unfreeze --amount-sun 100000000 --resource energy --network tron:3448148188

# 第 2 步（等待期结束后）：把已到期的解质押提取回余额
wallet-cli stake withdraw --network tron:3448148188

# 可选：到期前取消全部待处理的解质押
wallet-cli stake cancel-unfreeze --network tron:3448148188
```

`cancel-unfreeze` 是取消这次退出，而不是继续推进它——它对所有待处理的解质押是全有或全无的，因此你无法只回滚其中一部分。运行之后，`withdraw` 也就没有任何可领取的内容了。`withdraw` 领取的是所有已过等待期的部分。

## 另请参见

[能量与带宽](../concepts/energy-bandwidth.md)——这些命令背后的模型 · [`account info`](../commands/account/info.md) · 各 `stake` 子命令的完整参数参考：[`freeze`](../commands/stake/freeze.md) · [`unfreeze`](../commands/stake/unfreeze.md) · [`withdraw`](../commands/stake/withdraw.md) · [`cancel-unfreeze`](../commands/stake/cancel-unfreeze.md) · [`delegate`](../commands/stake/delegate.md) · [`undelegate`](../commands/stake/undelegate.md) · [`info`](../commands/stake/info.md) · [`delegated`](../commands/stake/delegated.md)
