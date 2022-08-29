# Great Voyage - v4.1.2
GreatVoyage-4.1.2版本发布， 本次升级主要有以下新功能和修改：

## 一、核心协议
###1、将燃烧带宽/燃烧能量（OUT_OF_TIME除外）的手续费转为SR产块奖励。

该功能开启后，燃烧带宽/燃烧能量（OUT_OF_TIME除外）的手续费将转入到TRANSACTION_FEE_POOL，在块中所有交易处理完成后，按照SR设定的比例转发给当前产块SR及该SR的投票者。同时在transactioninfo中，增加packingFee字段，用于表示当前产块SR和该SR的投票者可获取的费用。

- TIP：[TIP-196](https://github.com/tronprotocol/tips/issues/196)
- 源代码:  [#3532](https://github.com/tronprotocol/java-tron/pull/3532)

### 2、新增账户历史余额查询功能。

账户历史余额查询功能可以方便开发者查询账户在特定区块高度的余额信息，开发者可以通过以下两个API获取到账户的历史余额信息。

- /wallet/getaccountbalance ：获取账户在特定区块高度的余额
- /wallet/getblockbalance ： 获取区块内交易账户的余额变化

**注意事项：**
1. 该功能默认处于关闭状态，可通过节点配置文件启用该功能。
2. 该功能启用之后只能查询启用时间之后的历史余额， 如果需要查询完整历史余额信息，可使用包含历史余额信息的数据快照重新同步节点。

- 源代码：[#3538](https://github.com/tronprotocol/java-tron/pull/3538)
- 使用教程： https://github.com/tronprotocol/documentation-zh/blob/master/docs/api/http.md

###3、黑洞账户优化。

功能开启之后，燃烧带宽和燃烧能量的TRX手续费将不再转给黑洞地址，直接记录到数据库中。

- 源代码： [#3617](https://github.com/tronprotocol/java-tron/pull/3617)

##二、TVM
###1、对以太坊solidity0.6.0特性进行兼容

本次升级之后TRON将完全兼容solidity0.6.0引入的新特性， 包括新增 virtual、override 关键字，支持try/catch等。详细内容请参看TRON Solidity release note：https://github.com/tronprotocol/solidity/releases/tag/tv_0.6.0

- TIP:  [TIP-209](https://github.com/tronprotocol/tips/issues/209)
- 源代码： [#3351](https://github.com/tronprotocol/java-tron/pull/3535)

###2、将MAX_FEE_LIMIT变更为可配置项。

新版本之后，超级代表和超级合伙人可针对47号提案发起投票请求来修改MAX_FEE_LIMIT， MAX_FEE_LIMIT的范围是[0,10000_000_000].

- TIP： [TIP-204](https://github.com/tronprotocol/tips/issues/204) 
- 源代码：  [#3534](https://github.com/tronprotocol/java-tron/pull/3534)
  
##三、其他变更
###1、使用jitpack仓库提供依赖支持，方便开发者的项目使用 java-tron 作为依赖。
- 源代码： [#3554](https://github.com/tronprotocol/java-tron/pull/3554)