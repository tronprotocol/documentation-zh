
















## 波场网络设计与协议问题

**问：如何生成一个账户**

答：可以使用[Wallet-cli](https://github.com/tronprotocol/wallet-cli) 或者 [Tronscan](https://tronscan.org/#/wallet/new)

**问：目前的网络流量有多大？数据能够传输到多个主机还是只能够满足个人的一些节点？**

答：网络流量取决于交易数量。作为大致参考，可以将每一个交易的流量算作200字节。当前网络配置是2000TPS（每秒交易量）。

**问：tokens 申请完成后，如何由not started yet 变更成 participate?**

答：发行通证后无法改变发行开始日期，需要等到创建通证时设置的具体时间才能开始发行。在创建通证后，只能修改URL和描述。

**问：在哪里可以查看目前的超级节点的出块状态？**

答：[Tronscan](https://tronscan.org/#/sr/representatives)

**问：超级节点出块的间隔会保持不变吗？**

答：目前是3秒钟，将来可能会优化到1秒钟。

**问：未来大概会有出块的TRX会减半的计划吗？如果有的话，大概在什么时间点？**

答：没有减半计划。

**问：如果某一个超级节点除了问题，它会被移除前27名吗？**

答：不会强行移出，当用户停止为其投票时，如果它的得票数不在前27名，会自动停止出块。

**问：成为超级代表的门槛是什么？**

答：你的得票数需要排在前27名。

**问：27个超级代表的出块奖励是平均分配，还是按照算力分配？**

答：平均分配，每出一个块，获得32个TRX奖励。

**问：是否有可能会出现算力超过50%的问题？**

答：不会。

**问：投票会消耗TRX吗？**

答：投票不会消耗TRX。

**问：超级代表的出块权利可以持续多久？**

答：每6小时会重新计票一次，只要还在前27名中，就可以持续产块。

**问：一笔交易的凭证是什么？**

答：交易哈希。

**问：为什么TRX的冻结不允许解冻期不能超过3天？**

答：目前冻结不允许解冻期固定为3天。意味着，满3天的冻结期后才能解冻，如果3天后不进行解冻操作，还是会保持冻结状态。

**问：如何监控与我的账户有关的交易？**

答：你可以使用波场事件订阅插件。请查阅[https://tronprotocol.github.io/documentation-EN/architecture/plugin/#tron-event-subscription](https://tronprotocol.github.io/documentation-EN/architecture/plugin/#tron-event-subscription)

**问：怎么计算交易费用？**

答：请查阅[https://tronprotocol.github.io/documentation-EN/mechanism&algorithm/resource/](https://tronprotocol.github.io/documentation-EN/mechanism&algorithm/resource/)

**问：怎么计算交易大小？**

答：tx-size  = grpcClient.getTransactionById(txId).get().getSerializedSize() + 60

**问：怎么将我的投票重置？**

答：只需要再投一次票，将票数置为0就可以了。


## 配置问题

**问：config.conf中的genesis.block.witnesses替换成在[https://tronscan.org/](https://tronscan.org/) 注册时给出的address字符串：是否需要删除其他address？url和voteCount字段是否需要删除？**

答：不需要删除其他地址，但是这些地址也会成为您网络的一部分，而如果您不持有其私钥，这些相当于是废地址。注意：Zion、Sun以及Blackhole账户不能从创世块的配置文件中删除，但是可以对它们的地址进行更改。 

**问：启动节点的时候怎么制定数据存储目录？**

答：可以在启动节点时指定数据存储目录，例如：
```text
java -jar FullNode.jar -c config.conf -d /data/output
```

**问：怎么修改配置可以让logs发送到stdout？**

答：步骤如下：

下载[https://github.com/tronprotocol/java-tron/blob/develop/src/main/resources/logback.xml](https://github.com/tronprotocol/java-tron/blob/develop/src/main/resources/logback.xml)

取消注释掉以下内容：

appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender"

在’root level="INFO"‘下
取消注释掉’appender-ref ref="STDOUT"‘
注释掉’appender-ref ref="ASYNC"‘

将logback.xml移到FullNode.jar所在的目录下

启动时，添加’--log-config logback.xml‘参数，例如：
```text
java -jar FullNode.jar --log-config logback.xml
```

**问：如何修改日志级别？**

答：日志级别在’logback.xml‘中定义。通过修改’root level‘来改变输出的日志级别。
```text
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

**问：在私有网络环境下，我如何设置我的资产？**

答：在私有网络环境下，你可以通过修改配置文件来设置你初始账户的资产。配置文件如下：
```text
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

## 编译问题

**Ask：java-tron编译时遇到单元测试没有通过问题**

答：可以用'./gradlew build -x test'命令忽略单元测试。

## 部署问题

**问：如何测试部署是否正常，比如是否有测试接口或者命令，类似redis，get ping 会返回 pong？**

答：Java-tron没有默认的接口。一旦服务器开始运行，就能够发送grpc命令，基于这一点，有几种检验部署是否成功的方法。
       
```text
- tail -f logs/tron.log |grep "MyheadBlockNumber"
```

**问：在部署private 环境时，SuperNode和FullNode 关系是什么样子？是否需要先部署SuperNode ,然后部署FullNode？**

答：在private环境中，至少需要部署一个SuperNode，但对FullNode的数量没有最低要求。

**问：我怎样才能知道我的测试超级节点在运行了呢？**

答：运行以下命令：
```text
- tail -f logs/tron.log |grep "Try Produce Block"
```

**问：SolidityNode与FullNode可以部署在一台机器上吗？他们会分享数据吗？**

答：指定数据目录是可以做到的，配置文件参数：db.directory = "database"，index.directory = "index"。但是也可以让FullNode.jar和SolidityNode.jar在不同目录下运行，将数据和日志文档完全分离。记得修改config.conf的端口，因为两个应用无法在同一端口运行。原则上不鼓励继续使用 SolidityNode, 目前 FullMode 可以替代 SolidityNode 的功能。


## 开发问题

## 节点运行问题

**问：既然是Private环境，为什么日志还持续的更新全网其他节点，并同步保存信息？那么private 和public 的区别是什么？**

答：如果和IP list有关  A: 需要在config.conf更新seed.ip，如果设置得和公网一样，并且电脑连入了互联网，电脑就会尝试连接其它节点，那么即使连接失败，IP list也会存入DB。如果和区块还有交易有关  A: 在private环境中，需要更改p2p版本和父哈希。如果设置同主网或测试网一样，并且电脑连入了互联网，那么节点也会和公网同步。

**问：Private环境，因为我看官网是通过手动投票产生的SuperNode节点，是否还需要提交TRON资料审核注册成为Super Node节点？**

答：在private环境的前提下，不需要向波场基金会提交申请材料。

**问：对公网需要暴露那些服务端口？**

答：端口18888，50051是两个默认端口。

**问：在最坏情况下，万一超级节点无法联通，最多允许多长时间恢复服务？**

答：SR节点重新连上网络的速度只取决于SR节点自己的恢复速度，跟网络没关系。

**问：solidity是根据full同步区块的吗？**

答：是的。

**问：节点有钱包功能吗？**

答：节点有钱包的RPC接口，不能直接用命令行调用钱包功能，可以用另外一个repo里的命令行钱包使用full node的钱包功能。

**问：为什么我的机器上区块处理时间非常久？**

答：Java-tron运行是需要更多的内存来处理交易。

## 测试网问题

**问：我们要测试超级节点出块和性能的情况，是不是需要你们投票我们的节点才能竞选上？**

答：测试的时候，我们可以给你投票，让你成为测试网的一个超级节点。

**问：测试网与Shasta的区别是?**

答：to be answered

**问：如何获得测试网TRX？**

答：[http://testnet.tronex.io/join/getJoinPage](http://testnet.tronex.io/join/getJoinPage)

## 智能合约问题


## 客户端问题

**问：如何离线签名交易？**

答：你可以使用[tronweb](https://developers.tron.network/docs/api-sign-flow)

**问：怎么把Tronscan的钱包导入到wallet-cli？**

答：通过调用wallet-cli api 'ImportWallet'。

## API问题

**问：gateway链接的是SolidityNode吗？**

答：gateway可以连接SolidityNode，也可以连接FullNode。

**问：'getTransactionById'与'getTransactionInfoById'的区别是什么？**

答：它们的数据取自不同的数据模块。'getTransactionById'主要侧重交易的通用数据，'getTransactionInfoById'侧重交易的费用数据。

**问：如何广播原始的交易数据？**

答：可以使用'wallet/broadcasthex'接口。

**问：如何获得一个智能合约账户的余额？**

答：可以使用以下wallet-cli api:

```text
triggercontract contractaddress balanceOf(address) "youraddress" false 0 0 0 #
```

## 常见错误

**问：以下错误信息表达了什么意思？**
```text
17:02:42.699 INFO [o.t.c.s.WitnessService] Try Produce Block
17:02:42.699 INFO [o.t.c.s.WitnessService] Not sync
```
答： 出现该消息，说明您的节点和网络未同步。开始出块前，首先需要进行同步。请使用以下命令检查区块高度。
```text
- tail -f logs/tron.log |grep "MyheadBlockNumber"
```

## 其他问题

**问：节点的机器是否搭建在北京，会不会遇到防火墙的问题？**

答：39.106.220.120在北京，其他的都在美国欧洲香港。
