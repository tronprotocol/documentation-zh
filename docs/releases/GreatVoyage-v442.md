# GreatVoyage-4.4.2(Augustinus)
GreatVoyage-v4.4.2(Augustinus)版本引入了三个重要的优化更新，新的操作码执行模型提高了TVM性能，个性化LevelDB参数提高了数据库性能，新增的log filter APIs使JSON-RPC API更加全面。

# TVM
## 1. 优化TVM操作码执行模型
GreatVoyage-v4.4.2(Augustinus)版本优化了TVM中的解释器的操作码执行模型，经测试，本次优化大幅提升了TVM的性能。

TIP: https://github.com/tronprotocol/tips/blob/master/tip-344.md 
源代码：https://github.com/tronprotocol/java-tron/pull/4157 

# API
## 1. 新增关于Event的JSON-RPC API
从GreatVoyage-v4.4.2(Augustinus)版本开始，对于兼容以太坊网络的JSON-RPC API，新增了log filter相关的APIs。

TIP: https://github.com/tronprotocol/tips/issues/343 
源代码：https://github.com/tronprotocol/java-tron/pull/4153 

# 其它变更
## 1. LevelDB数据库性能优化
从GreatVoyage-v4.4.2(Augustinus)版本开始，根据数据库的读写频繁程度，对各个LevelDB数据库进行个性化参数设置，大幅提升数据库的性能。
源代码：https://github.com/tronprotocol/java-tron/pull/4154 

--- 

*Patience is the companion of wisdom.* 
<p align="right"> ---  Augustinus </p>