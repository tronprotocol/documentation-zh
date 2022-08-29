# GreatVoyage-4.2.2(Lucretius)
GreatVoyage-v4.2.2(Lucretius)版本引入了3个重要的优化更新，区块处理的优化有效得提高区块的执行速度，从而大幅提高TRON网络的性能，高效的HTTP/RPC查询和更高性能TVM将为TRON DAPP用户带来更好的体验，进一步繁荣波场生态。
# 核心协议

##1、优化区块处理。

在GreatVoyage-v4.2.2(Lucretius)之前的版本中，区块处理过程中为了获取witness列表，执行了多次数据库查询和反序列化操作，这部分操作占用了近1/3的区块处理时间。

GreatVoyage-v4.2.2(Lucretius)版本简化了witness的查询，区块处理过程只需一次查询即可获取witness列表，经过测试，本次优化大幅提升了区块处理性能。

- TIP： [TIP-269](https://github.com/tronprotocol/tips/blob/master/tip-269.md)
- 源代码:  [#3827](https://github.com/tronprotocol/java-tron/pull/3827)

##2、优化数据查询。

在GreatVoyage-v4.2.2(Lucretius)之前的版本中，多个HTTP或RPC对链上数据的查询是互斥的，如果有查询请求正在处理，新的查询请求会等待之前的请求完成以后才会被处理。

实际上，查询数据的方法中并没有使用到共享数据, 所以并不需要加锁操作。本次优化去除了查询过程中不必要的同步锁，大幅提高了节点内部查询、HTTP和RPC的查询请求性能。

- TIP： [TIP-281](https://github.com/tronprotocol/tips/blob/master/tip-281.md)
- 源代码:  [#3830](https://github.com/tronprotocol/java-tron/pull/3830)


##3、优化智能合约ABI的存储。

在GreatVoyage-v4.2.2(Lucretius)之前的版本中，一个智能合约的ABI数据和这个智能合约的其他数据是一起存储在合约数据库中， TVM的一些高频指令(SLOAD,SSTORE等等)会从合约数据库读取一个智能合约的所有数据，然而合约的执行并不会使用到这些ABI数据，所以频繁的读取会降低这些指令的执行性能。

GreatVoyage-v4.2.2(Lucretius)版本将智能合约的ABI数据从合约数据库中转存到一个专门的ABI数据库中，合约执行过程中将不再读取ABI数据，从而大幅提高TVM的执行性能。

- TIP： [TIP-268](https://github.com/tronprotocol/tips/blob/master/tip-268.md)
- 源代码:  [#3836](https://github.com/tronprotocol/java-tron/pull/3836)

# 其他变更

## 1、优化系统合约`BatchValidateSign`的初始化流程。

- 源代码:  [#3836](https://github.com/tronprotocol/java-tron/pull/3836)



 --- *Truths kindle light for truths.*
 <p align="right"> --- Lucretius</p>


