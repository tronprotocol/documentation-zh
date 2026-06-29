# 治理

TRON 治理：注册和更新见证人（超级代表候选人）、投票、管理链上参数提案、佣金，以及奖励提取。

投票权来自质押的 TRX（TRON_POWER）。REPL 的构建交易命令用可选的首参 `[OwnerAddress]` 支持多签；
标准 CLI 用 `--owner` + `--multi`。改变状态的命令需要鉴权；查询则不需要。

## 见证人

### 创建见证人 —— `create-witness` / `CreateWitness`

将账户注册为见证人（SR 候选人）。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile create-witness --url https://my-sr.example
    ```

    - `--url`（必填）。`--owner`、`--multi`（可选）。

=== "交互模式"

    ```
    CreateWitness [OwnerAddress] Url
    ```

### 更新见证人 —— `update-witness` / `UpdateWitness`

更新见证人的 URL。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile update-witness --url https://my-sr.example
    ```

    - `--url`（必填）。`--owner`、`--multi`（可选）。

=== "交互模式"

    ```
    UpdateWitness [OwnerAddress] Url
    ```

### 列出见证人 —— `list-witnesses` / `ListWitnesses`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile list-witnesses
    ```

=== "交互模式"

    ```
    ListWitnesses
    ```

### 列出当前见证人（分页）—— `GetPaginatedNowWitnessList`（仅 REPL）

```
GetPaginatedNowWitnessList offset limit
```

## 投票

### 为见证人投票 —— `vote-witness` / `VoteWitness`

为一个或多个见证人投票。每一票分配你的部分投票权；投票会替换你之前的投票。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile vote-witness \
      --votes "TWitnessA... 100 TWitnessB... 50"
    ```

    - `--votes`（必填）—— 以空格分隔的 `address count` 对。
    - `--owner`、`--permission-id`、`--multi`（可选）。

=== "交互模式"

    ```
    VoteWitness [OwnerAddress] Address0 Count0 ... AddressN CountN
    ```

## 奖励与佣金

### 提取奖励 —— `withdraw-balance` / `WithdrawBalance`

将累积的投票/见证人奖励提取到可花费余额。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile withdraw-balance
    ```

    - `--owner`、`--multi`（可选）。

=== "交互模式"

    ```
    WithdrawBalance [OwnerAddress]
    ```

### 查询奖励 —— `get-reward` / `GetReward`

显示某地址当前可领取的奖励。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-reward --address TXyz...
    ```

    - `--address`（必填）。无需鉴权。

=== "交互模式"

    ```
    GetReward Address
    ```

### 查询佣金 —— `get-brokerage` / `GetBrokerage`

显示某见证人的佣金比例（SR 保留的奖励份额）。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-brokerage --address TWitness...
    ```

    - `--address`（必填）。无需鉴权。

=== "交互模式"

    ```
    GetBrokerage Address
    ```

### 更新佣金 —— `update-brokerage` / `UpdateBrokerage`

设置见证人的佣金比例（0–100）。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile update-brokerage --brokerage 20
    ```

    - `--brokerage`（必填，0–100）。`--owner`、`--multi`（可选）。

=== "交互模式"

    ```
    UpdateBrokerage OwnerAddress BrokeragePercent
    ```

    在 REPL 中，owner 地址为必填（它就是要设置佣金的见证人）。

## 提案

提案用于更改链上网络参数；由 SR 创建、由 SR 批准，并在收集到足够批准后生效。每个提案是一组
`parameter_id value` 对。

### 创建提案 —— `create-proposal` / `CreateProposal`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile create-proposal \
      --parameters "9 1 18 1"
    ```

    - `--parameters`（必填）—— 以空格分隔的 `id value` 对。
    - `--owner`、`--multi`（可选）。

=== "交互模式"

    ```
    CreateProposal [OwnerAddress] id0 value0 ... idN valueN
    ```

### 批准提案 —— `approve-proposal` / `ApproveProposal`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile approve-proposal --id 42 --approve true
    ```

    - `--id`（必填）、`--approve`（必填，`true` 表示添加批准 / `false` 表示撤回批准）。
    - `--owner`、`--multi`（可选）。

=== "交互模式"

    ```
    ApproveProposal [OwnerAddress] id is_or_not_add_approval
    ```

    `is_or_not_add_approval`：`true` 添加你的批准，`false` 移除它。

### 删除提案 —— `delete-proposal` / `DeleteProposal`

取消一个提案（仅提案人可操作）。

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile delete-proposal --id 42
    ```

    - `--id`（必填）。`--owner`、`--multi`（可选）。

=== "交互模式"

    ```
    DeleteProposal [OwnerAddress] proposalId
    ```

### 列出提案 —— `list-proposals` / `ListProposals`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile list-proposals
    ```

=== "交互模式"

    ```
    ListProposals
    ```

### 列出提案（分页）—— `list-proposals-paginated` / `ListProposalsPaginated`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile list-proposals-paginated --offset 0 --limit 20
    ```

    - `--offset`（必填）、`--limit`（必填）。

=== "交互模式"

    ```
    ListProposalsPaginated offset limit
    ```

### 查询某个提案 —— `get-proposal` / `GetProposal`

=== "标准 CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-proposal --id 42
    ```

    - `--id`（必填）。

=== "交互模式"

    ```
    GetProposal proposalId
    ```
