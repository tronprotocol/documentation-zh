# Java-tron代码结构
Java-tron是基于Java语言开发的TRON网络客户端，它实现了TRON白皮书中所提到的所有功能，包括共识机制、密码学、数据库、TVM虚拟机、网络管理等。我们可以通过启动Java-tron来运行一个TRON网络节点。在本文中，我们将详细描述Java-tron的代码结构，介绍其各个功能模块的作用，便于开发者后续的代码分析与开发。

Java-tron采用模块化的代码结构，代码结构清晰，易于维护与扩展。Java-tron 目前分为7个模块：[protocol](#protocol)、[common](#common)、[chainbase](#chainbase)、[consensus](#consensus)、[actuator](#actuator)、[crypto](#crypto)、[framework](#framework)，下面分别介绍各个模块的功能及其代码组织结构。


## protocol

对于区块链这种分布式网络，简洁高效的数据交互协议非常重要，protocol模块定义了：

* 节点间通信协议
* 节点内部模块间的通信协议
* 对外提供的服务协议

上述协议采用了[`Google Protobuf`](https://developers.google.com/protocol-buffers)数据交互格式，相比于JSON和XML，`Google Protobuf`格式更高效和灵活，可以通过ProtoBuf编译器为定义的协议文件生成特定语言的序列化和反序列化的源代码。Protobuf是 java-tron 实现跨语言跨平台的基础。

[protocol](https://github.com/tronprotocol/java-tron/tree/develop/protocol) 模块的代码路径为`https://github.com/tronprotocol/java-tron/tree/develop/protocol`，其目录结构如下：
```
|-- protos
    |-- api
    |   |-- api.proto
    |   |-- zksnark.proto
    |-- core
        |-- Discover.proto
        |-- Tron.proto
        |-- TronInventoryItems.proto
        |-- contract
```

* `protos/api/` - Java-tron节点对外提供的gRPC接口及数据结构
* `protos/core/` - 节点间及节点内部各个模块间通信的数据结构
    * `Discover.proto` - 节点发现相关的数据结构
    * `TronInventoryItems.proto` - 节点间区块传输相关数据结构
    * `contract/` - 合约相关的数据结构
    * `Tron.proto` - 其它重要的数据结构定义，其中包括账户、区块、交易、资源、超级代表、投票、提案相关的数据结构。



## common

common模块对公共组件和一些工具类进行了封装，比如异常处理、指标监控工具等，以方便其他模块调用。

[common](https://github.com/tronprotocol/java-tron/tree/develop/common) 模块的代码路径为`https://github.com/tronprotocol/java-tron/tree/develop/common`, 其目录结构如下：

```
|-- /common/src/main/java/org/tron
    |-- common
    |   |-- args
    |   |-- config
    |   |-- entity
    |   |-- logsfilter
    |   |-- overlay
    |   |-- parameter
    |   |-- prometheus
    |   |-- runtime
    |   |-- setting
    |   |-- utils
    |-- core
        |-- config
        |-- db
        |-- db2
        |-- exception
```


* `common/prometheus` - prometheus指标监控
* `common/utils` - 基础数据类型封装类
* `core/config` - 节点配置相关类
* `core/exception` - 所有的TRON网络异常处理相关类




## chainbase

chainbase 模块是数据库层面的抽象，像 PoW、PoS、DPoS 这类基于概率性的共识算法不可避免的会以一定的概率发生切链，因此 chainbase 定义了一个支持可回退数据库的接口标准，该接口要求数据库实现状态回滚机制、checkpoint容灾机制等。

另外 chainbase 模块具有良好的接口抽象设计，任何满足接口实现的数据库都可以作为区块链的底层存储，赋予开发者更多的灵活性，LevelDB和RocksDB是默认提供的两种具体实现。

[chainbase](https://github.com/tronprotocol/java-tron/tree/develop/chainbase) 模块的代码路径为`https://github.com/tronprotocol/java-tron/tree/develop/chainbase`，其目录结构如下：
```
|-- chainbase.src.main.java.org.tron
    |-- common
    |   |-- bloom
    |   |-- error
    |   |-- overlay
    |   |-- runtime
    |   |-- storage
    |   |   |-- leveldb
    |   |   |-- rocksdb
    |   |-- utils
    |   |-- zksnark
    |-- core
        |-- actuator
        |-- capsule
        |-- db
        |   |-- RevokingDatabase.java
        |   |-- TronStoreWithRevoking.java
        |   |-- ......
        |-- db2
        |   |-- common
        |   |-- core
        |       |-- SnapshotManager.java
        |       |-- ......
        |-- net
        |-- service
        |-- store
```


* `common/` - 公共组件，比如异常处理类、工具类
    * `storage/leveldb/` 实现了使用LevelDB作为底层存储数据库
    * `storage/rocksdb/` 实现了使用RocksDB作为底层存储数据库
* `core/` - chainbase模块核心代码
    * `capsule/` 

        各个数据结构的封装类，比如AccountCapsule，BlockCapsule等，AccountCapsule为Account数据结构的封装类，提供了账户数据的修改与查询；BlockCapsule为Block数据结构的封装类，提供了区块数据的修改与查询。

    * `store/` 
        
        各个数据库，比如`AccountStore`，`ProposalStore`等。`AccountStore`是账户数据库，数据库名称为`account`，存储了TRON网络中的所有账户信息；`ProposalStore`是提案数据库，数据库名称为`proposal`，存储了TRON网络中的所有提案信息。

    * `db/` 和 `db2/` 

        实现了可回退数据库，其中包含了两种可回退数据库：位于`db/`目录下`AbstractRevokingStore`和位于`db2/` 目录下`SnapshotManager`。`SnapshotManager`相比与`AbstractRevokingStore`，数据回退更稳定，并支持底层数据库的扩展，因此Java-tron采用`SnapshotManager`可回退数据库，其中的几个重要接口及实现类如下：

        * `RevokingDatabase.java` 是数据库容器的接口，用于所有可回退数据库的管理，`SnapshotManager` 是该接口的一个实现
        * `TronStoreWithRevoking.java` 是支持可回退的数据库的基类，所有的可回退数据库都是它的具体实现，比如`BlockStore`，`TransactionStore`等
    

## consensus

共识机制是区块链中非常重要的模块，常见的有 PoW、PoS、DPoS、PBFT 等，联盟链以及其他一些可信网络中也会采用 Paxos、Raft 等共识机制，共识的选择需要和业务场景相匹配，比如对共识效率敏感实时游戏类就不适合采用 PoW，而对实时性要求极高的交易所来说 PBFT 可能是首选。所以支持可替换的共识是非常有必要的，同时也是实现特定应用区块链的重要一环，consensus 模块最终目标是能够让应用开发者能够像配置参数那样简单的切换共识机制。

[consensus](https://github.com/tronprotocol/java-tron/tree/develop/consensus) 模块的代码路径为`https://github.com/tronprotocol/java-tron/tree/develop/consensus`，其目录结构如下：
```
|-- consensus/src/main/java/org/tron/consensus
    |-- Consensus.java
    |-- ConsensusDelegate.java
    |-- base
    |   |-- ConsensusInterface.java
    |   |-- ......
    |-- dpos
    |-- pbft
```
[consensus](https://github.com/tronprotocol/java-tron/tree/develop/consensus) 模块将共识过程抽象成几个重要的部分，定义在 ConsensusInterface 接口中：

1. `start` - 启动共识服务，可以自定制启动参数
2. `stop` - 停止共识服务
3. `receiveBlock` - 定义接收区块的共识逻辑
4. `validBlock` - 定义验证区块的共识逻辑
5. `applyBlock` - 定义处理区块的共识逻辑

目前Java-tron基于 ConsensusInterface 接口实现了DPOS共识和PBFT共识，分别位于`dpos/`和`pbft/`目录下，开发者也可以根据自身业务需求实现 ConsensusInterface 接口，来自定义共识机制。

## actuator

以太坊初创性的引入了虚拟机并定义了智能合约这种开发方式，但对于一些复杂的应用，智能合约不够灵活且受限于性能，这也是 Java-tron 提供创建应用链的一个原因。为此 Java-tron 独立出来了 actuator 模块，该模块为应用开发者提供一种新的开发范式：可以将应用代码直接植入链中而不再将应用代码跑在虚拟机中。

actuator是交易的执行器，可以将应用看成是不同交易类型组成的交易集，每类交易都由对应的 actuator 负责执行。

[actuator](https://github.com/tronprotocol/java-tron/tree/develop/actuator) 模块的代码路径为`https://github.com/tronprotocol/java-tron/tree/develop/actuator`，其目录结构如下：
```
|-- actuator/src/main/java/org/tron/core
    |-- actuator
    |   |-- AbstractActuator.java
    |   |-- ActuatorCreator.java
    |   |-- ActuatorFactory.java
    |   |-- TransferActuator.java
    |   |-- VMActuator.java
    |   |-- ......
    |-- utils
    |-- vm
```

* `actuator/` - TRON网络中各种类型交易的执行器，定义了不同类型交易的处理逻辑，比如`TransferActuator`是转账TRX交易的处理类，`FreezeBalanceActuator`是质押TRX获取资源交易的处理类
* `utils/` - 执行交易所需的工具类
* `vm/` - 虚拟机相关代码


actuator模块定义的 Actuator 接口有4个方法：
* `execute` - 负责交易具体需要执行的动作，可以是状态修改、流程跳转、逻辑判断
* `validate` - 负责验证交易的正确性
* `getOwnerAddress` - 获取交易发起方的地址
* `calcFee` - 定义交易手续费计算逻辑

开发者也可以根据自身业务实现 Actuator 接口，来实现自定义交易类型的处理。
 
## crypto
crypto是一个相对独立的模块，但也是非常重要的模块，Java-tron中的数据安全几乎全由该模块来保证，目前支持SM2和ECKey加密算法。

[crypto](https://github.com/tronprotocol/java-tron/tree/develop/crypto)模块的路径为`https://github.com/tronprotocol/java-tron/tree/develop/crypto`，其目录结构如下：
```
|-- crypto/src/main/java/org/tron/common/crypto
    |-- Blake2bfMessageDigest.java
    |-- ECKey.java
    |-- Hash.java
    |-- SignInterface.java
    |-- SignUtils.java
    |-- SignatureInterface.java
    |-- cryptohash
    |-- jce
    |-- sm2
    |-- zksnark
```

* `sm2`和`jce` - 提供SM2和ECKey加密算法和签名算法
* `zksnark` - 提供零知识证明算法

## framework

framework是 java-tron 的核心模块，也是节点的入口，framework 模块负责各个模块的初始化及业务逻辑的跳转，framework包含了节点对外提供的服务，P2P网络相关的节点发现与管理流程、区块广播及处理流程。

[framework](https://github.com/tronprotocol/java-tron/tree/develop/framework)模块的代码路径为`https://github.com/tronprotocol/java-tron/tree/develop/framework`，其目录结构如下：

```
|-- framework/src/main/java/org/tron
    |-- common
    |   |-- application
    |   |-- backup
    |   |-- logsfilter
    |   |-- net
    |   |-- overlay
    |   |   |-- client
    |   |   |-- discover
    |   |   |-- message
    |   |   |-- server
    |   |-- runtime
    |   |-- zksnark
    |-- core
    |   |-- Wallet.java
    |   |-- capsule
    |   |-- config
    |   |-- consensus
    |   |-- db
    |   |-- metrics
    |   |-- net
    |   |-- services
    |   |-- trie
    |   |-- zen
    |-- keystore
    |-- program
    |   |-- FullNode.java
    |-- tool
```

* `program/FullNode.java`  - 它是程序的入口点，初始化对外的HTTP、gRPC和json-rpc接口服务
* `core/services` - 定义了对外提供的服务，其子目录`http/`包含了所有的http接口处理类，`json-rpc/` 包含了所有的json-rpc接口处理类
* `common/overlay/discover` - 节点发现逻辑
* `common/overlay/server` - 节点管理及节点间区块同步逻辑
* `core/net` - 消息处理，其子目录`/service` 为交易及区块广播、区块抓取及同步逻辑
* `core/db/Manager.java` - 交易及区块校验并处理逻辑


## 总结
本文主要介绍了Java-tron的代码结构，以及各个功能模块的作用、位置及目录结构，通过本文您会对Java-tron的整体结构及关键接口有了大致的了解，方便后续的代码分析和开发。