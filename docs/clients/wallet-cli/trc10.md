# TRC-10 资产

TRC-10 是 TRON 的原生代币标准（由系统管理，而非由智能合约管理）。这些命令用于发行代币、更新其参数、
参与代币销售、转账代币，以及查询代币信息。

REPL 的构建交易命令用可选的首参 `[OwnerAddress]` 支持多签；标准 CLI 用 `--owner` + `--multi`。发行、
更新、参与、转账和解冻都需要鉴权；查询则不需要。

## 发行代币 —— `asset-issue` / `AssetIssue`

创建一个新的 TRC-10 代币。`TrxNum` 与 `AssetNum` 共同定义销售期间 TRX 与代币的兑换比例。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile asset-issue \
      --name MyToken --abbr MTK --total-supply 1000000000 \
      --trx-num 1 --ico-num 100 --precision 6 \
      --start-time 1700000000000 --end-time 1701000000000 \
      --description "My token" --url https://example.com \
      --free-net-limit 0 --public-free-net-limit 0
    ```

    - 必填：`--name`、`--abbr`、`--total-supply`、`--trx-num`、`--ico-num`、`--start-time`、
      `--end-time`、`--url`、`--free-net-limit`、`--public-free-net-limit`。
    - 可选：`--precision`、`--description`、`--owner`、`--multi`。

=== "交互模式"

    ```
    AssetIssue [OwnerAddress] AssetName AbbrName TotalSupply TrxNum AssetNum Precision \
      StartDate EndDate Description Url FreeNetLimitPerAccount PublicFreeNetLimit \
      [FrozenAmount0 FrozenDays0 ... FrozenAmountN FrozenDaysN]
    ```

    `StartDate`/`EndDate` 使用形如 `2018-03-01 2018-03-21` 的格式。结尾的
    `FrozenAmount/FrozenDays` 对为可选，用于冻结一部分供应量。

## 更新代币 —— `update-asset` / `UpdateAsset`

更新你已发行代币的可变参数。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile update-asset \
      --description "Updated" --url https://example.com \
      --new-limit 0 --new-public-limit 0
    ```

    - 必填：`--description`、`--url`、`--new-limit`、`--new-public-limit`。
    - 可选：`--owner`、`--multi`。

=== "交互模式"

    ```
    UpdateAsset [OwnerAddress] newLimit newPublicLimit description url
    ```

## 参与代币销售 —— `participate-asset-issue` / `ParticipateAssetIssue`

在代币的 ICO 窗口期内，通过向发行方发送 TRX 来购买代币。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile participate-asset-issue \
      --to TIssuer... --asset 1000001 --amount 1000000
    ```

    - 必填：`--to`、`--asset`、`--amount`。可选：`--owner`、`--multi`。

=== "交互模式"

    ```
    ParticipateAssetIssue [OwnerAddress] ToAddress AssetID Amount
    ```

## 转账代币

TRC-10 转账使用 `transfer-asset` / `TransferAsset`。见
[交易 → 转账 TRC-10 资产](transactions.md#trc-10-transfer-asset-transferasset)。

## 解冻代币供应 —— `unfreeze-asset` / `UnfreezeAsset`

在锁定期满后，解冻发行时被冻结的供应量。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile unfreeze-asset
    ```

    - `--owner`、`--multi`（可选）。

=== "交互模式"

    ```
    UnfreezeAsset [OwnerAddress]
    ```

## 代币查询（无需鉴权）

### 按发行账户查询 —— `get-asset-issue-by-account` / `GetAssetIssueByAccount`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-asset-issue-by-account --address TXyz...
    ```

    - `--address`（必填）。

=== "交互模式"

    ```
    GetAssetIssueByAccount Address
    ```

### 按 ID 查询 —— `get-asset-issue-by-id` / `GetAssetIssueById`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-asset-issue-by-id --id 1000001
    ```

    - `--id`（必填）。

=== "交互模式"

    ```
    GetAssetIssueById AssetID
    ```

### 按名称查询 —— `get-asset-issue-by-name` / `GetAssetIssueByName`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-asset-issue-by-name --name MyToken
    ```

    - `--name`（必填）。

=== "交互模式"

    ```
    GetAssetIssueByName AssetName
    ```

### 按名称查询全部 —— `get-asset-issue-list-by-name` / `GetAssetIssueListByName`

代币名称并不唯一；该命令返回共享同一名称的每一个代币。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-asset-issue-list-by-name --name MyToken
    ```

    - `--name`（必填）。

=== "交互模式"

    ```
    GetAssetIssueListByName AssetName
    ```

### 列出所有代币 —— `list-asset-issue` / `ListAssetIssue`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile list-asset-issue
    ```

=== "交互模式"

    ```
    ListAssetIssue
    ```

### 列出代币（分页）—— `list-asset-issue-paginated` / `ListAssetIssuePaginated`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile list-asset-issue-paginated \
      --offset 0 --limit 20
    ```

    - `--offset`（必填）、`--limit`（必填）。

=== "交互模式"

    ```
    ListAssetIssuePaginated offset limit
    ```
