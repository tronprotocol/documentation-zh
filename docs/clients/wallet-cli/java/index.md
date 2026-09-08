# wallet-cli —— Java 实现

Java 版是 wallet-cli 最早的完整实现，采用交互式命令行（REPL），支持账户与
keystore、TRX / TRC10 / TRC20 转账、质押资源、为超级代表投票、部署和调用智能合约、Ledger 硬件
签名，以及 [GasFree](https://gasfree.io) 免 gas 转账。所有 gRPC 调用都基于
[Trident SDK](https://github.com/tronprotocol/trident)。

> 关于两种实现的定位，以及 Java 版与支持脚本调用、优先提供 JSON 输出的 [TypeScript 实现](../typescript/index.md)
> 的对比，参见[仓库总览](../index.md)。

**快速链接：** [环境准备](#setup) · [快速上手](#quickstart) · [命令](#commands) ·
[理解 TRON 机制](#understanding-tron-mechanics) · [配置](reference/config.md)

需要帮助？欢迎加入 [Telegram 开发者群](https://t.me/TronOfficialDevelopersGroupEn)。

## 环境准备 {#setup}

### 下载

```
git clone https://github.com/tronprotocol/wallet-cli.git
```

### 配置

一份最小的 `config.conf` 只需要一个 FullNode 端点。`net.type` **并不决定连接哪个网络**，它只控制是否应用 `grpc.mainnet.apiKey`；启动时使用的网络是根据所配置的节点端点推断出来的。

```
net {
  type = mainnet
}

fullnode = {
  ip.list = [
    "fullnode ip : port"
  ]
}
```

你也可以在运行时用 [`SwitchNetwork`](commands/network.md) 命令切换网络，因此只有在使用自定义节点
或高级功能时才需要编辑 `config.conf`。**完整的带注释配置**——可选的 Solidity 节点、Ledger 调试、
账户锁定、GasFree、TronGrid API key、TronLink 多重签名和记录条数限制——以及逐字段参考，都在
[配置参考](reference/config.md)中。

### 构建与运行

- **连接 fullNode**——参见 [java-tron 部署文档](../../../using_javatron/installing_javatron.md)。
  可以在本地 PC 或远程服务器上运行 fullNode。
- **编译并运行**：

    ```console
    $ cd wallet-cli/java
    $ ./gradlew build
    $ cd build/libs
    $ java -jar wallet-cli.jar
    ```

wallet-cli 通过 gRPC 连接 java-tron。启动时它会先在当前工作目录查找 `config.conf`，找不到才回退到 JAR 内置的
classpath 资源。可使用 `SwitchNetwork` 在主网、测试网（Nile 和 Shasta）以及自定义网络之间切换。

## 快速上手 {#quickstart}

构建、创建账户并发出第一笔转账——全部在交互式提示符中完成：

```console
# 1. 构建
$ git clone https://github.com/tronprotocol/wallet-cli.git
$ cd wallet-cli/java && ./gradlew build && cd build/libs

# 2. 启动交互式钱包
$ java -jar wallet-cli.jar

# 3. 在钱包提示符下：创建账户（或使用 ImportWallet）、解锁并查看
> RegisterWallet             # 先两次提示输入密码，再询问助记词长度
> Login                      # 解锁账户
> GetAddress                 # 显示你的地址
> GetBalance                 # TRX 余额

# 4. 发送 1 TRX（金额以 SUN 计；1 TRX = 1,000,000 SUN）
> SendCoin <toAddress> 1000000
```

> 在主网上执行这些命令会使用**真实资产**。学习阶段请用 `SwitchNetwork` 切换到测试网（Nile 或
> Shasta），并从该网络的水龙头领取测试币。

完整的首次运行流程见[快速上手指南](guide/getting-started.md)；端到端的完整会话示例见
[命令行操作流程](guide/command-flow.md)。全部指南索引见[指南](guide/index.md)。

## 命令 {#commands}

每条命令都记录在[命令](commands/index.md)下的分类页面中。**[命令索引](commands/index.md)**提供
完整的 A–Z 列表，把每条命令链接到它所在的章节；在钱包中执行 `help <command>` 可看到该命令的内置用法提示
（单独执行 `help` 会打印完整命令表）。

### 钱包与账户

| 领域 | 页面 |
|---|---|
| 创建 / 导入 / 导出 / 备份钱包、子账户、登录、锁定、切换 | [wallet](commands/wallet.md) |
| 账户查询、元数据、备份与交易记录、收款二维码 | [account](commands/account.md) |
| 切换 / 显示网络 | [network](commands/network.md) |

### 转账与 token

| 领域 | 页面 |
|---|---|
| USDT / TRC20 余额与转账、地址簿 | [usdt](commands/usdt.md) |
| 发行 / 更新 / 转移 / 查询 TRC10 token | [transfer-trc10](commands/transfer-trc10.md) |

### 质押与资源

| 领域 | 页面 |
|---|---|
| FreezeV2 质押、代理、解绑（Stake 2.0） | [stake-v2](commands/stake-v2.md) |
| 旧版冻结 / 解冻 / 代理（Stake 1.0） | [stake-v1-legacy](commands/stake-v1-legacy.md) |
| 资源单价与备注费 | [resources](commands/resources.md) |

### 投票、奖励与治理

| 领域 | 页面 |
|---|---|
| 为 SR 投票、佣金比例与奖励、见证人 | [vote-reward](commands/vote-reward.md) |
| 治理提案 | [proposals](commands/proposals.md) |
| 链上交易所（Bancor） | [exchange](commands/exchange.md) |
| TRON-DEX 订单市场 | [dex](commands/dex.md) |
| 多重签名：权限、联合签名、TronLink 多签 | [multisig](commands/multisig.md) |

### 合约、GasFree 与链上数据 {#contracts-gasfree--chain-data}

| 领域 | 页面 |
|---|---|
| 部署、触发和查看智能合约 | [contract](commands/contract.md) |
| GasFree 免 gas TRC20 转账 | [gasfree](commands/gasfree.md) |
| 交易、区块、链参数、编码工具 | [chain-data](commands/chain-data.md) |

## 理解 TRON 机制 {#understanding-tron-mechanics}

建议先了解以下机制，避免操作结果与预期不符（完整索引见[核心概念](concepts/index.md)）：

- [资源：带宽、能量与份额](concepts/resources.md)——冻结如何产生资源，以及带宽如何计算
- [质押模型：Stake 1.0 与 2.0](concepts/staking-models.md)——两代冻结机制，以及各自对应哪些命令
- [多重签名概念](concepts/multisig.md)——权限类型、密钥、权重和阈值
