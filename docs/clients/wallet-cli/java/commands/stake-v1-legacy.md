# 质押（Stake 1.0，旧版）

> ⚠️ **旧版。** 这些是 Stake 2.0 之前的冻结命令，保留供参考。新的用法应优先选择
> [Stake 2.0](stake-v2.md)。两种模型的区别参见
> [concepts/staking-models](../concepts/staking-models.md)。

旧版的冻结/解冻与资源代理（v1）。带宽机制在 [concepts/resources](../concepts/resources.md) 中说明。

## 如何冻结/解冻余额 {#how-to-freezeunfreeze-balance}

资金冻结之后，将获得相应数量的份额和带宽。份额可用于投票，带宽可用于交易。份额和带宽的使用与计算
规则在 [concepts/resources](../concepts/resources.md) 中描述。

**冻结操作如下：**

```console
> freezeBalance [OwnerAddress] frozen_balance frozen_duration [ResourceCode:0 BANDWIDTH, 1 ENERGY, 2 TRON_POWER] [receiverAddress]
```

- `OwnerAddress`——发起交易的账户地址，可选，默认为登录账户的地址。
- `frozen_balance`——冻结资金的数量，单位是 Sun。最小值为 **1000000 Sun（1 TRX）**。
- `frozen_duration`——冻结时间，该值目前只允许为 **3 天**。
- `ResourceCode`——`0` BANDWIDTH；`1` ENERGY；只有在 `getAllowNewResourceModel` 已开启时才可用 `2` TRON_POWER。TRON_POWER 不能代理，因此使用 `2` 时不要传 `receiverAddress`。

例如：

```console
> freezeBalance 100000000 3 1 TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW
```

冻结后，资金会从账户的 `Balance` 转入 `Frozen`，可在账户信息中查看。解冻后，资金会从 `Frozen`
转回 `Balance`。处于冻结状态的资金不能用于交易。

当临时需要更多份额或带宽时，可以冻结额外的资金以获得额外的份额和带宽。解冻时间会顺延至最后一次
冻结操作之后 3 天。

冻结时间到期后，资金即可解冻。

**解冻操作如下：**

```console
> unfreezeBalance [OwnerAddress] ResourceCode(0 BANDWIDTH, 1 ENERGY, 2 TRON_POWER) [receiverAddress]
```

## 如何代理资源 {#how-to-delegate-resource}

### FreezeBalance（代理）

```console
> freezeBalance [OwnerAddress] frozen_balance frozen_duration [ResourceCode:0 BANDWIDTH, 1 ENERGY] [receiverAddress]
```

`ResourceCode` 和 `receiverAddress` 为可选参数。不指定接收地址时，冻结 TRX 获得的资源由本账户
使用；指定后，资源将代理给 `receiverAddress`。

- `OwnerAddress`——发起交易的账户地址，可选，默认为登录账户的地址。
- `frozen_balance`——冻结 TRX 的数量，单位为 SUN，最小值为 1,000,000 SUN（1 TRX）。
- `frozen_duration`——冻结时长，3 天。
- `ResourceCode`——0 BANDWIDTH；1 ENERGY。
- `receiverAddress`——目标账户地址。

### UnfreezeBalance（取消代理） {#unfreezebalance-undelegate}

```console
> unfreezeBalance [OwnerAddress] ResourceCode(0 BANDWIDTH, 1 ENERGY) [receiverAddress]
```

`ResourceCode` 和 `receiverAddress` 为可选参数。不指定时默认解冻 BANDWIDTH；指定
`receiverAddress` 时，解冻的是代理给该地址的资源。

### 获取资源代理信息 {#get-resource-delegation-information}

- `getDelegatedResource fromAddress toAddress`——获取从 `fromAddress` 到 `toAddress` 的资源代理
  信息。
- `getDelegatedResourceAccountIndex address`——获取 `address` 代理给其他账户资源的信息。

## 另请参见

- [stake-v2](stake-v2.md)——当前的质押模型（Stake 2.0）
- [concepts/staking-models](../concepts/staking-models.md) · [concepts/resources](../concepts/resources.md)
