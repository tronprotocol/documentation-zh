# TypeScript / npm CLI

从 `wallet-cli` 仓库的 4.9.7 发布版本开始，仓库同时提供一个面向智能体优先设计的 TypeScript CLI。
该 CLI 以 npm 包 `@tron-walletcli/wallet-cli` 发布，并采用独立的 npm 版本号；`wallet-cli --version`
显示的是 npm 包版本。它与本节其他页面介绍的 Java JAR 是两套命令面：Java CLI 使用 `send-coin`
这类命令，而 TypeScript CLI 使用 `tx send` 这类分组命令。

当前 TypeScript CLI 支持 TRON 主网、Nile 和 Shasta。本版本尚不支持 EVM 链。

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
| `--wait-timeout` | `--wait` 轮询的上限，单位为毫秒。 |
| `--password-stdin` | 从 stdin 读取 master password。 |

命令级 stdin 标志包括 `--mnemonic-stdin`、`--private-key-stdin`、`--tx-stdin` 和
`--message-stdin`。单次调用中只能有一个 `*-stdin` 标志消费 stdin。

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
```

4.9.7 中，HD 子账户派生需要显式传入 seed id；该 seed id 可通过 `wallet-cli list` 查看。

```bash
wallet-cli derive --seed-id wlt_ab12cd34 --label operations
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

改变链上状态的命令支持三种执行模式：

| 模式 | 行为 |
|------|----------|
| 默认 | 构建、签名并广播。 |
| `--dry-run` | 构建并估算，不签名、不广播。 |
| `--sign-only` | 签名并输出交易，但不广播。 |

稍后广播已签名交易：

```bash
wallet-cli tx broadcast --tx-stdin < signed.json
```

`tx status` 返回四状态模型：`confirmed`、`failed`、`pending` 或 `not_found`。

```bash
wallet-cli tx status --txid <TXID>
wallet-cli tx info --txid <TXID> --output json
```

## 查询和签名

与钱包绑定的账户查询默认使用 active account，也可以通过 `--account` 指定账户。

```bash
wallet-cli account info --output json
wallet-cli account history --limit 10
wallet-cli account portfolio
wallet-cli networks
wallet-cli block
wallet-cli block 12345
wallet-cli message sign --message 'hello'
```

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
```

`stake cancel-unfreeze` 需要软件账户；Ledger TRON app 无法签名 `CancelAllUnfreezeV2Contract`。

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

输入 secret 时，应通过 stdin 管道传入，避免放在 argv 或导出的环境变量中：

```bash
printf '%s\n' "$WALLET_PASSWORD" | wallet-cli message sign --message 'hello' --password-stdin --output json
printf '%s\n' "$MNEMONIC" | wallet-cli import mnemonic --label main --mnemonic-stdin
printf '%s\n' "$PRIVATE_KEY" | wallet-cli import private-key --label hot --private-key-stdin
```

这些示例假设 shell 变量通过安全方式注入且没有 export。每次调用只能有一个 `*-stdin` 标志消费 stdin。
`import mnemonic` 和 `import private-key` 等命令同时需要 master password 与 mnemonic/private key；
如果通过管道传入其中一个 secret，另一个必须在 TTY 中交互输入。它们不能在单 stdin 调用中完全非交互式完成。
