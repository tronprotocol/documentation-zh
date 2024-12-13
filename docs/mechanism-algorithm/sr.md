# 超级代表与委员会

## 1. 申请成为超级代表候选人规则

 TRON网络中的区块生产者也叫超级代表，通过投票选举产生。任何账户只需支付9999个TRX就可以申请成为超级代表候选人，参与超级代表竞选。任何账户都可以给超级代表候选人投票。得票前27名的候选人即成为超级代表（SR），具有出块的权利。超级代表需要运行一个TRON节点来参与区块生产，同时也会获得出块奖励和投票奖励，给超级代表投票的选民会获得投票奖励。
 
 票数排名第28～127名的超级代表候选人也叫超级代表合伙人。超级代表合伙人不参与出块和打包交易，但会获得投票奖励，给超级代表合伙人投票的选民也会获得投票奖励。
 
 投票统计每6小时统计一次，超级代表和超级合伙人也就每6个小时变更一次。


## 2. 选举超级代表

 投票需要TRON Power(TP)，你的TRON Power(TP)的多少由当前质押资金决定。TRON Power(TP)的计算方法：每质押1TRX，就可以获得1单位TRON Power(TP)。

 TRON网络中的每一个账户都具有选举权，可以通过投票选出自己认同的超级代表。

 在解锁后，你没有了质押的资产，相应地失去了所有的TRON Power(TP)，因此以前的投票会失效。你可以通过重新质押并投票来避免投票失效。

注意: 波场网络只记录你最后一次投票的状态，也就是说你的每一次投票都会覆盖以前所有的投票效果

+ 示例：

```shell
freezebalancev2 10,000,000 3 # 质押了10TRX，获取了10单位TRON Power(TP)
votewitness witness1 4 witness2 6 # 同时给witness1投了4票，给witness2投了6票
votewitness witness1 3 witness2 7 # 同时给witness1投了3票，给witness2投了7票
```

以上命令的最终结果是给witness1投了3票，给witness2投了7票

### Witnesses分红

默认比例是20%，超级代表和超级代表合伙人可以通过[wallet/getBrokerage](../api/http.md/#walletgetbrokerage)接口查询佣金比例, 也可以通过[wallet/updateBrokerage](../api/http.md/#walletupdatebrokerage)接口修改佣金比例。

如果一个witness获得20%的奖励，那么剩余的80%奖励会被分配给投票者。如果分红比例设置为100%，那么只有witness可以获得奖励；相反，如果设置为0，那么只有投票者会获得奖励。

## 3. 超级代表和合伙人的奖励

### 票数奖励

票数奖励是每生成一个区块奖励160TRX，分给SR和Partner。

`每天总票数奖励数 = (24h/出块时间3s) * 160 = 4,608,000 TRX / 天`

对每一个SR与Partner，每天获得的票数奖励TRX = 总奖励数 * ( 获得的票数 / SR与Partner的总票数) x 分红比例

### 出块奖励

波场协议网络每3秒中会出一个区块，每个区块将给予超级代表16个TRX奖励，每年总计 365 * 24 * 3600 * 16TRX / 3 = 168,192,000 TRX将会被奖励给超级代表。

超级代表每次出块完成后，出块奖励都会发到超级代表的账号当中，超级代表不能直接使用这部分资产，但可以查询。

`每天总出块奖励 = (24h/出块时间3s) * 16 = 460,800 (TRX/天)`

单个SR每天获得的出块奖励 = (460,800 / 27) x Witness分红  TRX

实际奖励可能会比理论上的奖励少，因为出块失败或者维护期切换。

### 奖励领取
SR与Partner的票数奖励以Allowance的方式记录在账户里面，每次新的区块生成之后会随即更新，通过[wallet/getaccount](../api/http.md/#walletgetaccount)可以查询。
统一通过[wallet/withdrawbalance](../api/http.md/#withdrawbalance)把账户相关的票数, 出块以及结算的投票奖励领取到账户余额，每24小时限领一次。

## 4. 投票者的奖励

每次出块时，投票者都会根据Witness分红比例获取所投SR或Partner对应的奖励：从SR分成出块和票数奖励，和从Partner分成票数奖励。
我们根据下面的参数公式，计算投票奖励：

- `总投票比例 = 你的投票数 / SR和Partner获取的总票数`
- `选民抽成 = (1 - Witness分红)`

如果投票给SR：

- 如果轮到该SR出块 `每次出块获得的Reward =（SR投票比例 * 16 + 总投票比例 * 160）* 选民抽成 TRX`
- 如果不是该SR出块 `每次出块获得的Reward =（总投票比例 * 160）* 选民抽成 TRX`
- `每日获得总奖励 = （SR投票比例 * 每天总出块奖励 / 27 + 总投票比例 * 每天总票数奖励数）* 选民抽成 TRX`
- `SR投票比例 = 你的投票数 / 该SR获取的总票数`

如果你投票给Partner：

- `每次出块获得的Reward =（总投票比例 * 160）* 选民抽成 TRX`
- `每日获得总奖励 = 总投票比例 * 每天总票数奖励数 * 选民抽成 TRX`

注意：上面的每日获得总奖励是理论上获取的奖励上限，实际情况每6个小时维护期后SR和Partner可能有变动，或者出块失败，或者账户重新投票，奖励应该会变小。

每次产块后波场的具体计算逻辑是：java-tron会以SR和Partner的账户地址+维护期Cycle为key累加新的分成Reward到代理存储delegationStore。
然后在维护期结束时，对每个witness计算本维护期Cycle的累积witnessVi = lastCycle witnessVi + (currentCycle reward)/voteCount，
即把每轮每个选票分得的reward累加一起。投票账户获得的奖励计算是从上次领取过的Cycle到上个维护期Cycle的witnessVi的差值，然后更新领取过的Cycle。
接口[wallet/getreward](../api/http.md/#walletgetreward)会返回结算过的可领的投票奖励+Allowance（见上面章节）。

### 奖励领取
统一通过[wallet/withdrawbalance](../api/http.md/#walletwithdrawbalance)把账户相关的票数, 出块以及投票的奖励领取到账户余额，每24小时限领一次。

## 5. 委员会

### 5.1 什么是委员会

委员会用于修改Tron网络动态参数，如出块奖励、交易费用等等。委员会由当前的27个超级代表组成。每个超级代表都具有提议权、对提议的投票权。从提议创建时间开始，3天时间内为提议的有效期。
当提议获得18个代表及以上的赞成票时，该提议获得通过，并在下个维护期内进行网络参数修改。

### 5.2 创建提议

只有超级代表（SR）、合伙人（Partner）和候选人（Candidates）对应账户具有提议权。

TRON网络动态参数及其编号请参考[这里](https://tronscan.org/#/sr/committee)。

+ Wallet-Cli指令示例：

```text
createproposal id0 value0 ... idN valueN
id0_N: 参数编号
value0_N: 新参数值
```


### 5.3 对提议进行投票

提议仅支持投赞成票，不投票代表不赞同。从提议创建时间开始，3天时间内为提议的有效期。超过该时间范围，该提议如果没有获得足够的
赞成票，该提议失效。允许取消之前投的赞成票。

+ Wallet-Cli指令示例：

```shell
approveProposal id is_or_not_add_approval
id: 提议Id，根据提议创建时间递增
is_or_not_add_approval: 赞成或取消赞成
```

### 5.4 取消提议

提议创建者，能够在提议生效前，取消提议。

+ Wallet-Cli指令示例：

```shell
deleteProposal proposalId
id: 提议Id，根据提议创建时间递增
```

### 5.5 查询提议

以下接口可以查询提议，包括：

+ 查询所有提议信息[wallet/listproposals](../api/http.md/#walletlistproposals)
+ 分页查询提议信息[wallet/getpaginatedproposallist](../api/http.md/#walletgetpaginatedproposallist)
+ 查询指定提议信息[wallet/getproposalbyid](../api/http.md/#walletgetproposalbyid)

相关api详情，请查询[Tron HTTP API](../api/http.md/#_6)。
其他相关参考文档[super-representatives](https://developers.tron.network/docs/super-representatives).
