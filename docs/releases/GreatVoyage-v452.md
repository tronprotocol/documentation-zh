
# GreatVoyage-v4.5.2(Aurelius)
GreatVoyage-v4.5.2(Aurelius)版本引入了多个重要的优化更新，优化的交易缓存机制，大幅减少了内存占用，提高了节点性能；优化的对等节点连接策略，提高了对等节点间建立连接的效率，加快了节点同步进程；优化的区块生产及处理逻辑，提高了节点稳定性；新增的数据库存储分区工具，减轻了数据存储压力；新增的区块头查询API以及历史带宽单价查询API，为用户带来更便捷的开发体验。


# 核心协议
## 1. 优化区块处理逻辑 
在GreatVoyage-v4.5.2(Aurelius)之前的版本中，区块生产、区块处理及交易处理等线程共同竞争同步锁，而在高并发，并且交易执行时间较长的情况下，区块生产或者区块处理线程获取到同步锁所需要的时间较长，从而导致小概率丢块事件的发生。为了提高节点稳定性，GreatVoyage-v4.5.2(Aurelius)版本优化了区块处理逻辑中的同步锁，仅允许一个交易处理线程与区块生产或处理线程竞争同步锁，并且当交易处理线程发现有区块相关线程在等待同步锁时，会主动退让，这大大提高了区块生产和区块处理线程获取到同步锁的概率，保证了节点高吞吐、稳定的运行。


TIP: https://github.com/tronprotocol/tips/blob/master/tip-428.md
源代码: https://github.com/tronprotocol/java-tron/pull/4551 

## 2. 优化交易缓存机制
节点使用交易缓存来判断新收到交易是否是重复交易，在GreatVoyage-v4.5.2(Aurelius)之前的版本中，交易缓存是一个hashmap数据结构，该结构会保存最近65536个区块中的交易，hashmap会为每一条交易单独分配内存，因此，在节点运行过程中，交易缓存占据了约2G内存空间，而且由于频繁的内存申请会触发频繁的JVM垃圾回收，也间接影响着节点的性能。为此，GreatVoyage-v4.5.2(Aurelius)版本优化了交易缓存的实现，采用布隆过滤器代替hashmap，布隆过滤器使用固定且极小的内存空间来记录最近的历史交易，极大的减少了交易缓存对内存的占用，提高了节点性能。


TIP: https://github.com/tronprotocol/tips/blob/master/tip-440.md
源代码：https://github.com/tronprotocol/java-tron/pull/4538  




## 3. 优化P2P节点连接策略

在GreatVoyage-v4.5.2(Aurelius)之前的版本中，一个节点所连接的远端节点的数量已经达到了最大值，该节点会拒绝新的远端节点的连接请求。随着网络中这样的满连接节点的增加，新加入的节点与网络中的其它节点建立连接将越来越困难。

为了加快网络中节点间的连接速度，GreatVoyage-v4.5.2(Aurelius)版本优化了P2P节点连接策略，周期性对节点的TCP连接数量进行检查，如果达到满连接，则采用一定的淘汰策略与其中一个或者两个节点进行断连，以增加网络中新加入的节点与其成功连接的可能性，从而提高网络中P2P节点间建立连接的效率，提升了网络稳定性。需要注意的是，配置文件中`node.active`和`node.passive`列表中配置的节点均为信任节点，不会被断开连接。

TIP: https://github.com/tronprotocol/tips/blob/master/tip-425.md 
源代码: https://github.com/tronprotocol/java-tron/pull/4549   



## 4. 优化区块打包逻辑
在GreatVoyage-v4.5.2(Aurelius)之前的版本中，对于预执行正常的交易，在打包时可能会碰到JVM GC停顿，导致交易执行超时，从而被丢弃。因此GreatVoyage-v4.5.2(Aurelius)版本优化了区块打包逻辑，对于预执行正常的交易，如果在打包时执行超时，则采取重试操作，以避免在打包交易过程中，由于JVM GC停顿导致交易丢失。

源代码：https://github.com/tronprotocol/java-tron/pull/4387 

## 5. 优化切链逻辑
在TRON网络中偶尔会出现微分叉的情况，微分叉时会产生切链行为，在切链时会回退区块，并将被回退区块内交易重新放回到待打包交易队列中。当这些交易被重新打包执行时，可能会由于切链导致执行结果不一致，在GreatVoyage-v4.5.2(Aurelius)之前的版本中，整个过程引用的是同一个交易对象，所以切链可能会导致回退区块中的交易结果被更改。当再次发生切链，并且切回到原链时，会再次执行原链上的交易，就会产生`Different resultCode`错误，从而导致节点停止同步。因此，GreatVoyage-v4.5.2(Aurelius)版本优化了切链逻辑，在进行区块回退时，为被回退区块内交易创建新的交易对象，避免交易结果被修改，提升了节点对微分叉处理的稳定性。

源代码：https://github.com/tronprotocol/java-tron/pull/4583 

## 6. 新增数据库存储分区工具
随着链上数据增长，全节点的磁盘空间可能不足，需要更换更大容量的磁盘。为此，从GreatVoyage-v4.5.2(Aurelius)版本开始，提供了数据库存储分区工具，它能够根据用户的配置将部分数据库迁移到其它磁盘分区，因此用户只需根据容量需求添加磁盘即可，无需更换原磁盘，方便用户对磁盘进行扩容，同时降低节点运行成本。


源代码：https://github.com/tronprotocol/java-tron/pull/4545 
               https://github.com/tronprotocol/java-tron/pull/4559 
               https://github.com/tronprotocol/java-tron/pull/4563 


 
# API
## 1. 新增区块头查询API

从GreatVoyage-v4.5.2(Aurelius)版本开始，新增区块头查询API，仅返回区块头信息，不返回区块中交易信息，用户不需查询整个区块即可获取到区块头信息，这不但降低了节点的网络I/O负载，而且由于区块不带交易信息，减少了序列化时间，降低了接口延迟，提升了查询效率。

 
源代码：https://github.com/tronprotocol/java-tron/pull/4492 
https://github.com/tronprotocol/java-tron/pull/4552 

## 2. 新增历史带宽单价查询API
根据带宽消耗规则，如果交易发起者账户通过质押获得的带宽或者免费带宽不足时，将燃烧TRX来支付带宽费用，这时，在交易记录中仅记录带宽费用，而不记录带宽消耗量，为了了解历史交易的带宽消耗量，从GreatVoyage-v4.5.2(Aurelius)版本开始，新增历史带宽单价查询API `/wallet/getbandwidthprices`，用户可以通过该接口获取到带宽代价的历史记录，从而可以计算出历史交易的带宽消耗量。

源代码：https://github.com/tronprotocol/java-tron/pull/4556 

# 其它变更
## 1. 优化区块同步逻辑
GreatVoyage-v4.5.2(Aurelius)版本优化了区块同步逻辑，避免了在同步区块过程中不必要的节点断连，提高了节点稳定性。


源代码：https://github.com/tronprotocol/java-tron/pull/4542 
https://github.com/tronprotocol/java-tron/pull/4540 
## 2. 优化`eth_estimateGas`和`eth_call` API
GreatVoyage-v4.5.2(Aurelius)版本优化了`eth_estimateGas`和`eth_cal` JSON-RPC接口，当智能合约交易执行中断时，能够返回错误信息。

源代码：https://github.com/tronprotocol/java-tron/pull/4570 

## 3. 增强接口的容错处理能力
GreatVoyage-v4.5.2(Aurelius)版本优化了多个API接口，增强了其对参数的容错能力，提高了API接口的稳定性。

源代码：https://github.com/tronprotocol/java-tron/pull/4560 
https://github.com/tronprotocol/java-tron/pull/4556 
 
--- 

*The universe is change; our life is what our thoughts make it.* 
<p align="right"> ---  Aurelius</p>