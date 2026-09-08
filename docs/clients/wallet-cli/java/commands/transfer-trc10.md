# TRC10 token

发行、更新、转移和查询 TRC10 资产。

## 如何发行 TRC10 token {#how-to-issue-a-trc10-token}

每个账户只能发行**一个** TRC10 token。

### AssetIssue

```console
> AssetIssue [OwnerAddress] AssetName AbbrName TotalSupply TrxNum AssetNum Precision StartDate EndDate Description Url FreeNetLimitPerAccount PublicFreeNetLimit FrozenAmount0 FrozenDays0 [...] FrozenAmountN FrozenDaysN
```

- `OwnerAddress`（可选）——发起交易的账户地址。默认：登录账户的地址。
- `AssetName`——所发行 TRC10 token 的名称。
- `AbbrName`——TRC10 token 的缩写。
- `TotalSupply`——总供应量，由发行时进入发行方账户的可用数量与全部冻结供应量组成。
- `TrxNum`、`AssetNum`——这两个参数决定 token 发行时的兑换比率。兑换比率 = TrxNum / AssetNum。
  AssetNum：以所发行 token 的基础单位计。TrxNum：以 SUN 计（0.000001 TRX）。
- `Precision`——精度，即小数点后位数。
- `FreeNetLimitPerAccount`——每个账户允许使用的最大带宽量。Token 发行方可以冻结 TRX 来获得带宽
  （仅限 TransferAssetContract）。
- `PublicFreeNetLimit`——所有账户允许使用的带宽总量上限。Token 发行方可以冻结 TRX 来获得带宽
  （仅限 TransferAssetContract）。
- `StartDate`、`EndDate`——token 发行期的开始和结束日期。其他用户只能在此期间参与发行。
- `FrozenAmount0`、`FrozenDays0`——冻结供应量及冻结天数。`FrozenAmount0` 必须大于 0，
  `FrozenDays0` 必须在 1 到 3653 之间。

示例：

```console
> AssetIssue TestTRX TRX 75000000000000000 1 1 2 "2019-10-02 15:10:00" "2020-07-11" "just for test121212" www.test.com 100 100000 10000 10 10000 1
> GetAssetIssueByAccount TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ  # 查看已发布的信息
{
    "assetIssue": [
        {
            "owner_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
            "name": "TestTRX",
            "abbr": "TRX",
            "total_supply": 75000000000000000,
            "frozen_supply": [
                {
                    "frozen_amount": 10000,
                    "frozen_days": 1
                },
                {
                    "frozen_amount": 10000,
                    "frozen_days": 10
                }
            ],
            "trx_num": 1,
            "precision": 2,
            "num": 1,
            "start_time": 1570000200000,
            "end_time": 1594396800000,
            "description": "just for test121212",
            "url": "www.test.com",
            "free_asset_net_limit": 100,
            "public_free_asset_net_limit": 100000,
            "id": "1000001"
        }
    ]
}
```

### UpdateAsset

更新 TRC10 token 的参数。

```console
> UpdateAsset [OwnerAddress] newLimit newPublicLimit description url
```

参数的具体含义与 `AssetIssue` 相同。

示例：

```console
> UpdateAsset 1000 1000000 "change description" www.changetest.com
> GetAssetIssueByAccount TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ  # 查看修改后的信息
{
    "assetIssue": [
        {
            "owner_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
            "name": "TestTRX",
            "abbr": "TRX",
            "total_supply": 75000000000000000,
            "frozen_supply": [
                {
                    "frozen_amount": 10000,
                    "frozen_days": 1
                },
                {
                    "frozen_amount": 10000,
                    "frozen_days": 10
                }
            ],
            "trx_num": 1,
            "precision": 2,
            "num": 1,
            "start_time": 1570000200000,
            "end_time": 1594396800000,
            "description": "change description",
            "url": "www.changetest.com",
            "free_asset_net_limit": 1000,
            "public_free_asset_net_limit": 1000000,
            "id": "1000001"
        }
    ]
}
```

### TransferAsset

TRC10 token 转账。

```console
> TransferAsset [OwnerAddress] ToAddress AssertID Amount
```

- `OwnerAddress`（可选）——发起交易的账户地址。默认：登录账户的地址。
- `ToAddress`——目标账户的地址。
- `AssertID`——TRC10 token ID（CLI 打印的参数名为 `AssertID`）。示例：1000001。
- `Amount`——要转移的 TRC10 token 数量。

示例：

```console
> TransferAsset TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz 1000001 1000
> getaccount TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz  # 转账后查看目标账户信息
{
  "address": "TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz",
  "balance": 9999900000,
  "assetV2": [
    {
      "key": "1000001",
      "value": 1000
    }
  ],
  "free_asset_net_usageV2": [
    {
      "key": "1000001",
      "value": 0
    }
  ]
}
```

### ParticipateAssetIssue

在发行期内参与购买 TRC10 token。

```console
> ParticipateAssetIssue [OwnerAddress] ToAddress AssetID Amount
```

- `OwnerAddress`（可选）——发起交易的账户地址。默认：登录账户的地址。
- `ToAddress`——TRC10 发行方的账户地址。
- `AssetID`——TRC10 token ID。示例：1000001。
- `Amount`——**要支付的 TRX 数量**，单位 SUN。这是你付出的金额，而不是你会收到的 token 数量：token 按发行时设定的固定汇率发放，向下取整到整数单位，而你支付的 TRX 会被全额转出——截断产生的零头不予退还。

该操作必须在 TRC10 token 的发行期内完成，否则会报错。

示例：

```console
> ParticipateAssetIssue TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ 1000001 1000
> getaccount TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW  # 查看剩余余额
{
  "address": "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW",
  "balance": 9999900000,
  "assetV2": [
    {
      "key": "1000001",
      "value": 1000
    }
  ]
}
```

### ListAssetIssuePaginated

分页查询所有 token 的列表。返回位于 offset 之后的 token 列表。

```console
> ListAssetIssuePaginated offset limit
```

示例：

```console
> ListAssetIssuePaginated 0 1
```

### UnfreezeAsset

解冻所有冻结期已经结束的 TRC10 token。

```console
> unfreezeasset [OwnerAddress]
```

## 如何获取 TRC10 token 信息 {#how-to-obtain-trc10-token-information}

| 命令 | 说明 |
|---|---|
| `ListAssetIssue` | 获取所有已发布的 TRC10 token 信息。 |
| `GetAssetIssueByAccount Address` | 根据发行地址获取 TRC10 token 信息。 |
| `getAssetIssueById AssetId` | 根据 ID 获取 TRC10 token 信息。 |
| `GetAssetIssueByName AssetName` | 根据名称获取 TRC10 token 信息。 |
| `getAssetIssueListByName AssetName` | 根据名称获取 TRC10 token 信息列表。 |

## 另请参见

- [usdt](usdt.md)——TRC20（USDT）转账
- [exchange](exchange.md) · [dex](dex.md)——在交易所 / DEX 上交易 TRC10 资产
