# 网络

wallet-cli 用**规范 id** 来标识网络，它是一个 [CAIP-2](https://chainagnostic.org/CAIPs/caip-2) 的 `namespace:reference`。这里的 namespace 不等于链家族：`eip155` 是 CAIP-2 为 EVM 链定义的 namespace，而本 CLI 用于分支判断的家族名是 `evm`。每个网络都属于两个链**家族**之一——`tron` 或 `evm`：

```bash
wallet-cli networks
```

```console
| Network         | Alias       | Family | Chain id   | Fee model     | Endpoint                            |
| --------------- | ----------- | ------ | ---------- | ------------- | ----------------------------------- |
| tron:728126428  | tron        | tron   | 728126428  | tron-resource | api.trongrid.io                     |
| tron:3448148188 | nile        | tron   | 3448148188 | tron-resource | nile.trongrid.io                    |
| tron:2494104990 | shasta      | tron   | 2494104990 | tron-resource | api.shasta.trongrid.io              |
| eip155:1        | ethereum    | evm    | 1          | evm-gas       | ethereum-rpc.publicnode.com         |
| eip155:11155111 | sepolia     | evm    | 11155111   | evm-gas       | ethereum-sepolia-rpc.publicnode.com |
| eip155:56       | bsc         | evm    | 56         | evm-gas       | bsc-dataseed.bnbchain.org           |
| eip155:97       | bsc-testnet | evm    | 97         | evm-gas       | bsc-testnet-dataseed.bnbchain.org   |
```

| Id | 别名 | 是什么 | 原生币价值 |
|---|---|---|---|
| `tron:728126428` | `tron` | TRON 生产主网 | **真实资金** |
| `tron:3448148188` | `nile` | 主要的 TRON 测试网；水龙头在 nileex.io | 无——可自由使用 |
| `tron:2494104990` | `shasta` | 备用的 TRON 测试网 | 无 |
| `eip155:1` | `ethereum` | 以太坊主网 | **真实资金** |
| `eip155:11155111` | `sepolia` | 以太坊测试网 | 无 |
| `eip155:56` | `bsc` | BNB Smart Chain | **真实资金** |
| `eip155:97` | `bsc-testnet` | BNB Smart Chain 测试网 | 无 |

**别名**是可以代替规范 ID 输入的简称，只在选择网络时解析一次。后续处理不会保留别名，JSON 响应中的 `chain.network` 始终返回规范 ID。由于配置中的别名可以重新指向其他网络，脚本应直接使用规范 ID。

对于每个内置网络，**chain id** 都是规范 id 的第二段，无论属于哪个家族。`chainId` 是独立配置的字段，并非根据规范 id 推导；在 `config.yaml` 中新增网络时，需要自行确保两者一致。EVM 的 chain id 是签名所覆盖的 EIP-155 数字（如 `56`）；TRON 的 chain id 是创世块哈希前缀的十进制表示（如 `3448148188`），目前仅用于显示。TRON 网络便于阅读的名称由别名提供（如 `nile`），不存储在 `chainId` 中。

用 [`config`](../commands/config.md) 把某个网络指向你自己的节点，或指向一个商用端点：

```bash
wallet-cli config networks.tron:3448148188.httpEndpoint http://127.0.0.1:8090
wallet-cli config networks.tron:728126428.apiKeyHeader TRON-PRO-API-KEY
wallet-cli config networks.tron:728126428.apiKey <your-key>
```

列表类输出（`networks`、`config`）只显示端点的**主机名**，因为商用 URL 可能把 key 放在路径中；只有按名称读取（`config networks.<id>.httpEndpoint`）时才会显示完整值。

## 命令如何选择网络

1. 命令上显式给出的 `--network <id|alias>`；
2. 否则是 `config.defaultNetwork`（`wallet-cli config defaultNetwork tron:3448148188`）；
3. 如果配置文件没有覆盖它，内置默认值是 `tron:728126428`（TRON 主网）。

因此，省略 `--network` 不会阻止链上命令执行。涉及资金的操作应显式传入规范网络 id，确保目标链明确记录在 shell 历史和审计日志中。

余额、token 和交易在各个网络之间是完全隔离的。Nile 上的一个 txid 在主网上并不存在——在主网查询它会返回 `not_found`/`rpc_error`。

## 链家族决定可用命令和执行身份

你的 TRON 地址在所有 TRON 网络上都相同，EVM 地址在所有 EVM 网络上也都相同——但它们是**由同一把密钥派生出的两个不同地址**，分别位于 BIP44 币种类型 195 和 60 下。因此所选网络决定了一条命令以你账户的哪个地址身份执行。参见[账户与 HD 钱包](accounts-and-hd.md)。

链家族也决定了哪些命令可用。TRON 的协议特性——质押、超级代表投票、TRC10、Bancor 交易所、链上权限、GasFree——在 EVM 上没有对应功能；这些命令在 EVM 网络上会在调用节点之前返回 `family_mismatch`。按家族划分的**参数**采用相同的处理方式，不匹配时返回 `invalid_option`。[命令参考](../commands/index.md#which-commands-run-on-which-networks)列出了具体范围。

## 手续费：`tron-resource` 模型 {#fees-the-tron-resource-model}

TRON 不像 EVM 链那样收取 gas。交易消耗**带宽**（字节），智能合约调用还会消耗**能量**；不足的部分通过燃烧 TRX 补上，而质押 TRX 可以持续获得配额。完整模型、质押相关命令以及解质押等待期，见[能量与带宽](energy-bandwidth.md)。

单位：**1 TRX = 1,000,000 SUN**。JSON 载荷携带的是原始 SUN——int64 量级的金额是十进制字符串（`"balance": "1976489000"` = 1976.489 TRX），而有界的费用与计数（`feeSun`、`energyUsed`、`netUsed`）有时是 JSON 数字；文本输出显示的是人类可读的 TRX。

`--fee-limit` 参数用来限制一次耗能调用最多可以燃烧多少 TRX，单位为 SUN。

## 手续费：`evm-gas` 模型 {#fees-the-evm-gas-model}

EVM 交易购买的是 **gas**：gas 上限（最多可消耗多少个单位）乘以每单位的价格。在 EIP-1559 链上，价格 = 网络给定的基础费用 + 优先费用（小费）；在 legacy 链上则是单一的 `gasPrice`。`chain prices` 会报告当前适用的那一种。

除非另行指定，wallet-cli 会根据节点数据自动填写这些值：gas 上限取自 `eth_estimateGas`（不做冗余放大），费用上限取自当前基础费用，nonce 取自该账户的 pending 计数。使用 `--gas-limit`、`--max-fee`、`--priority-fee`、`--nonce` 可以覆盖其中任意一项。如果费用设置可以签名但存在风险——例如小费被压到上限，或上限低于当前基础费用——CLI 会通过 `meta.warnings` 给出警告，而不会直接拒绝。

单位：**1 币 = 10^18 wei**，而 `--max-fee` / `--priority-fee` 以 **gwei** 给出（写作 `25` 或 `25gwei`）。JSON 载荷以字符串携带原始 wei。

币种本身是**网络**层面的事实，而不是家族层面的：`eip155:1` 用 ETH 支付，`eip155:56` 用 BNB。最小单位及其 18 位精度是共通的，符号则不是。

## 另请参见

- [`networks`](../commands/networks.md)——上面这张列表，以及它的 JSON 形式
- [`chain prices`](../commands/chain/prices.md)——当前一笔交易要花多少，两种模型都适用
- [`account info`](../commands/account/info.md)——TRON 上是当前的带宽/能量使用情况，EVM 上是 nonce 和是否有合约代码
- [快速上手](../guide/getting-started.md)——在 Nile 上给账户充值
