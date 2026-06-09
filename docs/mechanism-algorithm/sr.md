# 超级代表与委员会

## 申请成为超级代表候选人规则

在 TRON 网络中，区块生产者被称为超级代表 (Super Representative, SR)，他们通过全网投票选举产生。任何账户只需支付 9999 TRX，即可申请成为超级代表候选人（SR Candidate）；任何持有 TRX 的账户都可以为 SR 候选人投票。

申请成为候选人可通过 wallet-cli 客户端的 `CreateWitness` 命令发起，申请时需要提交一个 URL（用于公示候选人主页等信息）。

根据最终的得票排名，得票数排名前 127 位的候选人将担任以下两种角色之一：

 - 超级代表 (SR)：得票数排名前 27 位的候选人。他们是 TRON 网络的核心节点，负责生产区块和打包交易，并因此获得出块奖励和投票奖励。
 - 超级代表合伙人 (Super Representative Partner，简称 SR Partner)：得票数排名第 28 至 127 位的候选人。他们作为网络的备用节点，不参与区块生产，但会分享投票奖励。

TRON 网络每 6 小时进行一轮投票统计，SR 和 SR Partner 的席位归属也随之每 6 小时更新一次。

## 选举超级代表

TRON 网络中的所有账户都拥有选举权，可以通过投票来支持自己认可的 SR 候选人。投票的核心是 TRON Power (TP)，它决定了您的投票权重。

 - 获取投票权 (TRON Power)

      您的 TP 数量与您质押（Stake）的 TRX 数量直接挂钩。计算方法：每质押 1 TRX，您将获得 1 TP。

 - 解质押对投票的影响

      当您解质押一部分 TRX 时，您会失去等量的 TP。系统将按以下规则回收 TP：

    * 优先回收未使用的 TP
    * 如果可用 TP 不足，系统将自动从您已投出的票数中按比例撤回，以弥补 TP 的不足
    * 若您已向多个 SR 投票，系统将根据您在每个 SR 上的投票比例，按比例从他们那里撤回相应的票数并回收 TP

**重要提示:** TRON 网络只记录你最后一次投票的状态，也就是说你的每一次投票都会覆盖以前所有的投票效果。

**示例：**

```
>freezebalancev2 10000000 1 # 质押 10 TRX（金额单位为 sun，1 TRX = 1,000,000 sun，故 10 TRX = 10000000 sun），获取 10 单位 TRON Power(TP)；资源类型：0 为带宽，1 为能量
>votewitness SR1 4 SR2 6 # 同时给 SR1 投了 4 票，给 SR2 投了 6 票
>votewitness SR1 3 SR2 7 # 同时给 SR1 投了 3 票，给 SR2 投了 7 票
```

以上命令的最终结果是给 SR1 投了 3 票，给 SR2 投了 7 票。


## 奖励

### 超级代表佣金比例

超级代表（SR）和超级代表合伙人（SR Partners）可以通过设置佣金比例 (Brokerage Rate)，来决定如何将获得的奖励在自己与投票者之间进行分配。

 - 默认比例

    新当选的超级代表或合伙人的默认佣金比例为 20%。这意味着，在总奖励中，20% 将归属超级代表本人，剩余的 80% 将按票数比例分配给其投票者。
    
 - 自定义设置

    超级代表与合伙人可以随时通过 [`wallet/updateBrokerage`](../api/http/witness-and-governance/updateBrokerage.md) 接口调整自己的佣金比例。

    - 100% 佣金：所有奖励都归超级代表/合伙人所有。
    - 0% 佣金：所有奖励都将分配给其投票者。


### 产块奖励和投票奖励

奖励可分为产块奖励和投票奖励，二者之间的差别如下所示：

|  | **产块奖励** | **投票奖励** |
| :--- | :--- | :--- |
| **奖励总数** | 链上参数，可以通过提案修改，目前是 8 TRX | 链上参数，可以通过提案修改，目前是 128 TRX |
| **相关链上参数序号** | #5 (要求 #30 链参数激活) | #31 (要求 #30 链参数激活) |
| **相关链上参数名** | `getWitnessPayPerBlock` | `getWitness127PayPerBlock` |
| **奖励发放对象** | 产块的 SR、SR 的投票者 | SR 和 SR 合伙人、SR 和 SR 合伙人的投票者 |
| **奖励发放** | **SR**: 每产完一个块<br><br>**SR 的投票者**：投票者发起以下 4 种交易之一触发奖励发放:<br>- `VoteWitnessContract`<br>- `UnfreezeBalanceContract`<br>- `UnfreezeBalanceV2Contract` <br>- `WithdrawBalanceContract`(和前三个交易不同：奖励发放后马上提取到账户余额)| **SR 和 SR 合伙人**: 每产完一个块<br><br>**SR 和 SR 合伙人的投票者**：投票者发起以下 4 种交易之一触发奖励发放:<br>- `VoteWitnessContract`<br>- `UnfreezeBalanceContract`<br>- `UnfreezeBalanceV2Contract` <br>- `WithdrawBalanceContract`(和前三个交易不同：奖励发放后马上提取到账户余额)|
| **提取奖励到账户余额** |  通过发起`WithdrawBalanceContract`交易触发 | 通过发起`WithdrawBalanceContract`交易触发 |
| **具体的奖励值** | **SR**:<br>`8 * brokerageRate`<br><br>**SR 的投票者**：<br>`8 * (1-brokerageRate) * (该投票者的投票数量) / (该SR获得的总投票数量)` | **SR / SR合伙人**：<br>`128 * brokerageRate * (该SR/SR合伙人获得的投票数量) / (所有SR和SR合伙人获得的总投票数量)`<br><br>**SR / SR 合伙人的投票者**：<br>`128 * (1-brokerageRate) * (该投票者的投票数量) / (所有SR和SR合伙人获得的总投票数量)`|

**注意**：

- 链上参数序号和参数名可以在 [这里](https://tronscan.org/#/sr/committee) 查看
- `brokerageRate`：佣金比例
- 超级代表和超级代表合伙人：前 127 位超级代表候选人。
- 排名在 127 位之后的候选人仍为超级代表候选人，既不获得出块奖励，也不获得投票奖励。同样地，他们的投票者也无法获得出块奖励和投票奖励。
- 如果投票者投票给 SR，那么它既有产块奖励，也有投票奖励，但是产块奖励只有其投票的 SR 产块时才有。如果投票者投票给超级代表合伙人，那么它只有投票奖励。
- 通过 `WithdrawBalanceContract` 交易将奖励提取到账户余额存在 24 小时提取间隔限制：若距离上一次提取不足 24 小时，再次提取会在校验阶段被拒绝。

## 委员会

### 关于委员会

委员会是 TRON 网络的最高治理机构，负责对网络的核心动态参数（如交易费、出块奖励等）进行调整。

 - **组成**：委员会由当前在任的 27 位超级代表 (SR) 组成。
 - **权力**：每位委员会成员（即超级代表）都拥有两项核心权力：

    - 创建提案：发起一个修改网络参数的提案。
    - 对提案投票：对修改网络参数的提案进行投票（包括自己发起的提案）。
    
 - **提案生效机制**：
当一个提案获得了至少 18 名超级代表的赞成票后，该提案即获通过。通过的提案将在下一个维护周期自动生效，完成对网络参数的修改。

**注意**：下面的创建、投票、取消提案示例均为 wallet-cli 客户端命令；对应的 HTTP 接口见 [ProposalCreate](../api/http/witness-and-governance/proposalcreate.md)、[ProposalApprove](../api/http/witness-and-governance/proposalapprove.md)、[ProposalDelete](../api/http/witness-and-governance/proposaldelete.md)。

### 创建提案

在 TRON 网络中，超级代表、超级代表合伙人、超级代表候选人均可以发起修改网络参数提案。

TRON 网络动态参数及其编号请参考 [这里](https://tronscan.org/#/sr/committee)。

**示例**：

```
createproposal parameter0 value0 ... parameterN valueN
parameter0_N: 要修改的网络参数编号（不是提案 id）
value0_N: 该参数的新值
```

**注意**：一个提案可以通过提供多组 `parameter value` 键值对，一次性修改多个网络参数。

### 对提案进行投票

对提案的投票过程遵循以下核心规则：

1. TRON 的治理投票系统仅支持赞成票。不进行投票操作，即代表不赞同该提案。
2. 从提案创建时间开始，默认 3 天为提案的有效期。该有效期由链上参数 `getProposalExpireTime`（#92）决定，可通过提案修改（主网当前为 3 天）。超过该时间范围，该提案如果没有获得足够的赞成票，则该提案失效。

**示例**：

```
approveProposal id is_or_not_add_approval
id: 提案Id
is_or_not_add_approval: true 表示投赞成票，false 表示撤回之前的赞成票
```

**注意**：以下两种情况会在校验阶段被拒绝：

- 已经赞成过该提案时，再次传 `true`（不能对同一提案重复赞成）。
- 之前没有赞成过该提案时，传 `false`（没有可撤回的赞成票）。

### 取消提案

提案创建者能够在提案生效前取消提案。

**示例**：

```
deleteProposal proposalId
id: 提案Id
```

### 查询提案

以下接口可以查询提案，包括：

+ 查询所有提案信息（[ListProposals](../api/http/witness-and-governance/listproposals.md)）
+ 分页查询提案信息（[GetPaginatedProposalList](../api/http/witness-and-governance/getpaginatedproposallist.md)）
+ 查询指定提案信息（[GetProposalById](../api/http/witness-and-governance/getproposalbyid.md)）
