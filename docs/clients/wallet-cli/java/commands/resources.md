# 资源价格与备注费

查询资源单价的历史记录以及备注费。关于带宽和能量的工作原理，参见
[concepts/resources](../concepts/resources.md)。奖励提取（`WithdrawBalance`）位于
[投票与奖励](vote-reward.md)页面。

## GetBandwidthPrices

获取带宽的历史单价。

```console
wallet> getBandwidthPrices
The BandwidthPrices is 0:10,1606537680000:40,1614238080000:140,1626581880000:1000,1626925680000:140,1627731480000:1000
```

## GetEnergyPrices

获取能量的历史单价。

```console
wallet> getEnergyPrices
The EnergyPrices is 0:100,1575871200000:10,1606537680000:40,1614238080000:140,1635739080000:280,1681895880000:420
```

## GetMemoFee

获取备注费。

```console
wallet> getMemoFee
The MemoFee is 0:0,1675492680000:1000000
```

## 另请参见

- [concepts/resources](../concepts/resources.md)——带宽 / 能量模型与带宽计算
- [stake-v2](stake-v2.md)——冻结 TRX 以获得资源
- [chain-data](chain-data.md)——`GetChainParameters` 及其他链上查询
