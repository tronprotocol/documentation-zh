
# History

## GreatVoyage-v4.7.1.1(Pittacus)

GreatVoyage-v4.7.1.1(Pittacus)版本优化了多个API接口，并且移除了涉及敏感信息的API。

下面是详细介绍。


### API 
#### 1. 删除涉及敏感信息的API

GreatVoyage-v4.7.1.1(Pittacus)之前的版本提供了签名和地址创建相关的API， 由于这些API的输入或输出包含了私钥，所以在网络中传输存在安全隐患。目前TRON生态的公共API服务提供商均关闭这些API，例如TronGrid、Anker、GetBlock等。开发者文档中之前已经将这些API标记成已废弃, 并建议通过SDK使用离线方式签名交易和创建地址。

GreatVoyage-v4.7.1.1(Pittacus)版本正式将这些API移除：

* HTTP
    * `createaddress`: 根据指定的密码创建地址
    * `generateaddress`: 随机创建地址
    * `easytransfer`：使用账户密码转账TRX
    * `easytransferbyprivate`：使用私钥转账TRX
    * `easytransferasset`: 使用账户密码转账TRC10代币
    * `easytransferassetbyprivate`：使用私钥转账TRC10代币
    * `gettransactionsign`：使用私钥签名交易
    * `addtransactionsign`：使用私钥签名交易，主要用于为多签交易签名
* gRPC
    * `CreateAddress`: 根据指定的密码创建地址
    * `GenerateAddress`: 随机创建地址
    * `EasyTransfer`：使用账户密码转账TRX
    * `EasyTransferByPrivate`：使用私钥转账TRX
    * `EasyTransferAsset`: 使用账户密码转账TRC10代币
    * `EasyTransferAssetByPrivate`：使用私钥转账TRC10代币
    * `GetTransactionSign`：使用私钥签名交易
    * `GetTransactionSign2`：使用私钥签名交易
    * `AddSign`：使用私钥签名交易，主要用于为多签交易签名



TIP: [https://github.com/tronprotocol/tips/issues/534](https://github.com/tronprotocol/tips/issues/534)

源代码：[https://github.com/tronprotocol/java-tron/pull/5096](https://github.com/tronprotocol/java-tron/pull/5096)    

#### 2. 优化资源代理信息查询接口
`/wallet/getdelegatedresourcev2`接口可以查询一个地址代理给其它地址的资源情况，而[资源代理](https://cn.developers.tron.network/reference/delegateresource)可以选择是否锁定，给同一个地址的2笔代理，其中一笔可以选择锁定，另外一笔选择不锁定，所以`/wallet/getdelegatedresourcev2`接口会返回两组信息：锁定的资源代理数据和非锁定的资源代理数据。在GreatVoyage-v4.7.1.1(Pittacus)之前的版本中，如果一个地址给另外一个地址代理的资源全部是锁定的，那么非锁定资源代理数据为0，则在这种情况下，接口可能也会将非锁定资源代理数据（0值）返回，GreatVoyage-v4.7.1.1(Pittacus)版本优化了`/wallet/getdelegatedresourcev2`接口，只返回代理资源数量非0的数据，使得返回的数据更加简洁清晰。

源代码:  [https://github.com/tronprotocol/java-tron/pull/5123](https://github.com/tronprotocol/java-tron/pull/5123) 


### 其它变更


#### 1. 优化交易收据中origin_energy_usage字段的更新逻辑
TRON网络支持合约部署者分摊一部分合约调用成本，为了方便用户查询合约交易的能量消耗情况，交易收据除了记录交易的总能量消耗量`energy_usage_total`字段，还会记录合约部署者分摊的能量数量`origin_energy_usage`字段，`energy_usage_total`包含了`origin_energy_usage`。在GreatVoyage-v4.7.1.1(Pittacus)之前的版本中，在极少数情况下会出现通过/wallet/gettransactioninfobyid查询到`energy_usage_total`字段为0，而`origin_energy_usage`字段不为0的情况，因此，GreatVoyage-v4.7.1.1(Pittacus)版本优化了交易收据中`origin_energy_usage`的更新逻辑，保证查询合约部署者的能量的准确性。


源代码：  [https://github.com/tronprotocol/java-tron/pull/5120](https://github.com/tronprotocol/java-tron/pull/5120)   


--- 

*Whatever you do, do it well.* 
<p align="right"> ---Pittacus</p>


## GreatVoyage-v4.7.1(Sartre)

GreatVoyage-v4.7.1(Sartre)版本引入了多个重要的优化和更新，优化的区块同步逻辑，提高了区块同步的稳定性；优化的节点IP设置，提高了节点的可用性；优化的节点日志模块，提高节点的可维护性。

下面是详细介绍。


### 核心协议
#### 1. 优化节点IP设置
节点启动时会获取节点的本地IP, 然后利用该IP与网路中的其他节点进行通信。如果节点无法访问外网，则将无法获取到本地IP，这时节点会将其本地IP设置为默认值0.0.0.0，而全0地址将使得节点无法与局域网内的其他节点正常通信，GreatVoyage-v4.7.1(Sartre)版本更改了节点默认IP，如果节点无法获取本地IP， 会将其本地IP设置为127.0.0.1，使得节点即便在没有连接外网的情况下，依然可以和局域网内的其它节点正常通信。

源代码：[https://github.com/tronprotocol/java-tron/pull/4990](https://github.com/tronprotocol/java-tron/pull/4990)  

#### 2. 优化区块同步逻辑 
在区块同步过程中，节点会维护一个区块请求列表，包含了已经向其他节点发送请求的所有区块的ID。当本节点和节点A连接极小概率异常断开时，会将向节点A正在请求的区块ID从请求列表中删除，此后节点会认为自己并没有请求过该区块，然后重新向节点B请求该区块，并将区块ID再次加入到请求列表中。而本节点在和节点A的连接断开之前，可能节点A已经向本节点发送了区块，断开连接后收到了该区块，由于发现是来自已断开节点A的区块，会丢弃该区块并将区块ID从请求列表中再次删除，导致本节点将再一次向节点B发送相同区块的请求。而当节点B收到重复的区块请求时，会认为是非法报文，断开与本节点的连接。

为了提高在并发场景下区块同步的效率，GreatVoyage-v4.7.1(Sartre)版本优化了区块请求列表的更新机制，列表中同时保存区块ID和节点信息，上述场景中，收到来自于已断开节点A区块后，将不会把向节点B请求的同一个区块ID从请求列表中删除，确保不会与节点B断开连接，从而提升区块同步的稳定性。


源代码：[https://github.com/tronprotocol/java-tron/pull/4995](https://github.com/tronprotocol/java-tron/pull/4995) 

节点在向其他节点同步区块时，需要获取本节点的区块状态摘要，状态摘要中包含本地头块在内的若干个区块的ID。在GreatVoyage-v4.7.1(Sartre)之前的版本中，获取状态摘要时，首先查询Dynamic数据库以获取区块高度，然后根据区块高度查询Block数据库以获取区块的ID。而由于节点在处理区块时，对各个数据库的写入不是同时进行的，节点会首先更新Dynamic数据库，然后再更新Block等其它数据库，同时由于状态摘要获取的线程和区块处理的线程是并发执行的，从而导致在GreatVoyage-v4.7.1(Sartre)之前的版本中，极小概率会出现最新的区块信息只写入了Dynamic数据库中，但还未来得及写入到区块数据库，即开始读取状态摘要，那么根据Dynamic库中的头块高度在区块数据库将找不到对应的区块ID，使得状态摘要读取失败。GreatVoyage-v4.7.1(Sartre)版本优化了链摘要获取逻辑，头块的ID直接从Dynamic数据库获取，不再从Block数据库获取，提高了状态摘要读取的稳定性。


源代码：[https://github.com/tronprotocol/java-tron/pull/5009](https://github.com/tronprotocol/java-tron/pull/5009) 

GreatVoyage-v4.7.1(Sartre)版本优化了区块同步时的锁机制，提升了节点在高并发的情况下连接的稳定性。

源代码：[https://github.com/tronprotocol/java-tron/pull/4996](https://github.com/tronprotocol/java-tron/pull/4996) 

### API
#### 1. 优化固化块API列表
GreatVoyage-v4.7.1(Sartre)版本删除了无用的固化块查询API，使代码更加清晰。


源代码：[https://github.com/tronprotocol/java-tron/pull/4997](https://github.com/tronprotocol/java-tron/pull/4997) 

#### 2. 优化资源代理关系查询API
GreatVoyage-v4.7.1(Sartre)版本优化了资源代理关系查询API，增加了对接口参数的检验，使接口更加稳定。


### 其它变更


#### 1. 优化轻节点检测逻辑
在GreatVoyage-v4.7.1(Sartre)之前的版本，节点的不同模块检测当前节点是否为轻节点的逻辑是不一样的，GreatVoyage-v4.7.1(Sartre)版本统一了轻节点判断逻辑，使代码更加简洁。


源代码：[https://github.com/tronprotocol/java-tron/pull/4986](https://github.com/tronprotocol/java-tron/pull/4986) 


#### 2. 优化数据库日志输出

**数据库日志**

GreatVoyage-v4.7.0.1(Aristotle)版本开始，将LevelDB或者RocksDB数据库的日志重定向到节点日志文件中，简化了数据库故障排查的难度，GreatVoyage-v4.7.1(Sartre)版本进一步优化日志模块，将数据库日志输出到一个单独的db.log文件中，以使节点日志更加清晰。

源代码:  [https://github.com/tronprotocol/java-tron/pull/4985](https://github.com/tronprotocol/java-tron/pull/4985) [https://github.com/tronprotocol/java-tron/pull/5001](https://github.com/tronprotocol/java-tron/pull/5001) [https://github.com/tronprotocol/java-tron/pull/5010](https://github.com/tronprotocol/java-tron/pull/5010)

**事件服务模块日志**

删除事件服务模块的无效的日志输出。

源代码：[https://github.com/tronprotocol/java-tron/pull/4974](https://github.com/tronprotocol/java-tron/pull/4974)  

**优化网络模块的日志输出**

优化了网络模块日志输出，对接收到的异常区块，输出Error级别日志，对已经超时的网络请求，输出Warn级别日志，提高网络相关问题的排查的效率。


源代码: [https://github.com/tronprotocol/java-tron/pull/4977](https://github.com/tronprotocol/java-tron/pull/4977)
 
--- 

*The more sand that has escaped from the hourglass of our life, the clearer we should see through it.* 
<p align="right"> ---Sartre</p>

## GreatVoyage-v4.7.0.1(Aristotle)

GreatVoyage-v4.7.0.1(Aristotle)版本引入了多个重要的优化和更新，全新的质押机制Stake 2.0, 提高了资源模型的灵活性和质押系统的稳定性；动态能量模型，有助于促进生态的均衡发展；二级缓存机制优化了数据库读取性能，提高了交易执行性能，提升了网络吞吐量；使用libp2p库作为Java-tron P2P网络模块，使代码结构更加清晰，并且降低代码耦合性；优化日志输出，将LevelDB和RocksDB的日志重定向到Java-tron日志文件；将更多工具包集成的toolkit工具箱，为用户带来更便捷的开发体验。

下面是详细介绍。



### 核心协议
#### 1. Stake 2.0 质押模型

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

#### 2. 优化数据库查询性能
Java-tron采用内存和磁盘数据库的方式进行数据存储，固化的区块数据会保存在多个磁盘数据库中，未被固化的数据保存在内存中，当一个区块被固化后，会将相应的内存数据写入到磁盘数据库。在查询数据时，首先查询内存中的数据，如果没有找到，再查询磁盘数据库。而磁盘数据库查询是比较耗时的，因此，GreatVoyage-v4.7.0.1(Aristotle)版本优化了数据库查询性能，在进行底层磁盘数据库操作之前，增加了二级缓存。在将数据写入磁盘的同时，也将数据写入到二级缓存。当需要查询磁盘数据库时，如果二级缓存中存在要查询的数据，则直接返回，而无需再查询磁盘数据库。二级缓存减少了查询磁盘数据库的次数，提高了交易执行速度，提升了网络吞吐量。

* 源代码：[https://github.com/tronprotocol/java-tron/pull/4740](https://github.com/tronprotocol/java-tron/pull/4740) 

#### 3. 优化区块生产流程
节点进行区块生产时会依次校验和执行可以打包进区块的所有交易，而每一次的交易验证和执行，都会涉及到区块数据的获取，比如区块号、区块大小、区块内的交易信息等。在GreatVoyage-v4.7.0.1(Aristotle)之前的版本中，节点打包交易时，在验证和执行每一笔交易过程中，区块数据都是被重新计算的，这其中包含了许多重复的计算。

为了提高节点打包交易效率，GreatVoyage-v4.7.0.1(Aristotle)版本优化了区块生产流程，只计算一次区块数据并仅在必要时更新数据，从而大幅减少了区块数据计算的次数，提高了区块打包效率。

* 源代码：[https://github.com/tronprotocol/java-tron/pull/4756](https://github.com/tronprotocol/java-tron/pull/4756) 

#### 4. 增加交易hash缓存
节点在处理区块时，会多次用到交易哈希值，而在GreatVoyage-v4.7.0.1(Aristotle)之前的版本中，交易哈希值都是随用随计算，而交易哈希值的计算比较耗时，从而导致区块处理较慢，因此，GreatVoyage-v4.7.0.1(Aristotle)版本增加了交易hash缓存，使用时直接从缓存中获取，只有当交易数据发生改变时，才重新计算交易哈希。交易hash的缓存，减少了不必要的交易哈希计算，提高了区块处理速度。

* 源代码：[https://github.com/tronprotocol/java-tron/pull/4792](https://github.com/tronprotocol/java-tron/pull/4792)   


#### 5. libp2p集成
从GreatVoyage-v4.7.0.1(Aristotle)版本开始，将直接使用模块的libp2p库作为Java-tron 的P2P网络模块，而不再使用原来的p2p模块，使代码结构更加清晰，代码耦合性更低，更易于维护。


* 源代码：[https://github.com/tronprotocol/java-tron/pull/4791](https://github.com/tronprotocol/java-tron/pull/4791) 


### TVM
#### 1. 新增Stake2.0相关的TVM指令和预编译合约

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

#### 2. 动态能量模型
动态能量模型是一种根据合约已知的能量使用情况来动态调整合约未来的能量消耗的方案，如果一个合约在一个周期内使用过多的资源，则下一个周期中该合约将增加一定百分比的惩罚性消耗，用户向该合约发送相同的交易将产生更多的能量消耗量。当合约合理使用资源时，用户调用该合约所产生的能源消耗将逐渐恢复正常，通过这个机制，让能源资源在链上的分配更加合理，防止网络资源过度集中在少数合约上。

更多关于动态能量模型的原理请参考：[Introduction to Dynamic Energy Model](https://coredevs.medium.com/introduction-to-dynamic-energy-model-31917419b61a)。

动态能量模型是TRON网络中的一个动态参数，GreatVoyage-v4.7.0.1(Aristotle)部署之后默认为关闭状态，可以通过发起提案投票的方式开启。

* TIP: [https://github.com/tronprotocol/tips/issues/491](https://github.com/tronprotocol/tips/issues/491) 
* 源代码: [https://github.com/tronprotocol/java-tron/pull/4873](https://github.com/tronprotocol/java-tron/pull/4873) 

#### 3. 优化chainId指令的返回值

从 GreatVoyage-v4.7.0.1(Aristotle)版本开始，将chainid指令的返回值从创世块区块哈希改成创世块区块哈希的最后四个字节，使chainid指令返回值与Java-tron json-rpc `eth_chainId` API的返回值一致。

优化chainId指令返回值是TRON网络的一个动态参数，GreatVoyage-v4.7.0.1(Aristotle)部署之后默认为关闭状态，可以通过发起提案投票的方式开启。

* TIP: [https://github.com/tronprotocol/tips/issues/474](https://github.com/tronprotocol/tips/issues/474) 
* 源代码: [https://github.com/tronprotocol/java-tron/pull/4863](https://github.com/tronprotocol/java-tron/pull/4863) 


### API

#### 1. 新增Stake 2.0相关API
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

#### 2. 新增预估能量接口

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


### 其它变更


#### 1. 优化编译参数
GreatVoyage-v4.7.0.1(Aristotle)版本优化了Gradle编译参数，将JVM堆内存最小值设置成1G，以加快Java-tron gradle编译速度。

* 源代码：  [https://github.com/tronprotocol/java-tron/pull/4837](https://github.com/tronprotocol/java-tron/pull/4837) 

#### 2. 优化节点自动停止功能

为了方便节点部署者进行数据备份或数据统计，从GreatVoyage-v4.5.1(Tertullian)版本开始，节点支持在特定的条件下停止运行，用户可以通过节点配置文件设置节点停止的条件，在满足设置的条件时，节点将停止运行。支持3个停止条件同时设置，满足任意个条件即停止节点。这三个条件包括区块时间、区块高度以和节点从启动到停止需要同步的区块数量， 但是由于允许同时设置多个停止条件，当用户只需要一个条件时，需要在配置文件中注释掉其他2个条件配置项，因此，如果用户忘记注释，可能出现节点停止在非预期的区块上。但实际并没有需要同时设置多个条件的应用场景，所以，GreatVoyage-v4.7.0.1(Aristotle)版本优化了节点自动停止功能，可选的配置参数不变，但是仅允许同时设置一个有效参数，如果节点部署者设置了多个参数，节点将报错并退出运行。该优化极大的简化了用户使用的复杂度。

* 源代码：  [https://github.com/tronprotocol/java-tron/pull/4853](https://github.com/tronprotocol/java-tron/pull/4853)
[https://github.com/tronprotocol/java-tron/pull/4858](https://github.com/tronprotocol/java-tron/pull/4858) 

#### 3. 删除数据库V1版本相关代码
在GreatVoyage-v4.7.0.1(Aristotle)之前的版本中，数据库有两个版本v1和v2，用户可以通过配置项`db.version`选择使用的版本，由于v2版本采用内存+磁盘数据库模式、支持底层数据库的扩展、异常情况下数据的正确恢复功能等，相对与v1版本, v2优势非常明显。 因此，为了使代码结构更加清晰，从GreatVoyage-v4.7.0.1(Aristotle)开始，删除了数据库v1版本相关的代码，以及数据库版本配置项`db.version `。用户无需再进行数据库版本配置，直接使用v2版本的数据库，降低了配置节点的复杂度。

* 源代码：  [https://github.com/tronprotocol/java-tron/pull/4836](https://github.com/tronprotocol/java-tron/pull/4836)

#### 4. 优化数据库日志输出
在GreatVoyage-v4.7.0.1(Aristotle)之前的版本中，节点日志中不包含LevelDB 或者 RocksDB 本身输出的底层日志，排查数据库读写问题比较困难。因此，GreatVoyage-v4.7.0.1(Aristotle)版本优化了数据库日志，将LevelDB或者RocksDB数据模块的底层日志的输出重定向到节点日志文件中，简化的了数据库故障排查的难度，提高了节点运维的效率。

* 源代码:  [https://github.com/tronprotocol/java-tron/pull/4833](https://github.com/tronprotocol/java-tron/pull/4833) 
#### 5. snapshot 最大落盘数量可配置
新加入到网络的节点需要从其他节点同步区块数据，节点将同步过来的区块数据首先保存在内存中，然后再存储到磁盘。在GreatVoyage-v4.7.0.1(Aristotle)之前的版本中，当节点追块时，一次落盘操作会将500个区块的数据从内存写入到磁盘，因此，内存中会保留超过500个区块的数据，并且各个区块数据通过链表关联。在查询数据时，先依次在500多个区块中查找，当找不到所要查询的数据时，再查询磁盘数据库，但遍历500多个区块数据降低了数据查询效率。

因此，从GreatVoyage-v4.7.0.1(Aristotle)版本开始，支持snapshot落盘数量可配置，通过`storage.snapshot.maxFlushCount`配置项设置一次落盘的最大区块数量，以使数据库查询效率最大化，提高区块处理速度。如果不设置，则snapshot最大落盘数量为默认值1。

* 源代码：[https://github.com/tronprotocol/java-tron/pull/4834](https://github.com/tronprotocol/java-tron/pull/4834) 

#### 6. Toolkit.jar工具箱集成
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



## GreatVoyage-v4.6.0(Socrates)

GreatVoyage-v4.6.0(Socrates)版本引入了多个重要的优化和更新，优化的数据库检查点机制，提高了节点运行的稳定性；优化的资源代理关系存储结构，以及新的投票奖励计算模型，加快了交易的执行速度，提高了网络吞吐量；增加备注收费的提案，提高带备注交易的成本来减少低价值交易的数量，提升波场网络的安全性和可靠性。集成的toolkit工具包、新增的网络相关prometheus指标、新增的help命令行选项，为用户带来更便捷的开发体验。

下面是详细介绍。



### 核心协议
#### 1.  优化资源代理关系的存储结构
TRON网络中，账户可以通过质押将资源代理给其它账户，也可以接受其它账户为自己的资源代理，因此，每个账户都需要维护一个代理关系的记录，包含该账户代理出去的所有账户地址，和为自己代理资源的所有账户地址。

在GreatVoyage-v4.6.0(Socrates)之前的版本中，代理关系以列表的形式存储，当执行资源代理操作时，需要首先在列表中查找是否已经存在该代理账户，如果已经存在，则不需要添加到列表，只有当不存在时才将地址添加到列表中。如果某账户给多个其它账户代理了资源或者多个其它账户为自己代理了资源，那么该账户中的代理关系列表的长度将非常大，当执行涉及该账户的资源代理交易时，对列表的查找操作将非常耗时，导致交易执行时间很长。因此，GreatVoyage-v4.6.0(Socrates)版本优化了资源代理关系的存储结构，将代理关系存储结构从数组改为键值对，以实现在常量时间内完成对其数据的读取和更改，极大的加快了代理相关交易的执行速度，提高网络吞吐量。

资源代理存储结构优化是TRON网络中的一个动态参数，GreatVoyage-v4.6.0(Socrates)部署之后默认为关闭状态，可以通过发起提案投票的方式开启。


* TIP: [https://github.com/tronprotocol/tips/issues/476](https://github.com/tronprotocol/tips/issues/476) 
* 源代码：[https://github.com/tronprotocol/java-tron/pull/4788](https://github.com/tronprotocol/java-tron/pull/4788) 
#### 2. 交易备注收费
从GreatVoyage-v4.6.0(Socrates)版本开始，将对交易中的备注收取额外的费用，备注收费将提高带备注交易的成本，减少低价值交易的数量，提升波场网络的安全性和可靠性。

备注费用是TRON网络的一个动态参数，GreatVoyage-v4.6.0(Socrates)部署之后默认为0，单位是 sun， 可以通过发起提案投票指定一个非0值来开启，例如设置为1000000， 表示带备注的交易需要额外消耗1 TRX费用。


* TIP: [https://github.com/tronprotocol/tips/issues/387](https://github.com/tronprotocol/tips/issues/387) 
* 源代码：[https://github.com/tronprotocol/java-tron/pull/4758](https://github.com/tronprotocol/java-tron/pull/4758) 

#### 3. 优化投票奖励计算算法
TRON网络中很多选民会累积很长时间的奖励再进行提取，两次提取奖励之间的间隔很长，在GreatVoyage-v4.6.0(Socrates)之前的版本中，如果用户提交了提取奖励的交易， 该交易会依次计算并累加距离上一次提取奖励之间的每一个维护期获得奖励，所以距离上一次提取奖励的时间越长，本次提取奖励的交易执行越耗时。因此，GreatVoyage-v4.6.0(Socrates)版本优化了投票奖励计算方法，不再累加每个维护期的奖励，而是将上一个维护期记录的奖励总数减去上一次提取奖励交易所在维护期记录的奖励总和，就可以得到未提取的奖励总和。该方法实现了常量时间内计算出未提取的奖励总数，极大的提高了计算效率，加快了奖励计算相关交易的执行速度，从而提升网络的吞吐量。


投票奖励算法的优化是TRON网络的一个动态参数，GreatVoyage-v4.6.0(Socrates)部署之后默认是关闭状态，可以通过发起提案投票的方式开启。

* TIP: [https://github.com/tronprotocol/tips/issues/465](https://github.com/tronprotocol/tips/issues/465) 
* 源代码：  [https://github.com/tronprotocol/java-tron/pull/4694](https://github.com/tronprotocol/java-tron/pull/4694) 

#### 4. 升级数据库模块中的Checkpoint机制
Checkpoint机制是为了防止节点宕机引起数据库损坏而建立的恢复机制，Java-tron采用内存和多磁盘数据库的方式进行数据存储，固化的区块数据会保存在多个业务数据库中。未被固化的数据保存在内存中，当一个区块被固化后，会将相应的内存数据写入到多个业务数据库，但由于多个业务数据库的写入并非原子操作，此时节点由于某种原因意外宕机，那么该区块的数据会无法完成全部落盘，导致节点会因为数据库损坏而无法重启。

所以在内存数据写入磁盘之前，先创建Checkpoint检查点，检查点中包含本次需要写入到各个业务数据库的所有数据， 完成检查点创建后，先将检查点数据落盘到一个独立的Checkpoint数据库，然后执行业务数据库落盘操作，Checkpoint数据库始终保留一个最新的固化块数据。如果业务数据库因宕机而损坏，节点重启后会通过之前保存在checkpoint中的区块数据来修复业务数据库。

目前Checkpoint机制可以应对绝多数多宕机的情况，但业务数据库仍然有小概率会因为宕机损坏。目前LevelDB的数据写入均是异步方式, 程序调用LevelDB请求将数据写入磁盘，实际上数据只是被写入到操作系统的高速缓冲中，之后操作系统会根据自己的策略决定真正写入到磁盘的时机。当Java-tron节点完成Checkpoint数据库写入，继续写入业务数据库时，此时发生意外宕机，有可能写入到Checkpoint数据库的数据并没有被操作系统真正写入磁盘，这种情况下，节点会因为Checkpoint数据库没有恢复数据而无法重启。

为了解决这一问题，GreatVoyage-v4.6.0(Socrates)版本增加了V2版本的Checkpoint实现，新的Checkpoint机制会存储多个已固化的区块数据，即便最新的固化块数据因为宕机没有被成功写入到Checkpoint数据库，节点重新后也可以拿历史固化块数据来恢复业务数据库。

配置文件中默认关闭了V2版本Checkpoint机制， 可通过修改配置来开启该功能，需要注意的是已经开启了V2版本的节点运行一段时间后，将无法重新设置回V1版本的Checkpoint机制。


* TIP: [https://github.com/tronprotocol/tips/issues/461](https://github.com/tronprotocol/tips/issues/461) 
* 源代码:  [https://github.com/tronprotocol/java-tron/pull/4614](https://github.com/tronprotocol/java-tron/pull/4614) 
#### 5. 优化超级代表主备节点区块生产的优先级
如果超级代表部署了主备节点，主备节点之间会保持连接，当主备节点因网络问题导致短暂性断连时，备用节点会认为主节点失效而参与区块生产，这种情况下会出现主备节点同时出块的情况，在GreatVoyage-v4.6.0(Socrates)之前的版本中，当主备节点收到了对方所产生的相同高度的区块时，各自都会暂停1-9个产块周期，也就是该超级代表会丢1-9个区块。

GreatVoyage-v4.6.0(Socrates)版本优化了主备节点产块的优先级，在上述情况中，当主备节点收到了对方所产生的相同高度的区块时，会比较自己生产区块的hash与对方生产区块的hash值。如果自己的hash更大，会继续产块。如果自己的hash更小，会暂停一个产块周期，之后会继续产块，再次进行区块hash比较， 总共27个超级代表顺序出块，所以跳过一个产块周期需要等待81秒，再此期间，如果主备节点之间的是因为网络短暂不佳，会有足够的时间恢复。另外其他节点收到这两个区块后也会选择hash较大的区块，丢弃hash较小的区块，因此该优化将大幅提高超级代表在主备节点之间网络通信不佳情况下的区块生产效率，提升网络的稳定性。

* 源代码：[https://github.com/tronprotocol/java-tron/pull/4630](https://github.com/tronprotocol/java-tron/pull/4630) 

#### 6 优化P2P网络模块的Kademlia算法
Java-tron节点ID是个随机数，每次节点启动都会重新生成，Java-tron的Kademlia算法实现中，会根据节点ID来计算该节点的距离， 然后再根据距离决定将该节点信息放在哪个K桶中。如果K桶中的节点由于某种原因重新启动，节点ID会发生变化，当检测到该节点再次下线，根据最新的节点ID计算的距离，已经无法定位到K桶的位置，导致无法在K桶中删除该节点。这种重启的节点过多，会导致节点K桶中存储了过多无效数据。

因此，GreatVoyage-v4.6.0(Socrates)版本优化了Kademlia算法，并采用Hash表来记录已经发现的节点。节点的距离只有在第一次写入K桶的时候计算一次，并赋值给节点的distance字段，然后将节点加入到哈希表中，以后直接通过该字段获取节点距离，即便节点重启后ID发生改变也不会更新Hash表中该节点的距离。当探测到该节点下线后，可以根据节点ip从hash表里找到对应的节点，然后通过节点distance字段获取到该节点的距离，然后从K桶中删除该节点。

* 源代码：[https://github.com/tronprotocol/java-tron/pull/4620](https://github.com/tronprotocol/java-tron/pull/4620) [https://github.com/tronprotocol/java-tron/pull/4622](https://github.com/tronprotocol/java-tron/pull/4622) 


### 其它变更
#### 1. 集成ArchiveManifest.jar到Toolkit.jar工具包

ArchiveManifest.jar是一个独立的LevelDB启动优化工具， 可以优化 LevelDB manifest的文件大小，从而减少内存占用，大幅提升节点启动速度。从 GreatVoyage-v4.6.0(Socrates)版本开始，将ArchiveManifest.jar工具集成到了Toolkit.jar工具中，未来Java-tron周边的工具将逐步都集成到Toolkit.jar工具箱中，以便于工具维护和开发者使用。

* 源代码: [https://github.com/tronprotocol/java-tron/pull/4603](https://github.com/tronprotocol/java-tron/pull/4603)   



#### 2. 新增网络模块相关Prometheus指标
GreatVoyage-v4.6.0(Socrates)版本新增了三个网络模块相关的prometheus指标：区块获取延迟、区块接收延迟和消息处理延迟。新的指标有助于节点网络健康监控。

* 源代码：[https://github.com/tronprotocol/java-tron/pull/4626](https://github.com/tronprotocol/java-tron/pull/4626) 

#### 3. 新增help命令行选项
GreatVoyage-v4.6.0(Socrates)版本增加了help命令行选项，用于查看所有的参数及其使用说明。下面是使用示例：
```
$ java -jar FullNode.jar --help

Name:
	FullNode - the java-tron command line interface

Usage: java -jar FullNode.jar [options] [seedNode <seedNode> ...]

VERSION:
4.5.2-d05f766

TRON OPTIONS:
-v, --version			Output code version
-h, --help   			Show help message
-c, --config 			Config file (default:config.conf)
--log-config 			Logback config file
--es         			Start event subscribe server

DB OPTIONS:
-d, --output-directory			Data directory for the databases (default:output-directory)

WITNESS OPTIONS:
-w, --witness    			Is witness node
-p, --private-key			Witness private key

VIRTUAL MACHINE OPTIONS:
--debug			Switch for TVM debug mode. In debug model, TVM will not check for timeout. (default: false)
```



* 源代码：[https://github.com/tronprotocol/java-tron/pull/4606](https://github.com/tronprotocol/java-tron/pull/4606) 


#### 4. 优化轻节点工具

LiteFullNodeTool.jar是java-tron的轻节点工具， 主要功能是将全节点数据库转化为轻节点数据库，GreatVoyage-v4.6.0(Socrates)版本优化了该工具，提升了工具的便捷性和稳定性。


* 源代码：[https://github.com/tronprotocol/java-tron/pull/4607](https://github.com/tronprotocol/java-tron/pull/4607)


#### 5. 优化eth_getBlockByHash和eth_getBlockByNumber 接口的返回值
为了更好地兼容Ethereum的JsonRPC 2.0协议接口，GreatVoyage-v4.6.0(Socrates)版本将eth_getBlockByHash和eth_getBlockByNumber 接口返回值中`timestamp`字段的单位从毫秒改为秒， 使接口返回值格式与Ethereum Geth完全兼容。

* 源代码：[https://github.com/tronprotocol/java-tron/pull/4642](https://github.com/tronprotocol/java-tron/pull/4642) 

--- 

*To move the world we must move ourselves.* 
<p align="right"> --- Socrates</p>






## GreatVoyage-v4.5.2(Aurelius)
GreatVoyage-v4.5.2(Aurelius)版本引入了多个重要的优化更新，优化的交易缓存机制，大幅减少了内存占用，提高了节点性能；优化的对等节点连接策略，提高了对等节点间建立连接的效率，加快了节点同步进程；优化的区块生产及处理逻辑，提高了节点稳定性；新增的数据库存储分区工具，减轻了数据存储压力；新增的区块头查询API以及历史带宽单价查询API，为用户带来更便捷的开发体验。


### 核心协议
#### 1. 优化区块处理逻辑 
在GreatVoyage-v4.5.2(Aurelius)之前的版本中，区块生产、区块处理及交易处理等线程共同竞争同步锁，而在高并发，并且交易执行时间较长的情况下，区块生产或者区块处理线程获取到同步锁所需要的时间较长，从而导致小概率丢块事件的发生。为了提高节点稳定性，GreatVoyage-v4.5.2(Aurelius)版本优化了区块处理逻辑中的同步锁，仅允许一个交易处理线程与区块生产或处理线程竞争同步锁，并且当交易处理线程发现有区块相关线程在等待同步锁时，会主动退让，这大大提高了区块生产和区块处理线程获取到同步锁的概率，保证了节点高吞吐、稳定的运行。


TIP: https://github.com/tronprotocol/tips/blob/master/tip-428.md
源代码: https://github.com/tronprotocol/java-tron/pull/4551 

#### 2. 优化交易缓存机制
节点使用交易缓存来判断新收到交易是否是重复交易，在GreatVoyage-v4.5.2(Aurelius)之前的版本中，交易缓存是一个hashmap数据结构，该结构会保存最近65536个区块中的交易，hashmap会为每一条交易单独分配内存，因此，在节点运行过程中，交易缓存占据了约2G内存空间，而且由于频繁的内存申请会触发频繁的JVM垃圾回收，也间接影响着节点的性能。为此，GreatVoyage-v4.5.2(Aurelius)版本优化了交易缓存的实现，采用布隆过滤器代替hashmap，布隆过滤器使用固定且极小的内存空间来记录最近的历史交易，极大的减少了交易缓存对内存的占用，提高了节点性能。


TIP: https://github.com/tronprotocol/tips/blob/master/tip-440.md
源代码：https://github.com/tronprotocol/java-tron/pull/4538  




#### 3. 优化P2P节点连接策略

在GreatVoyage-v4.5.2(Aurelius)之前的版本中，一个节点所连接的远端节点的数量已经达到了最大值，该节点会拒绝新的远端节点的连接请求。随着网络中这样的满连接节点的增加，新加入的节点与网络中的其它节点建立连接将越来越困难。

为了加快网络中节点间的连接速度，GreatVoyage-v4.5.2(Aurelius)版本优化了P2P节点连接策略，周期性对节点的TCP连接数量进行检查，如果达到满连接，则采用一定的淘汰策略与其中一个或者两个节点进行断连，以增加网络中新加入的节点与其成功连接的可能性，从而提高网络中P2P节点间建立连接的效率，提升了网络稳定性。需要注意的是，配置文件中`node.active`和`node.passive`列表中配置的节点均为信任节点，不会被断开连接。

TIP: https://github.com/tronprotocol/tips/blob/master/tip-425.md 
源代码: https://github.com/tronprotocol/java-tron/pull/4549   



#### 4. 优化区块打包逻辑
在GreatVoyage-v4.5.2(Aurelius)之前的版本中，对于预执行正常的交易，在打包时可能会碰到JVM GC停顿，导致交易执行超时，从而被丢弃。因此GreatVoyage-v4.5.2(Aurelius)版本优化了区块打包逻辑，对于预执行正常的交易，如果在打包时执行超时，则采取重试操作，以避免在打包交易过程中，由于JVM GC停顿导致交易丢失。

源代码：https://github.com/tronprotocol/java-tron/pull/4387 

#### 5. 优化切链逻辑
在TRON网络中偶尔会出现微分叉的情况，微分叉时会产生切链行为，在切链时会回退区块，并将被回退区块内交易重新放回到待打包交易队列中。当这些交易被重新打包执行时，可能会由于切链导致执行结果不一致，在GreatVoyage-v4.5.2(Aurelius)之前的版本中，整个过程引用的是同一个交易对象，所以切链可能会导致回退区块中的交易结果被更改。当再次发生切链，并且切回到原链时，会再次执行原链上的交易，就会产生`Different resultCode`错误，从而导致节点停止同步。因此，GreatVoyage-v4.5.2(Aurelius)版本优化了切链逻辑，在进行区块回退时，为被回退区块内交易创建新的交易对象，避免交易结果被修改，提升了节点对微分叉处理的稳定性。

源代码：https://github.com/tronprotocol/java-tron/pull/4583 

#### 6. 新增数据库存储分区工具
随着链上数据增长，全节点的磁盘空间可能不足，需要更换更大容量的磁盘。为此，从GreatVoyage-v4.5.2(Aurelius)版本开始，提供了数据库存储分区工具，它能够根据用户的配置将部分数据库迁移到其它磁盘分区，因此用户只需根据容量需求添加磁盘即可，无需更换原磁盘，方便用户对磁盘进行扩容，同时降低节点运行成本。


源代码：https://github.com/tronprotocol/java-tron/pull/4545 
               https://github.com/tronprotocol/java-tron/pull/4559 
               https://github.com/tronprotocol/java-tron/pull/4563 


 
### API
#### 1. 新增区块头查询API

从GreatVoyage-v4.5.2(Aurelius)版本开始，新增区块头查询API，仅返回区块头信息，不返回区块中交易信息，用户不需查询整个区块即可获取到区块头信息，这不但降低了节点的网络I/O负载，而且由于区块不带交易信息，减少了序列化时间，降低了接口延迟，提升了查询效率。

 
源代码：https://github.com/tronprotocol/java-tron/pull/4492 
https://github.com/tronprotocol/java-tron/pull/4552 

#### 2. 新增历史带宽单价查询API
根据带宽消耗规则，如果交易发起者账户通过质押获得的带宽或者免费带宽不足时，将燃烧TRX来支付带宽费用，这时，在交易记录中仅记录带宽费用，而不记录带宽消耗量，为了了解历史交易的带宽消耗量，从GreatVoyage-v4.5.2(Aurelius)版本开始，新增历史带宽单价查询API `/wallet/getbandwidthprices`，用户可以通过该接口获取到带宽代价的历史记录，从而可以计算出历史交易的带宽消耗量。

源代码：https://github.com/tronprotocol/java-tron/pull/4556 

### 其它变更
#### 1. 优化区块同步逻辑
GreatVoyage-v4.5.2(Aurelius)版本优化了区块同步逻辑，避免了在同步区块过程中不必要的节点断连，提高了节点稳定性。


源代码：https://github.com/tronprotocol/java-tron/pull/4542 
https://github.com/tronprotocol/java-tron/pull/4540 
#### 2. 优化`eth_estimateGas`和`eth_call` API
GreatVoyage-v4.5.2(Aurelius)版本优化了`eth_estimateGas`和`eth_cal` JSON-RPC接口，当智能合约交易执行中断时，能够返回错误信息。

源代码：https://github.com/tronprotocol/java-tron/pull/4570 

#### 3. 增强接口的容错处理能力
GreatVoyage-v4.5.2(Aurelius)版本优化了多个API接口，增强了其对参数的容错能力，提高了API接口的稳定性。

源代码：https://github.com/tronprotocol/java-tron/pull/4560 
https://github.com/tronprotocol/java-tron/pull/4556 
 
--- 

*The universe is change; our life is what our thoughts make it.* 
<p align="right"> ---  Aurelius</p>




## GreatVoyage-v4.5.1(Tertullian)
GreatVoyage-v4.5.1(Tertullian)版本引入多个重要的优化更新，优化的交易缓存加载流程，加快了节点启动速度；优化的获取区块逻辑和轻节点同步逻辑，提升了节点的稳定性；优化的账户资产结构和TVM存储结构，提升了交易的处理速度，从而进一步提高了节点的性能；支持prometheus协议接口为用户带来更便捷的开发体验，有助于进一步繁荣波场生态。


### 核心协议
#### 1. 优化交易缓存的加载
GreatVoyage-v4.5.1(Tertullian)之前版本，从节点启动到区块同步需要较长的时间，其中交易缓存的加载占用了大部分的节点启动时间。交易缓存被节点用来判断一个交易是否是重复的交易，因此在节点启动过程中，需要将交易缓存从数据库加载到内存，而在GreatVoyage-v4.5.1(Tertullian)之前的版本中，交易缓存的加载是以交易为存储单元进行数据库读取的，因此读取的数据量较大，整个读取过程较耗时。

为了加快节点启动速度，GreatVoyage-v4.5.1(Tertullian)版本优化了交易缓存的加载方式，通过以区块为存储单元进行数据库读取，减少了数据库读取的次数，提高了交易缓存加载的效率，提升了节点启动的速度。


TIP: https://github.com/tronprotocol/tips/blob/master/tip-383.md
源代码: https://github.com/tronprotocol/java-tron/pull/4319 

#### 2. 优化账户TRC-10资产存储结构
在GreatVoyage-v4.5.1(Tertullian)之前的版本中，当账户中的TRC10资产过多时，账户在数据库中存储的内容很大， 导致在执行交易的过程中，账户的反序列化操作非常耗时，因此，GreatVoyage-v4.5.1(Tertullian)版本增加了一个优化账户资产结构的新提案，允许将TRC-10资产从账户中分离出来，并单独存储在一个key-value数据结构中，以减少账户结构中的内容，加快账户的反序列化操作，减少交易的执行时间，从而提高网络吞吐量，提升网络性能。

TIP: https://github.com/tronprotocol/tips/blob/master/tip-382.md 
源代码：https://github.com/tronprotocol/java-tron/pull/4392 

#### 3. 优化轻节点同步逻辑
由于轻节点不保存完整的区块数据，因此，某个节点所连接的轻节点中有可能没有它想要与之同步的区块，这时所连接的轻节点会主动断开连接。在GreatVoyage-v4.5.1(Tertullian)之前的版本中，节点有可能重复的与这样的轻节点建立连接，然后被对方断开连接，这极大的影响了节点间同步区块的效率。因此，在GreatVoyage-v4.5.1(Tertullian)版本中，优化了节点建立连接的逻辑，在节点间握手消息中加入了”节点类型”和”节点的最低区块”两个字段，并且节点会保存与各个节点的握手消息。如果当前节点的最高区块低于轻节点最低区块时，它将主动与该轻节点断开连接，并且下次再与节点建立连接时，会过滤掉这样的节点，避免了更多的无效连接，提高了节点间同步的效率。


TIP: https://github.com/tronprotocol/tips/blob/master/tip-388.md 
源代码: https://github.com/tronprotocol/java-tron/pull/4323  



#### 4. 优化区块广播逻辑
GreatVoyage-v4.5.1(Tertullian)版本优化了区块广播逻辑，使fast farward节点只将区块广播到接下来将要出块的三个超级代表节点（广播到的超级代表节点的数量可以通过配置文件更改），以保证超级代表节点可以及时的获取到最新区块，提高了区块生产的效率。

源代码：https://github.com/tronprotocol/java-tron/pull/4336 

#### 5. 优化区块获取逻辑
由于网络原因，节点有可能接收不到广播的新区块，在GreatVoyage-v4.5.1(Tertullian)之前的版本中，当获取区块超时后，节点将通过P2P同步流程来获取该区块，但是同步流程比较复杂并且耗时，因此，GreatVoyage-v4.5.1(Tertullian)版本优化了获取最新区块的流程，节点将首先根据各个节点的状态选择一个节点，然后直接发送区块获取消息`FetchInvDataMessage`给该节点，来获取最新区块，这节省了区块同步过程中的大部分时间，加快了最新区块获取的速度，提高了节点的稳定性。

TIP: https://github.com/tronprotocol/tips/blob/master/tip-391.md 
源代码：https://github.com/tronprotocol/java-tron/pull/4326 

#### 6. 支持prometheus协议接口
从GreatVoyage-v4.5.1(Tertullian)版本开始，节点提供开源的系统监控工具prometheus协议接口，用户可以更方便的监控节点的健康状态。

TIP: https://github.com/tronprotocol/tips/blob/master/tip-369.md 
源代码：https://github.com/tronprotocol/java-tron/pull/4337 

#### 7. 节点支持在特定状态下停止运行
为了方便节点部署者进行数据备份或数据统计，从GreatVoyage-v4.5.1(Tertullian)版本开始，节点支持在特定的条件下停止运行，用户可以通过节点配置文件设置节点停止的条件，如节点停止的区块时间，区块高度，节点从启动到停止需要同步的区块数量。在满足设置的条件时，节点将停止运行。

TIP: https://github.com/tronprotocol/tips/blob/master/tip-370.md  
源代码：https://github.com/tronprotocol/java-tron/pull/4325 


### TVM
#### 1. 调整TVM最大执行时间可设置的上限
“TVM最大执行时间”是TRON网络的一个动态参数，表示允许一笔智能合约执行的最大时间，超级代表可以通过提案投票来更改此参数，在GreatVoyage-v4.5.1(Tertullian)之前的版本中，该参数可修改的最大值是100ms。而随着TRON网络基础设施的稳定和生态的蓬勃发展，100ms上限一定程度上限制了智能合约的复杂性。因此，GreatVoyage-v4.5.1(Tertullian)版本增加了一个新的提案，允许将”TVM最大执行时间”的可设置上限提升到400ms。

TIP: https://github.com/tronprotocol/tips/blob/master/tip-397.md  
源代码：https://github.com/tronprotocol/java-tron/pull/4375 
#### 2. 优化TVM缓存结构

在GreatVoyage-v4.5.1(Tertullian)之前的版本中，TVM中的缓存数据是以字节数组的形式存储的，当需要对缓存中的数据进行更改时，首先要将数据从字节数组的形式进行序列化操作变为protobuf对象，然后更改对象的某个字段（如账户余额等）生成一个新的对象，然后再对新生成的protobuf对象进GreatVoyage-v4.5.1(Tertullian)版本优化了TVM执行时缓存中的数据结构，直接保存protobuf对象数据，以减少访问缓存中数据时的序列化/反序列化操作，加快TVM执行字节码的速度。


源代码：https://github.com/tronprotocol/java-tron/pull/4375   


--- 

*Hope is patience with the lamp lit.* 
<p align="right"> --- Tertullian </p>


## GreatVoyage-v4.4.6(David)
GreatVoyage-v4.4.6(David)更新了使用的fastjson依赖库版本，保证了使用fastjson的安全性。

### 其它变更

#### 1. 更新fastjson依赖库到最新版本
由于fastjson1.2.80及之前的版本存在安全漏洞，因此，GreatVoyage-v4.4.6(David)版本将fastjson依赖库的版本更新到1.2.83，并且开启fastjson的`safemode`模式，保证了使用fastjson的安全性。

源代码：https://github.com/tronprotocol/java-tron/pull/4393 




---
*Beauty in things exists in the mind which contemplates them.* 
<p align="right"> ---David Hume</p>



## GreatVoyage-4.4.5(Cicero)
GreatVoyage-v4.4.5(Cicero)版本优化了节点的查询接口，使其过滤掉无效字段，保证了接口解析数据的稳定性。

### 其它变更

#### 1. 优化节点查询接口
GreatVoyage-v4.5.0(Cicero)版本优化了节点的查询接口，在解析获取到的数据时，节点将过滤掉无效字段，保证接口数据的正常返回。

源代码: https://github.com/tronprotocol/java-tron/pull/4349 



---
*No one can give you better advice than yourself.* 
<p align="right"> ---Cicero </p>



## GreatVoyage-4.4.4(Plotinus)
GreatVoyage-v4.4.4(Plotinus)版本引入多个重要的优化更新，降低了节点对内存的占用；加快了节点启动速度；优化的网络服务、产块线程，提升了节点的稳定性；改进的版本升级机制，实现了更高效的分散治理；TVM支持多版本程序执行器，使其更好的兼容EVM，为用户带来更便捷的开发体验，有助于进一步繁荣波场生态。


### 核心协议

#### 1. 优化节点启动时间
GreatVoyage-v4.4.4(Plotinus)之前的版本，节点从启动到区块同步，需要执行约一分钟左右，区块同步线程首先会延迟30s来等待P2P线程发现其他远端节点， 然后与发现的节点建立TCP链接，最后进行区块同步，而这段延迟时间占据了大部分的启动时间。实际上每一次新发现的节点都会被持久化到本地，所以第二次节点启动时无需花额外时间去等待节点发现，完全可以使用之前持久化到本地的节点进行TCP连接, 因此从GreatVoyage-v4.4.4(Plotinus)版本开始，将等待节点发现的时间从30s降低到100ms, 以提升节点启动的速度。


TIP: https://github.com/tronprotocol/tips/blob/master/tip-366.md 
源代码: https://github.com/tronprotocol/java-tron/pull/4254  


#### 2. 优化内存使用
节点在广播交易时，为了避免重复广播，会将相应的交易存储到广播数据缓存池中, 但是由于JVM的回收策略限制，旧的缓存数据不能被及时删除，直至缓存池被占满才会触发旧数据回收，因此，容量较大的缓存池将极大的占用内存。在GreatVoyage-v4.4.4(Plotinus)之前的版本中，交易缓存池大小为100000笔。为了及时释放过期交易所占内存，GreatVoyage-v4.4.4(Plotinus)版本将交易缓存池大小更改为20000笔，以减少内存占用。

TIP: https://github.com/tronprotocol/tips/blob/master/tip-362.md 
源代码: https://github.com/tronprotocol/java-tron/pull/4250 


#### 3. 优化产块线程
GreatVoyage-v4.4.4(Plotinus)版本的产块线程，增加了对中断异常的处理，使出块节点捕获到中断指令时，节点能够安全退出。

源代码：https://github.com/tronprotocol/java-tron/pull/4219 

### TVM
#### 1. TVM支持多版本程序执行器
为了使TRON网络未来能够支持多种类型的智能合约交易，GreatVoyage-v4.4.4(Plotinus)将TVM代码进行了重构，能够支持根据智能合约的版本信息，选择其对应的指令集来解释执行该版本的智能合约的字节码。

源代码：https://github.com/tronprotocol/java-tron/pull/4257 
                 https://github.com/tronprotocol/java-tron/pull/4259 


### 其它变更
#### 1. 优化节点日志存储
GreatVoyage-v4.4.4(Plotinus)版本修改了节点日志保留的时间，从3天增加到7天，以方便用户排查问题。

源代码：https://github.com/tronprotocol/java-tron/pull/4245 



#### 2. 优化网络服务关闭逻辑
GreatVoyage-v4.4.4(Plotinus)版本优化了网络服务关闭逻辑，先关闭同步服务，再关闭TCP连接服务，以确保所有P2P连接相关服务安全退出。

源代码：https://github.com/tronprotocol/java-tron/pull/4220 




#### 3. 改进Java-tron升级机制
对于java-tron的版本升级机制，在GreatVoyage-v4.4.4(Plotinus)之前的版本中需要全部27个超级代表节点完成代码升级，TRON网络才能升级到新版本，而TRON是一个完全去中心化治理的网络，有时候27个超级代表节点无法在某一时间内完成代码升级，使得版本升级过程缓慢。为了实现更高效的去中心化治理，在GreatVoyage-v4.4.4(Plotinus)中，改进了Java-tron的版本升级机制，只需要22个超级代表节点完成代码升级，TRON网络即可升级到新版本。

源代码：https://github.com/tronprotocol/java-tron/pull/4218

---
*The world is knowable, harmonious, and good..* 
<p align="right"> --- Plotinus </p>


## GreatVoyage-4.4.2(Augustinus)
GreatVoyage-v4.4.2(Augustinus)版本引入了三个重要的优化更新，新的操作码执行模型提高了TVM性能，个性化LevelDB参数提高了数据库性能，新增的log filter APIs使JSON-RPC API更加全面。

### TVM
#### 1. 优化TVM操作码执行模型
GreatVoyage-v4.4.2(Augustinus)版本优化了TVM中的解释器的操作码执行模型，经测试，本次优化大幅提升了TVM的性能。

TIP: https://github.com/tronprotocol/tips/blob/master/tip-344.md 
源代码：https://github.com/tronprotocol/java-tron/pull/4157 

### API
#### 1. 新增关于Event的JSON-RPC API
从GreatVoyage-v4.4.2(Augustinus)版本开始，对于兼容以太坊网络的JSON-RPC API，新增了log filter相关的APIs。

TIP: https://github.com/tronprotocol/tips/issues/343 
源代码：https://github.com/tronprotocol/java-tron/pull/4153 

### 其它变更
#### 1. LevelDB数据库性能优化
从GreatVoyage-v4.4.2(Augustinus)版本开始，根据数据库的读写频繁程度，对各个LevelDB数据库进行个性化参数设置，大幅提升数据库的性能。
源代码：https://github.com/tronprotocol/java-tron/pull/4154 

--- 

*Patience is the companion of wisdom.* 
<p align="right"> ---  Augustinus </p>


## GreatVoyage-4.4.0(Rousseau)
GreatVoyage-v4.4.0(Rousseau)版本引入了多个重要的更新：区块广播的优化将使区块可以更快的广播到全网；`dynamic store`的查询性能优化以及数据库参数的优化将大幅提升区块处理速度，进而提升java-tron的性能；节点API定制化使得节点配置更加灵活以适应不同的应用场景；TVM也将更好的兼容EVM并适配以太坊London升级，全新的JSON-RPC API将为开发者们带来更好的开发体验，帮助开发者们更容易的加入到波场生态，促进波场生态繁荣。

### 核心协议
#### 1. 优化区块广播
在GreatVoyage-v4.4.0(Rousseau)之前的版本中，区块处理的逻辑是：验证区块->处理区块->广播区块。但由于区块处理时间较长，广播区块时有延迟。为了加快区块广播，GreatVoyage-v4.4.0(Rousseau)版本将区块处理逻辑更改为：验证区块->广播区块->处理区块，以使区块可以快速广播至全网。

TIP: https://github.com/tronprotocol/tips/blob/master/tip-289.md 
源代码: https://github.com/tronprotocol/java-tron/pull/3986 

#### 2. 优化`dynamic store`的查询性能
在区块处理过程中，`dynamic store`的访问频率非常高，GreatVoyage-v4.4.0(Rousseau) 版本优化了`dynamic store`的查询性能，将`dynamic store`全部数据加载到第一级缓存，提高`dynamic store`缓存命中率，提升数据查询效率，加快区块处理速度。

TIP: https://github.com/tronprotocol/tips/blob/master/tip-290.md 
源代码：https://github.com/tronprotocol/java-tron/pull/3993 

#### 3. 优化交易广播接口
GreatVoyage-v4.4.0(Rousseau)版本优化了交易广播接口的处理流程，将交易广播由异步转为同步，广播成功后再返回结果，使得广播的返回结果更为准确。

源代码：https://github.com/tronprotocol/java-tron/pull/4000 

#### 4. 优化数据库参数
GreatVoyage-v4.4.0(Rousseau)版本优化了部分数据库参数，提升了数据库读写性能，从而提升了区块处理效率。

源代码：https://github.com/tronprotocol/java-tron/pull/4018 https://github.com/tronprotocol/java-tron/pull/3992 

### TVM
#### 1. TVM更好的兼容EVM
GreatVoyage-v4.4.0(Rousseau)版本为TVM与EVM存在差异的指令提供兼容性方案，新部署的合约支持以下特性：
1. `GASPRICE`指令返回能量单价 
2. `try-catch`支持捕获所有类型的TVM异常 
3. 禁止系统合约`TransferContract`给智能合约账户转账

TIP: https://github.com/tronprotocol/tips/blob/master/tip-272.md 
源代码：https://github.com/tronprotocol/java-tron/pull/4032 

**注意事项**：
该功能默认处于关闭状态，后续将由超级代表或超级合伙人发起相应投票请求来开启该功能。

#### 2. 对以太坊London升级进行兼容
GreatVoyage-v4.4.0(Rousseau)版本对以太坊London升级进行兼容：新增了`BASEFEE`指令； 禁止部署以0xEF为起始字节的新合约。

TIP: https://github.com/tronprotocol/tips/blob/master/tip-318.md 
源代码：https://github.com/tronprotocol/java-tron/pull/4032 

**注意事项**：
该功能默认处于关闭状态，后续将由超级代表或超级合伙人发起相应投票请求来开启该功能。

#### 3. Constant模式下的`energy limit`可配置且增大默认值
在GreatVoyage-v4.4.0(Rousseau)版本之前， constant 模式下的energy  limit是一个固定值`3,000,000`，在GreatVoyage-v4.4.0(Rousseau)中引入了修改机制，用户可以通过启动参数`--max-energy-limit-for-constant`或者节点配置文件(`vm.maxEnergyLimitForConstant`)修改 constant 模式下的energy limit值， 同时将energy limit 的默认值修改为`100,000,000`。

源代码： https://github.com/tronprotocol/java-tron/pull/4032 

### API
#### 1. 新增JSON-RPC API
从GreatVoyage-v4.4.0(Rousseau)版本开始，新增兼容以太坊网络的JSON-RPC API(不包括filter API)，使用指南请参考文档：https://developers.tron.network/reference#json-rpc-api 

源代码：https://github.com/tronprotocol/java-tron/pull/4046 

#### 2. 节点支持禁用特定API
为了节点可定制化，从GreatVoyage-v4.4.0(Rousseau)版本开始，支持通过节点配置文件关闭指定的API。

源代码：https://github.com/tronprotocol/java-tron/pull/4045 

#### 3. 优化`TriggerConstantContract`接口
在GreatVoyage-v4.4.0(Rousseau)中，对`TriggerConstantContract`接口引入了以下优化：
-  当 `ContractAddress` 为空时执行合约创建
-  `callvalue`和 `tokenvalue` 非零值将不会产生执行异常
- `TransactionExtention` 中增加事件列表和内部交易列表 

源代码： https://github.com/tronprotocol/java-tron/pull/4032 

### 其它变更

#### 1. 升级事件插件以支持`BTTC`
GreatVoyage-v4.4.0(Rousseau)中升级了事件插件，升级后的事件插件将支持`BTTC`。

源代码：https://github.com/tronprotocol/java-tron/pull/4067 

#### 2. 提升`MaxFeeLimit`的取值范围
在GreatVoyage-v4.4.0(Rousseau)之前的版本中，`MaxFeeLimit` 的取值范围是[0,1e10sun]，GreatVoyage-v4.4.0(Rousseau)版本中将`MaxFeeLimit` 的取值范围扩大为[0,1e17sun]。

**注意事项：**
该功能默认处于关闭状态，将在London升级提案生效后开启。

源代码： https://github.com/tronprotocol/java-tron/pull/4032 

####  3. 优化快速启动脚本`start.sh`
GreatVoyage-v4.4.0(Rousseau)版本中优化了快速启动脚本，最新的使用指南请参考： https://github.com/tronprotocol/java-tron/blob/release_v4.4.0/shell.md

--- 

*The world of reality has its limits; the world of imagination is boundless.* 
<p align="right"> ---  Rousseau</p>



## GreatVoyage-4.3.0(Bacon)
GreatVoyage-v4.3.0(Bacon)版本引入多个重要的优化更新，`FREE_NET_LIMIT` 和 `TOTAL_NET_LIMIT` 的可配置化有助于TRON社区完成更好的链上治理；全新的TVM指令和ABI类型使智能合约的使用场景更加丰富；全新的加密算法库提高了TRON网络的安全性；Account数据存储、交易验证流程的优化提升了交易处理速度和区块验证速度，从而大幅提高TRON网络的性能；节点启动速度的优化将为用户带来更好的体验，进一步繁荣波场生态。

### 核心协议
#### 1. 账户每天的免费带宽额度可配置

在GreatVoyage-v4.3.0(Bacon)之前的版本中，账户每天的免费带宽额度固定为5000。GreatVoyage-v4.3.0(Bacon)版本增加了#61提案 `FREE_NET_LIMIT`，使免费带宽额度可配置。超级代表和超级合伙人可针对61号提案发起投票请求来修改`FREE_NET_LIMIT`，`FREE_NET_LIMIT`的范围是[0, 100,000]

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-292.md 
* 源代码：https://github.com/tronprotocol/java-tron/pull/3917 

**注意事项**：
账户每天的免费带宽额度，目前仍然是5000，后续将由超级代表或超级合伙人发起相应投票请求来更改其值。

#### 2. 全网通过质押TRX可获得的带宽总额可配置

在GreatVoyage-v4.3.0(Bacon)之前的版本中，全网通过质押TRX可获得的总带宽额度固定为43,200,000,000。
GreatVoyage-v4.3.0(Bacon)版本增加了#62提案`TOTAL_NET_LIMIT`，使全网通过质押TRX可获得的总带宽额度可配置。超级代表和超级合伙人可针对62号提案发起投票请求来修改`TOTAL_NET_LIMIT`，`TOTAL_NET_LIMIT`的范围是[0, 1000,000,000,000]

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-293.md 
* 源代码: https://github.com/tronprotocol/java-tron/pull/3917  

**注意事项**：
全网通过质押TRX可获得的总带宽额度，目前仍然是43,200,000,000，后续将由超级代表或超级合伙人发起相应投票请求来更改其值。

#### 3. 优化Account 数据库存储结构
在节点运行过程中，Account是访问频率非常高的数据库，需要频繁对account数据结构进行反序列化操作，在GreatVoyage-v4.3.0(Bacon)之前的版本中，Account中不仅包含账户的基本数据，还包括用户TRC-10资产数据。但对于TRX转账和智能合约相关交易，一般情况下只使用了Account的基本数据。过大的TRC-10资产列表会对Account数据结构的反序列性能造成极大影响。
GreatVoyage-v4.3.0(Bacon)版本优化了Account数据库的存储结构，将TRC-10资产数据从Account中剥离出来，单独存储在`AccountAssetIssue`中。减少了Account反序列时的数据量，提升了反序列化速度。

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-295.md 
* 源代码：https://github.com/tronprotocol/java-tron/pull/3906 

**注意事项**：
该功能默认处于关闭状态，后续将由超级代表或超级合伙人发起相应投票请求来开启该功能。

### TVM
#### 1. 虚拟机中新增投票指令

在GreatVoyage-v4.3.0(Bacon)之前的版本中，普通账户可以通过给超级代表或超级代表候选人投票来获得出块奖励和投票奖励。但对于智能合约账户，由于TVM不支持投票指令，智能合约账户中的TRX资产无法通过投票获取收益。
GreatVoyage-v4.3.0(Bacon)版本在TVM中引入了投票指令:`VOTE` / `WITHDRAWBALANCE` ，使得智能合约账户也可以给超级代表或超级代表候选人投票以获取收益。

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-271.md 
* 源代码：https://github.com/tronprotocol/java-tron/pull/3921 

**注意事项**：
该功能默认处于关闭状态，后续将由超级代表或超级合伙人发起相应投票请求来开启该功能。

#### 2. 新增ABI类型 `Error`
GreatVoyage-v4.3.0(Bacon)版本引入了新的ABI类型 `Error` , 即自定义错误类型，将兼容以太坊solidity_0.8.4引入的新特性。

* TIP：https://github.com/tronprotocol/tips/blob/master/tip-306.md 
* 源代码：https://github.com/tronprotocol/java-tron/pull/3921 

### API
#### 1. `TransactionExtention`新增`energy_used`字段
在GreatVoyage-v4.3.0(Bacon)之前的版本中，用户无法预知智能合约交易的能量消耗。
GreatVoyage-v4.3.0(Bacon)版本为`TransactionExtention`新增`energy_used`字段，用户通过`TriggerConstantContract`调用合约方法时，将会在当前节点基于其最新同步的区块，构建一个沙盒环境来提供给TVM执行该方法调用，执行完毕后会将实际消耗的能量值设置到`energy_used`字段并返回给用户（该操作不会产生上链交易，也不会改变当前节点的状态）。

* 源代码：https://github.com/tronprotocol/java-tron/pull/3940 

### 其它变更

#### 1. 更新BouncyCastle为加密算法程序库
由于SpongyCastle已经不再被维护，从GreatVoyage-v4.3.0(Bacon)版本开始，采用Bouncy Castle作为加密算法的程序库。

* 源代码：https://github.com/tronprotocol/java-tron/pull/3919 

#### 2. 更新新账户创建时`net_usage`的计算方法
在GreatVoyage-v4.3.0(Bacon)版本中，更新了新账户创建时`net_usage`的计算方法。 
源代码: https://github.com/tronprotocol/java-tron/pull/3917 

#### 3. 优化区块验证
在GreatVoyage-v4.3.0(Bacon)之前的版本中，节点在验证区块时，对于其中的每一个交易来说，无论之前是否已经验证通过，都会被再次验证。而交易验证这个过程占据了整个区块处理的1/3时间。
GreatVoyage-v4.3.0(Bacon)版本优化了区块验证的逻辑，对于区块中的非`AccountUpdateContract`类型的交易(`AccountUpdateContract`交易涉及到账户权限变更)，如果之前已经被验证通过，那么它们将不再被验证，以加快区块验证速度。

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-276.md 
* 源代码: https://github.com/tronprotocol/java-tron/pull/3910 

#### 4. 优化节点启动
GreatVoyage-v4.3.0(Bacon)之前的版本里，在节点启动过程中，会读取数据库中的交易缓存数据和区块数据来完成内存交易缓存的初始化。 在GreatVoyage-v4.3.0(Bacon)版本优化了内存交易缓存的初始化流程，去掉了一些不必要的解析过程， 优化后将提升节点启动的速度。

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-285.md 
* 源代码：https://github.com/tronprotocol/java-tron/pull/3907 

#### 5. 优化交易处理流程降低内存使用
GreatVoyage-v4.3.0(Bacon)版本中，优化了交易处理流程，提前释放了不需要再使用的对象，优化内存使用。

* 源代码： https://github.com/tronprotocol/java-tron/pull/3911 

#### 6. 新增插件优化leveldb的启动性能
在GreatVoyage-v4.3.0(Bacon)之前的版本中，随着levelDB的运行，manifest文件会持续增长，过大的manifest文件不但影响节点启动速度，而且还有可能导致内存持续增长而导致内存不足，服务异常中止。
GreatVoyage-v4.3.0(Bacon)引入了leveldb 启动优化插件，插件优化了manifest的文件大小以及LevelDB的启动过程，减少了内存占用，提升了节点启动速度。

* TIP： https://github.com/tronprotocol/tips/blob/master/tip-298.md 
* 源代码： https://github.com/tronprotocol/java-tron/pull/3925
* 插件使用指南： https://github.com/tronprotocol/documentation-zh/blob/master/docs/developers/archive-manifest.md 

*Knowledge is power.* 
<p align="right"> --- Francis Bacon </p>


## GreatVoyage-4.2.2.1(Epictetus)
GreatVoyage-v4.2.2.1(Epictetus) 版本已发布， 主要新功能和修改如下：

### 核心协议
#### 1、优化`pending transaction`的处理逻辑。

在GreatVoyage-v4.2.2.1(Epictetus) 之前的版本中，如果节点如果开启了事件订阅服务，会有小概率发生节点同步异常的问题。

GreatVoyage-v4.2.2.1(Epictetus) 版本对`pending transaction`的处理逻辑进行了优化，修复了该同步异常的问题，提升了事件订阅服务的稳定性。

- 源代码:  [#3874](https://github.com/tronprotocol/java-tron/pull/3874 )

GreatVoyage-v4.2.2.1(Epictetus) 版本引入的更新优化了`pending transaction`的处理逻辑，将大幅提升事件订阅服务的稳定性，将为TRON用户带来更好的体验，进一步繁荣波场生态。

 --- 
*No great thing is created suddenly.* 
<p align="right"> --- Epictetus</p>


## GreatVoyage-4.2.2(Lucretius)
GreatVoyage-v4.2.2(Lucretius)版本引入了3个重要的优化更新，区块处理的优化有效得提高区块的执行速度，从而大幅提高TRON网络的性能，高效的HTTP/RPC查询和更高性能TVM将为TRON DAPP用户带来更好的体验，进一步繁荣波场生态。
### 核心协议

####1、优化区块处理。

在GreatVoyage-v4.2.2(Lucretius)之前的版本中，区块处理过程中为了获取witness列表，执行了多次数据库查询和反序列化操作，这部分操作占用了近1/3的区块处理时间。

GreatVoyage-v4.2.2(Lucretius)版本简化了witness的查询，区块处理过程只需一次查询即可获取witness列表，经过测试，本次优化大幅提升了区块处理性能。

- TIP： [TIP-269](https://github.com/tronprotocol/tips/blob/master/tip-269.md)
- 源代码:  [#3827](https://github.com/tronprotocol/java-tron/pull/3827)

####2、优化数据查询。

在GreatVoyage-v4.2.2(Lucretius)之前的版本中，多个HTTP或RPC对链上数据的查询是互斥的，如果有查询请求正在处理，新的查询请求会等待之前的请求完成以后才会被处理。

实际上，查询数据的方法中并没有使用到共享数据, 所以并不需要加锁操作。本次优化去除了查询过程中不必要的同步锁，大幅提高了节点内部查询、HTTP和RPC的查询请求性能。

- TIP： [TIP-281](https://github.com/tronprotocol/tips/blob/master/tip-281.md)
- 源代码:  [#3830](https://github.com/tronprotocol/java-tron/pull/3830)


####3、优化智能合约ABI的存储。

在GreatVoyage-v4.2.2(Lucretius)之前的版本中，一个智能合约的ABI数据和这个智能合约的其他数据是一起存储在合约数据库中， TVM的一些高频指令(SLOAD,SSTORE等等)会从合约数据库读取一个智能合约的所有数据，然而合约的执行并不会使用到这些ABI数据，所以频繁的读取会降低这些指令的执行性能。

GreatVoyage-v4.2.2(Lucretius)版本将智能合约的ABI数据从合约数据库中转存到一个专门的ABI数据库中，合约执行过程中将不再读取ABI数据，从而大幅提高TVM的执行性能。

- TIP： [TIP-268](https://github.com/tronprotocol/tips/blob/master/tip-268.md)
- 源代码:  [#3836](https://github.com/tronprotocol/java-tron/pull/3836)

### 其他变更

#### 1、优化系统合约`BatchValidateSign`的初始化流程。

- 源代码:  [#3836](https://github.com/tronprotocol/java-tron/pull/3836)



 --- *Truths kindle light for truths.*
 <p align="right"> --- Lucretius</p>




## GreatVoyage-4.2.0(Plato)
GreatVoyage-4.2.0(Plato)版本引入了2个重要的更新，资源模型的优化将大福提升波场网络资源使用率，使资源获取方式更加合理。全新的TVM指令使智能合约的使用场景更加丰富，将进一步丰富波场生态。

### 核心协议
####1、资源模型优化。

GreatVoyage-4.2.0(Plato)版本之前，用户通过质押TRX获取大额投票权的同时，也获得了大量的能量和带宽，而这部分资源的使用率极低，大多数处于闲置状态，增加了开发者们获取资源的成本，为了提高资源的利用率，GreatVoyage-4.2.0(Plato)版本提出了一种新的资源优化模型，质押TRX只获得带宽，能量，投票权三种资源中的一种，用户可以根据自己的需求获取相应的资源，从而提升资源的利用率。

- TIP： [TIP-207](https://github.com/tronprotocol/tips/blob/master/tip-207.md)
- 源代码:  [#3726](https://github.com/tronprotocol/java-tron/pull/3726)

**注意事项：**
  * 该功能默认处于关闭状态，可通过提案系统开启该。
  * 功能开启后，用户之前已获取的资源保持不变，当用户发送任意一个解冻交易（解冻带宽，能量，或者投票权），提案通过前获取的投票权将被清空。
  
### TVM
#### 1、虚拟机中新增Freeze/Unfreeze 指令。

在波场网络中，普通账户质押TRX可以获取带宽，能量，投票权等资源，合理使用这些资源可以为用户带来一定的收益。与此同时，智能合约账户虽然也拥有TRX，但是却没有办法通过质押TRX获取资源，为了解决这种不一致性，GreatVoyage-4.2.0(Plato)版本在TVM中引入了Freeze/Unfreeze指令，使得智能合约也支持质押TRX获取资源。

- TIP：[TIP-157](https://github.com/tronprotocol/tips/blob/master/tip-157.md)
- 源代码： [#3728](https://github.com/tronprotocol/java-tron/pull/3728)

**注意事项：**
  * 该功能默认处于关闭状态，可通过提案系统开启该。
  * TVM的质押指令目前可以获取带宽和能量，对于投票权，需要在TVM支持投票指令以后才可以获取并使用。
  * Freeze/Unfreeze指令中的接收地址/目标地址都必须是`address payable` 类型，且接收地址/目标地址不能是合约地址（合约自身地址除外）。
  * 如果调用合约给未激活地址代理资源会自动激活目标账户，同时额外扣除25,000能量作为账户激活成本。

### 其他变更
#### 1、优化区块同步逻辑

- 源代码：[#3732](https://github.com/tronprotocol/java-tron/pull/3732)




--- 
*The beginning is the most important part of the work.* 
<p align="right"> --- Plato</p>



## GreatVoyage-4.1.3(Thales)
GreatVoyage-4.1.3(Thales)版本主要有以下新功能和修改：

### 核心协议
#### 1.对待打包的交易进行排序，SR优先打包费用较高的交易
在GreatVoyage-4.1.2及之前版本中，SR打包交易是按照交易到达的时间顺序进行的，这很容易受到低交易费用的攻击。

本次优化后，出块节点根据费用对待打包的交易进行排序，然后优先打包费用较高的交易， 防止低交易费用攻击。

### API
#### 1.新增查询待打包交易列表相关接口
在GreatVoyage-4.1.2及之前版本中, SR打包交易是按照交易到达的时间顺序进行的，这很容易受到低交易费用的攻击。本次升级后, Fullnode节点提供3个接口来获取待打包交易列表的详细信息：

- /wallet/gettransactionfrompending ：通过交易ID从待打包交易列表中获取完整的交易信息
- /wallet/gettransactionlistfrompending ：从待打包交易列表中获取所有交易
- /wallet/getpendingsize ：获取当前待打包交易的数量
  

   
  



Great Voyage-v4.1.3 (Thales) 版本的交易打包逻辑的优化将有效减少低费用攻击，极大提升TRON公链的安全性。



## Great Voyage - v4.1.2
GreatVoyage-4.1.2版本发布， 本次升级主要有以下新功能和修改：

### 一、核心协议
####1、将燃烧带宽/燃烧能量（OUT_OF_TIME除外）的手续费转为SR产块奖励。

该功能开启后，燃烧带宽/燃烧能量（OUT_OF_TIME除外）的手续费将转入到TRANSACTION_FEE_POOL，在块中所有交易处理完成后，按照SR设定的比例转发给当前产块SR及该SR的投票者。同时在transactioninfo中，增加packingFee字段，用于表示当前产块SR和该SR的投票者可获取的费用。

- TIP：[TIP-196](https://github.com/tronprotocol/tips/issues/196)
- 源代码:  [#3532](https://github.com/tronprotocol/java-tron/pull/3532)

#### 2、新增账户历史余额查询功能。

账户历史余额查询功能可以方便开发者查询账户在特定区块高度的余额信息，开发者可以通过以下两个API获取到账户的历史余额信息。

- /wallet/getaccountbalance ：获取账户在特定区块高度的余额
- /wallet/getblockbalance ： 获取区块内交易账户的余额变化

**注意事项：**
1. 该功能默认处于关闭状态，可通过节点配置文件启用该功能。
2. 该功能启用之后只能查询启用时间之后的历史余额， 如果需要查询完整历史余额信息，可使用包含历史余额信息的数据快照重新同步节点。

- 源代码：[#3538](https://github.com/tronprotocol/java-tron/pull/3538)
- 使用教程： https://github.com/tronprotocol/documentation-zh/blob/master/docs/api/http.md

####3、黑洞账户优化。

功能开启之后，燃烧带宽和燃烧能量的TRX手续费将不再转给黑洞地址，直接记录到数据库中。

- 源代码： [#3617](https://github.com/tronprotocol/java-tron/pull/3617)

###二、TVM
####1、对以太坊solidity0.6.0特性进行兼容

本次升级之后TRON将完全兼容solidity0.6.0引入的新特性， 包括新增 virtual、override 关键字，支持try/catch等。详细内容请参看TRON Solidity release note：https://github.com/tronprotocol/solidity/releases/tag/tv_0.6.0

- TIP:  [TIP-209](https://github.com/tronprotocol/tips/issues/209)
- 源代码： [#3351](https://github.com/tronprotocol/java-tron/pull/3535)

####2、将MAX_FEE_LIMIT变更为可配置项。

新版本之后，超级代表和超级合伙人可针对47号提案发起投票请求来修改MAX_FEE_LIMIT， MAX_FEE_LIMIT的范围是[0,10000_000_000].

- TIP： [TIP-204](https://github.com/tronprotocol/tips/issues/204) 
- 源代码：  [#3534](https://github.com/tronprotocol/java-tron/pull/3534)
  
###三、其他变更
####1、使用jitpack仓库提供依赖支持，方便开发者的项目使用 java-tron 作为依赖。
- 源代码： [#3554](https://github.com/tronprotocol/java-tron/pull/3554)





## GreatVoyage-v4.1.1
GreatVoyage-4.1.1版本发布， 本次升级主要有以下新功能和修改：

### 核心协议
#### 新的共识协议
新的共识机制将波场现有的DPOS共识同PBFT共识机制进行结合，在区块固化阶段采用PBFT的三阶段投票机制进行确认。波场区块从生产出来到固化确认的时间将从原来的19个区块时间（1个区块时间为3s）缩短至平均1～2个区块时间，区块确认速度大幅提升。
- TIP: [TICP-Optimized-PBFT](https://github.com/tronprotocol/tips/blob/master/tp/ticp/ticp-optimized-pbft/ticp-Optimized-PBFT.md) 
- 源代码: [#3082](https://github.com/tronprotocol/java-tron/pull/3082) 

#### 新的节点类型
在现有FullNode的基础上新增了一种节点类型：Lite FullNode。Lite FullNode和普通的FullNode运行同样的代码，所不同的是Lite FullNode是基于状态数据快照进行启动，状态数据快照包含所有的状态数据和最近的256个区块的历史数据。
状态数据快照可以通过执行LiteFullNodeTool.jar进行获得（请参考：[如何使用LiteFullNode Tool](https://tronprotocol.github.io/documentation-zh/developers/litefullnode/)）。
- TIP: [TIP-128](https://github.com/tronprotocol/tips/blob/master/tip-128.md) 
- 源代码: [#3031](https://github.com/tronprotocol/java-tron/pull/3031) 

### TVM
#### 对以太坊的伊斯坦布尔升级进行兼容
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

### 机制
1、增加了两个新的系统合约MarketSellAssetContract和MarketCancelOrderContract用于支持TRX、TRC10资产在链上去中心化交易所进行交易。
- TIP: [TIP-127](https://github.com/tronprotocol/tips/blob/master/tip-127.md)
- 源代码: [#3302](https://github.com/tronprotocol/java-tron/pull/3302) 

### 其他变更
1、增加了多个节点性能指标数据。
- 源代码: [#3350](https://github.com/tronprotocol/java-tron/pull/3350) 

2、在原有的transactionInfo接口中增加了市场订单详情的信息。
- TIP: [TIP-127](https://github.com/tronprotocol/tips/blob/master/tip-127.md) 
- 源代码: [#3302](https://github.com/tronprotocol/java-tron/pull/3302)

3、优化了docker部署脚本
- 源代码： [#3330](https://github.com/tronprotocol/java-tron/pull/3330)




## GreatVoyage-v4.0.0


4.0 版已实现匿名 TRC20 合约，可以隐藏源地址、目标地址和 TRC20 代币交易数额，并为用户提供更好的隐私性。 匿名 TRC20 合约包含三种类型的交易：

  * 公开地址到匿名地址交易(mint)： t-addr到z-addr的交易。“t-addr”的信息是公开的，“z-addr”的信息是隐藏的。
  * 完全匿名交易(transfer)： z-addr到z-addr的交易，发送方和接收方的地址和交易金额都被隐藏。
  * 匿名地址到公开地址交易(burn)： z-addr到t-addr的交易，z-addr的信息是隐藏的，t-addr的信息是公开的。

为支持匿名 TRC20 合约，TVM 中添加了四个新零知识指令（`verifyMintProof`, `verifyTransferProof`, `verifyBurnProof`  及  `pedersenHash`），可以为任意 TRC20 合约提供隐私保护。

### 注意
该版本为强制升级

### 新功能
 - 在 TVM 中添加 4 项新指令（`verifyMintProof`, `verifyTransferProof`, `verifyBurnProof` 和 `pedersenHash`）以支持基于零知识证明的TRC20 匿名交易（#3172）。
   - `verifyMintProof`: 用于验证 mint 函数的零知识证明。
   - `verifyTransferProof`: 用于验证 transfer 函数的零知识证明。
   - `verifyBurnProof`: 用于验证 burn 函数的零知识证明。
   - `pedersenHash`: 用于计算 Pedersen 哈希。
- 更新由 MPC 火炬计划生成的零知识证明方案的初始参数（#3210）。
- 添加 API 以支持匿名 TRC20 合约交易（#3172）。
  
   1.&nbsp;Create shielded contract parameters
  ```protobuf
  rpc CreateShieldedContractParameters (PrivateShieldedTRC20Parameters) returns (ShieldedTRC20Parameters) {}
  ```
  2.&nbsp;Create shielded contract parameters without ask
  ```protobuf
  rpc CreateShieldedContractParametersWithoutAsk (PrivateShieldedTRC20ParametersWithoutAsk) returns (ShieldedTRC20Parameters) {}
  ```
  3.&nbsp;Scan shielded TRC20 notes by ivk
  ```protobuf
  rpc ScanShieldedTRC20NotesByIvk (IvkDecryptTRC20Parameters) returns (DecryptNotesTRC20) {}
  ```
  4.&nbsp;Scan shielded TRC20 notes by ovk
  ```protobuf
  rpc ScanShieldedTRC20NotesByOvk (OvkDecryptTRC20Parameters) returns (DecryptNotesTRC20) {}
  ```
  5.&nbsp;Check if the shielded TRC20 note is spent
  ```protobuf
  rpc IsShieldedTRC20ContractNoteSpent (NfTRC20Parameters) returns (NullifierResult) {}
  ```
  6.&nbsp;Get the trigger input for the shielded TRC20 contract
  ```protobuf
    rpc GetTriggerInputForShieldedTRC20Contract (ShieldedTRC20TriggerContractParameters) returns (BytesMessage) {}
  ```
- 支持 `ovk` 扫描 burn 交易的输出（#3203）。
- 支持有 0 或 1 个匿名输出的 `burn` 交易（#3224）。
- 在事件日志触发器添加数据字段，可用于备注（#3200）。

此版本中实现了以下 TIP：
- [TIP-135](https://github.com/tronprotocol/tips/blob/master/tip-135.md): 匿名 TRC20 合约标准，保证 TRC20 代币匿名转账的隐私性。
- [TIP-137](https://github.com/tronprotocol/tips/blob/master/tip-137.md): 在波场虚拟机中实现三个零知识证明指令，以支持匿名 TRC-20合约（#3172）。

- [TIP-138](https://github.com/tronprotocol/tips/blob/master/tip-138.md): 在波场虚拟机中实现 Pedersen 哈希计算指令，以支持匿名TRC-20合约（#3172）。
 
### 更新
- 修复从 DB 获取交易信息时 `getTransactioninfoByBlkNum`异常，增加检查 getInstance 是否为空值（#3165）。



## Odyssey-v3.7
奥德赛 3.7 版本为非强制升级，包含以下新功能和改进。

### 模块化
奥德赛 3.7 进行了代码组织结构的模块化工作，方便开发者对模块进行自定义开发。几个主要模块如下：

#### 框架
作为核心模块，框架模块既是区块链的入口，也将其他所有模块紧密地连接在一起。换言之，框架模块负责各个模块的初始化和模块之间的通信。

#### 协议
去中心化波场协议可由任何团队实现，不受编程语言限制。所有遵循波场协议的客户端都能相互通信。
简洁高效的数据传输协议对分布式网络来说至关重要，对区块链而言则更甚。因此，该协议是基于谷歌（Google）的优质开源软件协议 Protocol Buffers 实现的。 
协议所定义的区块链具体业务逻辑包括：
- 消息的数据格式，包括区块、交易、提议、见证人、投票、账户、交易所等等。
- 区块链节点间的通信协议，包括节点发现协议、节点数据同步协议、节点打分协议等。
- 区块链为外部系统或客户端提供的接口协议。

#### 共识 
共识机制是区块链的重要组成部分。波场区块链采用 DPoS 作为核心共识机制，长期以来运行稳定。但是，要想将 Java-tron 改造成为强大的基础设施，支持搭建用于实际应用场景的区块链，我们就必须为其装备可替换的共识模块。 区块链开发者应选取最适合具体应用情景的共识机制。利用可替换的共识模块，我们的终极目标是使共识机制可以通过设置一些必要参数来决定。除此之外，只要实现几个必要的接口，开发者即可自定义共识模块。


#### 加密
作为区块链的核心模块之一，加密是区块链数据安全的基础， 应用于公钥和私钥的推论、交易验证和零知识证明等。Java-tron 对加密模块进行了抽象化，并支持替换加密算法，可以根据不同的业务需求选择合适的加密算法。

#### 执行器
执行器是用于处理各种交易的核心模块。众所周知，波场区块链上的每一笔交易都包含一个合约。总体而言，波场区块链共有两种合约：系统合约和智能合约。大量应用程序通过智能合约实现，在区块链的内部虚拟机中运行。然而，智能合约在功能性和灵活性方面仍受限制，无法满足复杂应用程序的要求。自定义的执行器则为应用程序开发者提供了一种全新的开发方式。他们可以选择将应用程序的代码植入链内，而不用在虚拟机上运行。

#### 内存数据库 
内存数据库专为区块链数据储存而设计。节点始终认为最长链是正确的区块链，并会持续将其延长。除非采用类似 PBFT 的确定性共识算法，目前区块链领域的常见做法是切换到最长链。因此，支持数据回滚是内存数据库模块最突出的功能。该模块中定义了几个设计精细的抽象接口，开发者可以自由选择存储引擎，实现对应的接口。现有的两个实现方案是 LevelDB 和 RocksDB。

### 固化块的新事件订阅触发器
添加了用于更新固化块的订阅触发器，该触发器触发了固化块更新事件到消息队列，以便用户可以及时获取最新的固化块信息。固化块是指不可撤销的区块。所以，当一个区块变成固化块后，打包在该区块内的交易即被区块链接受。

### 新增两个HTTP API
**gettransactioninfobyblocknum**

此 API 已添加到 /wallet 和 /walletsolidity 中

* 描述：查询特定区块内的交易信息列表。
* 参数 num：区块高度。
* 返回：交易信息列表。

**broadcasthex**

/wallet/broadcasthex
 
* 描述：广播十六进制字符串格式的签名交易
* 参数：十六进制字符串格式的签名交易
* 返回：广播结果

### 新增一个 RPC 接口

在`Wallet` `WalletSolidity` 服务中添加 `GetTransactionInfoByBlockNum` 方法
```
rpc GetTransactionInfoByBlockNum (NumberMessage) returns (TransactionInfoList) { 
}
```
代码片段：
```
NumberMessage.Builder builder = NumberMessage.newBuilder(); 
builder.setNum(blockNum); 
TransactionInfoList transactionInfoList = blockingStubFull.getTransactionInfoByBlockNum(builder.build()); 
```


## Odyssey-v3.6.5
本次奥德赛v3.6.5升级主要有以下新功能和修改：

###1、新的抵押机制 

新的抵押机制提供了为SR设置佣金的功能，SR可以自行设置佣金比例，这样用户在为SR投票时可以进行参考，同时SR的佣金比例可以在链上进行查询，将使用户获得的投票奖励数额更加透明。另外，新的抵押机制为下一步进行更加复杂的共识机制和激励计划提供了实现基础。

###2、更加公平高效的股权分红机制

股权收益的分发从原来的部分去中心化方式变为完全去中心化的方式。一方面，股权收益的分发完全在区块链上进行，完全保证分发过程受到链的监督，是完全去中心化的；另一方面，减少了不必要的股权分红交易，从而减少了带宽消耗，波场网络的运行将更有效率。

###3、更加合理的激励机制

出块奖励从原来的32TRX调整为16TRX，投票奖励从原来的16TRX提升为160TRX，这样大大促进了社区用户参与投票的热情，增加波场生态用户的锁仓率。同时结合新的股权分红机制，保证用户能够切实收到股权收益。

###4、虚拟机TVM的改进和优化

（1）增加新的虚拟机指令 ISCONTRACT(0xd4) 新指令让开发者在编写合约可以从虚拟机层面更加灵活的判断目标地址类型，提升了智能合约开发的灵活性。
（2）将虚拟机验证签名的方式修改为多线程的方式，相比于以太坊的ecrecover速度更快，同时能量消耗仅为ecrecover的一半。
合约地址: 0x09, solidity内使用方式：batchvalidatesign(bytes32 hash, bytes[] memory signatures, address[] memory addresses) 
（3）增加了一条新的预编译合约，用于支持在虚拟机中进行多重验签的特性，加快验签速度, 同时降低能量消耗。
合约地址: 0x0a, solidity内使用方式： validatemultisign(address accountAddress, uint256 permissionId, bytes32 content, bytes[] signatures)
（4）禁止通过系统合约转账到TransferContract和TransferAssetContract向智能合约地址进行转账，当使用TransferContract和TransferAssetContract以上两个合约进行进行转账时，如目标地址为合约地址，转账将不成功。这可以防止普通用户误操作将资产转移到到智能合约地址，从而避免给造成用户资产的丢失
（5）在智能合约里向账户转账trx /trc10时, 如果该账户尚未激活，支持先自动激活然后转账。
（6）为SolidityNode和FullNode增加了triggerConstantContract功能，完善和丰富了节点API的功能性。

###5、完善能量上限动态调整机制

将单位时间内能量的消耗统计方式由只统计质押的能量消耗调整为统计所有能量的消耗。这样统计的能量消耗数据更加精确有效，为能量上限的调整提供依据，有利于降低用户使用波场区块链网络的成本，提高波场网络的效率。

