# 超级代表与委员会

## 申请成为超级代表候选人规则

 TRON网络中的区块生产者也叫超级代表，通过投票选举产生。任何账户只需支付9999个TRX就可以申请成为超级代表候选人，参与超级代表竞选。任何账户都可以给超级代表候选人投票。得票前27名的候选人即成为超级代表（SR），具有出块的权利。超级代表需要运行一个TRON节点来参与区块生产，同时也会获得出块奖励和投票奖励，给超级代表投票的选民会获得投票奖励。
 
 票数排名第28～127名的超级代表候选人也叫超级代表合伙人。超级代表合伙人不参与出块和打包交易，但会获得投票奖励，给超级代表合伙人投票的选民也会获得投票奖励。
 
 投票统计每6小时统计一次，超级代表和超级合伙人也就每6个小时变更一次。


## 选举超级代表

 投票需要TRON Power(TP)，你的TRON Power(TP)的多少由当前质押资金决定。TRON Power(TP)的计算方法：每质押1TRX，就可以获得1单位TRON Power(TP)。

 TRON网络中的每一个账户都具有选举权，可以通过投票选出自己认同的超级代表。

 在解锁后，你没有了质押的资产，相应地失去了所有的TRON Power(TP)，因此以前的投票会失效。你可以通过重新质押并投票来避免投票失效。

注意: 波场网络只记录你最后一次投票的状态，也就是说你的每一次投票都会覆盖以前所有的投票效果

+ 示例：

```shell
freezebalancev2 10,000,000 3 # 质押了10TRX，获取了10单位TRON Power(TP)
votewitness SR1 4 SR2 6 # 同时给SR1投了4票，给SR2投了6票
votewitness SR1 3 SR2 7 # 同时给SR1投了3票，给SR2投了7票
```

以上命令的最终结果是给SR1投了3票，给SR2投了7票


## 奖励
### 超级代表佣金比例
默认佣金比例是20%，即超级代表获得20%的奖励，剩余的80%奖励会被分配给投票者，超级代表和超级代表合伙人可以通过wallet/getBrokerage接口查询佣金比例, 也可以通过wallet/updateBrokerage接口修改佣金比例。如果分红比例设置为100%，那么只有超级代表可以获得奖励；相反，如果设置为0，那么只有投票者会获得奖励。

### 产块奖励和投票奖励
奖励可分为产块奖励和投票奖励，二者之间的差别如下所示：

|  | **产块奖励** | **投票奖励** |
| :--- | :--- | :--- |
| **奖励总数** | 链上参数，可以通过提案修改，目前是8 TRX | 链上参数，可以通过提案修改，目前是128 TRX |
| **相关链上参数序号** | #5 (要求#30链参数激活) | #31 (要求#30链参数激活) |
| **相关链上参数名** | getWitnessPayPerBlock | getWitness127PayPerBlock |
| **奖励发放对象** | 产块的SR、SR的投票者 | SR和SR合伙人、SR和SR合伙人的投票者 |
| **奖励发放时间** | SR: 每产完一个块<br>SR的投票者：投票者发起以下4种交易之一触发奖励:<br><span style="margin-left: 1em;">VoteWitnessContract<br><span style="margin-left: 1em;">WithdrawBalanceContract<br><span style="margin-left: 1em;">UnfreezeBalanceContract<br><span style="margin-left: 1em;">UnfreezeBalanceV2Contract | SR和SR合伙人: 同SR，SR和SR合伙人的投票者：同SR的投票者 |
| **具体的奖励值** | SR:8 * brokerageRate<br>SR的每个投票者：8 * (1-brokerageRate) * 投票数量/SR获得的总投票数量 | 每个SR和SR合伙人：(128 * brokerageRate)/127，SR和SR合伙人的每个投票者：128 * (1-brokerageRate) * 投票数量/（SR和SR合伙人获得的总投票数量）|

**注意** ：

- brokerageRate：佣金比例
- SR和SR的合伙人：前127位的witness。
- 如果投票者投票给SR，那么它既有产块奖励，也有投票奖励，如果投票者投票给SR合伙人，那么它只有投票奖励。

## 委员会

### 什么是委员会

委员会用于修改TRON网络动态参数，如出块奖励、交易费用等等。委员会由当前的27个超级代表组成。每个超级代表都具有提议权和对提议的投票权，
当提议获得至少18个代表的赞成票时，该提议获得通过，并在下个维护期内进行网络参数修改。

### 创建提议
除超级代表（SR）外，超级代表合伙人（SR Partner）和超级代表候选人（SR Candidate）也具有提议权, 并且只有它们拥有这个权利。

TRON网络动态参数及其编号请参考[这里](https://tronscan.org/#/sr/committee)。

+ 示例：

```text
createproposal id0 value0 ... idN valueN
id0_N: 参数编号
value0_N: 新参数值
```


### 对提议进行投票

提议仅支持投赞成票，不投票代表不赞同。从提议创建时间开始，3天时间内为提议的有效期。超过该时间范围，该提议如果没有获得足够的
赞成票，该提议失效。允许取消之前投的赞成票。

+ 示例：

```shell
approveProposal id is_or_not_add_approval
id: 提议Id，根据提议创建时间递增
is_or_not_add_approval: 赞成或取消赞成
```

### 取消提议

提议创建者，能够在提议生效前，取消提议。

+ 示例：

```shell
deleteProposal proposalId
id: 提议Id，根据提议创建时间递增
```

### 查询提议

以下接口可以查询提议，包括：

+ 查询所有提议信息（ListProposals）
+ 分页查询提议信息（GetPaginatedProposalList）
+ 查询指定提议信息（GetProposalById）

相关api详情，请查询[TRON HTTP API](../api/http.md).
