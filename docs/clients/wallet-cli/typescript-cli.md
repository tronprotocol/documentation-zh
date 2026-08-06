# TypeScript / npm CLI

从 `wallet-cli` 仓库的 4.9.7 发布版本开始，仓库同时提供一个面向智能体优先设计的 TypeScript CLI。
该 CLI 以 npm 包 `@tron-walletcli/wallet-cli` 发布，并采用独立的 npm 版本号；`wallet-cli --version`
显示的是 npm 包版本。它与本节其他页面介绍的 Java JAR 是两套命令面：Java CLI 使用 `send-coin`
这类命令，而 TypeScript CLI 使用 `tx send` 这类分组命令。

当前 TypeScript CLI 支持 TRON 主网、Nile 和 Shasta，尚不支持 EVM 链。

## 安装

需要 Node.js 20 或更高版本。

```bash
npm install -g @tron-walletcli/wallet-cli
wallet-cli --version
wallet-cli --help
```

## 快速开始

创建本地 HD 钱包，选择该钱包，并使用 Nile 进行测试交易：

```bash
wallet-cli create --label main
wallet-cli list
wallet-cli use main
wallet-cli current
wallet-cli config defaultNetwork tron:nile
wallet-cli account balance
```

也可以只为某一条命令临时指定网络，而不修改默认网络：

```bash
wallet-cli account balance --network tron:nile
```

## 全局选项

常用全局选项包括：

| 选项 | 说明 |
|--------|-------------|
| <code>--output text&#124;json</code>, <code>-o</code> | 选择 text 或 JSON 输出。 |
| `--network` | 网络 ID，例如 `tron:mainnet`、`tron:nile` 或 `tron:shasta`。 |
| `--account` | 账户 ID、标签或地址；默认使用 `use` 设置的 active account。 |
| `--timeout` | 每次 RPC/设备调用的超时时间，单位为毫秒。 |
| `--verbose`, `-v` | 输出更多诊断信息。 |
| `--wait` | 广播后轮询，直到交易 confirmed 或 failed。 |
| `--wait-timeout` | `--wait` 轮询的上限，单位为毫秒；默认使用 `config.waitTimeoutMs`（内置值为 60000）。 |
| `--password-stdin` | 从 stdin 读取 master password。 |

命令级 stdin 标志为 `--tx-stdin` 和 `--message-stdin`。它们与全局的 `--password-stdin`
合计只能有一个 `*-stdin` 标志在单次调用中消费 stdin。

可以使用 `wallet-cli config` 持久化默认值。例如：

```bash
wallet-cli config waitTimeoutMs 90000
```

## 钱包和账户

TypeScript CLI 默认把数据保存在 `~/.wallet-cli`。可通过 `WALLET_CLI_HOME` 隔离测试或自动化数据。

```bash
WALLET_CLI_HOME=/tmp/wallet-cli-demo wallet-cli list --output json
```

常用钱包命令：

```bash
wallet-cli create --label main
wallet-cli import mnemonic --label imported
wallet-cli import private-key --label hot
wallet-cli import watch --address T... --label treasury
wallet-cli import ledger --app tron --index 0 --label cold
wallet-cli list
wallet-cli use main
wallet-cli current
wallet-cli rename main --label primary
wallet-cli backup primary --out ~/primary-backup.json
wallet-cli change-password
```

`import mnemonic`、`import private-key` 和 `change-password` 只能交互执行。它们要求使用真实终端，
并通过隐藏提示读取 secret，不提供非交互式 stdin 替代方式。

以非交互方式使用 `derive`、`backup` 和 `tx sign` 等命令时，通过 `--password-stdin` 传入 master
password。使用 Ledger 账户签名时，不要通过管道传入密码，也不要传入 `--password-stdin`。下方
`derive` 示例展示了完整的非交互式写法。为了保持后续示例简洁，其中可能省略密码输入管道和
`--password-stdin`。

派生 HD 子账户时，需要传入 `wallet-cli list` 显示的 HD seed id。

```bash
printf '%s\n' "$WALLET_PASSWORD" |
  wallet-cli derive --seed-id wlt_ab12cd34 --label operations --password-stdin
```

删除根 HD 钱包会级联删除从该根派生出的账户，并清理孤立标签。在非交互式 shell 中需要传入 `--yes`；
否则命令会要求确认。

```bash
wallet-cli delete old --yes
```

## 交易

通过 `--amount` 传入的是人类可读金额。使用 `--raw-amount` 可传入 SUN 或 token 基础单位。

```bash
wallet-cli tx send --to T... --amount 1 --dry-run
wallet-cli tx send --to T... --amount 1 --wait
wallet-cli tx send --to T... --token USDT --amount 5
wallet-cli tx send --to T... --contract TR7... --amount 5
wallet-cli tx send --to T... --asset-id 1002000 --raw-amount 1000000
```

交易构建命令支持三种执行模式：

| 模式 | 行为 |
|------|----------|
| 默认 | 构建、签名并广播。 |
| `--dry-run` | 构建并估算，不签名、不广播。 |
| `--sign-only` | 签名并输出交易，但不广播。 |

默认模式在交易提交后返回。添加 `--wait` 后，CLI 会轮询 FullNode 的未确认视图，直到交易确认或失败。
如果达到轮询时间上限，CLI 会返回已提交的回执，而不会错误地表示广播失败。

稍后广播已签名交易：

```bash
wallet-cli tx broadcast --tx-stdin < signed.json
```

`tx status` 返回四状态模型：`confirmed`、`failed`、`pending` 或 `not_found`。

```bash
wallet-cli tx status --txid <TXID>
wallet-cli tx info --txid <TXID> --output json
```

CLI 还提供一个纯粹、可离线使用的签名器，用于签名在其他位置构建的交易：

```bash
wallet-cli tx sign --transaction "$TX_JSON"
```

它始终验证 `txID` 是否为 `raw_data_hex` 的哈希，并验证声明的合约类型是否与编码后的交易一致。
对于可以重新编码的合约类型，它还会验证 `raw_data` 的字段级内容。在多签工作流中，它会向已有的
签名数组追加签名。详见[签名与安全](typescript-cli-signing.md#sign-an-existing-transaction)。

## 查询

与钱包绑定的账户查询默认使用 active account，也可以通过 `--account` 指定账户。

```bash
wallet-cli account info --output json
wallet-cli account history --limit 10
wallet-cli account portfolio
wallet-cli networks
wallet-cli block
wallet-cli block 12345
wallet-cli chain params
wallet-cli chain prices
wallet-cli chain node
wallet-cli stake info
wallet-cli stake delegated --direction out
wallet-cli vote status
wallet-cli reward balance
```

有关字段级命令语义和更多示例，请参见
[上游 TypeScript 命令参考](https://github.com/tronprotocol/wallet-cli/tree/master/ts/docs/commands)。

## Token 和合约

Token 地址簿内置了 USDT、USDC 等常见主网 token，也可以加入自定义 TRC-20 合约。

```bash
wallet-cli token add --contract TR7...
wallet-cli token list
wallet-cli token balance --contract TR7...
wallet-cli token info --contract TR7...
wallet-cli token remove --contract TR7...
```

合约调用使用 JSON 编码的参数描述：

```bash
wallet-cli contract info --contract TR7...

wallet-cli contract call \
  --contract T... \
  --method 'balanceOf(address)' \
  --params '[{"type":"address","value":"T..."}]'

wallet-cli contract send \
  --contract T... \
  --method 'transfer(address,uint256)' \
  --params '[{"type":"address","value":"T..."},{"type":"uint256","value":"1000000"}]' \
  --dry-run

wallet-cli contract deploy \
  --abi '[...]' \
  --bytecode 60... \
  --fee-limit 1000000000 \
  --params '[100,"T..."]' \
  --dry-run
```

在 JSON 输出中，TypeScript CLI 的合约部署成功后，部署回执数据会包含部署出的 `contractAddress`。

当地址上没有已部署的合约时，`contract info` 会返回 not-found 错误，而不是返回空合约。

合约部署需要软件账户。Ledger TRON app 无法签名 `CreateSmartContract`，因此 Ledger 支持的
账户不能使用 `wallet-cli contract deploy`。

## Stake 2.0

质押金额以 SUN 为单位。TypeScript CLI 提供 Stake 2.0 命令：

```bash
wallet-cli stake freeze --amount-sun 1000000 --resource energy --dry-run
wallet-cli stake delegate --amount-sun 1000000 --receiver T... --resource energy --dry-run
wallet-cli stake undelegate --amount-sun 1000000 --receiver T... --resource energy --dry-run
wallet-cli stake unfreeze --amount-sun 1000000 --resource energy --dry-run
wallet-cli stake cancel-unfreeze --dry-run
wallet-cli stake withdraw --dry-run
wallet-cli stake info
wallet-cli stake delegated --direction out
```

`stake cancel-unfreeze` 需要软件账户；Ledger TRON app 无法签名 `CancelAllUnfreezeV2Contract`。

`stake withdraw` 会在构建交易前检查可提取金额；如果没有已到期的解冻 TRX，则返回
`nothing_to_withdraw`。

## 投票和奖励

TypeScript CLI 可以查看超级代表、替换账户的投票分配、查询可领取奖励并提取奖励：

```bash
wallet-cli vote list
wallet-cli vote status
wallet-cli vote cast --for TZ4...=600 --for TT5...=400
wallet-cli reward balance
wallet-cli reward withdraw
```

`vote cast` 会替换现有的完整投票分配，未列出的 SR 会被设为零票。`vote cast` 和
`reward withdraw` 都会创建交易，因此需要签名账户。当可领取余额为空时，`reward withdraw` 返回
`no_reward`；未满 24 小时的提取间隔时，则返回 `withdraw_too_frequent`。

## 签名

除 `message sign` 外，CLI 还提供 `tx sign` 和 EIP-712/TIP-712 `typed-data sign`。软件账户和
Ledger 账户均受支持；watch-only 账户会在写入或签名操作开始前失败。

```bash
wallet-cli message sign --message 'hello'
wallet-cli tx sign --transaction "$TX_JSON"
wallet-cli typed-data sign --typed-data "$TYPED_DATA_JSON"
```

有关交易完整性检查、多签行为、Ledger 设置和 secret 输入规则，请参见
[签名与安全](typescript-cli-signing.md)。

## 自动化

JSON 模式向 stdout 输出一个 `wallet-cli.result.v1` envelope，并使用确定的退出码：

| 代码 | 含义 |
|------|---------|
| `0` | 成功。 |
| `1` | 执行、鉴权、设备或链上错误。 |
| `2` | 命令用法或参数无效。 |

智能体和脚本可以发现完整命令目录与 JSON Schema，无需解析面向人的 help 文本：

```bash
wallet-cli --json-schema
wallet-cli tx send --json-schema
```

规范命令 ID 不带 `tron.` 前缀：例如命令 ID 是 `tx.send`，而不是 `tron.tx.send`。网络 family 则通过
`chain.family` 单独提供。

`--timeout 0` 或不受支持的 `--output` 值等无效全局选项会返回 `invalid_value`，而不是静默退回
默认值。
