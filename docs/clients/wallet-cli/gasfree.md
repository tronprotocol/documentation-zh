# GasFree

GasFree 让账户无需持有 TRX 作为 gas 即可转账代币（USDT）—— GasFree 服务的中继方提交链上交易，
并从转账的代币中扣除手续费。这些命令用于查询该服务、发起 GasFree 转账，以及追踪此前的转账。

GasFree 转账用你的密钥在本地签名，由 GasFree 服务中继，因此需要鉴权（一个活动/已登录的钱包）。
`gas-free-info` 仅在省略 `--address` 时需要鉴权（此时上报当前钱包）；`gas-free-trace` 无需鉴权。

## 服务信息 —— `gas-free-info` / `GasFreeInfo`

显示某地址的 GasFree 账户信息：派生出的 GasFree 地址、激活状态，以及构建转账时所用的当前
nonce/余额等细节。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile gas-free-info --address TXyz...
    ```

    - `--address`（可选）—— 默认为当前钱包的地址。提供 `--address` 时无需鉴权；省略时使用当前钱包，
      需要鉴权。

=== "交互模式"

    ```
    GasFreeInfo [Address]
    ```

    不带参数时，使用已登录账户的地址。

## GasFree 转账 —— `gas-free-transfer` / `GasFreeTransfer`

向收款方发起一笔 GasFree 代币转账（USDT）。手续费通过 GasFree 中继方以转账代币支付，而非以 TRX 支付。
JSON 模式下，响应的 `data` 包含所提交请求的 `gas_free_id`。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile gas-free-transfer \
      --to TXyz... --amount 1000000
    ```

    - `--to`（必填）、`--amount`（必填，最小单位 / 6 位小数）。

=== "交互模式"

    ```
    GasFreeTransfer receiverAddress amount
    ```

## 追踪转账 —— `gas-free-trace` / `GasFreeTrace`

按追踪/请求 ID（转账返回的 `gas_free_id`）查询此前提交的 GasFree 转账的状态。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile gas-free-trace --id <traceId>
    ```

    - `--id`（必填）。无需鉴权。

=== "交互模式"

    ```
    GasFreeTrace id
    ```
