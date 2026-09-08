# 投票、奖励与见证人

为超级代表投票、管理佣金比例并领取奖励，以及创建 / 更新见证人。

## 如何投票 {#how-to-vote}

投票需要份额（share）。份额可以通过冻结资金获得。

- 份额的计算方式是：每冻结 **1 TRX** 可获得 **1** 单位份额。
- 解冻后，此前的投票会失效；如需恢复票数，需要重新冻结并再次投票。

**注意** TRON 网络只记录你最后一次投票的状态，也就是说，你的每一次投票都会覆盖此前的全部投票
结果。

例如：

```console
> freezeBalance 10000000 3 1  # 冻结 10 TRX，获得 10 单位份额

> votewitness TJmka325yjJKeFpQDwKSQAoNwEyNGhsaEV 4 TFFLWM7tmKiwGtbh2mcz2rBssoFjHjSShG 6  # 同时为第一个 SR 投 4 票、为第二个 SR 投 6 票

> votewitness TJmka325yjJKeFpQDwKSQAoNwEyNGhsaEV 10  # 只为第一个 SR 投 10 票
```

每个超级代表都必须以 Base58Check 地址给出，不接受占位名称。上述命令的最终结果是 `TJmka325…` 得 10 票，`TFFLWM7t…` 得 0 票。

## 佣金比例（Brokerage） {#brokerage}

为见证人投票后，投票者可以获得奖励。见证人可以设置佣金比例，默认值为 20%；也就是说，见证人
获得总奖励的 20%，其余 80% 分配给投票者。

### GetBrokerage

查看见证人的佣金比例。

```console
> getbrokerage OwnerAddress
```

`OwnerAddress`——见证人账户的 Base58Check 地址。

### GetReward

查询未领取的奖励。

```console
> getreward OwnerAddress
```

`OwnerAddress`——投票者账户的 Base58Check 地址。

### UpdateBrokerage

更新佣金比例。该命令通常由见证人账户使用。

```console
> updateBrokerage OwnerAddress brokerage
```

- `OwnerAddress`——见证人账户的 Base58Check 地址。
- `brokerage`——新的佣金比例，取值范围为 0 到 100。例如，输入 10 表示 SR 获得总奖励的 10%，
  其余 90% 分配给投票者。

示例：

```console
> getbrokerage TZ7U1WVBRLZ2umjizxqz3XfearEHhXKX7h

> getreward  TNfu3u8jo1LDWerHGbzs2Pv88Biqd85wEY

> updateBrokerage TZ7U1WVBRLZ2umjizxqz3XfearEHhXKX7h 30
```

## WithdrawBalance

提取投票奖励或出块奖励。

每个区块产生后，出块奖励会进入账户的 `allowance`；每 **24 小时**可以提取一次，将奖励转入
`balance`。`allowance` 中的资金不能被锁定或交易。

```console
> WithdrawBalance [owner_address]
```

```console
> WithdrawBalance TEDapYSVvAZ3aYH7w8N9tMEEFKaNKUD5Bp
```

## 如何创建见证人 {#how-to-create-witness}

注册为超级代表候选人需要燃烧一笔费用，其数额由链参数 `getAccountUpgradeCost` 决定。该参数可以通过治理提案修改，因此请用 [`GetChainParameters`](chain-data.md#getchainparameters) 查询当前值，不要按固定数额估算。这部分资金会被直接燃烧。

### CreateWitness

申请成为超级代表候选人。

```console
> CreateWitness [owner_address] url
```

```console
> CreateWitness TEDapYSVvAZ3aYH7w8N9tMEEFKaNKUD5Bp https://sr.example.com
```

### UpdateWitness

编辑 SR 官方网站的 URL。

```console
> UpdateWitness TEDapYSVvAZ3aYH7w8N9tMEEFKaNKUD5Bp https://sr.example.com/v2
```

## ListWitnesses

获取所有见证人节点的信息。

## GetPaginatedNowWitnessList

分页获取当前见证人列表。

```console
wallet> getPaginatedNowWitnessList 0 2
{
	"witnesses": [
		{
			"address": "TJmka325yjJKeFpQDwKSQAoNwEyNGhsaEV",
			"voteCount": 5405926918,
			"url": "http://sr-8.com",
			"totalProduced": 1801675,
			"totalMissed": 456,
			"latestBlockNum": 64577529,
			"latestSlotNum": 590063589,
			"isJobs": true
		},
		{
			"address": "TFFLWM7tmKiwGtbh2mcz2rBssoFjHjSShG",
			"voteCount": 2322244615,
			"url": "http://sr-27.com",
			"totalProduced": 1807756,
			"totalMissed": 619,
			"latestBlockNum": 64577530,
			"latestSlotNum": 590063590,
			"isJobs": true
		}
	]
}
```

## 另请参见

- [concepts/resources](../concepts/resources.md)——份额如何获得
- [stake-v2](stake-v2.md)——冻结 TRX 以获得投票份额
