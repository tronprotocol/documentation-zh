#GreatVoyage-v4.7.1(Sartre)

GreatVoyage-v4.7.1(Sartre)版本引入了多个重要的优化和更新，优化的区块同步逻辑，提高了区块同步的稳定性；优化的节点IP设置，提高了节点的可用性；优化的节点日志模块，提高节点的可维护性。

下面是详细介绍。


## 核心协议
### 1. 优化节点IP设置
节点启动时会获取节点的本地IP, 然后利用该IP与网路中的其他节点进行通信。如果节点无法访问外网，则将无法获取到本地IP，这时节点会将其本地IP设置为默认值0.0.0.0，而全0地址将使得节点无法与局域网内的其他节点正常通信，GreatVoyage-v4.7.1(Sartre)版本更改了节点默认IP，如果节点无法获取本地IP， 会将其本地IP设置为127.0.0.1，使得节点即便在没有连接外网的情况下，依然可以和局域网内的其它节点正常通信。

源代码：[https://github.com/tronprotocol/java-tron/pull/4990](https://github.com/tronprotocol/java-tron/pull/4990)  

### 2. 优化区块同步逻辑 
在区块同步过程中，节点会维护一个区块请求列表，包含了已经向其他节点发送请求的所有区块的ID。当本节点和节点A连接极小概率异常断开时，会将向节点A正在请求的区块ID从请求列表中删除，此后节点会认为自己并没有请求过该区块，然后重新向节点B请求该区块，并将区块ID再次加入到请求列表中。而本节点在和节点A的连接断开之前，可能节点A已经向本节点发送了区块，断开连接后收到了该区块，由于发现是来自已断开节点A的区块，会丢弃该区块并将区块ID从请求列表中再次删除，导致本节点将再一次向节点B发送相同区块的请求。而当节点B收到重复的区块请求时，会认为是非法报文，断开与本节点的连接。

为了提高在并发场景下区块同步的效率，GreatVoyage-v4.7.1(Sartre)版本优化了区块请求列表的更新机制，列表中同时保存区块ID和节点信息，上述场景中，收到来自于已断开节点A区块后，将不会把向节点B请求的同一个区块ID从请求列表中删除，确保不会与节点B断开连接，从而提升区块同步的稳定性。


源代码：[https://github.com/tronprotocol/java-tron/pull/4995](https://github.com/tronprotocol/java-tron/pull/4995) 

节点在向其他节点同步区块时，需要获取本节点的区块状态摘要，状态摘要中包含本地头块在内的若干个区块的ID。在GreatVoyage-v4.7.1(Sartre)之前的版本中，获取状态摘要时，首先查询Dynamic数据库以获取区块高度，然后根据区块高度查询Block数据库以获取区块的ID。而由于节点在处理区块时，对各个数据库的写入不是同时进行的，节点会首先更新Dynamic数据库，然后再更新Block等其它数据库，同时由于状态摘要获取的线程和区块处理的线程是并发执行的，从而导致在GreatVoyage-v4.7.1(Sartre)之前的版本中，极小概率会出现最新的区块信息只写入了Dynamic数据库中，但还未来得及写入到区块数据库，即开始读取状态摘要，那么根据Dynamic库中的头块高度在区块数据库将找不到对应的区块ID，使得状态摘要读取失败。GreatVoyage-v4.7.1(Sartre)版本优化了链摘要获取逻辑，头块的ID直接从Dynamic数据库获取，不再从Block数据库获取，提高了状态摘要读取的稳定性。


源代码：[https://github.com/tronprotocol/java-tron/pull/5009](https://github.com/tronprotocol/java-tron/pull/5009) 

GreatVoyage-v4.7.1(Sartre)版本优化了区块同步时的锁机制，提升了节点在高并发的情况下连接的稳定性。

源代码：[https://github.com/tronprotocol/java-tron/pull/4996](https://github.com/tronprotocol/java-tron/pull/4996) 

## API
### 1. 优化固化块API列表
GreatVoyage-v4.7.1(Sartre)版本删除了无用的固化块查询API，使代码更加清晰。


源代码：[https://github.com/tronprotocol/java-tron/pull/4997](https://github.com/tronprotocol/java-tron/pull/4997) 

### 2. 优化资源代理关系查询API
GreatVoyage-v4.7.1(Sartre)版本优化了资源代理关系查询API，增加了对接口参数的检验，使接口更加稳定。


## 其它变更


### 1. 优化轻节点检测逻辑
在GreatVoyage-v4.7.1(Sartre)之前的版本，节点的不同模块检测当前节点是否为轻节点的逻辑是不一样的，GreatVoyage-v4.7.1(Sartre)版本统一了轻节点判断逻辑，使代码更加简洁。


源代码：[https://github.com/tronprotocol/java-tron/pull/4986](https://github.com/tronprotocol/java-tron/pull/4986) 


### 2. 优化数据库日志输出

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
