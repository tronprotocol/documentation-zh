# 发送原生币和 token

一条命令即可发送多种资产，包括网络原生币、TRC20/ERC20 合约 token 和 TRC10 资产；具体类型由选择器参数决定。示例均在 Nile 上运行；对于支持 EVM 的操作，只需更换 `--network` 即可用于 EVM 网络。

> **密码**：软件签名的发送需要通过 stdin 提供 master password，且签名时不会弹出任何提示。下面的示例省略了它，以便把注意力集中在 token 相关参数上——请在前面加上 `printf '%s' "$PW" |` 并在末尾追加 `--password-stdin`，或者从密码管理器通过管道传入（见[快速上手](getting-started.md#3-send-your-first-transaction)）。`--dry-run`、`--build-only` 和 Ledger 签名都不使用 master password。

## 原生币

```bash
wallet-cli tx send --to TSx72ViULFepRGCS4PM5dP4FqD1d8qggCc --amount 1 --network nile
```

```bash
wallet-cli tx send --to 0x742d35Cc6634C0532925a3b844Bc454e4438f44e --amount 0.01 --network sepolia
```

`--amount` 使用原生币的常用单位：在 TRON 上，`1` = 1 TRX = 1,000,000 SUN；在 Sepolia 上，`0.01` = 0.01 ETH = 10^16 wei。如需直接指定基础单位，请使用 `--raw-amount 1000000`。两个参数只能选择其一，不能同时使用。

## 合约 token（TRC20 / ERC20）

合约类 token 由它的**合约地址**标识。你可以直接传入该地址，也可以传入一个简短的**符号**，由 wallet-cli 帮你解析成对应合约：

```bash
# by contract address — always works
wallet-cli tx send --to T... --contract TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t --amount 5 --network nile
```

```bash
wallet-cli tx send --to 0x... --contract 0xdAC17F958D2ee523a2206206994597C13D831ec7 --amount 5 --network ethereum
```

```bash
# by symbol — needs the token to be in the token book (see below)
wallet-cli tx send --to T... --token USDT --amount 5 --network nile
```

token 转账会执行合约代码，而费用相关的参数因家族而异：

- **TRON**——它消耗**能量**；`--fee-limit` 限制为此可以燃烧的 TRX 上限（默认 100000000 SUN = 100 TRX）。如果转账因费用上限而失败，请先弄清原因再调高它——参见[能量与带宽](../concepts/energy-bandwidth.md)。
- **EVM**——它消耗 **gas**，由节点估算得出。可用 `--gas-limit`、`--max-fee`、`--priority-fee`、`--nonce` 覆盖——参见 [`evm-gas` 模型](../concepts/networks.md#fees-the-evm-gas-model)。

把其中一组用在另一个家族上会以 `invalid_option` 被拒绝。

### token 地址簿（符号 → token）

`--token USDT` 的工作方式是在按网络划分的 **token 地址簿**中查找该符号：这是一张本地表，把符号映射到链上的 token——可以是一个 TRC20/ERC20 合约，也可以是一个 TRC10 资产 id。条目有两个来源，显示在 `token list` 的 `Source` 列中：

- **official**——内置条目，按网络分别甄选。`tron:728126428` 内置 USDT / USDC / USDD，`tron:3448148188` 内置 USDT / USDD，`eip155:1` 内置 USDT / USDC。其余网络不附带任何官方条目。
- **user**——你自己添加的 token。

```bash
wallet-cli token list --network tron
```

```console
| Symbol | Name            | Source   | Contract / ID                      |
| ------ | --------------- | -------- | ---------------------------------- |
| USDT   | Tether USD      | official | TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t |
| USDC   | USD Coin        | official | TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8 |
| USDD   | Usdd Stablecoin | official | TXDk8mbtRbXeYuMNS83CfKPaYYT8XWv9Hz |
```

地址簿是**按网络**分开的，官方条目绝不会在链之间复制——同一个符号在别的链上可能对应不同的地址和不同的精度（USDT 在以太坊上是 6 位精度，在 BNB Smart Chain 上是 18 位）。在没有官方条目的网络上，需要先添加一次该 token，`--token` 才能在那里解析到它。`token add` 会从 token 上读取符号和精度，并存为一条**用户**条目，作用范围仅限那一个网络：

```bash
wallet-cli token add --contract T... --network nile      # TRC20, by contract
```

```bash
wallet-cli token add --contract 0x... --network sepolia     # ERC20, by contract
```

```bash
wallet-cli token add --asset-id 1000001 --network nile   # TRC10, TRON only
```

其余管理操作都在同一个命令组里：`token list` 查看全部条目，`token remove` 删除一条 user 条目，`token balance` / `token info` 在不添加 token 的前提下直接查询它。

## TRC10 token——仅限 TRON

TRC10 资产用的是数字 id，而不是合约：

```bash
wallet-cli tx send --to T... --asset-id 1002000 --raw-amount 1000000 --network nile
```

`--asset-id` 是仅限 TRON 的参数；在 EVM 网络上它会以 `invalid_option` 失败。

`--token`、`--contract` 和 `--asset-id` 三者互斥；一个都不给就表示发送该网络的原生币。

## 先演练，再发送

`--dry-run` 会通过所选网络构建交易并估算费用，然后直接返回，不签名也不广播——不会有任何东西离开你的钱包：

```bash
wallet-cli tx send --to T... --token USDT --amount 5 --network nile --dry-run -o json
```

检查输出中的 `fee` 字段，然后去掉 `--dry-run` 再次执行。交易已提交并不代表执行成功；之后应使用 [`tx status`](../commands/tx/status.md) 查询结果，或为 `tx send` 添加 `--wait`，等待交易确认或失败。

> **主网**：同样的命令换成 `--network tron`、`--network ethereum` 或 `--network bsc`，动的就是真实资产，且不可逆。请反复核对 `--to`（转错地址一旦确认就找不回来了），并先做一次试运行。

## 另请参见

[`tx send` 参考](../commands/tx/send.md)——每个参数和输出字段 · [`token` 命令](../commands/token/index.md)——token 地址簿 · [快速上手](getting-started.md) · [脚本编写](scripting.md)——安全地自动化发送
