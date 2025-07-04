# 去中心化交易所

## 什么是交易对

TRON网络原生支持去中心化交易所(DEX)。去中心化交易所由多个交易对构成。一个交易对（Exchange）是token与token之间，或者token与TRX之间的交易市场（Exchange Market）。
任何账户都可以创建任何token之间的交易对，即使TRON网络中已经存在相同的交易对。交易对的买卖与价格波动遵循Bancor协议。
TRON网络规定，所有交易对中的两个token的权重相等，因此它们数量（balance）的比率即是它们之间的价格。
举一个简单的例子，假设一个交易对包含ABC和DEF两种token，ABC的balance为1000万，DEF的balance为100万，由于权重相等，因此10 ABC = 1 DEF，也就是说，当前ABC对于DEF的价格为10ABC/DEF。

## 创建交易对

任何账户都可以创建任何token之间的交易对。创建交易对的手续费是1024TRX，这个手续费会被TRON网络烧掉。
创建交易对相当于为该交易对注入（inject）原始资本，因此创建者账户中要拥有该交易对的初始balance。当创建成功后，会立即从创建者账户中扣除这两个token的balance。

创建交易对的合约是ExchangeCreateContract，该合约有4个参数：

- first_token_id，第1种token的id
- first_token_balance，第1种token的balance
- second_token_id，第2种token的id
- second_token_balance，第2种token的balance

如果交易对中包含TRX，则使用" _ "表示TRX的id。需要注意的是，TRX的单位是SUN。
例子：

```shell
ExchangeCreate abc 10000000 _ 1000000000000
```

该交易会创建abc与TRX之间的交易对，初始balance分别为10000000个abc和1000000000000 sun（1000000TRX），
如果创建者没有足够的abc和TRX，则交易对创建失败；否则创建者账户中立即扣除相应的abc和TRX，交易对创建成功，可以开始交易。

## 交易

任何账户都可以在任何交易对中进行交易。交易量和价格完全遵循Bancor协议。也就是说，一个账户在交易时，交易的对象是exchange。交易是即时的，不需要挂单和抢单，只要有足够的token，就可以交易成功。

交易的合约是ExchangeTransactionContract，该合约有4个参数：

- exchange_id，交易对的id，TRON网络会根据交易对创建时间顺序给每个交易对唯一的id
- token_id，要卖出的token的id
- quant，要卖出的token的金额
- expected，期望得到的另一个token的最小金额。如果小于此数值，交易不会成功

例子：
我们在刚刚创建的abc与TRX的交易对中进行交易，假设此交易对id为1，当前交易对中abc balance为10000000，TRX balance为1000000，如果期望花100个TRX买到至少990个abc，则

```shell
ExchangeTransaction 1 _ 100 990
```

其中" _ "表示TRX，即向交易对卖出100个TRX。如果成功，该交易会使得交易对中增加100个TRX，并根据Bancor协议计算出减少的abc的数量，交易创建者的账户中abc和TRX的数量会相应地增加和减少。实际交易到的abc数量，通过transaction result的exchange_received_amount字段返回，可以通过gettransactioninfobyid查询。

## 注资

当一个交易对其中1种token的balance很小时，只需要很小的交易量就会造成很大的价格波动，这不利于正常交易。为了避免这种情况，该交易对的创建者可以选择向该交易对注资（inject）。
一个交易对只能由该交易对的创建者来注资。注资不需要手续费。
注资需要指定一种token以及注资金额，TRON网络会自动根据当前交易对中两种token的比例，计算出另一个token所需的金额，从而保证注资前后，交易对中两个token的比例相同，价格没有变化。   与创建交易对相同，注资要求创建者拥有足够多的两种token的balance。

注资的合约是ExchangeInjectContract，该合约有3个参数：

- exchange_id，交易对的id
- token_id，要注资的token的id
- quant，要注资的token的金额

例子：
我们对刚刚创建的abc与TRX的交易对进行注资，假设此交易对id为1（TRON网络中第1个交易对），当前交易对中abc balance为10000000，TRX balance为1000000，如果要增加10%的abc，则

```shell
ExchangeInject 1 abc 1000000
```

如果成功，该交易会使得交易对中增加1000000个abc，并增加100000个TRX，交易对创建者的账户中abc和TRX的数量会相应地减少。

## 撤资

一个交易对中的所有资产都是创建者的。创建者可以随时撤资（withdraw），把交易对中的token赎回到自身账户中。一个交易对只能由该交易对的创建者来撤资。撤资不需要手续费。
和注资一样，撤资需要指定一种token以及撤资金额，TRON网络会自动根据当前交易对中两种token的比例，计算出另一个token撤资的金额，从而保证撤资前后，交易对中两个token的比例相同，价格没有变化。
撤资前后价格没有变化，但是价格波动会更大。

撤资的合约是ExchangeWithdrawContract，该合约有3个参数：

- exchange_id，交易对的id
- token_id，要撤资的token的id
- quant，要撤资的token的金额

例子：
我们对之前创建的abc与TRX的交易对进行撤资，假设此交易对id为1，当前交易对中abc balance为10000000，TRX balance为1000000，如果要赎回10%的abc，则

```shell
ExchangeWithdraw 1 abc 1000000
```

如果成功，该交易会使得交易对中减少1000000个abc，以及减少100000个TRX，交易对创建者的账户中abc和TRX的数量会相应地增加。

## 查询

### 1. 查询交易

有三个查询交易对的接口，包括：

查询所有交易对信息（ListExchanges）

分页查询交易对信息（GetPaginatedExchangeList）(Odyssey-v3.1.1暂不支持)

查询指定交易对信息（GetExchangeById）

相关api详情，请查询[波场RPC-API说明](https://github.com/tronprotocol/Documentation/blob/master/%E4%B8%AD%E6%96%87%E6%96%87%E6%A1%A3/%E6%B3%A2%E5%9C%BA%E5%8D%8F%E8%AE%AE/%E6%B3%A2%E5%9C%BA%E9%92%B1%E5%8C%85RPC-API.md#64-%E6%9F%A5%E8%AF%A2%E6%8C%87%E5%AE%9A%E4%BA%A4%E6%98%93%E5%AF%B9)

### 2. 计算当前价格

交易中token的当前价格信息的计算过程：

假设 first_token 当前的价格为 100 Sun，first_token_balance 为1,000,000, second_token_balance 为2,000,000，

second_token 当前的价格为 first_token * first_token_balance/second_token_balance = 50 Sun

### 3. 计算交易获得token量

交易中花费first_token置换获得的second_token的数量的计算过程：

sellTokenQuant是要卖出的first_token的金额

buyTokenQuant是要买入的second_token的金额

supply = 1,000,000,000,000,000,000L

supplyQuant = -supply * (1.0 - Math.pow(1.0 + (double) sellTokenQuant/（firstTokenBalance + sellTokenQuant）, 0.0005))

buyTokenQuant = （long）balance * (Math.pow(1.0 + (double) supplyQuant / supply, 2000.0) - 1.0)

注意：由于网络其他账户发生交易，价格可能发生变化。

相关api详情，请查询[HTTP API](../api/http.md)。
