# P2P 网络深入解析

> 本文聚焦 P2P 网络的内部原理（架构、区块同步与广播）。关于如何**配置**节点发现对等节点并接入网络（config.conf 参数、boot/seed 节点、active/passive peer 等），请参阅[连接到 TRON 网络](../using_javatron/connecting_to_tron.md)。

## 概述
P2P是一种分布式网络，网络的参与者共享他们所拥有的一部分硬件资源，比如处理能力、存储能力、网络连接能力、打印机等，这些共享的资源需要由网络提供服务和内容，能被其它对等节点直接访问而无需经过中间实体。在此网络中的参与者既是服务和内容提供者，又是服务和内容获取者。

区别于传统的Client/Server中央服务器结构，P2P网络中的每个节点的地位都是对等的。每个节点在充当客户端的同时，也可以作为服务端给其它节点提供服务，极大地提高了资源的利用率。


### 区块链网络
P2P 是区块链结构中的网络层，网络层的主要目的是实现区块链网络中节点之间的信息传播、验证和交流。区块链网络本质上是一个P2P网络，每个节点既能接受信息也能产生信息。节点之间通过维护一个共同的区块链数据来保持通信。

P2P网络作为区块链的基础，为区块链带来如下优点：

* 防止单点攻击
* 高容错性
* 较好的兼容性与可扩展性

### TRON网络
TRON架构图如下：
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/network_architecture.png)

P2P网络作为TRON的最底层模块，直接决定了整个区块链网络的稳定性。网络模块按照功能可以划分成以下四部分：

* 节点发现
* 节点连接
* [区块同步](#block-synchronization)
* [区块和交易广播](#block-and-transaction-broadcast)

其中**节点发现**与**节点连接**这两部分的底层实现已从 java-tron 仓库抽离为独立的外部依赖 [`io.github.tronprotocol:libp2p`](https://github.com/tronprotocol/libp2p)，由该库负责底层的节点发现（基于 Kademlia 算法）与连接传输，并新增了基于 DNS 的节点发现等能力。其上的 TRON 协议层——包括 P2P_HELLO 握手、P2P_PING/P2P_PONG 保活、peer 业务状态管理、消息分发、同步与广播——仍由 java-tron 的 `core/net` 实现，并通过 `TronNetService` 与 libp2p 对接。底层节点发现与连接的实现细节请参阅 libp2p 仓库，本文不再展开。

而**区块同步**与**区块和交易广播**仍由 java-tron 的 `core/net` 实现，下面分别介绍这两个功能部分。

## 区块同步 { #block-synchronization }

在与对方节点完成握手后，如果发现对方节点的区块链比本地的区块链要长，根据最长链原则，会触发区块同步的处理流程`syncService.startSync`。同步过程中的报文交互如下图：

![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/network_syncflow.png)

节点A向对方节点B发送 `SYNC_BLOCK_CHAIN` 消息，以宣告本地链的摘要信息。对方节点B收到后，计算出节点A缺失的区块清单，并将缺失区块的id列表通过 `BLOCK_CHAIN_INVENTORY` 消息发送给节点A，一次最多携带2000个区块id。

节点A收到 `BLOCK_CHAIN_INVENTORY` 消息后，取出缺失区块id，并通过异步的方式向节点B发送 `FETCH_INV_DATA` 消息以请求缺少的区块，一次最多请求100个区块。如果还有需要同步的区块（即 `BLOCK_CHAIN_INVENTORY` 报文中的remain_num大于0），会触发新一轮的区块同步流程。

节点B收到节点A的 `FETCH_INV_DATA` 报文后，通过 `BLOCK` 消息将区块发送给节点A。节点A收到 `BLOCK` 报文后，异步处理该区块。

### 链摘要及缺失区块清单
下面根据几个不同的区块同步场景示例，说明链摘要和节点缺少的区块清单的生成。

* 链摘要：有序的区块blockID列表，包括：最高固化块、最高非固化块，以及之间二分法对应的区块
* 缺失区块清单：邻居节点根据链摘要与自己链进行比较，确定对方缺失的区块清单，返回一组连续的区块blockID以及剩余的块数
#### 普通场景

本地头块高度为1018，固化块高度为1000，两个节点刚建立连接，所以共同块高度为0，通过二分方式获取到节点A的本地链摘要为：1000、1010、1015、1017、1018。

节点B收到节点A的链摘要后，结合本地链可以生产节点A缺少的区块清单为：1018、1019、1020、1021。之后节点A根据缺失区块清单，请求同步区块1019、1020、1021。
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/network_sync1.png)


#### 切链场景

本地主链头块高度为1018，固化块高度为1000，两个节点刚建立连接，所以共同块高度为0，通过二分方式获取到节点A的本地链摘要为：1000、1010、1015、1017、1018。

节点B收到节点A的链摘要后，发现本地主链跟节点A的主链不在同一条链上，对比节点A的链摘要，找到共同块高度为1015，则认为节点A缺少的区块清单为：1015、1016'、1017'、1018'，1019'。之后节点A根据缺失区块清单，请求同步区块1018'，1019'。
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/network_sync2.png)

另一种切链场景，本地主链头块高度为1018，固化块高度为1000，共同块为1017‘，位于fork链上，通过二分方式获取到节点A的本地链摘要为：1000、1009、1014、1016'、1017'。

节点B收到节点A的链摘要后，结合本地链可以生产节点A缺少的区块清单为：1017'、1018'、1019'。之后节点A根据缺失区块清单，请求同步区块1018'，1019'。
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/network_sync3.png)



## 区块和交易广播 { #block-and-transaction-broadcast }

当超级代表节点生产出新的区块，或者全节点接收到用户发起的新交易时，会发起交易&区块广播流程。当节点接收到新区块或者新交易时，会转发相应的区块或交易，转发与广播的流程一样。报文交互如下图所示：
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/network_broadcastflow.png)



其中涉及到的消息类型包括：

* `INVENTORY` - 广播清单：区块或者交易id列表
* `FETCH_INV_DATA` - 请求需要获取的清单数据：区块或者交易id列表
* `BLOCK` - 区块数据 
* `TRXS` - 交易数据

节点A将待广播交易或区块通过 `INVENTORY` 清单消息发送到节点B。节点B收到 `INVENTORY` 清单消息后，需要检查对方节点的状态，如果可以接收该消息，则将清单中的区块/交易放入待获取队列 `invToFetch` 中。如果是区块清单，还会立即触发"获取区块&交易任务"，来向节点A发送 `FETCH_INV_DATA` 消息获取区块&交易。

节点A收到 `FETCH_INV_DATA` 消息后，会检查是否发送过清单消息给对方，如果发送过，则根据清单数据，向节点B发送交易或者区块消息。节点B收到交易或者区块消息后，处理消息，并触发转发流程。

## 总结
本文介绍了TRON最底层模块——P2P网络。其中节点发现与节点连接已抽离至外部依赖 libp2p，本文仅做简要定位；仍保留在 java-tron `core/net` 中的区块同步、区块和交易广播流程则做了详细介绍。希望通过阅读本文能帮助开发者进一步了解和开发java-tron网络相关模块。
