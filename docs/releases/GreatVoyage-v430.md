# GreatVoyage-4.3.0(Bacon)
GreatVoyage-v4.3.0(Bacon)版本引入多个重要的优化更新，`FREE_NET_LIMIT` 和 `TOTAL_NET_LIMIT` 的可配置化有助于TRON社区完成更好的链上治理；全新的TVM指令和ABI类型使智能合约的使用场景更加丰富；全新的加密算法库提高了TRON网络的安全性；Account数据存储、交易验证流程的优化提升了交易处理速度和区块验证速度，从而大幅提高TRON网络的性能；节点启动速度的优化将为用户带来更好的体验，进一步繁荣波场生态。

# 核心协议
## 1. 账户每天的免费带宽额度可配置

在GreatVoyage-v4.3.0(Bacon)之前的版本中，账户每天的免费带宽额度固定为5000。GreatVoyage-v4.3.0(Bacon)版本增加了#61提案 `FREE_NET_LIMIT`，使免费带宽额度可配置。超级代表和超级合伙人可针对61号提案发起投票请求来修改`FREE_NET_LIMIT`，`FREE_NET_LIMIT`的范围是[0, 100,000]

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-292.md 
* 源代码：https://github.com/tronprotocol/java-tron/pull/3917 

**注意事项**：
账户每天的免费带宽额度，目前仍然是5000，后续将由超级代表或超级合伙人发起相应投票请求来更改其值。

## 2. 全网通过质押TRX可获得的带宽总额可配置

在GreatVoyage-v4.3.0(Bacon)之前的版本中，全网通过质押TRX可获得的总带宽额度固定为43,200,000,000。
GreatVoyage-v4.3.0(Bacon)版本增加了#62提案`TOTAL_NET_LIMIT`，使全网通过质押TRX可获得的总带宽额度可配置。超级代表和超级合伙人可针对62号提案发起投票请求来修改`TOTAL_NET_LIMIT`，`TOTAL_NET_LIMIT`的范围是[0, 1000,000,000,000]

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-293.md 
* 源代码: https://github.com/tronprotocol/java-tron/pull/3917  

**注意事项**：
全网通过质押TRX可获得的总带宽额度，目前仍然是43,200,000,000，后续将由超级代表或超级合伙人发起相应投票请求来更改其值。

##3. 优化Account 数据库存储结构
在节点运行过程中，Account是访问频率非常高的数据库，需要频繁对account数据结构进行反序列化操作，在GreatVoyage-v4.3.0(Bacon)之前的版本中，Account中不仅包含账户的基本数据，还包括用户TRC-10资产数据。但对于TRX转账和智能合约相关交易，一般情况下只使用了Account的基本数据。过大的TRC-10资产列表会对Account数据结构的反序列性能造成极大影响。
GreatVoyage-v4.3.0(Bacon)版本优化了Account数据库的存储结构，将TRC-10资产数据从Account中剥离出来，单独存储在`AccountAssetIssue`中。减少了Account反序列时的数据量，提升了反序列化速度。

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-295.md 
* 源代码：https://github.com/tronprotocol/java-tron/pull/3906 

**注意事项**：
该功能默认处于关闭状态，后续将由超级代表或超级合伙人发起相应投票请求来开启该功能。

# TVM
## 1. 虚拟机中新增投票指令

在GreatVoyage-v4.3.0(Bacon)之前的版本中，普通账户可以通过给超级代表或超级代表候选人投票来获得出块奖励和投票奖励。但对于智能合约账户，由于TVM不支持投票指令，智能合约账户中的TRX资产无法通过投票获取收益。
GreatVoyage-v4.3.0(Bacon)版本在TVM中引入了投票指令:`VOTE` / `WITHDRAWBALANCE` ，使得智能合约账户也可以给超级代表或超级代表候选人投票以获取收益。

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-271.md 
* 源代码：https://github.com/tronprotocol/java-tron/pull/3921 

**注意事项**：
该功能默认处于关闭状态，后续将由超级代表或超级合伙人发起相应投票请求来开启该功能。

## 2. 新增ABI类型 `Error`
GreatVoyage-v4.3.0(Bacon)版本引入了新的ABI类型 `Error` , 即自定义错误类型，将兼容以太坊solidity_0.8.4引入的新特性。

* TIP：https://github.com/tronprotocol/tips/blob/master/tip-306.md 
* 源代码：https://github.com/tronprotocol/java-tron/pull/3921 

# API
## 1. `TransactionExtention`新增`energy_used`字段
在GreatVoyage-v4.3.0(Bacon)之前的版本中，用户无法预知智能合约交易的能量消耗。
GreatVoyage-v4.3.0(Bacon)版本为`TransactionExtention`新增`energy_used`字段，用户通过`TriggerConstantContract`调用合约方法时，将会在当前节点基于其最新同步的区块，构建一个沙盒环境来提供给TVM执行该方法调用，执行完毕后会将实际消耗的能量值设置到`energy_used`字段并返回给用户（该操作不会产生上链交易，也不会改变当前节点的状态）。

* 源代码：https://github.com/tronprotocol/java-tron/pull/3940 

# 其它变更

## 1. 更新BouncyCastle为加密算法程序库
由于SpongyCastle已经不再被维护，从GreatVoyage-v4.3.0(Bacon)版本开始，采用Bouncy Castle作为加密算法的程序库。

* 源代码：https://github.com/tronprotocol/java-tron/pull/3919 

## 2. 更新新账户创建时`net_usage`的计算方法
在GreatVoyage-v4.3.0(Bacon)版本中，更新了新账户创建时`net_usage`的计算方法。 
源代码: https://github.com/tronprotocol/java-tron/pull/3917 

## 3. 优化区块验证
在GreatVoyage-v4.3.0(Bacon)之前的版本中，节点在验证区块时，对于其中的每一个交易来说，无论之前是否已经验证通过，都会被再次验证。而交易验证这个过程占据了整个区块处理的1/3时间。
GreatVoyage-v4.3.0(Bacon)版本优化了区块验证的逻辑，对于区块中的非`AccountUpdateContract`类型的交易(`AccountUpdateContract`交易涉及到账户权限变更)，如果之前已经被验证通过，那么它们将不再被验证，以加快区块验证速度。

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-276.md 
* 源代码: https://github.com/tronprotocol/java-tron/pull/3910 

## 4. 优化节点启动
GreatVoyage-v4.3.0(Bacon)之前的版本里，在节点启动过程中，会读取数据库中的交易缓存数据和区块数据来完成内存交易缓存的初始化。 在GreatVoyage-v4.3.0(Bacon)版本优化了内存交易缓存的初始化流程，去掉了一些不必要的解析过程， 优化后将提升节点启动的速度。

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-285.md 
* 源代码：https://github.com/tronprotocol/java-tron/pull/3907 

## 5. 优化交易处理流程降低内存使用
GreatVoyage-v4.3.0(Bacon)版本中，优化了交易处理流程，提前释放了不需要再使用的对象，优化内存使用。

* 源代码： https://github.com/tronprotocol/java-tron/pull/3911 

## 6. 新增插件优化leveldb的启动性能
在GreatVoyage-v4.3.0(Bacon)之前的版本中，随着levelDB的运行，manifest文件会持续增长，过大的manifest文件不但影响节点启动速度，而且还有可能导致内存持续增长而导致内存不足，服务异常中止。
GreatVoyage-v4.3.0(Bacon)引入了leveldb 启动优化插件，插件优化了manifest的文件大小以及LevelDB的启动过程，减少了内存占用，提升了节点启动速度。

* TIP： https://github.com/tronprotocol/tips/blob/master/tip-298.md 
* 源代码： https://github.com/tronprotocol/java-tron/pull/3925
* 插件使用指南： https://github.com/tronprotocol/documentation-zh/blob/master/docs/developers/archive-manifest.md 

*Knowledge is power.* 
<p align="right"> --- Francis Bacon </p>