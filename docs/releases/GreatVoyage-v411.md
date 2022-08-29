# GreatVoyage-v4.1.1
GreatVoyage-4.1.1版本发布， 本次升级主要有以下新功能和修改：

## 核心协议
### 新的共识协议
新的共识机制将波场现有的DPOS共识同PBFT共识机制进行结合，在区块固化阶段采用PBFT的三阶段投票机制进行确认。波场区块从生产出来到固化确认的时间将从原来的19个区块时间（1个区块时间为3s）缩短至平均1～2个区块时间，区块确认速度大幅提升。
- TIP: [TICP-Optimized-PBFT](https://github.com/tronprotocol/tips/blob/master/tp/ticp/ticp-optimized-pbft/ticp-Optimized-PBFT.md) 
- 源代码: [#3082](https://github.com/tronprotocol/java-tron/pull/3082) 

### 新的节点类型
在现有FullNode的基础上新增了一种节点类型：Lite FullNode。Lite FullNode和普通的FullNode运行同样的代码，所不同的是Lite FullNode是基于状态数据快照进行启动，状态数据快照包含所有的状态数据和最近的256个区块的历史数据。
状态数据快照可以通过执行LiteFullNodeTool.jar进行获得（请参考：[如何使用LiteFullNode Tool](https://tronprotocol.github.io/documentation-zh/developers/litefullnode/)）。
- TIP: [TIP-128](https://github.com/tronprotocol/tips/blob/master/tip-128.md) 
- 源代码: [#3031](https://github.com/tronprotocol/java-tron/pull/3031) 

## TVM
### 对以太坊的伊斯坦布尔升级进行兼容
a. 增加新的指令CHAINID，用于获取当前链的创世区块id，防止交易在不同链上潜在的重放攻击风险。
- TIP: [TIP-174](https://github.com/tronprotocol/tips/blob/master/tip-174.md)
- 源代码: [#3351](https://github.com/tronprotocol/java-tron/pull/3351) 

b. 增加新的指令SELFBALANCE, 用于在智能合约中获取当前合约地址的余额，获取任意地址的余额依然是BALANCE指令。使用SELFBALANCE指令更加安全，未来有可能提高BALANCE指令的能量消耗。
TIP: [TIP-175](https://github.com/tronprotocol/tips/blob/master/tip-175.md) 
源代码: [#3351](https://github.com/tronprotocol/java-tron/pull/3351) 

c. 修改预编译合约指令BN128Addition消耗的能量费用，从500 energy降低为150 energy。
修改预编译合约指令BN128Multiplication消耗的能量费用，从40000 energy降低为6000 energy。
修改预编译合约指令BN128Pairing消耗的能量费用，从(80000 \* pairs + 100000) energy降低为(34000 \* pairs + 45000) energy。
TIP: [TIP-176](https://github.com/tronprotocol/tips/blob/master/tip-176.md) 
源代码: [#3351](https://github.com/tronprotocol/java-tron/pull/3351) 

## 机制
1、增加了两个新的系统合约MarketSellAssetContract和MarketCancelOrderContract用于支持TRX、TRC10资产在链上去中心化交易所进行交易。
- TIP: [TIP-127](https://github.com/tronprotocol/tips/blob/master/tip-127.md)
- 源代码: [#3302](https://github.com/tronprotocol/java-tron/pull/3302) 

## 其他变更
1、增加了多个节点性能指标数据。
- 源代码: [#3350](https://github.com/tronprotocol/java-tron/pull/3350) 

2、在原有的transactionInfo接口中增加了市场订单详情的信息。
- TIP: [TIP-127](https://github.com/tronprotocol/tips/blob/master/tip-127.md) 
- 源代码: [#3302](https://github.com/tronprotocol/java-tron/pull/3302)

3、优化了docker部署脚本
- 源代码： [#3330](https://github.com/tronprotocol/java-tron/pull/3330)