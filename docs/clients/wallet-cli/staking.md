# 质押与资源

TRON 账户质押（冻结）TRX 以获取**带宽**和**能量**，并获得投票权。共有两套质押机制：

- **Stake 1.0** —— `freeze-balance` / `unfreeze-balance`。质押的 TRX 会被锁定固定时长。
- **Stake 2.0** —— `freeze-balance-v2` / `unfreeze-balance-v2` 以及资源**代理**。这是当前机制；
  解除质押需要经过一段可提取的等待期。

全文使用的资源码：

| 码 | 资源 |
|------|----------|
| `0` | BANDWIDTH（带宽） |
| `1` | ENERGY（能量） |
| `2` | TRON_POWER（投票权；仅 freeze/unfreeze，且受网络开关限制） |

码 `2`（TRON_POWER）对 freeze/unfreeze 命令受网络开关限制：
`FreezeBalance`/`UnfreezeBalance`（Stake 1.0）、`FreezeBalanceV2`/`UnfreezeBalanceV2`（Stake 2.0）
以及对应的标准 CLI 命令，只有在链参数 `getAllowNewResourceModel` 启用时才接受它。如果无法获取该链参数，
4.9.7 客户端会 fail-open，让节点在广播时进行最终校验。代理命令（两种模式）始终只接受 `0` 或 `1`；
TRON_POWER 不可代理。

金额以 **SUN** 为单位（1 TRX = 1,000,000 SUN）。

与别处一样，REPL 用可选的首参 `[OwnerAddress]` 支持多签；标准 CLI 用 `--owner` + `--multi`。本页所有
改变状态的质押/代理命令都需要鉴权；页尾的资源查询则不需要。

## Stake 1.0

### 冻结余额 —— `freeze-balance` / `FreezeBalance`

!!! warning "已废弃"
    `freeze-balance` 已**废弃** —— 新的质押请使用 `freeze-balance-v2`（Stake 2.0）。它仅为兼容性
    保留。（`unfreeze-balance` 仍然可用，用于释放已有的 Stake 1.0 仓位。）

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile freeze-balance \
      --amount 1000000 --duration 3 --resource 1
    ```

    - `--amount`（必填，SUN）、`--duration`（必填，天）。
    - `--resource`（可选，`0`/`1`/`2`，默认 `0`）。`2` 是 TRON_POWER，仅在
      `getAllowNewResourceModel` 启用时允许。如果设置了 `--receiver`，该操作属于代理，`2` 会被拒绝。
    - `--receiver`（可选）—— 把获得的资源代理给另一个地址。
    - `--owner`、`--multi`（可选）。

=== "交互模式"

    ```
    FreezeBalance [OwnerAddress] frozen_balance frozen_duration [ResourceCode] [receiverAddress]
    ```

    `ResourceCode`：`0` BANDWIDTH，`1` ENERGY，`2` TRON_POWER。

### 解冻余额 —— `unfreeze-balance` / `UnfreezeBalance`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile unfreeze-balance --resource 1
    ```

    - `--resource`（可选，`0`/`1`/`2`，默认 `0`）。`2` 是 TRON_POWER，仅在
      `getAllowNewResourceModel` 启用时允许。如果设置了 `--receiver`，该操作针对代理冻结，`2` 会被拒绝。
    - `--receiver`（可选）—— 若该资源曾被代理则必填。
    - `--owner`、`--multi`（可选）。

=== "交互模式"

    ```
    UnfreezeBalance [OwnerAddress] ResourceCode [receiverAddress]
    ```

## Stake 2.0

### 冻结余额 v2 —— `freeze-balance-v2` / `FreezeBalanceV2`

无时长：质押的 TRX 一直保持质押，直到你显式解除。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile freeze-balance-v2 \
      --amount 1000000 --resource 1
    ```

    - `--amount`（必填，SUN）、`--resource`（可选，`0`/`1`/`2`，默认 `0`）。
      `2` 是 TRON_POWER，仅在 `getAllowNewResourceModel` 启用时允许；如果无法获取该链参数，客户端会让节点
      在广播时校验。
    - `--owner`、`--permission-id`、`--multi`（可选）。

=== "交互模式"

    ```
    FreezeBalanceV2 [OwnerAddress] frozen_balance [ResourceCode]
    ```

### 解冻余额 v2 —— `unfreeze-balance-v2` / `UnfreezeBalanceV2`

开始解除指定数量的质押。该 TRX 在网络的解冻等待期过后变为可提取（见 `withdraw-expire-unfreeze`）。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile unfreeze-balance-v2 \
      --amount 1000000 --resource 1
    ```

    - `--amount`（必填，SUN）、`--resource`（可选，`0`/`1`/`2`，默认 `0`）。
      `2` 是 TRON_POWER，仅在 `getAllowNewResourceModel` 启用时允许；如果无法获取该链参数，客户端会让节点
      在广播时校验。
    - `--owner`、`--permission-id`、`--multi`（可选）。

=== "交互模式"

    ```
    UnfreezeBalanceV2 [OwnerAddress] unfreezeBalance ResourceCode
    ```

### 提取已到期的解冻 —— `withdraw-expire-unfreeze` / `WithdrawExpireUnfreeze`

提取解冻等待期已过的 TRX，将其返还到可花费余额。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile withdraw-expire-unfreeze
    ```

    - `--owner`、`--multi`（可选）。

=== "交互模式"

    ```
    WithdrawExpireUnfreeze [OwnerAddress]
    ```

### 取消所有解冻 —— `cancel-all-unfreeze-v2` / `CancelAllUnfreezeV2`

取消所有待处理的 v2 解除质押请求，将这些 TRX 返还到质押状态。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile cancel-all-unfreeze-v2
    ```

    - `--owner`、`--multi`（可选）。

=== "交互模式"

    ```
    CancelAllUnfreezeV2 [owner_address]
    ```

## 资源代理

### 代理资源 —— `delegate-resource` / `DelegateResource`

把质押得到的带宽/能量出借给另一个账户。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile delegate-resource \
      --amount 1000000 --resource 1 --receiver TXyz... --lock --lock-period 86400
    ```

    - `--amount`（必填，SUN）、`--resource`（必填，`0`/`1`）、`--receiver`（必填）。
    - `--lock`（可选标志）—— 锁定该代理；`--lock-period`（可选）以区块数设置锁定时长。
    - `--owner`、`--multi`（可选）。

=== "交互模式"

    ```
    DelegateResource [OwnerAddress] balance ResourceCode ReceiverAddress [lock] [lockPeriod]
    ```

    `ResourceCode`：`0` BANDWIDTH，`1` ENERGY。`lock` 为 `true`/`false`。

### 取消代理资源 —— `undelegate-resource` / `UnDelegateResource`

收回先前代理出去的资源。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile undelegate-resource \
      --amount 1000000 --resource 1 --receiver TXyz...
    ```

    - `--amount`（必填）、`--resource`（必填）、`--receiver`（必填）。
    - `--owner`、`--multi`（可选）。

=== "交互模式"

    ```
    UnDelegateResource [OwnerAddress] balance ResourceCode ReceiverAddress
    ```

## 资源查询（无需鉴权）

### 账户带宽 —— `get-account-net` / `GetAccountNet`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-account-net --address TXyz...
    ```

    - `--address`（必填）。

=== "交互模式"

    ```
    GetAccountNet Address
    ```

### 账户资源 —— `get-account-resource` / `GetAccountResource`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-account-resource --address TXyz...
    ```

    - `--address`（必填）。

=== "交互模式"

    ```
    GetAccountResource Address
    ```

### 已代理资源 —— `get-delegated-resource(-v2)` / `GetDelegatedResource(V2)`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-delegated-resource \
      --from TFrom... --to TTo...
    java -jar build/libs/wallet-cli.jar --network nile get-delegated-resource-v2 \
      --from TFrom... --to TTo...
    ```

    - `--from`（必填）、`--to`（必填）。

=== "交互模式"

    ```
    GetDelegatedResource   FromAddress ToAddress
    GetDelegatedResourceV2 FromAddress ToAddress
    ```

### 代理资源账户索引 —— `get-delegated-resource-account-index(-v2)`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile \
      get-delegated-resource-account-index --address TXyz...
    java -jar build/libs/wallet-cli.jar --network nile \
      get-delegated-resource-account-index-v2 --address TXyz...
    ```

    - `--address`（必填）。

=== "交互模式"

    ```
    GetDelegatedResourceAccountIndex   Address
    GetDelegatedResourceAccountIndexV2 Address
    ```

### 最大可代理额度 —— `get-can-delegated-max-size` / `GetCanDelegatedMaxSize`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-can-delegated-max-size \
      --owner TXyz... --type 1
    ```

    - `--owner`（必填）、`--type`（必填，`0` BANDWIDTH / `1` ENERGY）。

=== "交互模式"

    ```
    GetCanDelegatedMaxSize [OwnerAddress] type
    ```

    `type`：`0` BANDWIDTH，`1` ENERGY。只给 `type` 时，使用已登录地址。

### 可用解冻次数 —— `get-available-unfreeze-count` / `GetAvailableUnfreezeCount`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-available-unfreeze-count --address TXyz...
    ```

    - `--address`（必填）。

=== "交互模式"

    ```
    GetAvailableUnfreezeCount [OwnerAddress]
    ```

### 可提取的解冻金额 —— `get-can-withdraw-unfreeze-amount` / `GetCanWithdrawUnfreezeAmount`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-can-withdraw-unfreeze-amount \
      --address TXyz... --timestamp 1700000000000
    ```

    - `--address`（必填）、`--timestamp`（可选，毫秒；默认为当前时间）。

=== "交互模式"

    ```
    GetCanWithdrawUnfreezeAmount [OwnerAddress] timestamp
    ```

    `timestamp`（毫秒）为必填。只给 `timestamp` 时，使用已登录地址。
