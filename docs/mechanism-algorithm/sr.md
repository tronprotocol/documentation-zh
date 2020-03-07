# 超级代表与委员会

<h3>1. 申请成为超级代表候选人规则 </h3>

 在TRON网络中，任何账户都可以申请成为超级代表候选人，都有机会成为超级代表。每个账户都可以投票给超级代表候选人。

 得票前27名的witness称为超级代表（SR），就具有出链块的权利。 从28名到127名（包含）的witness称为合伙人（Partner），从128名之后的witness称为候选人（Candidates）。

 投票统计每6小时统计一次，超级代表也就每6个小时变更一次。

 为了防止恶意攻击，成为超级代表候选人也需要一定代价的。TRON网络将直接烧掉申请者账户9999TRX。申请成功后，您就可以竞选超级代表了。

<h3>2. 选举超级代表 </h3>

 投票需要TRON Power(TP)，你的TRON Power(TP)的多少由当前冻结资金决定。TRON Power(TP)的计算方法：每冻结1TRX，就可以获得1单位TRON Power(TP)。

 TRON网络中的每一个账户都具有选举权，可以通过投票选出自己认同的超级代表了。

 在解冻后，你没有了冻结的资产，相应地失去了所有的TRON Power(TP)，因此以前的投票会失效。你可以通过重新冻结并投票来避免投票失效。

注意: 波场网络只记录你最后一次投票的状态，也就是说你的每一次投票都会覆盖以前所有的投票效果

+ 示例：

```
freezebalance 10,000,000 3 // 冻结了10TRX，获取了10单位TRON Power(TP)
votewitness witness1 4 witness2 6 // 同时给witness1投了4票，给witness2投了6票
votewitness witness1 3 witness2 7 // 同时给witness1投了3票，给witness2投了7票
```

以上命令的最终结果是给witness1投了3票，给witness2投了7票

**Witnesses分红**

默认比例是20%，witnesses可以调整该值。

如果一个witness获得20%的奖励，那么剩余的80%奖励会被分配给投票者。如果分红比例设置为100%，那么只有witness可以获得奖励；相反，如果设置为0，那么只有投票者会获得奖励。

<h3>3. 超级代表的奖励 </h3>

1.&nbsp;票数奖励

票数奖励是每生成一个区块奖励160TRX，总奖励数是4,608,000 TRX / 天。

对每一个SR与Partner，每天获得的票数奖励 = 4,608,000 * ( 获得的票数 /  总票数) x 20%  TRX

2.&nbsp;出块奖励

波场协议网络每3秒中会出一个区块，每个区块将给予超级代表16个TRX奖励，每年总计168,192,000 TRX将会被奖励给超级代表。

超级代表每次出块完成后，出块奖励都会发到超级代表的子账号当中，超级代表不能直接使用这部分资产，但可以查询。 每24h允许一次提取操作。从该子账号转移到超级代表的账户中。

16 (TRX/区块) * 28,800 (总区块数/day) = 460,800 (TRX/天)

对每一个SR，每天获得的出块奖励 = (460,800 / 27) x 20%  TRX

实际奖励可能会比理论上的奖励少，因为出块失败或者维护期切换。

<h3>4. 投票者的奖励 </h3>

如果投票给Super Representative：

每日获得奖励 =  (((你投给一个witness的票数) * 4,608,000 / 总票数) * 80%) + ((460,800 / 27) * 80%) * (你投给一个witness的票数) / (一个witness获得的总票数) TRX

如果你投票给Partner：

每日获得奖励 =  (((你投给一个witness的票数) * 4,608,000 / 总票数) * 80%) TRX

<h3> 5. 委员会 </h3>

<h4> 5.1 什么是委员会 </h4>
委员会用于修改Tron网络动态参数，如出块奖励、交易费用等等。委员会由当前的27个超级代表组成。每个超级代表都具有提议权、对提议的投票权，
当提议获得19个代表及以上的赞成票时，该提议获得通过，并在下个维护期内进行网络参数修改。

<h4> 5.2 创建提议 </h4>
只有超级代表（SR）、合伙人（Partner）和候选人（Candidates）对应账户具有提议权。

允许修改的网络动态参数以及编号如下( [min,max] )：
{0,1}：1代表‘通过’或者‘激活’，0代表否。

|  #    | Command  |  Value  |
|  ----  | ----    | ---- |
|  0     | getMaintenanceTimeInterval <br> (修改超级代表调整时间间隔)	| 6  Hours <br> [3 * 27, 24 * 3600] s |
|  1     | getAccountUpgradeCost <br> (修改账户升级为超级代表的费用) | 9999  TRX <br> [0, 100000000000] TRX |
|  2     | getCreateAccountFee <br> (修改创建账户费用) | 0.1  TRX <br> [0, 100000000000] TRX |
|  3     | getTransactionFee <br> (修改TRX抵扣带宽的费用) | 10  Sun/Byte <br> [0, 100000000000] TRX |
|  4     | getAssetIssueFee <br> (修改资产发行费用) | 1024  TRX <br> [0, 100000000000] TRX|
|  5     | getWitnessPayPerBlock <br> (修改超级代表出块奖励) | 16 TRX <br> [0, 100000000000] TRX |
|  6     | getWitnessStandbyAllowance <br> (修改分给前127名超级代表候选人的奖励) | 115200  TRX <br> [0, 100000000000] TRX |
|  7     | getCreateNewAccountFeeInSystemContract <br> (修改系统创建账户的费用) | 0 TRX  |
|  8     | getCreateNewAccountBandwidthRate <br> (提议7、8，组合使用，用于修改创建账户时对资源或TRX的消耗) | 1&nbsp;Bandwith/Byte |
|  9     | getAllowCreationOfContracts <br> (控制虚拟机功能的开启 ) | 1 <br> {0, 1} |
|  10	 | getRemoveThePowerOfTheGr <br> (用于清除GR的创世票数) |	1 <br> {0, 1}|
|  11	 | getEnergyFee <br> (修改能量费用) | 10 Sun <br> [0, 100000000000] TRX |
|  12	 | getExchangeCreateFee <br> (修改创建交易对的费用) | 1024 TRX <br> [0, 100000000000] TRX |
|  13	 | getMaxCpuTimeOfOneTx <br> (修改交易最长执行时间) | 50 ms <br> [0, 1000] ms |
|  14	 | getAllowUpdateAccountName <br> (允许用户更改昵称以及昵称同名) | 0 <br> {0, 1} |
|  15	 | getAllowSameTokenName <br> (允许创建相同名称的token) | 1 <br> {0, 1} |
|  16	 | getAllowDelegateResource <br> (控制资源代理功能的开启) | 1 <br> {0, 1} |
|  18	 | getAllowTvmTransferTrc10 <br> (允许智能合约调用TRC10 token的接口) | 1 <br> {0, 1} |
|  19	 | getTotalEnergyCurrentLimit <br> (修改ENERGY总量) | 50000000000 |
|  20	 | getAllowMultiSign <br> (允许开启多重签名) | 1 <br> {0, 1} |
|  21	 | getAllowAdaptiveEnergy <br> (允许ENERGY总量自适应调整) | 0 <br> {0, 1} |
|  22	 | getUpdateAccountPermissionFee <br> (修改账户权限费用) | 100 TRX |
|  23	 | getMultiSignFee <br> (修改多重签名费用) | 1 TRX |
|  24	 | getAllowProtoFilterNum <br> (允许更新protobuf的数字) | 0 <br> {0, 1} |
|  26	 | getAllowTvmConstantinople <br> (允许TVM支持君士坦丁堡更新) | 1 <br> {0, 1} |
|  27	 | getAllowShieldedTransaction <br> (允许匿名交易开启) | 0 <br> {0, 1} |
|  28	 | getShieldedTransactionFee <br> (修改匿名交易手续费) | 10 TRX <br> [0, 10000] TRX |
|  29	 | getAdaptiveResourceLimitMultiplier <br> (用于修改动态能量最大值) | 1000 <br> [1, 10000] |
|  30    | getChangeDelegation <br> (修改更换委托机制) | 1 <br> {0, 1} |
|  31    | getWitness127PayPerBlock <br> (修改票数排名奖励) | 160  TRX <br> [0, 100000000000] TRX |
|  32    | getAllowTvmSolidity059 <br> (允许虚拟机支持0.5.9版本的Solidity编译器) | 0 <br> {0, 1} |
|  33    | getAdaptiveResourceLimitTargetRatio <br> (修改能量目标值) | 10 <br> [1, 1000] |


+ 示例：
```text
createproposal id0 value0 ... idN valueN
id0_N: 参数编号
value0_N: 新参数值
```

注：Tron网络中，1 TRX = 1000_000 SUN。

<h4> 5.3 对提议进行投票 </h4>
提议仅支持投赞成票，不投票代表不赞同。从提议创建时间开始，3天时间内为提议的有效期。超过该时间范围，该提议如果没有获得足够的
赞成票，该提议失效。允许取消之前投的赞成票。


+ 示例：
```text
approveProposal id is_or_not_add_approval
id: 提议Id，根据提议创建时间递增
is_or_not_add_approval: 赞成或取消赞成
```

<h4> 5.4 取消提议 </h4>
提议创建者，能够在提议生效前，取消提议。

+ 示例：
```text
deleteProposal proposalId
id: 提议Id，根据提议创建时间递增
```

<h4> 5.5 查询提议 </h4>

以下接口可以查询提议，包括：

- 查询所有提议信息（ListProposals）
- 分页查询提议信息（GetPaginatedProposalList）
- 查询指定提议信息（GetProposalById）

相关api详情，请查询[Tron HTTP API](../api/http.md).
