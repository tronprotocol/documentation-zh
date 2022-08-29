# GreatVoyage-4.4.0(Rousseau)
GreatVoyage-v4.4.0(Rousseau)版本引入了多个重要的更新：区块广播的优化将使区块可以更快的广播到全网；`dynamic store`的查询性能优化以及数据库参数的优化将大幅提升区块处理速度，进而提升java-tron的性能；节点API定制化使得节点配置更加灵活以适应不同的应用场景；TVM也将更好的兼容EVM并适配以太坊London升级，全新的JSON-RPC API将为开发者们带来更好的开发体验，帮助开发者们更容易的加入到波场生态，促进波场生态繁荣。

# 核心协议
## 1. 优化区块广播
在GreatVoyage-v4.4.0(Rousseau)之前的版本中，区块处理的逻辑是：验证区块->处理区块->广播区块。但由于区块处理时间较长，广播区块时有延迟。为了加快区块广播，GreatVoyage-v4.4.0(Rousseau)版本将区块处理逻辑更改为：验证区块->广播区块->处理区块，以使区块可以快速广播至全网。

TIP: https://github.com/tronprotocol/tips/blob/master/tip-289.md 
源代码: https://github.com/tronprotocol/java-tron/pull/3986 

## 2. 优化`dynamic store`的查询性能
在区块处理过程中，`dynamic store`的访问频率非常高，GreatVoyage-v4.4.0(Rousseau) 版本优化了`dynamic store`的查询性能，将`dynamic store`全部数据加载到第一级缓存，提高`dynamic store`缓存命中率，提升数据查询效率，加快区块处理速度。

TIP: https://github.com/tronprotocol/tips/blob/master/tip-290.md 
源代码：https://github.com/tronprotocol/java-tron/pull/3993 

## 3. 优化交易广播接口
GreatVoyage-v4.4.0(Rousseau)版本优化了交易广播接口的处理流程，将交易广播由异步转为同步，广播成功后再返回结果，使得广播的返回结果更为准确。

源代码：https://github.com/tronprotocol/java-tron/pull/4000 

## 4. 优化数据库参数
GreatVoyage-v4.4.0(Rousseau)版本优化了部分数据库参数，提升了数据库读写性能，从而提升了区块处理效率。

源代码：https://github.com/tronprotocol/java-tron/pull/4018 https://github.com/tronprotocol/java-tron/pull/3992 

# TVM
## 1. TVM更好的兼容EVM
GreatVoyage-v4.4.0(Rousseau)版本为TVM与EVM存在差异的指令提供兼容性方案，新部署的合约支持以下特性：
1. `GASPRICE`指令返回能量单价 
2. `try-catch`支持捕获所有类型的TVM异常 
3. 禁止系统合约`TransferContract`给智能合约账户转账

TIP: https://github.com/tronprotocol/tips/blob/master/tip-272.md 
源代码：https://github.com/tronprotocol/java-tron/pull/4032 

**注意事项**：
该功能默认处于关闭状态，后续将由超级代表或超级合伙人发起相应投票请求来开启该功能。

## 2. 对以太坊London升级进行兼容
GreatVoyage-v4.4.0(Rousseau)版本对以太坊London升级进行兼容：新增了`BASEFEE`指令； 禁止部署以0xEF为起始字节的新合约。

TIP: https://github.com/tronprotocol/tips/blob/master/tip-318.md 
源代码：https://github.com/tronprotocol/java-tron/pull/4032 

**注意事项**：
该功能默认处于关闭状态，后续将由超级代表或超级合伙人发起相应投票请求来开启该功能。

## 3. Constant模式下的`energy limit`可配置且增大默认值
在GreatVoyage-v4.4.0(Rousseau)版本之前， constant 模式下的energy  limit是一个固定值`3,000,000`，在GreatVoyage-v4.4.0(Rousseau)中引入了修改机制，用户可以通过启动参数`--max-energy-limit-for-constant`或者节点配置文件(`vm.maxEnergyLimitForConstant`)修改 constant 模式下的energy limit值， 同时将energy limit 的默认值修改为`100,000,000`。

源代码： https://github.com/tronprotocol/java-tron/pull/4032 

# API
## 1. 新增JSON-RPC API
从GreatVoyage-v4.4.0(Rousseau)版本开始，新增兼容以太坊网络的JSON-RPC API(不包括filter API)，使用指南请参考文档：https://developers.tron.network/reference#json-rpc-api 

源代码：https://github.com/tronprotocol/java-tron/pull/4046 

## 2. 节点支持禁用特定API
为了节点可定制化，从GreatVoyage-v4.4.0(Rousseau)版本开始，支持通过节点配置文件关闭指定的API。

源代码：https://github.com/tronprotocol/java-tron/pull/4045 

## 3. 优化`TriggerConstantContract`接口
在GreatVoyage-v4.4.0(Rousseau)中，对`TriggerConstantContract`接口引入了以下优化：
-  当 `ContractAddress` 为空时执行合约创建
-  `callvalue`和 `tokenvalue` 非零值将不会产生执行异常
- `TransactionExtention` 中增加事件列表和内部交易列表 

源代码： https://github.com/tronprotocol/java-tron/pull/4032 

# 其它变更

## 1. 升级事件插件以支持`BTTC`
GreatVoyage-v4.4.0(Rousseau)中升级了事件插件，升级后的事件插件将支持`BTTC`。

源代码：https://github.com/tronprotocol/java-tron/pull/4067 

## 2. 提升`MaxFeeLimit`的取值范围
在GreatVoyage-v4.4.0(Rousseau)之前的版本中，`MaxFeeLimit` 的取值范围是[0,1e10sun]，GreatVoyage-v4.4.0(Rousseau)版本中将`MaxFeeLimit` 的取值范围扩大为[0,1e17sun]。

**注意事项：**
该功能默认处于关闭状态，将在London升级提案生效后开启。

源代码： https://github.com/tronprotocol/java-tron/pull/4032 

##  3. 优化快速启动脚本`start.sh`
GreatVoyage-v4.4.0(Rousseau)版本中优化了快速启动脚本，最新的使用指南请参考： https://github.com/tronprotocol/java-tron/blob/release_v4.4.0/shell.md
--- 

*The world of reality has its limits; the world of imagination is boundless.* 
<p align="right"> ---  Rousseau</p>