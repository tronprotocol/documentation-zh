# 波场 FAQ

<!-- markdownlint-disable MD026 -->

[TOC]

## 日常使用

### 如何生成一个账户

- [Tronscan: 生成账户](https://tronscan.org/#/wallet/new)
- [Wallet-cli](https://github.com/tronprotocol/wallet-cli)

### 目前的 TRON 网络处理性能有多高？需要多大网络带宽？

网络流量取决于交易数量。作为大致参考，可以将每一个交易的流量算作200字节。当前网络配置是 2000TPS（每秒交易量）。

### TRC10 token 申请完成后，如何由 not started yet 变更成 participate?

发行 TRC10 通证后无法改变发行开始日期，需要等到创建通证时设置的具体时间才能开始发行。在创建通证后，只能修改 URL 和描述。

### 未来大概会有 TRX 有出块的减半计划吗？如果有的话，大概在什么时间点？

目前没有减半计划。

### 是否有可能会出现算力超过 50% 的问题？

TRON 没有采用 PoW 共识机制，不会出现该问题。

### 一笔交易的凭证是什么？

交易哈希，对交易的签名。

### 投票会消耗 TRX 吗？

投票不会消耗 TRX. 只需要提前冻结 TRX 为 Bandwidth, 获得 TP(TRON Power) 点数即可。

### 怎么将我的投票重置？

只需要再投一次票，将对应的票数置为 0 就可以了。

### 超级代表

#### 在哪里可以查看目前的超级代表节点的出块状态？

区块浏览器 [Tronscan](https://tronscan.org/#/sr/representatives).

#### 超级代表节点出块的间隔会保持不变吗？

目前是3秒钟，将来有可能会优化到1秒钟。

#### 如果某一个超级代表节点出了问题，它会被移除前27名吗？

不会强行移出，当用户停止为其投票时，如果它的得票数不在前27名，会自动停止出块。

#### 成为超级代表的门槛是什么？

该超级代表得票数需要排在前27名。

#### 27个超级代表的出块奖励是平均分配，还是按照算力分配？

平均分配，每出一个块，获得32个TRX奖励。

#### 超级代表的出块权利可以持续多久？

每6小时会重新计票一次，只要票数排名还在前27名中，就可以持续产块。

### 资源消耗

#### 为什么 TRX 的冻结解冻期不能超过3天？

目前冻结解冻期固定为3天。意味着，满3天的冻结期后才能解冻，如果3天后不进行解冻操作，还是会保持冻结状态。

#### 怎么计算交易费用？

请查阅 [资源模型](../mechanism-algorithm/resource.md).

#### 怎么计算交易带宽消耗？

`Transaction` pb 结构去除 `ret` 字段，然后再加上 64 字节。

```java
Transaction transaction = result.get();
long bytesSize = transaction.toBuilder().clearRet().build().getSerializedSize() + 64;
```

参考 [tronprotocol/documentation#370](https://github.com/tronprotocol/documentation/issues/370).

## API 使用

### getTransactionById 与 getTransactionInfoById 的区别是什么？

它们的数据取自不同的数据模块。

- `getTransactionById` 主要侧重交易的通用数据
- `getTransactionInfoById` 侧重交易的费用，执行结果，中间结果数据

### 如何广播原始的交易数据？

可以使用 `wallet/broadcasthex` 接口。

### 如何在交易数据里添加备注？

Transaction 里有 `data` 字段，可以附带任意 bytes, 用于保存不超过 500k 的信息数据。
创建交易的时候在 `raw_data` 里手动添加这个字段，目前 HTTP API 没有有接口实现。需要通过 gRPC 接口访问。

可参考：[本地构建交易](https://cn.developers.tron.network/docs/%E6%9C%AC%E5%9C%B0%E6%9E%84%E5%BB%BA%E4%BA%A4%E6%98%93).

### 如何调用 TRC20 API?

可参考：[TRC20 合约交互](https://cn.developers.tron.network/docs/trc20%E5%90%88%E7%BA%A6%E4%BA%A4%E4%BA%92%E4%BB%A5usdt%E4%B8%BA%E4%BE%8B).

### 如何判断交易是否成功？

通过交易状态 API `getTransactionInfoById`.

参考：[交易状态](https://cn.developers.tron.network/docs/%E4%BA%A4%E6%98%93#section-%E4%BA%A4%E6%98%93%E7%8A%B6%E6%80%81).

### 广播交易出现 DUP_TRANSACTION_ERROR 错误

是重复广播了，交易第一次广播到节点 A, 节点 A 会先缓存起来（可能没上链），交易再次广播到节点 A, 就会报重复交易。
如果第一次广播没报错，最好等到交易的超时时间过了，确定没有上链再选择重发。

### 如何监控与我的账户有关的交易？

你可以使用波场事件订阅插件。请查阅 [TRON 事件订阅机制](../architecture/event.md).

## 智能合约

### 出现 OUT_OF_TIME 错误

该错误是超时错误。合约最长执行时间是 50ms.
如果同样的逻辑有时候会发生超时错误，有时候不会发生，是因为代码执行的复杂度正好在某个临界点附近，
出块节点的机器性能波动恰好导致错误概率发生。

### 出现 OUT_OF_ENERGY 错误

1. 检查 feelimit 设置的是否为 0 或太小
2. trx 余额不足，能量不够

### 如何把以太坊合约转到波场？

波场是兼容以太坊的，修改代币相关的字段后，理论上是可以直接部署到波场的，可以编译部署到测试网测试一下。

目前波场不兼容以太坊的 json-rpc API, 相关 API 请求需要做相应转换。

## 部署问题

### java-tron 编译时单元测试没有通过

可以用 `./gradlew build -x test` 命令忽略单元测试。对报错有疑惑，欢迎在 Github 项目提出 Issue.

### 如何测试部署是否正常？

Java-tron 没有默认的接口。一旦服务器开始运行，就能够发送 grpc 命令，基于这一点，有几种检验部署是否成功的方法。

- 查看日志，确认是否区块同步，或有在出块
- 检查 18888/tcp, 18888/udp 端口流量
- 发送测试 API 请求，例如 `getnodeinfo`

### 在部署 private 环境时, SuperNode 和 FullNode 关系是什么样子？

在 private 环境中，至少需要部署一个 SuperNode, 但对 FullNode 的数量没有最低要求。

### 我怎样才能知道我的测试超级节点在运行了呢？

运行以下命令：

```console
tail -f logs/tron.log | grep "Try Produce Block"
```

### SolidityNode 与 FullNode可以部署在一台机器上吗？他们会分享数据吗？

指定数据目录是可以做到的，配置文件参数: `db.directory = "database"`, `index.directory = "index"`。
但是也可以让 FullNode.jar 和 SolidityNode.jar 在不同目录下运行，将数据和日志文档完全分离。
记得修改 `config.conf` 的端口，因为两个应用无法在同一端口运行。

!!! warning
    原则上不鼓励继续使用 SolidityNode, 目前 FullMode 可以替代 SolidityNode 的功能。

### 配置文件

#### 调用合约报错: "contract validate error : this node don't support constant"

修改配置 `vm.supportConstant = true`.

#### 节点启动时如何指定 log 日志文件路径

添加启动参数 `--log-config logback.xml`(在 `logback.xml` 里面修改 `tron.log` 路径)

#### config.conf 中的 genesis.block.witnesses 如何设置？

是否需要删除其他 address？url和voteCount字段是否需要删除？

不需要删除其他地址，但是这些地址也会成为您网络的一部分，而如果您不持有其私钥，这些相当于是废地址。注意：Zion、Sun以及Blackhole账户不能从创世块的配置文件中删除，但是可以对它们的地址进行更改。

#### 启动节点的时候怎么指定数据存储目录？

可以在启动节点时指定数据存储目录，例如：

```console
java -jar FullNode.jar -c config.conf -d /data/output
```

#### 怎么修改配置可以让 java-tron 日志发送到 stdout?

步骤如下：

下载[logback.xml](https://github.com/tronprotocol/java-tron/blob/develop/src/main/resources/logback.xml)

取消注释掉以下内容：

```xml
appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender"
```

在 `root level="INFO"` 下

- 取消注释`appender-ref ref="STDOUT"`
- 注释 `appender-ref ref="ASYNC"`

将 `logback.xml` 移到 `FullNode.jar` 所在的目录下

启动时，添加 `--log-config logback.xml` 参数，例如：

```console
java -jar FullNode.jar --log-config logback.xml
```

#### 如何修改日志级别？

日志级别在 `logback.xml` 中定义。通过修改 `root level=` 来改变输出的日志级别。

```xml
<root level="ERROR">
    <!--<appender-ref ref="STDOUT"/>-->
    <appender-ref ref="ASYNC"/>
  </root>

  <logger name="app" level="ERROR"/>
  <logger name="net" level="ERROR"/>
  <logger name="backup" level="ERROR"/>
  <logger name="discover" level="ERROR"/>
  <logger name="crypto" level="ERROR"/>
  <logger name="utils" level="ERROR"/>
  <logger name="actuator" level="ERROR"/>
  <logger name="API" level="ERROR"/>
  <logger name="witness" level="ERROR"/>
  <logger name="DB" level="ERROR"/>
  <logger name="capsule" level="ERROR"/>
  <logger name="VM" level="ERROR"/>
```

#### 在私有网络环境下，我如何设置我的资产？

在私有网络环境下，你可以通过修改配置文件来设置你初始账户的资产。配置文件如下：

```conf
genesis.block = {
  # Reserve balance
  assets = [
    {
      accountName = "TestA"
      accountType = "AssetIssue"
      address = "THRR7uvFbRLfNzpKPXEyQa8KCJqi59V59e"
      balance = "1000000000000000"
    },
    {
      accountName = "TestB"
      accountType = "AssetIssue"
      address = "TBLZaw93rsnLJ1SWTvoPkr7GVg5ixn2Jv1"
      balance = "1000000000000000"
    },
    {
      accountName = "TestC"
      accountType = "AssetIssue"
      address = "TJg8yZ4Co8RXsHmTWissmSL1VpL7dCybY1"
      balance = "1000000000000000"
    }
  ]
```

#### 广播交易时出现 TAPOS 错误

修改配置文件: `trx.reference.block = "solid"`.

每一个合法的交易需要有一个链上已存在的一定时间内的块作为参考块(TAPOS: Transaction As Proof Of Stake),
如果你创建交易时用作参考块的块被回退了或者不够新，就会出现 TAPOS 验证失败,
`solid` 指的是用已确认的块作为参考块, `head` 表示使用最新块。

#### TRC20 交易的 internal transaction 查不到

配置文件选项 `vm.saveInternalTx` 没有打开，需要改成 `true` 并重启节点。

该配置项目打开后只会保存修改配置之后的区块的 internal transaction 数据。不会同步历史 internal transaction.

## 节点运行相关

### 既然是Private环境，为什么日志还持续的更新全网其他节点，并同步保存信息？那么private 和public 的区别是什么？

和 IP list 有关。

需要在 `config.conf` 更新 `seed.ip`.
如果设置和公网一样，并且服务器连入了互联网，服务器会尝试连接其它节点，那么即使连接失败，IP list 也会存入 DB.

在 private 环境中，需要更改 *p2p版本* 和 *父哈希*。

如果设置同主网或测试网一样，并且服务器连入了互联网，那么节点也会和公网同步。

### Private环境，是否还需要提交TRON资料审核注册成为Super Node节点？

在private环境的前提下，不需要向波场基金会提交申请材料。

### 对公网需要暴露那些服务端口？

- 节点发现 18888/udp
- 区块广播同步 18888/tcp
- gRPC API 50051/tcp, 500061/tcp (可选)
- HTTP API 8090/tcp, 8091/tcp (可选)

### 在最坏情况下，万一超级节点无法联通，最多允许多长时间恢复服务？

SR节点重新连上网络的速度只取决于SR节点自己的恢复速度，跟网络没关系。

### 节点有钱包功能吗？

节点有钱包的 RPC 接口，不能直接用命令行调用钱包功能，可以用 [wallet-cli](https://github.com/tronprotocol/wallet-cli)
里的命令行钱包使用 full node 的钱包功能。

### 为什么我的服务器上区块处理时间非常久？

Java-tron 运行时需要更多的内存来处理交易。

### Not sync 错误信息表达了什么意思？

出现日志

```text
17:02:42.699 INFO [o.t.c.s.WitnessService] Try Produce Block
17:02:42.699 INFO [o.t.c.s.WitnessService] Not sync
```

出现该消息，说明您的节点和网络未同步。开始出块前，首先需要进行同步。请使用以下命令检查区块高度。

```console
tail -f logs/tron.log | grep "MyheadBlockNumber"
```

## 测试网问题

### 我们要测试超级节点出块和性能的情况，是不是需要足够投票我们的节点才能竞选上？

测试的时候，我们可以给你投票，让你成为测试网的一个超级节点。

### 如何获得测试网TRX？

[http://testnet.tronex.io/join/getJoinPage](http://testnet.tronex.io/join/getJoinPage)

## 工具使用

### 如何离线签名交易？

你可以使用 [tronweb](https://developers.tron.network/docs/api-sign-flow).

### 怎么把 Tronscan 的钱包导入到 wallet-cli？

通过调用 wallet-cli 命令 `ImportWallet`.

### 如何获得一个智能合约账户的余额？

可以使用以下 wallet-cli 命令:

```text
triggercontract contractaddress balanceOf(address) "youraddress" false 0 0 0 #
```

## 其他问题

### 节点的机器是否搭建在北京，会不会遇到防火墙的问题？

`39.106.220.120` 在北京，其他节点均位于美洲欧洲或香港。

## 没有找到你的问题？

欢迎到社区提问，或在 Gihub 项目页面提出 Issue.

- 波场开发者电报群: [t.me/troncoredevscommunity](https://t.me/troncoredevscommunity)
- Github 仓库: [tronprotocol/java-tron](https://github.com/tronprotocol/java-tron)
