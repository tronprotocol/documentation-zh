
# Tron 事件订阅机制

<h3> 简介 </h3>

TIP: [https://github.com/tronprotocol/TIPs/issues/12](https://github.com/tronprotocol/TIPs/issues/12)

波场事件订阅支持四种类型的事件：

- 交易相关事件

订阅的内容：

transactionId: 交易哈希  
blockHash: 区块哈希  
blockNumber: 区块高度  
energyUsage: 此次调用中，合约调用者消耗的Energy的总量  
energyFee: 此次调用中，合约调用者消耗的Energy中，需要TRX支付的数目(SUN为单位)  
originEnergyUsage: 此次调用中，合约开发者消耗的Energy的总量  
energyUsageTotal: 此次调用中，合约调用者和合约开发者消耗的Energy的总量  


- 区块相关事件

订阅的内容：

blockHash: 区块哈希  
blockNumber: 区块高度  
transactionSize: 区块中包含的交易的数目  
latestSolidifiedBlockNumber: 最新的固化块的高度  
transactionList: 交易哈希列表  

- 合约事件相关

订阅的内容：

transactionId: 交易哈希  
contractAddress: 合约地址  
callerAddress: 合约调用者地址  
blockNumber: 合约事件所在的区块高度  
blockTimestamp: 区块时间戳  
eventSignature: 事件签名  
topicMap: the map of topic in solidity language  
data: the data information in solidity language  


- 合约日志事件相关

订阅的内容：

transactionId: 交易哈希  
contractAddress: 合约地址  
callerAddress: 合约调用者地址  
blockNumber: 合约事件所在的区块高度  
blockTimestamp: 区块时间戳  
contractTopics: the list of topic in solidity language  
data: the data information in solidity language  
removed: 'true'代表日志已经被移除  


合约事件与合约日志事件订阅支持过滤功能：

fromBlock: 起始区块索引  
toBlock: 结束区块索引  
contractAddress: 合约地址  
contractTopics: 合约主题  

**注意**: 不支持历史数据查询


<h3> 新功能 </h3>

1.&nbsp;支持事件插件，kafka & mongodb 插件已经发布，开发者可以按照需求自定义插件。

2.&nbsp;支持订阅链上数据，例如区块，交易，合约以及合约日志。开发者还可以通过设置过滤条件来订阅指定的数据。

3.&nbsp;提供事件订阅的数据查询服务，线上地址为[https://api.tronex.io](https://api.tronex.io)。

<h3> Github 项目 </h3>

- [事件订阅](https://github.com/tronprotocol/event-plugin)
- [事件订阅数据查询](https://github.com/tronprotocol/tron-eventquery)

<h3> 事件订阅相关插件部署 </h3>

- [kafka部署](https://tronprotocol.github.io/documentation-zh/developers/deployment/#kafka)
- [mongo部署](https://tronprotocol.github.io/documentation-zh/developers/deployment/#mongo)

<h3> 事件订阅数据查询 </h3>

事件订阅数据查询服务实现了事件订阅模型。

查看更多信息，请查阅[https://github.com/tronprotocol/TIPs/issues/12](https://github.com/tronprotocol/TIPs/issues/12)

- [事件订阅数据查询服务部署](https://tronprotocol.github.io/documentation-zh/developers/deployment/#_6)
- [事件订阅数据查询服务http api](https://github.com/tronprotocol/documentation-en/blob/master/docs_without_index/plugin/event-query-http.md)
