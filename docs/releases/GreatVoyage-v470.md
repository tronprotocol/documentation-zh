# GreatVoyage-v4.7.0.1(Aristotle)

GreatVoyage-v4.7.0.1(Aristotle)版本引入了多个重要的优化和更新，全新的质押机制Stake 2.0, 提高了资源模型的灵活性和质押系统的稳定性；动态能量模型，有助于促进生态的均衡发展；二级缓存机制优化了数据库读取性能，提高了交易执行性能，提升了网络吞吐量；使用libp2p库作为Java-tron P2P网络模块，使代码结构更加清晰，并且降低代码耦合性；优化日志输出，将LevelDB和RocksDB的日志重定向到Java-tron日志文件；将更多工具包集成的toolkit工具箱，为用户带来更便捷的开发体验。

下面是详细介绍。



## 核心协议
### 1. Stake 2.0 质押模型

GreatVoyage-v4.7.0.1(Aristotle)版本引入一种全新的质押模型Stake 2.0，旨在建立一种更为灵活，高效，稳定的质押系统。相比于目前的Stake1.0质押模型， Stake 2.0在下面几个方面进行了提升：

* 质押和资源代理分离

    在Stake 1.0中，质押和资源代理合并在一条指令中，质押指令中指定资源接受者，完成质押后，资源会代理给指定的资源接收者。解质押和解代理也是合并在解质押指令中，如果想要取消资源代理，就必须将对应的TRX解质押。Stake 2.0将质押和资源代理分离成2条指令，用户首先执行质押指令，完成质押后资源首先被分配给质押者，之后再执行代理指令将资源代理其他人。 解质押和资源解代理也是分离成2条指令，用户想要取消对一个地址的资源代理， 无需解质押即可直接执行解代理操作，然后可以根据需要再次将资源代理给其他人。将质押和资源代理操作分离，简化了用户的操作，降低了操作的复杂度。

* 资源的碎片化管理

    在Stake 1.0中，一次解质押操作，会解质押所有质押的TRX，无法完成指定数量的TRX解质押。Stake 2.0中优化了这一点，我们可以指定任意数量的TRX进行解质押，只要这个指定的数量小于等于质押量。Stake 1.0中，取消对某一个地址的某种资源代理，只能一次全部取消，无法指定数量进行取消。Stake 2.0中进行了优化，我们可以根据需要只取消一部分，提高了资源管理的灵活性。

* 解质押时间和解压后资产延迟到账

    在Stake 1.0中，质押TRX之后，我们需要等待3天后才能解质押，解质押后，资金立刻到达用户的账户中。在Stake 2.0中，完成TRX质押后，可随时解质押，但需要等待N天，N天后，用户可以将解质押后的资金提取到自己的账户，N是TRON网络参数。当TRX市场产生剧烈波动时，由于资金延迟到账，将不再会引发大量的质押或解质押操作，提高了质押模型的稳定性，同时也不会引起大量的资金涌入市场加剧市场波动，有助于网络参与者对整个网络流通总量形成更稳定的预期。

* TVM集成质押和资源管理

    Stake 2.0中，TVM虚拟机集成了质押和网络资源管理相关的指令，用户可以在智能合约中执行TRX质押和解质押操作，也可以在智能合约中执行资源代理和解代理操作。

更多关于Stake 2.0请参考： [What is Stake 2.0?](https://coredevs.medium.com/what-is-stake-2-0-e04f59b948a6)

新的质押机制Stake 2.0是TRON网络中的一个动态参数，GreatVoyage-v4.7.0.1(Aristotle)部署之后默认为关闭状态，可以通过发起提案投票的方式开启。


* TIP: [https://github.com/tronprotocol/tips/issues/467](https://github.com/tronprotocol/tips/issues/467) 
* 源代码：[https://github.com/tronprotocol/java-tron/pull/4838](https://github.com/tronprotocol/java-tron/pull/4838) 

### 2. 优化数据库查询性能
Java-tron采用内存和磁盘数据库的方式进行数据存储，固化的区块数据会保存在多个磁盘数据库中，未被固化的数据保存在内存中，当一个区块被固化后，会将相应的内存数据写入到磁盘数据库。在查询数据时，首先查询内存中的数据，如果没有找到，再查询磁盘数据库。而磁盘数据库查询是比较耗时的，因此，GreatVoyage-v4.7.0.1(Aristotle)版本优化了数据库查询性能，在进行底层磁盘数据库操作之前，增加了二级缓存。在将数据写入磁盘的同时，也将数据写入到二级缓存。当需要查询磁盘数据库时，如果二级缓存中存在要查询的数据，则直接返回，而无需再查询磁盘数据库。二级缓存减少了查询磁盘数据库的次数，提高了交易执行速度，提升了网络吞吐量。

* 源代码：[https://github.com/tronprotocol/java-tron/pull/4740](https://github.com/tronprotocol/java-tron/pull/4740) 

### 3. 优化区块生产流程
节点进行区块生产时会依次校验和执行可以打包进区块的所有交易，而每一次的交易验证和执行，都会涉及到区块数据的获取，比如区块号、区块大小、区块内的交易信息等。在GreatVoyage-v4.7.0.1(Aristotle)之前的版本中，节点打包交易时，在验证和执行每一笔交易过程中，区块数据都是被重新计算的，这其中包含了许多重复的计算。

为了提高节点打包交易效率，GreatVoyage-v4.7.0.1(Aristotle)版本优化了区块生产流程，只计算一次区块数据并仅在必要时更新数据，从而大幅减少了区块数据计算的次数，提高了区块打包效率。

* 源代码：[https://github.com/tronprotocol/java-tron/pull/4756](https://github.com/tronprotocol/java-tron/pull/4756) 

### 4. 增加交易hash缓存
节点在处理区块时，会多次用到交易哈希值，而在GreatVoyage-v4.7.0.1(Aristotle)之前的版本中，交易哈希值都是随用随计算，而交易哈希值的计算比较耗时，从而导致区块处理较慢，因此，GreatVoyage-v4.7.0.1(Aristotle)版本增加了交易hash缓存，使用时直接从缓存中获取，只有当交易数据发生改变时，才重新计算交易哈希。交易hash的缓存，减少了不必要的交易哈希计算，提高了区块处理速度。

* 源代码：[https://github.com/tronprotocol/java-tron/pull/4792](https://github.com/tronprotocol/java-tron/pull/4792)   


### 5. libp2p集成
从GreatVoyage-v4.7.0.1(Aristotle)版本开始，将直接使用模块的libp2p库作为Java-tron 的P2P网络模块，而不再使用原来的p2p模块，使代码结构更加清晰，代码耦合性更低，更易于维护。


* 源代码：[https://github.com/tronprotocol/java-tron/pull/4791](https://github.com/tronprotocol/java-tron/pull/4791) 


## TVM
### 1. 新增Stake2.0相关的TVM指令和预编译合约

GreatVoyage-v4.7.0.1(Aristotle)引入了Stake2.0，TVM将同步支持Stake 2.0质押、资源代理相关指令，用户可以通过智能合约进行质押和资源代理操作，进一步丰富了TRON网络智能合约的应用场景。TVM增加了从0xda至0xdf 总共6个指令:

|  ID |  TVM指令 |  描述 |
| -------- | -------- | -------- |
| 0xda     | FREEZEBALANCEV2     | 执行与系统合约FreezeBalanceV2相同的操作     |
| 0xdb     | UNFREEZEBALANCEV2     | 执行与系统合约UnfreezeBalanceV2相同的操作     |
| 0xdc     | CANCELALLUNFREEZEV2     | 取消所有解质押操作     |
| 0xdd     | WITHDRAWEXPIREUNFREEZE     | 执行与系统合约WithdrawExpireUnfreeze相同的操作     |
| 0xde     | DELEGATERESOURCE     | 执行与系统合约DelegateResource相同的操作     |
| 0xdf     | UNDELEGATERESOURCE     | 执行与系统合约UnDelegateResource相同的操作     |


TVM增加了从0x100000b至0x1000015 总共11个预编译合约：

|  ID |  预编译合约 |  描述 |
| -------- | -------- | -------- |
| 0x100000b     | GetChainParameter     | 查询特定的网络参数     |
| 0x100000c     | AvailableUnfreezeV2Size     | 查询给定地址的可解冻队列长度     |
| 0x100000d     | UnfreezableBalanceV2     | 查询指定资源类型下，目标地址可解质押的余额数量(单位:sun)     |
| 0x100000e     | ExpireUnfreezeBalanceV2     | 查询目标地址，在指定时间戳的可提取本金数量     |
| 0x100000f     | DelegatableResource     | 查询指定资源类型下，目标地址的可代理资源数量(单位:sun)     |
| 0x1000010     | ResourceV2     | 查询指定资源类型下，某地址代理给目标地址的资源数量(单位:sun)     |
| 0x1000011     | CheckUnDelegateResource     | 查询指定资源类型下，是否可以回收已代理给目标地址的指定数量的资源，并返回资源未使用数量(单位:sun)、已使用数量(单位:sun)和恢复时间     |
| 0x1000012     | ResourceUsage     | 查询指定资源类型下，目标地址的资源已使用量(单位:sun)和恢复时间     |
| 0x1000013     | TotalResource     | 查询指定资源类型下，目标地址的资源总量(单位:sun)     |
| 0x1000014     | TotalDelegatedResource     | 查询指定资源类型下，目标地址所代理出去的资源总量(单位:sun)      |
| 0x1000015     | TotalAcquiredResource     | 查询指定资源类型下，目标地址所获取的资源总量(单位:sun)     |

Stake 2.0是TRON网络中的一个动态参数，GreatVoyage-v4.7.0.1(Aristotle)部署之后默认为关闭状态，可以通过发起提案投票的方式开启。

* TIP: [https://github.com/tronprotocol/tips/issues/467](https://github.com/tronprotocol/tips/issues/467) 
* 源代码: [https://github.com/tronprotocol/java-tron/pull/4872](https://github.com/tronprotocol/java-tron/pull/4872) 

### 2. 动态能量模型
动态能量模型是一种根据合约已知的能量使用情况来动态调整合约未来的能量消耗的方案，如果一个合约在一个周期内使用过多的资源，则下一个周期中该合约将增加一定百分比的惩罚性消耗，用户向该合约发送相同的交易将产生更多的能量消耗量。当合约合理使用资源时，用户调用该合约所产生的能源消耗将逐渐恢复正常，通过这个机制，让能源资源在链上的分配更加合理，防止网络资源过度集中在少数合约上。

更多关于动态能量模型的原理请参考：[Introduction to Dynamic Energy Model](https://coredevs.medium.com/introduction-to-dynamic-energy-model-31917419b61a)。

动态能量模型是TRON网络中的一个动态参数，GreatVoyage-v4.7.0.1(Aristotle)部署之后默认为关闭状态，可以通过发起提案投票的方式开启。

* TIP: [https://github.com/tronprotocol/tips/issues/491](https://github.com/tronprotocol/tips/issues/491) 
* 源代码: [https://github.com/tronprotocol/java-tron/pull/4873](https://github.com/tronprotocol/java-tron/pull/4873) 

### 3. 优化chainId指令的返回值

从 GreatVoyage-v4.7.0.1(Aristotle)版本开始，将chainid指令的返回值从创世块区块哈希改成创世块区块哈希的最后四个字节，使chainid指令返回值与Java-tron json-rpc `eth_chainId` API的返回值一致。

优化chainId指令返回值是TRON网络的一个动态参数，GreatVoyage-v4.7.0.1(Aristotle)部署之后默认为关闭状态，可以通过发起提案投票的方式开启。

* TIP: [https://github.com/tronprotocol/tips/issues/474](https://github.com/tronprotocol/tips/issues/474) 
* 源代码: [https://github.com/tronprotocol/java-tron/pull/4863](https://github.com/tronprotocol/java-tron/pull/4863) 


## API

## 1. 新增Stake 2.0相关API
GreatVoyage-v4.7.0.1(Aristotle)版本新增了10个 API 以支持Stake 2.0质押模型：

|  API |  描述 |
| -------- | -------- |
| /wallet/freezebalancev2     | 质押TRX以获取资源     | 
| /wallet/unfreezebalancev2     | 解质押     |
| /wallet/delegateresource     | 将资源代理给其他账户     |
| /wallet/undelegateresource     | 取消资源代理     |
| /wallet/withdrawexpireunfreeze     | 提取已过锁定期的本金     |
| /wallet/getavailableunfreezecount     | 查询解质押剩余次数     |
| /wallet/getcanwithdrawunfreezeamount     | 查询在指定时间戳的可提取本金数量     |
| /wallet/getcandelegatedmaxsize     |  查询最大可代理指定类型资源的数量（单位:sun）|
| /wallet/getdelegatedresourcev2     | 查询某地址代理给目标地址的资源情况(单位:sun)     |
| /wallet/getdelegatedresourceaccountindexv2     | 查询账户的资源代理情况：包括为该账户代理资源的所有地址，和该账户将资源代理出去的所有地址     |


新增API的详细使用说明请参考： [What is Stake 2.0?](https://coredevs.medium.com/what-is-stake-2-0-e04f59b948a6)

* TIP: [https://github.com/tronprotocol/tips/issues/467](https://github.com/tronprotocol/tips/issues/467) 
* 源代码：[https://github.com/tronprotocol/java-tron/pull/4838](https://github.com/tronprotocol/java-tron/pull/4838) 

## 2. 新增预估能量接口

在GreatVoyage-v4.7.0.1(Aristotle)之前的版本中，可以通过`/wallet/triggerconstantcontract`接口预估执行智能合约交易所需的能量消耗量，然后根据预估的消耗量来设置交易的`feelimit`参数。但由于某些智能合约交易可能存在对其他智能合约的调用，这时有可能出现预估`feelimit`参数不准确的情况。

因此，GreatVoyage-v4.7.0.1(Aristotle)版本新增了一个能量预估接口`/wallet/estimateenergy`，利用该接口预估的`feelimit`在任何情况下都是可靠的。该接口返回值中的`energy_required`字段表示这笔智能合约调用交易执行成功所需要的能量预估量，用户根据该字段来计算`feelimit`参数：`feelimit` = `energy_required` * 能量单价， 当前能量单价是420sun 。

如果由于某种原因导致预估接口执行失败时，`energy_required`字段值为0，在返回值中将不显示该字段，这时可以通过`result`字段查看预估失败原因。

新版本部署成功后，该接口默认为关闭状态，打开该接口需要节点配置文件中同时开启`vm.estimateEnergy`和`vm.supportConstant`这两个配置项。`vm.estimateEnergy`和`vm.supportConstant`的默认值均为false。

`/wallet/triggerconstantcontract`接口调用示例如下：

```
curl --location --request POST 'https://api.nileex.io/wallet/estimateenergy' \
--header 'Content-Type: application/json' \
--data-raw '{
     "owner_address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
     "contract_address": "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj",
     "function_selector": "transfer(address,uint256)",
     "parameter": "0000000000000000000000002EEF13ADA48F286066F9066CE84A9AD686A3EA480000000000000000000000000000000000000000000000000000000000000004",
     "visible": true
}'
```


* 源代码: [https://github.com/tronprotocol/java-tron/pull/4873](https://github.com/tronprotocol/java-tron/pull/4873) 


## 其它变更


### 1. 优化编译参数
GreatVoyage-v4.7.0.1(Aristotle)版本优化了Gradle编译参数，将JVM堆内存最小值设置成1G，以加快Java-tron gradle编译速度。

* 源代码：  [https://github.com/tronprotocol/java-tron/pull/4837](https://github.com/tronprotocol/java-tron/pull/4837) 

### 2. 优化节点自动停止功能

为了方便节点部署者进行数据备份或数据统计，从GreatVoyage-v4.5.1(Tertullian)版本开始，节点支持在特定的条件下停止运行，用户可以通过节点配置文件设置节点停止的条件，在满足设置的条件时，节点将停止运行。支持3个停止条件同时设置，满足任意个条件即停止节点。这三个条件包括区块时间、区块高度以和节点从启动到停止需要同步的区块数量， 但是由于允许同时设置多个停止条件，当用户只需要一个条件时，需要在配置文件中注释掉其他2个条件配置项，因此，如果用户忘记注释，可能出现节点停止在非预期的区块上。但实际并没有需要同时设置多个条件的应用场景，所以，GreatVoyage-v4.7.0.1(Aristotle)版本优化了节点自动停止功能，可选的配置参数不变，但是仅允许同时设置一个有效参数，如果节点部署者设置了多个参数，节点将报错并退出运行。该优化极大的简化了用户使用的复杂度。

* 源代码：  [https://github.com/tronprotocol/java-tron/pull/4853](https://github.com/tronprotocol/java-tron/pull/4853)
[https://github.com/tronprotocol/java-tron/pull/4858](https://github.com/tronprotocol/java-tron/pull/4858) 

### 3. 删除数据库V1版本相关代码
在GreatVoyage-v4.7.0.1(Aristotle)之前的版本中，数据库有两个版本v1和v2，用户可以通过配置项`db.version`选择使用的版本，由于v2版本采用内存+磁盘数据库模式、支持底层数据库的扩展、异常情况下数据的正确恢复功能等，相对与v1版本, v2优势非常明显。 因此，为了使代码结构更加清晰，从GreatVoyage-v4.7.0.1(Aristotle)开始，删除了数据库v1版本相关的代码，以及数据库版本配置项`db.version `。用户无需再进行数据库版本配置，直接使用v2版本的数据库，降低了配置节点的复杂度。

* 源代码：  [https://github.com/tronprotocol/java-tron/pull/4836](https://github.com/tronprotocol/java-tron/pull/4836)

### 4. 优化数据库日志输出
在GreatVoyage-v4.7.0.1(Aristotle)之前的版本中，节点日志中不包含LevelDB 或者 RocksDB 本身输出的底层日志，排查数据库读写问题比较困难。因此，GreatVoyage-v4.7.0.1(Aristotle)版本优化了数据库日志，将LevelDB或者RocksDB数据模块的底层日志的输出重定向到节点日志文件中，简化的了数据库故障排查的难度，提高了节点运维的效率。

* 源代码:  [https://github.com/tronprotocol/java-tron/pull/4833](https://github.com/tronprotocol/java-tron/pull/4833) 
### 5. snapshot 最大落盘数量可配置
新加入到网络的节点需要从其他节点同步区块数据，节点将同步过来的区块数据首先保存在内存中，然后再存储到磁盘。在GreatVoyage-v4.7.0.1(Aristotle)之前的版本中，当节点追块时，一次落盘操作会将500个区块的数据从内存写入到磁盘，因此，内存中会保留超过500个区块的数据，并且各个区块数据通过链表关联。在查询数据时，先依次在500多个区块中查找，当找不到所要查询的数据时，再查询磁盘数据库，但遍历500多个区块数据降低了数据查询效率。

因此，从GreatVoyage-v4.7.0.1(Aristotle)版本开始，支持snapshot落盘数量可配置，通过`storage.snapshot.maxFlushCount`配置项设置一次落盘的最大区块数量，以使数据库查询效率最大化，提高区块处理速度。如果不设置，则snapshot最大落盘数量为默认值1。

* 源代码：[https://github.com/tronprotocol/java-tron/pull/4834](https://github.com/tronprotocol/java-tron/pull/4834) 

### 6. Toolkit.jar工具箱集成
`DBConvert.jar`是数据库数据转换工具， 它可以将LevelDB数据转换为RocksDB数据；`LiteFullNodeTool.jar`是轻节点工具，可以将全节点数据转换成轻节点数据。从 GreatVoyage-v4.7.0.1(Aristotle)版本开始，将`DBConvert.jar` 和`LiteFullNodeTool.jar`集成到了`Toolkit.jar`工具箱中，并对`Toolkit.jar`工具箱新增数据库拷贝功能，以实现快速的节点数据库拷贝。未来Java-tron周边的工具将逐步都集成到`Toolkit.jar`工具箱中，以便于工具维护和开发者使用。`Toolkit.jar`工具箱新增功能的使用命令如下：

```
// 将LevelDB数据转换为RocksDB数据
$ java -jar Toolkit.jar db convert -h
// 将全节点数据转换成轻节点数据
$ java -jar Toolkit.jar db lite -h
// 数据库拷贝
$ java -jar Toolkit.jar db copy -h
```

* 源代码: [https://github.com/tronprotocol/java-tron/pull/4813](https://github.com/tronprotocol/java-tron/pull/4813) 

--- 

*Courage is the first of human qualities because it is the quality which guarantees the others.* 
<p align="right"> --- Aristotle</p>
