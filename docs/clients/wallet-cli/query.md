# 查询

针对区块、交易、链参数和资源价格、当前网络、已连接节点，以及 USDT 余额的只读查询。

接受显式地址的查询一般无需鉴权。省略地址时默认作用于当前钱包的查询则需要鉴权：`get-address` 始终
上报活动钱包（因而始终需要鉴权），而 `get-balance` 和 `get-usdt-balance` 仅在未提供 `--address`
时需要鉴权。

账户、质押/资源、资产、合约、见证人和提案相关的查询位于各自的页面
（[账户](accounts.md)、[质押与资源](staking.md)、[TRC-10 资产](trc10.md)、
[智能合约](smart-contracts.md)、[治理](governance.md)）。

## 网络与链

### 当前网络 —— `current-network` / `CurrentNetwork`

显示客户端当前连接的网络（`MAIN`、`NILE`、`SHASTA` 或 `CUSTOM`）。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile current-network
    ```

=== "交互模式"

    ```
    CurrentNetwork
    ```

### 链参数 —— `get-chain-parameters` / `GetChainParameters`

返回链上治理参数及其当前取值。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-chain-parameters
    ```

=== "交互模式"

    ```
    GetChainParameters
    ```

### 下次维护时间 —— `get-next-maintenance-time` / `GetNextMaintenanceTime`

返回下一个维护周期的时间戳（毫秒），即 SR/投票变更生效的时刻。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-next-maintenance-time
    ```

=== "交互模式"

    ```
    GetNextMaintenanceTime
    ```

### 带宽价格 —— `get-bandwidth-prices` / `GetBandwidthPrices`

返回历史带宽价格表。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-bandwidth-prices
    ```

=== "交互模式"

    ```
    GetBandwidthPrices
    ```

### 能量价格 —— `get-energy-prices` / `GetEnergyPrices`

返回历史能量价格表。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-energy-prices
    ```

=== "交互模式"

    ```
    GetEnergyPrices
    ```

### 备注手续费 —— `get-memo-fee` / `GetMemoFee`

返回为交易附加备注所收取的手续费。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-memo-fee
    ```

=== "交互模式"

    ```
    GetMemoFee
    ```

## 区块

### 查询区块 —— `get-block` / `GetBlock`

按编号返回区块；不给编号时返回最新区块。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-block --number 1000000
    ```

    - `--number`（可选）—— 区块编号；默认为最新区块。

=== "交互模式"

    ```
    GetBlock [BlockNum]
    ```

    不带参数时，返回当前区块。

### 按 ID 查询区块 —— `get-block-by-id` / `GetBlockById`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-block-by-id --id 00000000000f4240...
    ```

    - `--id`（必填）—— 区块 ID（哈希）。

=== "交互模式"

    ```
    GetBlockById block_id
    ```

### 按 ID 或编号查询区块 —— `get-block-by-id-or-num` / `GetBlockByIdOrNum`

接受区块编号或区块 ID。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-block-by-id-or-num --value 1000000
    ```

    - `--value`（必填）—— 区块编号或区块 ID。

=== "交互模式"

    ```
    GetBlockByIdOrNum [idOrNum] [true]
    ```

    不带参数时，返回当前区块头。结尾加 `true` 则返回完整区块而非仅区块头。运行
    `GetBlockByIdOrNum help` 查看所有形式。

### 查询最近 N 个区块 —— `get-block-by-latest-num` / `GetBlockByLatestNum`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-block-by-latest-num --count 5
    ```

    - `--count`（必填）—— 要返回的最近区块数量。

=== "交互模式"

    ```
    GetBlockByLatestNum num
    ```

### 查询区块范围 —— `get-block-by-limit-next` / `GetBlockByLimitNext`

返回半开区间 `[start, end)` 内的区块。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-block-by-limit-next \
      --start 1000000 --end 1000005
    ```

    - `--start`（必填）、`--end`（必填，必须大于 `start`）。

=== "交互模式"

    ```
    GetBlockByLimitNext start_block_number end_block_number
    ```

### 区块内交易数 —— `get-transaction-count-by-block-num` / `GetTransactionCountByBlockNum`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile \
      get-transaction-count-by-block-num --number 1000000
    ```

    - `--number`（必填）—— 区块编号。

=== "交互模式"

    ```
    GetTransactionCountByBlockNum number
    ```

## 交易

### 查询交易 —— `get-transaction-by-id` / `GetTransactionById`

返回某交易 ID 对应的交易体。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-transaction-by-id --id <txid>
    ```

    - `--id`（必填）—— 交易 ID（哈希）。

=== "交互模式"

    ```
    GetTransactionById txid
    ```

### 查询交易信息 —— `get-transaction-info-by-id` / `GetTransactionInfoById`

返回交易的执行结果：手续费、能量/带宽消耗、合约结果和日志。用它来读取改变状态的合约调用的结果。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-transaction-info-by-id --id <txid>
    ```

    - `--id`（必填）。

=== "交互模式"

    ```
    GetTransactionInfoById txid
    ```

### 区块内交易信息 —— `GetTransactionInfoByBlockNum`（仅 REPL）

返回某区块内每笔交易的执行结果。

```
GetTransactionInfoByBlockNum number
```

- `number`（必填）—— 区块编号。

## 节点

### 列出节点 —— `list-nodes` / `ListNodes`

列出已连接节点所知的对等节点。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile list-nodes
    ```

=== "交互模式"

    ```
    ListNodes
    ```

## USDT

### USDT 余额 —— `get-usdt-balance` / `GetUSDTBalance`

返回某地址的 USDT（TRC-20）余额。仅在 `main`、`nile`、`shasta` 上支持。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-usdt-balance --address TXyz...
    ```

    - `--address`（可选）—— 默认为当前钱包的地址。

=== "交互模式"

    ```
    GetUSDTBalance [Address]
    ```

    不带参数时，使用已登录账户的地址。

### 按 ID 查询 USDT 转账 —— `GetUsdtTransferById`（仅 REPL）

按交易 ID 在本地交易历史中查询此前记录的 USDT 转账。仅在 `main`、`nile`、`shasta` 上支持。

```
GetUsdtTransferById txId
```

- `txId`（必填）—— 要在本地历史中查询的交易 ID。

## 编码转换器 —— `EncodingConverter`（仅 REPL）

交互式助手，用于在地址/数值的各种编码之间转换（例如 Base58Check ↔ 十六进制）。它提示输入，而非
接受参数。

```
EncodingConverter
```
