# 智能合约

部署 TVM 智能合约并与之交互：部署、改变状态的调用、只读（常量）调用、能量预估，以及合约元数据管理。

通用概念：

- **`fee_limit`** —— 你愿意为该调用的能量花费的最大 TRX（以 SUN 计）。
- **`method`** —— 函数选择器/签名，例如 `transfer(address,uint256)`。
- **`params` / `args`** —— 调用参数。在 REPL 中，`isHex` 标志表示 `args` 是已经过 ABI 十六进制编码
  （`true`）还是普通的逗号分隔值（`false`）。
- **`value`** —— 随调用发送的 TRX（SUN）；**`token_value`/`token_id`** 随调用发送一个 TRC-10 代币
  （`token_id` 为 `#` 或 `TRXTOKEN` 表示不发送）。
- **`consume_user_resource_percent`** —— 由调用方支付的资源占比（0–100）。
- **`origin_energy_limit`** —— 合约所有者每次调用愿意提供的最大能量。

REPL 的构建交易命令用可选的首参 `[OwnerAddress]` 支持多签；标准 CLI 用 `--owner` + `--multi`。部署和
改变状态的调用需要鉴权；常量调用、能量预估和合约查询则不需要。

## 部署合约 —— `deploy-contract` / `DeployContract`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile deploy-contract \
      --name MyToken \
      --abi '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"}, ...]' \
      --bytecode 608060405234801561001057600080fd5b50... \
      --fee-limit 1000000000 \
      --consume-user-resource-percent 100 \
      --origin-energy-limit 10000000
    ```

    - 必填：`--name`、`--abi`（JSON）、`--bytecode`（十六进制）、`--fee-limit`（SUN）。
    - 可选：`--constructor`、`--params`、`--consume-user-resource-percent`（0–100）、
      `--origin-energy-limit`、`--value`、`--token-value`、`--token-id`、`--library`、
      `--compiler-version`、`--owner`、`--multi`。
    - JSON 模式下，响应的 `data` 包含部署得到的 `contract_address`。

=== "交互模式"

    ```
    DeployContract [ownerAddress] contractName ABI byteCode constructor params isHex \
      fee_limit consume_user_resource_percent origin_energy_limit value token_value \
      token_id(e.g: TRXTOKEN, use # if don't provided) \
      <library:address,library:address,...> <lib_compiler_version(e.g:v5)>
    ```

    `token_id` 为空时用 `#`。`<library...>` 和 `<lib_compiler_version>` 参数为可选，仅当字节码引用库
    时才需要。

## 调用合约（改变状态）—— `trigger-contract` / `TriggerContract`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile trigger-contract \
      --contract TContract... \
      --method "transfer(address,uint256)" \
      --params "TRecipient...,1000000" \
      --fee-limit 100000000
    ```

    - 必填：`--contract`、`--method`、`--fee-limit`。
    - 可选：`--params`、`--value`、`--token-value`、`--token-id`、`--owner`、
      `--permission-id`、`--multi`。

=== "交互模式"

    ```
    TriggerContract [OwnerAddress] contractAddress method args isHex \
      fee_limit value token_value token_id(e.g: TRXTOKEN, use # if don't provided)
    ```

    需要 8 个参数（带 `OwnerAddress` 则为 9 个）。

要读取改变状态的调用的执行结果，事后用 `get-transaction-info-by-id` / `GetTransactionInfoById`
查询（见 [查询](query.md)）。

## 调用合约（只读）—— `trigger-constant-contract` / `TriggerConstantContract`

在本地执行合约函数而不创建交易；返回结果。不消耗 gas。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile trigger-constant-contract \
      --contract TContract... \
      --method "balanceOf(address)" \
      --params "TAccount..."
    ```

    - 必填：`--contract`、`--method`。可选：`--params`、`--owner`。

=== "交互模式"

    ```
    TriggerConstantContract ownerAddress(use # if you own) contractAddress method args isHex \
      [value token_value token_id(e.g: TRXTOKEN, use # if don't provided)]
    ```

    需要 5 个或 8 个参数。`ownerAddress` 用 `#` 表示使用你自己的账户。

## 预估能量 —— `estimate-energy` / `EstimateEnergy`

预估一次合约调用将消耗的能量。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile estimate-energy \
      --contract TContract... \
      --method "transfer(address,uint256)" \
      --params "TRecipient...,1000000"
    ```

    - 必填：`--contract`、`--method`。可选：`--params`、`--value`、`--token-value`、
      `--token-id`、`--owner`。

=== "交互模式"

    ```
    EstimateEnergy ownerAddress(use # if you own) contractAddress method args isHex \
      [value token_value token_id(e.g: TRXTOKEN, use # if don't provided)]
    ```

    需要 5 个或 8 个参数。

## 预测 CREATE2 地址 —— `Create2`（仅 REPL）

计算合约通过 CREATE2 操作码部署后将得到的确定性地址。

```
Create2 address code salt
```

- `address` —— 部署者地址，`code` —— 合约字节码，`salt` —— CREATE2 的盐值。

## 合约维护

### 更新资源占比 —— `update-setting` / `UpdateSetting`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile update-setting \
      --contract TContract... --consume-user-resource-percent 50
    ```

    - `--contract`（必填）、`--consume-user-resource-percent`（必填，0–100）。
    - `--owner`、`--multi`（可选）。

=== "交互模式"

    ```
    UpdateSetting [OwnerAddress] contractAddress consume_user_resource_percent
    ```

### 更新能量上限 —— `update-energy-limit` / `UpdateEnergyLimit`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile update-energy-limit \
      --contract TContract... --origin-energy-limit 10000000
    ```

    - `--contract`（必填）、`--origin-energy-limit`（必填）。
    - `--owner`、`--multi`（可选）。

=== "交互模式"

    ```
    UpdateEnergyLimit [OwnerAddress] contractAddress origin_energy_limit
    ```

### 清除合约 ABI —— `clear-contract-abi` / `ClearContractABI`

删除链上为某合约存储的 ABI。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile clear-contract-abi --contract TContract...
    ```

    - `--contract`（必填）。`--owner`、`--multi`（可选）。

=== "交互模式"

    ```
    ClearContractABI [OwnerAddress] contractAddress
    ```

## 合约查询（无需鉴权）

### 查询合约 —— `get-contract` / `GetContract`

返回合约的字节码和 ABI。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-contract --address TContract...
    ```

    - `--address`（必填）。

=== "交互模式"

    ```
    GetContract contractAddress
    ```

### 查询合约信息 —— `get-contract-info` / `GetContractInfo`

返回扩展的合约信息（包括运行时/代码哈希等细节）。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-contract-info --address TContract...
    ```

    - `--address`（必填）。

=== "交互模式"

    ```
    GetContractInfo contractAddress
    ```
