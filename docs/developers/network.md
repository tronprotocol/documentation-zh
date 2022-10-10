# 网络
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

* [节点发现](#_4)
* [节点连接](#_5)
* [区块同步](#_10)
* [区块和交易广播](#_14)

下面将分别介绍这四个功能部分。

## 节点发现
节点发现是区块链节点接入区块链网络的第一步。区块链网络是一种结构化的P2P网络。结构化网络会将所有节点按照某种结构有序的组织起来，比如形成一个环状网络或者树状的网络。 结构化网络普遍基于DHT(Distributed Hash Table，分布式哈希表) 算法实现。具体的实现方案有 Chord、Pastry、CAN、Kademlia 等算法。TRON 网络采用 Kademlia 算法。

### Kademlia 算法
Kademlia 是分布式散列表(DHT，Distributed Hash Table)的一种实现，是去中心化 P2P 网络中最核心的一种路由寻址技术，可以在无中心服务器的情况下，在网络中快速找到目标节点。

关于算法的详细介绍请参考 [Kademlia](https://zh.m.wikipedia.org/zh-hans/Kademlia)。

### TRON 实现
TRON 实现的 Kademlia 算法，要点如下：

* 节点ID：随机产生的512bit ID
* 节点距离：节点距离通过两个节点的ID异或运算得到，公式为：`节点距离 = 256 - 节点ID异或结果的前导0的个数`，如果计算结果为负数，距离等于0。
* k桶：即节点路由表。根据节点距离的远近，将远端节点划分到不同的桶中，与本节点距离相同的远端节点被记录在相同的桶中，每个桶最多容纳16个节点。根据节点距离的计算公式就可以看出，TRON 实现的 Kademlia 算法一共维护256个桶。

TRON 节点发现协议包括以下四种UDP消息：

* `DISCOVER_PING` - 用于探测⼀个节点是否在线
* `DISCOVER_PONG` - 用于响应 `DISCOVER_PING` 消息
* `DISCOVER_FIND_NODE` - 用于查找与⽬标节点距离最近的其它节点
* `DISCOVER_NEIGHBORS` - 用于响应 `DISCOVER_FIND_NODE` 消息，会返回一个或者多个节点，最多16个

#### 初始化K桶
节点启动后，会读取节点配置文件中配置的种子节点，以及数据库中记录的对等节点，然后向它们发送 `DISCOVER_PING` 消息，如果收到回复 `DISCOVER_PONG` ，在K桶没满的情况下，将相应节点写入K桶；如果相应桶已经达到了16个节点，则向桶中最早的节点发起挑战，挑战成功，将被挑战节点删除，将挑战节点加入K桶。K桶初始化完成后，进行节点发现流程。
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/network_discoverinit.png)


#### 发送DISCOVER_FIND_NODE消息，发现更多节点

节点发现服务会开启两个节点发现定时任务（`DiscoverTask`和`RefreshTask`），周期执行节点发现过程来更新k桶。

* `DiscoverTask` 是发现更多距离自己近的节点，每30s执行一次，执行流程如下图所示:
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/network_discovertask.png)


* `RefreshTask` 是通过随机节点ID来扩充本地k桶，即发现距离随机节点ID更近的节点，每7.2s执行一次，执行流程如下图所示:
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/network_refreshtask.png)


`DiscoverTask`和`RefreshTask`中使用的节点发现算法，在一次调用中会执行8轮，每轮向K桶中距离目标节点 ID 最近的3个节点发送 `DISCOVER_FIND_NODE` 消息，并等待回复。


#### 接收到neighbors消息，更新K桶
当本节点接收到远端节点回复的 `DISCOVER_NEIGHBORS` 消息后，会依次向收到的邻居节点发送 `DISCOVER_PING` 消息，接下来如果收到了回复消息`DISCOVER_PONG`，则判断相应的K桶是否装满，如果K桶未满，则将新节点加入K桶，如果K桶满了，则向其中的某个节点发起挑战，若挑战成功(向被挑战的节点发送`DISCOVER_PING` 消息，如果未能收到其回复`DISCOVER_PONG`，则为挑战成功，否则挑战失败)，则将旧节点从K桶中删除，将新节点加入K桶。
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/network_updatek.png)


节点周期的执行节点发现任务，不断的更新K桶，构建自己的节点路由表。接下来就是节点间建立连接的过程了。

## 节点连接

在了解节点间如何建立TCP连接之前，您需要首先了解peer节点类型。
### peer节点管理
节点需要对peer节点进行管理分类，以进行高效稳定的节点连接。远端节点可以分为如下几类：

* Active nodes：通过配置文件指定，系统启动后，会主动与其建立连接的节点。如果连接建立失败，则在每个TCP连接定时任务中都会重新尝试与其建立连接。
* Passive nodes：通过配置文件指定，被动接受连接的节点。
* Trust nodes：通过配置文件指定，Active nodes和Passive nodes都是trust nodes。当收到trust node的连接请求时，会跳过其它的条件检查，直接接受请求。
* badNodes：当收到异常的协议报文时，会将节点加入到badNodes，生效时长1个小时，当收到 badNodes 的连接请求，会直接拒绝请求
* recentlyDisconnectedNodes：当断开某条连接后，会把节点加入到recentlyDisconnectedNodes，有效时长30s，当收到 recentlyDisconnectedNodes 的连接请求，会直接拒绝请求

### 建立节点间TCP连接
在节点启动后，会创建一个建立节点间TCP连接的定时任务`poolLoopExecutor`，用于选择节点，并与之建立连接。建立TCP连接定时任务，工作过程如下：
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/network_connect.png)



TCP连接主要分为两步：首先，确定要与之建立连接的节点的列表；列表中需要包含active nodes中还没有成功建立连接的节点，然后计算还需要建立连接的数量，从邻居发现节点列表里面根据 [节点过滤策略](#_6) 过滤出满足要求的节点，再根据 [节点打分策略](#_7) 对节点打分排序，将最高的相应数量的节点加入到请求列表中。最后，与请求列表中的节点建立TCP连接。

#### 节点过滤策略
建立节点连接时，需过滤掉如下几类节点，并判断节点自己的连接数是否达到了最大连接。

* 自身节点
* recentlyDisconnectedNodes列表中的节点
* badNodes列表中的节点
* 已经建立了连接的节点
* 与该节点ip建立的连接数已经达到了上限值maxConnectionsWithSameIp的节点

但是对于可信节点，会忽略掉部分过滤策略，始终与其建立连接。
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/network_filterrule.png)

#### 节点打分策略
节点分数用于确定建立连接的优先级，分数越高，优先级越高。打分维度包括：

* 丢包率：丢包率越低，说明数据通信质量越好。分数与丢包率成反比，最高分为100，最低为0
* 网络延迟：网络延时越小，说明网络质量越好。分数与平均网络延时成反比，最高分为20，最低为0
* TCP流量：TCP流量越大，说明通信比较活跃。分数与TCP流量成正比，最高分为20，最低为0
* 断开连接次数：断开连接次数越少，说明节点越稳定。断开连接分数为负数，且与断开连接次数为正比，值为断开连接次数的10倍
* Handshake：曾经handshake成功过的节点，表示有相同的区块链信息，因此优先选择和他们建立连接。Handshake成功次数大于0时，Handshake得分为20，否则得分为0
* 处罚状态：处于处罚状态的节点，分数为0，不参与其它维度打分，包含以下几种情况：
    * 节点断开连接时间不到60s
    * 节点在badNodes列表中
    * 区块链信息不一致

计算节点分数时，首先判断节点是否为处罚状态，如果是，则分数计为0，否则，节点分数为各个维度的得分之和。


### 握手

TCP 连接建立成功后，主动发起TCP连接请求的节点，会向邻居节点发送握手消息 `P2P_HELLO`，目的为了确认节点间的链路信息是否一致，以及是否需要发起区块同步流程。

当邻居节点收到 `P2P_HELLO` 后，会与本地信息做比较，比如检查p2p version、创世块信息是否一致，若一致，还需要检查固化快，以及判断是否是重复的连接、恶意节点等。若所有的检查条件都通过，则会回复`P2P_HELLO`消息，然后进行区块同步或广播；否则，断开连接。


### 信道保活
信道保活是通过 `P2P_PING`、`P2P_PONG` TCP报文来完成的。当节点与邻居节点建立了TCP连接并握手成功后，节点会为连接开启一个线程 `pingTask` 定期发送 `P2P_PING` 消息以维护该TCP连接，每10s调度一次。如果在超时时间内未收到节点回复的 `P2P_PONG` 消息，则断开连接。

## 区块同步

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



## 区块和交易广播

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
本文介绍了TRON最底层模块-P2P网络相关的实现细节，包括节点发现、节点连接、区块同步、区块和交易广播流程，希望通过阅读本文能帮助开发者进一步了解和开发java-tron网络相关模块。