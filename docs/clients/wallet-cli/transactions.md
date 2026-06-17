# 交易

转移价值（TRX、TRC-10 资产、USDT）、多签签名流程，以及广播原始交易。

TRX 金额以 **SUN** 为单位（1 TRX = 1,000,000 SUN）。USDT 金额以代币的最小单位计（USDT 有 6 位小数，
故 1 USDT = 1,000,000）。

REPL 用可选的首参 `[OwnerAddress]` 支持多签；标准 CLI 用 `--owner` 配合 `--multi`。转账命令都需要鉴权。

## 转账 TRX —— `send-coin` / `SendCoin`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile send-coin \
      --to TXyz... --amount 1000000
    ```

    - `--to`（必填）、`--amount`（必填，SUN）。
    - `--owner`、`--permission-id`、`--multi`（可选）。
    - JSON 模式下，响应的 `data` 包含广播得到的 `txid`（仅单签转账）。

=== "交互模式"

    ```
    SendCoin [OwnerAddress] ToAddress Amount
    ```

## 转账 TRC-10 资产 —— `transfer-asset` / `TransferAsset`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile transfer-asset \
      --to TXyz... --asset 1000001 --amount 100
    ```

    - `--to`（必填）、`--asset`（必填，TRC-10 资产 ID）、`--amount`（必填）。
    - `--owner`、`--multi`（可选）。

=== "交互模式"

    ```
    TransferAsset [OwnerAddress] ToAddress AssetID Amount
    ```

## 转账 USDT —— `transfer-usdt` / `TransferUSDT`

转账 USDT（TRC-20）的便捷命令。仅在 `main`、`nile`、`shasta` 上支持。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile transfer-usdt \
      --to TXyz... --amount 1000000
    ```

    - `--to`（必填）、`--amount`（必填，最小单位 / 6 位小数）。
    - `--owner`、`--permission-id`、`--multi`（可选）。

=== "交互模式"

    ```
    TransferUSDT [OwnerAddress] ToAddress Amount
    ```

## 多签签名流程（仅 REPL）

对于多签账户，交易由一方构建，然后由额外的授权密钥依次签名，直到达到所需的签名权重，再进行广播。
以下命令作用于十六进制编码的交易字符串，仅在 REPL 中可用：

```
AddTransactionSign           TransactionHexString   # 为交易追加你的签名
GetTransactionSignWeight     TransactionHexString   # 显示当前与所需的签名权重
GetTransactionApprovedList   TransactionHexString   # 列出已签名的地址
```

典型流程：

1. 用某个转账/合约命令以 `[OwnerAddress]`（多签）形式构建交易。REPL 返回未签名/部分签名的交易
   十六进制串。
2. 每个联署者运行 `AddTransactionSign <hex>` 追加自己的签名，得到新的十六进制串。
3. 用 `GetTransactionSignWeight <hex>` 和 `GetTransactionApprovedList <hex>` 查看进度。
4. 一旦达到阈值，广播该交易。

在标准 CLI 中，单密钥的多签交易可在相关命令上用 `--multi` 和 `--permission-id` 选项一步完成。

### TronLink 多签 —— `TronlinkMultiSign`（仅 REPL）

交互式助手，引导你完成与 TronLink 兼容的多签签名流程。它提示输入，而非接受参数，且仅在 `main`、
`nile`、`shasta` 上支持。

```
TronlinkMultiSign
```

## 广播交易 —— `broadcast-transaction` / `BroadcastTransaction`

把已签名的十六进制编码交易提交到网络。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile broadcast-transaction \
      --transaction 0a83010a02...
    ```

    - `--transaction`（必填）—— 已签名交易的十六进制串。无需鉴权（交易已签名）。

=== "交互模式"

    ```
    BroadcastTransaction TransactionHexString
    ```
