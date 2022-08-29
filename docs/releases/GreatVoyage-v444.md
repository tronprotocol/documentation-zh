# GreatVoyage-4.4.4(Plotinus)
GreatVoyage-v4.4.4(Plotinus)版本引入多个重要的优化更新，降低了节点对内存的占用；加快了节点启动速度；优化的网络服务、产块线程，提升了节点的稳定性；改进的版本升级机制，实现了更高效的分散治理；TVM支持多版本程序执行器，使其更好的兼容EVM，为用户带来更便捷的开发体验，有助于进一步繁荣波场生态。


# 核心协议

## 1. 优化节点启动时间
GreatVoyage-v4.4.4(Plotinus)之前的版本，节点从启动到区块同步，需要执行约一分钟左右，区块同步线程首先会延迟30s来等待P2P线程发现其他远端节点， 然后与发现的节点建立TCP链接，最后进行区块同步，而这段延迟时间占据了大部分的启动时间。实际上每一次新发现的节点都会被持久化到本地，所以第二次节点启动时无需花额外时间去等待节点发现，完全可以使用之前持久化到本地的节点进行TCP连接, 因此从GreatVoyage-v4.4.4(Plotinus)版本开始，将等待节点发现的时间从30s降低到100ms, 以提升节点启动的速度。


TIP: https://github.com/tronprotocol/tips/blob/master/tip-366.md 
源代码: https://github.com/tronprotocol/java-tron/pull/4254  


## 2. 优化内存使用
节点在广播交易时，为了避免重复广播，会将相应的交易存储到广播数据缓存池中, 但是由于JVM的回收策略限制，旧的缓存数据不能被及时删除，直至缓存池被占满才会触发旧数据回收，因此，容量较大的缓存池将极大的占用内存。在GreatVoyage-v4.4.4(Plotinus)之前的版本中，交易缓存池大小为100000笔。为了及时释放过期交易所占内存，GreatVoyage-v4.4.4(Plotinus)版本将交易缓存池大小更改为20000笔，以减少内存占用。

TIP: https://github.com/tronprotocol/tips/blob/master/tip-362.md 
源代码: https://github.com/tronprotocol/java-tron/pull/4250 


## 3. 优化产块线程
GreatVoyage-v4.4.4(Plotinus)版本的产块线程，增加了对中断异常的处理，使出块节点捕获到中断指令时，节点能够安全退出。

源代码：https://github.com/tronprotocol/java-tron/pull/4219 

# TVM
## 1. TVM支持多版本程序执行器
为了使TRON网络未来能够支持多种类型的智能合约交易，GreatVoyage-v4.4.4(Plotinus)将TVM代码进行了重构，能够支持根据智能合约的版本信息，选择其对应的指令集来解释执行该版本的智能合约的字节码。

源代码：https://github.com/tronprotocol/java-tron/pull/4257 
                 https://github.com/tronprotocol/java-tron/pull/4259 


# 其它变更
## 1. 优化节点日志存储
GreatVoyage-v4.4.4(Plotinus)版本修改了节点日志保留的时间，从3天增加到7天，以方便用户排查问题。

源代码：https://github.com/tronprotocol/java-tron/pull/4245 



## 2. 优化网络服务关闭逻辑
GreatVoyage-v4.4.4(Plotinus)版本优化了网络服务关闭逻辑，先关闭同步服务，再关闭TCP连接服务，以确保所有P2P连接相关服务安全退出。

源代码：https://github.com/tronprotocol/java-tron/pull/4220 




## 3. 改进Java-tron升级机制
对于java-tron的版本升级机制，在GreatVoyage-v4.4.4(Plotinus)之前的版本中需要全部27个超级代表节点完成代码升级，TRON网络才能升级到新版本，而TRON是一个完全去中心化治理的网络，有时候27个超级代表节点无法在某一时间内完成代码升级，使得版本升级过程缓慢。为了实现更高效的去中心化治理，在GreatVoyage-v4.4.4(Plotinus)中，改进了Java-tron的版本升级机制，只需要22个超级代表节点完成代码升级，TRON网络即可升级到新版本。

源代码：https://github.com/tronprotocol/java-tron/pull/4218

---
*The world is knowable, harmonious, and good..* 
<p align="right"> --- Plotinus </p>