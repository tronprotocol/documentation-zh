# GreatVoyage-4.2.0(Plato)
GreatVoyage-4.2.0(Plato)版本引入了2个重要的更新，资源模型的优化将大福提升波场网络资源使用率，使资源获取方式更加合理。全新的TVM指令使智能合约的使用场景更加丰富，将进一步丰富波场生态。

# 核心协议
##1、资源模型优化。

GreatVoyage-4.2.0(Plato)版本之前，用户通过质押TRX获取大额投票权的同时，也获得了大量的能量和带宽，而这部分资源的使用率极低，大多数处于闲置状态，增加了开发者们获取资源的成本，为了提高资源的利用率，GreatVoyage-4.2.0(Plato)版本提出了一种新的资源优化模型，质押TRX只获得带宽，能量，投票权三种资源中的一种，用户可以根据自己的需求获取相应的资源，从而提升资源的利用率。

- TIP： [TIP-207](https://github.com/tronprotocol/tips/blob/master/tip-207.md)
- 源代码:  [#3726](https://github.com/tronprotocol/java-tron/pull/3726)

**注意事项：**
  * 该功能默认处于关闭状态，可通过提案系统开启该。
  * 功能开启后，用户之前已获取的资源保持不变，当用户发送任意一个解冻交易（解冻带宽，能量，或者投票权），提案通过前获取的投票权将被清空。
  
# TVM
## 1、虚拟机中新增Freeze/Unfreeze 指令。

在波场网络中，普通账户质押TRX可以获取带宽，能量，投票权等资源，合理使用这些资源可以为用户带来一定的收益。与此同时，智能合约账户虽然也拥有TRX，但是却没有办法通过质押TRX获取资源，为了解决这种不一致性，GreatVoyage-4.2.0(Plato)版本在TVM中引入了Freeze/Unfreeze指令，使得智能合约也支持质押TRX获取资源。

- TIP：[TIP-157](https://github.com/tronprotocol/tips/blob/master/tip-157.md)
- 源代码： [#3728](https://github.com/tronprotocol/java-tron/pull/3728)

**注意事项：**
  * 该功能默认处于关闭状态，可通过提案系统开启该。
  * TVM的质押指令目前可以获取带宽和能量，对于投票权，需要在TVM支持投票指令以后才可以获取并使用。
  * Freeze/Unfreeze指令中的接收地址/目标地址都必须是`address payable` 类型，且接收地址/目标地址不能是合约地址（合约自身地址除外）。
  * 如果调用合约给未激活地址代理资源会自动激活目标账户，同时额外扣除25,000能量作为账户激活成本。

# 其他变更
## 1、优化区块同步逻辑

- 源代码：[#3732](https://github.com/tronprotocol/java-tron/pull/3732)




--- 
*The beginning is the most important part of the work.* 
<p align="right"> --- Plato</p>