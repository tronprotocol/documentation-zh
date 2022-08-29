# GreatVoyage-4.1.3(Thales)
GreatVoyage-4.1.3(Thales)版本主要有以下新功能和修改：

# 核心协议
## 1.对待打包的交易进行排序，SR优先打包费用较高的交易
在GreatVoyage-4.1.2及之前版本中，SR打包交易是按照交易到达的时间顺序进行的，这很容易受到低交易费用的攻击。

本次优化后，出块节点根据费用对待打包的交易进行排序，然后优先打包费用较高的交易， 防止低交易费用攻击。

# API
## 1.新增查询待打包交易列表相关接口
在GreatVoyage-4.1.2及之前版本中, SR打包交易是按照交易到达的时间顺序进行的，这很容易受到低交易费用的攻击。本次升级后, Fullnode节点提供3个接口来获取待打包交易列表的详细信息：

- /wallet/gettransactionfrompending ：通过交易ID从待打包交易列表中获取完整的交易信息
- /wallet/gettransactionlistfrompending ：从待打包交易列表中获取所有交易
- /wallet/getpendingsize ：获取当前待打包交易的数量
  

   
  



Great Voyage-v4.1.3 (Thales) 版本的交易打包逻辑的优化将有效减少低费用攻击，极大提升TRON公链的安全性。

