# wallet-cli —— TypeScript 实现

TypeScript 版面向脚本、CI 和 AI 智能体调用：每条命令都有稳定的 JSON 响应结构、确定的退出码和
可查询的 schema；交互式提示被限制在一份很短的白名单内——`create`、各个 `import` 子命令、`backup`、
`change-password` 和 `delete`——除此之外，凭据缺失一律直接报错，绝不弹出提示。关于 wallet-cli 以及
两种实现的对比，参见[仓库总览](../index.md)；关于最早的实现，参见 [Java 实现](../java/index.md)。

## 主要特性

- **便于自动化集成**——提供稳定的 JSON 输出、确定的退出码和可查询的 schema，适合脚本、CI 和
  AI 智能体调用（细节见[接口约定概要](#the-contract-in-one-paragraph)）。
- **加密的本地存储**——软件 keystore 在磁盘上加密保存；敏感信息只经由 stdin/TTY 进入，绝不经过命令行参数或专用的敏感信息环境变量。
- **软件签名与 Ledger 签名**——用软件签名，或在 Ledger 设备上签名（私钥绝不离开设备）。
- **完整的 TRON 功能支持**——HD 钱包、TRX 与 TRC20/TRC10 转账、质押 / 资源代理、投票 / 奖励、
  治理提案与超级代表运营、智能合约调用、部署与治理、TRC10 发行、链上 Bancor 交易所、多重签名、
  GasFree 转账、消息签名，以及链上查询。
- **EVM 链同样支持**——转账、token、合约和签名在以太坊与 BNB Smart Chain 上同样可用。仅属于 TRON 协议的命令在 EVM 网络上会以 `family_mismatch` 拒绝执行；参见[哪些命令能在哪些网络上运行](commands/index.md#which-commands-run-on-which-networks)。

## 目录

- [支持的链](#supported-chains)
- [安装](#install)
- [快速上手](#quickstart)
- [命令](#commands)
  - [钱包与账户](#wallets-and-accounts)
  - [交易](#transactions)
  - [链上查询](#on-chain-queries)
  - [Token、合约、质押、签名](#tokens-contracts-staking-signing)
  - [治理、TRC10 与链上交易所](#governance-trc10-and-the-on-chain-exchange)
  - [本地工具与配置](#local-tools-and-configuration)
- [接口约定概要](#the-contract-in-one-paragraph)
- [理解 TRON 机制](#understanding-tron-mechanics)
- [故障排查](#troubleshooting)

## 支持的链 {#supported-chains}

内置支持七个网络。网络使用规范的 [CAIP-2](https://chainagnostic.org/CAIPs/caip-2) `namespace:reference` id 标识。**namespace 不等于链家族**：`eip155` 是 CAIP-2 为 EVM 链定义的 namespace，而本 CLI 用于分支判断的家族名是 `evm`。**别名**是可代替 id 输入的简称；它只在选择网络时解析，不会出现在输出中：

| 网络 id | 别名 | 说明 | 原生币价值 |
|---|---|---|---|
| `tron:728126428` | `tron` | TRON 生产主网 | **真实资金** |
| `tron:3448148188` | `nile` | 主要的 TRON 测试网（水龙头在 nileex.io） | 无——可自由使用 |
| `tron:2494104990` | `shasta` | 备用的 TRON 测试网 | 无 |
| `eip155:1` | `ethereum` | 以太坊主网（ETH） | **真实资金** |
| `eip155:11155111` | `sepolia` | 以太坊测试网（ETH） | 无 |
| `eip155:56` | `bsc` | BNB Smart Chain（BNB） | **真实资金** |
| `eip155:97` | `bsc-testnet` | BNB Smart Chain 测试网（BNB） | 无 |

在同一个家族内部，你的地址在每个网络上都相同（TRON 上是 base58 的 `T…`，EVM 上是 `0x…`——两个家族由同一份种子派生出的是**不同**的地址），而余额、token 和交易按网络隔离。费用跟随家族：TRON 的 `tron-resource` 模型（带宽 + 能量），或者 EVM 的 gas——参见[网络](concepts/networks.md)和[能量与带宽](concepts/energy-bandwidth.md)。

## 安装 {#install}

**前置条件**：[Node.js](https://nodejs.org) **20 或更高版本**（用 `node --version` 检查）。Ledger
签名还需要一台受支持的 Ledger 设备，并安装与所选家族对应的 app——TRON 账户用 TRON app，EVM 账户用 Ethereum app。参见 [Ledger 指南](guide/ledger.md)。

```bash
npm install -g @tron-walletcli/wallet-cli
```

注意 scope：包名是 `@tron-walletcli/wallet-cli`，不是不带 scope 的 `wallet-cli`（那是一个无关的
第三方包）。

验证：

```bash
wallet-cli --version
```

```console
<version>          # 显示已安装的版本
```

用 `npm update -g @tron-walletcli/wallet-cli` 升级；用 `npm uninstall -g @tron-walletcli/wallet-cli`
卸载。

**从源码构建**（贡献者，或要运行未发布的改动）——还需要 Git：

```bash
git clone https://github.com/tronprotocol/wallet-cli.git
cd wallet-cli/ts
npm ci && npm run build
npm link             # 把 `wallet-cli` 放到 PATH 上（或直接运行：node dist/index.js）
```

## 快速上手 {#quickstart}

**创建你的第一个钱包。** `create` 会提示输入 master password，然后显示新账户：

```bash
wallet-cli create --label main
```

```console
✅ Created wallet "main"
  Account ID    wlt_2dbv24de.0
  Type          HD
  TRON address  TTVdGTBXY5mmY3nJFGUp7Vo898kUJ6gtFQ
  EVM address   0x5c8e1b04A7f39d62C0B3e85A1d47F9028b6ce713
  Active        yes

⚠️ Recovery phrase is encrypted locally and was not printed.
⚠️ Run `backup` soon and store the file offline.
```

```bash
wallet-cli list
```

```console
HD  wlt_2dbv24de
└─ [0] main  TTVdGTBXY5mmY3nJFGUp7Vo898kUJ6gtFQ  (active)
```

完整流程——在测试网上充值、查看余额、发送第一笔 TRX——见[快速上手指南](guide/getting-started.md)。
之后可以按主题深入：[发送 token](guide/send-tokens.md) · [质押与资源](guide/stake-and-resources.md) ·
[使用 Ledger 硬件钱包](guide/ledger.md) · [脚本编写](guide/scripting.md)。

## 命令 {#commands}

每条命令——包括每个子命令——都有自己的参考页；完整的逐命令列表见
**[命令索引](commands/index.md)**；也可以运行 `wallet-cli <command> --help` 查看内置帮助。

### 钱包与账户 {#wallets-and-accounts}

创建、导入和管理本地钱包与账户。

| 命令 | 说明 |
|---|---|
| [`create`](commands/create.md) | 创建新的 HD 钱包（BIP39 种子） |
| `import` | 导入钱包——[mnemonic](commands/import/mnemonic.md) · [private-key](commands/import/private-key.md) · [keystore](commands/import/keystore.md) · [ledger](commands/import/ledger.md) · [watch](commands/import/watch.md)（仅观察） |
| [`list`](commands/list.md) | 列出钱包与账户 |
| [`use`](commands/use.md) · [`current`](commands/current.md) | 设置 / 显示当前账户（`current --qr` 显示收款二维码） |
| [`derive`](commands/derive.md) | 从种子钱包派生下一个 HD 账户 |
| [`rename`](commands/rename.md) · [`backup`](commands/backup.md) · [`delete`](commands/delete.md) | 重命名、备份或删除账户（backup 以 0600 权限导出密钥材料和元数据；`--keystore` 使用 Web3 keystore 格式，`--records` 输出导出审计日志） |
| [`change-password`](commands/change-password.md) | 更换 master password（重新加密全部软件 keystore） |

### 交易 {#transactions}

发送、广播、查看和联合签名交易。

| 命令 | 说明 |
|---|---|
| [`tx send`](commands/tx/send.md) | 发送原生 TRX 或 TRC20/TRC10 token |
| [`tx broadcast`](commands/tx/broadcast.md) | 广播已签名的交易 |
| [`tx status`](commands/tx/status.md) · [`tx info`](commands/tx/info.md) | 确认状态，或完整详情 + 回执 |
| [`tx sign`](commands/tx/sign.md) · [`tx approvals`](commands/tx/approvals.md) · [`tx multisig`](commands/tx/multisig.md) | 联合签名多签交易并查看批准情况 |

### 链上查询 {#on-chain-queries}

读取账户、区块和链的状态。

| 命令 | 说明 |
|---|---|
| [`account balance`](commands/account/balance.md) · [`info`](commands/account/info.md) · [`portfolio`](commands/account/portfolio.md) | 余额、账户原始数据，或带 USD 估值的余额 |
| [`account history`](commands/account/history.md) | 交易历史（需要 TronGrid） |
| [`account activate`](commands/account/activate.md) · [`set`](commands/account/set.md) | 激活账户，或设置其链上名称 / ID |
| [`block`](commands/block.md) | 获取区块（省略则取最新块） |
| [`chain params`](commands/chain/params.md) · [`prices`](commands/chain/prices.md) · [`node`](commands/chain/node.md) | 治理参数、资源价格，或节点状态 |

### Token、合约、质押、签名 {#tokens-contracts-staking-signing}

Token 与合约操作、资源质押、投票奖励、消息签名，以及权限管理。

| 命令                                                                                              | 说明                                                                                                                                                                                                                                   |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`token`](commands/token/index.md)                                                         | Token 地址簿与查询（[balance](commands/token/balance.md) · [info](commands/token/info.md) · [add](commands/token/add.md) · [list](commands/token/list.md) · [remove](commands/token/remove.md)) |
| [`contact`](commands/contact/index.md)                                                     | 收款人联系簿（[add](commands/contact/add.md) · [list](commands/contact/list.md) · [remove](commands/contact/remove.md))                                                                                     |
| [`contract`](commands/contract/index.md)                                                   | 调用、发送、部署、查看和治理合约（[call](commands/contract/call.md) · [send](commands/contract/send.md) · [deploy](commands/contract/deploy.md) · [info](commands/contract/info.md) · [clear-abi](commands/contract/clear-abi.md) · [set-origin-energy-limit](commands/contract/set-origin-energy-limit.md) · [set-user-resource-percent](commands/contract/set-user-resource-percent.md) · [create2](commands/contract/create2.md)) |
| [`stake`](commands/stake/index.md)                                                         | 质押 / 代理资源（[freeze](commands/stake/freeze.md) · [unfreeze](commands/stake/unfreeze.md) · [delegate](commands/stake/delegate.md) · [info](commands/stake/info.md), …)                            |
| [`vote`](commands/vote/index.md) · [`reward`](commands/reward/index.md)               | 为超级代表投票并领取投票奖励                                                                                                                                                                              |
| [`message`](commands/message/index.md) · [`typed-data`](commands/typed-data/index.md) | 签名任意消息，或 EIP-712/TIP-712 结构化数据                                                                                                                                                                          |
| [`permission`](commands/permission/index.md)                                               | 查看 / 更新用于多重签名的账户权限                                                                                                                                                                                      |
| [`gasfree`](commands/gasfree/index.md)                                                     | 通过 GasFree 服务进行免 gas 的 token 转账                                                                                                                                                                                     |

### 治理、TRC10 与链上交易所 {#governance-trc10-and-the-on-chain-exchange}

链治理、超级代表运营，以及 TRON 协议级的 TRC10 与 Bancor 交易所机制。

| 命令 | 说明 |
|---|---|
| [`proposal`](commands/proposal/index.md) | 链参数提案（[list](commands/proposal/list.md) · [show](commands/proposal/show.md) · [create](commands/proposal/create.md) · [approve](commands/proposal/approve.md) · [delete](commands/proposal/delete.md)) ——`list` / `show` 对任何人开放，写操作命令需要已注册的见证人 |
| [`witness`](commands/witness/index.md) | 注册和运营超级代表（[create](commands/witness/create.md) · [update](commands/witness/update.md) · [set-brokerage](commands/witness/set-brokerage.md)) |
| [`asset`](commands/asset/index.md) | 发行和管理 TRC10 token（[issue](commands/asset/issue.md) · [update](commands/asset/update.md) · [participate](commands/asset/participate.md) · [unfreeze](commands/asset/unfreeze.md) · [info](commands/asset/info.md) · [list](commands/asset/list.md)）；TRC10 转账通过 [`tx send`](commands/tx/send.md) 进行 |
| [`exchange`](commands/exchange/index.md) | TRX 与 TRC10 之间的协议级 Bancor 交易所（[create](commands/exchange/create.md) · [inject](commands/exchange/inject.md) · [withdraw](commands/exchange/withdraw.md) · [trade](commands/exchange/trade.md) · [show](commands/exchange/show.md) · [list](commands/exchange/list.md)) |

### 本地工具与配置 {#local-tools-and-configuration}

离线的本地命令与配置。

| 命令 | 说明 |
|---|---|
| [`encoding convert`](commands/encoding/convert.md) | 转换 / 校验地址和编码 |
| [`address generate`](commands/address/generate.md) | 生成随机密钥对（本地，不保存） |
| [`config`](commands/config.md) | 显示 / 读取 / 设置配置值 |
| [`networks`](commands/networks.md) | 列出已知网络 |

## 接口约定概要 {#the-contract-in-one-paragraph}

每条命令都支持 `-o json`，并在 stdout 上输出**恰好一个完整的 JSON 对象**，schema 为
[`wallet-cli.result.v1`](machine-interface.md#the-result-envelope)。退出码是固定的：`0` 成功、
`1` 执行失败、`2` 用法错误。敏感信息（密码、助记词、私钥）绝不接受通过命令行参数传入，也不会从专用的敏感信息环境变量读取。密码可以通过 stdin 标志或交互式 TTY 提示进入；助记词/私钥导入和 `change-password` 只能交互执行（完全没有 stdin 路径）。完整规范：[machine-interface.md](machine-interface.md)。

## 理解 TRON 机制 {#understanding-tron-mechanics}

TRON 在费用、账户和密钥权限方面与 EVM 链有较大差异，建议在操作前了解以下内容：

- [网络](concepts/networks.md)——七个内置网络、CAIP-2 id，以及两个链家族
- [账户与 HD](concepts/accounts-and-hd.md)——助记词、派生路径、账户激活
- [能量与带宽](concepts/energy-bandwidth.md)——TRON 基于资源的费用模型（取代 EVM gas）
- [安全](concepts/security.md)——keystore 加密、敏感信息处理、多签权限

## 故障排查 {#troubleshooting}

命令报错或行为异常？常见问题及诊断方法见 [troubleshooting.md](troubleshooting.md)。

> 凡是会花钱的可复制示例都指向测试网——TRON 上是 **Nile**（`--network tron:3448148188`），EVM 上是
> **Sepolia**（`--network eip155:11155111`）。主网 id（`tron:728126428`、`eip155:1`）也会出现：用在只读示例中，
> 例如 token 地址簿列表和配置路径，以及少数几处主网 token 合约的示意。最后这类示例带的是占位收款方
> （`T...` / `0x...`），照抄是跑不通的。
