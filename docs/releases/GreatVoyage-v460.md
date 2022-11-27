# GreatVoyage-v4.6.0(Socrates)

GreatVoyage-v4.6.0(Socrates)版本引入了多个重要的优化和更新，优化的数据库检查点机制，提高了节点运行的稳定性；优化的资源代理关系存储结构，以及新的投票奖励计算模型，加快了交易的执行速度，提高了网络吞吐量；增加备注收费的提案，提高带备注交易的成本来减少低价值交易的数量，提升波场网络的安全性和可靠性。集成的toolkit工具包、新增的网络相关prometheus指标、新增的help命令行选项，为用户带来更便捷的开发体验。

下面是详细介绍。



## 核心协议
### 1.  优化资源代理关系的存储结构
TRON网络中，账户可以通过质押将资源代理给其它账户，也可以接受其它账户为自己的资源代理，因此，每个账户都需要维护一个代理关系的记录，包含该账户代理出去的所有账户地址，和为自己代理资源的所有账户地址。

在GreatVoyage-v4.6.0(Socrates)之前的版本中，代理关系以列表的形式存储，当执行资源代理操作时，需要首先在列表中查找是否已经存在该代理账户，如果已经存在，则不需要添加到列表，只有当不存在时才将地址添加到列表中。如果某账户给多个其它账户代理了资源或者多个其它账户为自己代理了资源，那么该账户中的代理关系列表的长度将非常大，当执行涉及该账户的资源代理交易时，对列表的查找操作将非常耗时，导致交易执行时间很长。因此，GreatVoyage-v4.6.0(Socrates)版本优化了资源代理关系的存储结构，将代理关系存储结构从数组改为键值对，以实现在常量时间内完成对其数据的读取和更改，极大的加快了代理相关交易的执行速度，提高网络吞吐量。

资源代理存储结构优化是TRON网络中的一个动态参数，GreatVoyage-v4.6.0(Socrates)部署之后默认为关闭状态，可以通过发起提案投票的方式开启。


* TIP: [https://github.com/tronprotocol/tips/issues/476](https://github.com/tronprotocol/tips/issues/476) 
* 源代码：[https://github.com/tronprotocol/java-tron/pull/4788](https://github.com/tronprotocol/java-tron/pull/4788) 
### 2. 交易备注收费
从GreatVoyage-v4.6.0(Socrates)版本开始，将对交易中的备注收取额外的费用，备注收费将提高带备注交易的成本，减少低价值交易的数量，提升波场网络的安全性和可靠性。

备注费用是TRON网络的一个动态参数，GreatVoyage-v4.6.0(Socrates)部署之后默认为0，单位是 sun， 可以通过发起提案投票指定一个非0值来开启，例如设置为1000000， 表示带备注的交易需要额外消耗1 TRX费用。


* TIP: [https://github.com/tronprotocol/tips/issues/387](https://github.com/tronprotocol/tips/issues/387) 
* 源代码：[https://github.com/tronprotocol/java-tron/pull/4758](https://github.com/tronprotocol/java-tron/pull/4758) 

### 3. 优化投票奖励计算算法
TRON网络中很多选民会累积很长时间的奖励再进行提取，两次提取奖励之间的间隔很长，在GreatVoyage-v4.6.0(Socrates)之前的版本中，如果用户提交了提取奖励的交易， 该交易会依次计算并累加距离上一次提取奖励之间的每一个维护期获得奖励，所以距离上次一次提取奖励的时间越长，本次提取奖励的交易执行越耗时。因此，GreatVoyage-v4.6.0(Socrates)版本优化了投票奖励计算方法，不再累加每个维护期的奖励，而是将上一个维护期记录的奖励总数减去上一次提取奖励交易所在维护期记录的奖励总和，就可以得到未提取的奖励总和。该方法实现了常量时间内计算出未提取的奖励总数，极大的提高了计算效率，加快了奖励计算相关交易的执行速度，从而提升网络的吞吐量。


投票奖励算法的优化是TRON网络的一个动态参数，GreatVoyage-v4.6.0(Socrates)部署之后默认是关闭状态，可以通过发起提案投票的方式开启。

* TIP: [https://github.com/tronprotocol/tips/issues/465](https://github.com/tronprotocol/tips/issues/465) 
* 源代码：  [https://github.com/tronprotocol/java-tron/pull/4694](https://github.com/tronprotocol/java-tron/pull/4694) 

### 4. 升级数据库模块中的Checkpoint机制
Checkpoint机制是为了防止节点宕机引起数据库损坏而建立的恢复机制，Java-tron采用内存和多磁盘数据库的方式进行数据存储，固化的区块数据会保存在多个业务数据库中。未被固化的数据保存在内存中，当一个区块被固化后，会将相应的内存数据写入到多个业务数据库，但由于多个业务数据库的写入并非原子操作，此时节点由于某种原因意外宕机，那么该区块的数据会无法完成全部落盘，导致节点会因为数据库损坏而无法重启。

所以在内存数据写入磁盘之前，先创建Checkpoint检查点，检查点中包含本次需要写入到各个业务数据库的所有数据， 完成检查点创建后，先将检查点数据落盘到一个独立的Checkpoint数据库，然后执行业务数据库落盘操作，Checkpoint数据库始终保留一个最新的固化块数据。如果业务数据库因宕机而损坏，节点重启后会通过之前保存在checkpoint中的区块数据来修复业务数据库。

目前Checkpoint机制可以应对绝多数多宕机的情况，但业务数据库仍然有小概率会因为宕机损坏。目前LevelDB的数据写入均是异步方式, 程序调用LevelDB请求将数据写入磁盘，实际上数据只是被写入到操作系统的高速缓冲中，之后操作系统会根据自己的策略决定真正写入到磁盘的时机。当Java-tron节点完成Checkpoint数据库写入，继续写入业务数据库时，此时发生意外宕机，有可能写入到Checkpoint数据库的数据并没有被操作系统真正写入磁盘，这种情况下，节点会因为Checkpoint数据库没有恢复数据而无法重启。

为了解决这一问题，GreatVoyage-v4.6.0(Socrates)版本增加了V2版本的Checkpoint实现，新的Checkpoint机制会存储多个已固化的区块数据，即便最新的固化块数据因为宕机没有被成功写入到Checkpoint数据库，节点重新后也可以拿历史固化块数据来恢复业务数据库。

配置文件中默认关闭了V2版本Checkpoint机制， 可通过修改配置来开启该功能，需要注意的是已经开启了V2版本的节点运行一段时间后，将无法重新设置回V1版本的Checkpoint机制。


* TIP: [https://github.com/tronprotocol/tips/issues/461](https://github.com/tronprotocol/tips/issues/461) 
* 源代码:  [https://github.com/tronprotocol/java-tron/pull/4614](https://github.com/tronprotocol/java-tron/pull/4614) 
### 5. 优化超级代表主备节点区块生产的优先级
如果超级代表部署了主备节点，主备节点之间会保持连接，当主备节点因网络问题导致短暂性断连时，备用节点会认为主节点失效而参与区块生产，这种情况下会出现主备节点同时出块的情况，在GreatVoyage-v4.6.0(Socrates)之前的版本中，当主备节点收到了对方所产生的相同高度的区块时，各自都会暂停1-9个产块周期，也就是该超级代表会丢1-9个区块。

GreatVoyage-v4.6.0(Socrates)版本优化了主备节点产块的优先级，在上述情况中，当主备节点收到了对方所产生的相同高度的区块时，会比较自己生产区块的hash与对方生产区块的hash值。如果自己的hash更大，会继续产块。如果自己的hash更小，会暂停一个产块周期，之后会继续产块，再次进行区块hash比较， 总共27个超级代表顺序出块，所以跳过一个产块周期需要等待81秒，再此期间，如果主备节点之间的是因为网络短暂不佳，会有足够的时间恢复。另外其他节点收到这两个区块后也会选择hash较大的区块，丢弃hash较小的区块，因此该优化将大幅提高超级代表在主备节点之间网络通信不佳情况下的区块生产效率，提升网络的稳定性。

* 源代码：[https://github.com/tronprotocol/java-tron/pull/4630](https://github.com/tronprotocol/java-tron/pull/4630) 

### 6 优化P2P网络模块的Kademlia算法
Java-tron节点ID是个随机数，每次节点启动都会重新生成，Java-tron的Kademlia算法实现中，会根据节点ID来计算该节点的距离， 然后再根据距离决定将该节点信息放在哪个K桶中。如果K桶中的节点由于某种原因重新启动，节点ID会发生变化，当检测到该节点再次下线，根据最新的节点ID计算的距离，已经无法定位到K桶的位置，导致无法在K桶中删除该节点。这种重启的节点过多，会导致节点K桶中存储了过多无效数据。

因此，GreatVoyage-v4.6.0(Socrates)版本优化了Kademlia算法，并采用Hash表来记录已经发现的节点。节点的距离只有在第一次写入K桶的时候计算一次，并赋值给节点的distance字段，然后将节点加入到哈希表中，以后直接通过该字段获取节点距离，即便节点重启后ID发生改变也不会更新Hash表中该节点的距离。当探测到该节点下线后，可以根据节点ip从hash表里找到对应的节点，然后通过节点distance字段获取到该节点的距离，然后从K桶中删除该节点。

* 源代码：[https://github.com/tronprotocol/java-tron/pull/4620](https://github.com/tronprotocol/java-tron/pull/4620) [https://github.com/tronprotocol/java-tron/pull/4622](https://github.com/tronprotocol/java-tron/pull/4622) 


## 其它变更
### 1. 集成ArchiveManifest.jar到Toolkit.jar工具包

ArchiveManifest.jar是一个独立的LevelDB启动优化工具， 可以优化 LevelDB manifest的文件大小，从而减少内存占用，大幅提升节点启动速度。从 GreatVoyage-v4.6.0(Socrates)版本开始，将ArchiveManifest.jar工具集成到了Toolkit.jar工具中，未来Java-tron周边的工具将逐步都集成到Toolkit.jar工具箱中，以便于工具维护和开发者使用。

* 源代码: [https://github.com/tronprotocol/java-tron/pull/4603](https://github.com/tronprotocol/java-tron/pull/4603)   



### 2. 新增网络模块相关Prometheus指标
GreatVoyage-v4.6.0(Socrates)版本新增了三个网络模块相关的prometheus指标：区块获取延迟、区块接收延迟和消息处理延迟。新的指标有助于节点网络健康监控。

* 源代码：[https://github.com/tronprotocol/java-tron/pull/4626](https://github.com/tronprotocol/java-tron/pull/4626) 

### 3. 新增help命令行选项
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


### 4. 优化轻节点工具

LiteFullNodeTool.jar是java-tron的轻节点工具， 主要功能是将全节点数据库转化为轻节点数据库，GreatVoyage-v4.6.0(Socrates)版本优化了该工具，提升了工具的便捷性和稳定性。


* 源代码：[https://github.com/tronprotocol/java-tron/pull/4607](https://github.com/tronprotocol/java-tron/pull/4607)


### 5. 优化eth_getBlockByHash和eth_getBlockByNumber 接口的返回值
为了更好地兼容Ethereum的JsonRPC 2.0协议接口，GreatVoyage-v4.6.0(Socrates)版本将eth_getBlockByHash和eth_getBlockByNumber 接口返回值中`timestamp`字段的单位从毫秒改为秒， 使接口返回值格式与Ethereum Geth完全兼容。

* 源代码：[https://github.com/tronprotocol/java-tron/pull/4642](https://github.com/tronprotocol/java-tron/pull/4642) 

--- 

*To move the world we must move ourselves.* 
<p align="right"> --- Socrates</p>
