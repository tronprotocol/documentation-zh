
## tron-dex概述
Tron-DEX是一个去中心化的交易所，包含链上订单表、高效的链上撮合引擎，用户在这里可以获得类似于中心化交易所的交易体验。 
在Tron-Dex中，所有的交易信息都是透明可验证，用户可以在这里进行挂单，买单操作。
Tron-Dex上支持TRX与TRC10的交易，TRC20的token需要通过转换合约，先兑换成对应的TRC10的token，然后在DEX中进行交易。

## 创建第一笔订单
任何用户都可以创建订单，只需要设定需要买卖的token对及交易数量。创建完成的订单将放到对应的订单表中，
如果之前没有该token对的订单，系统将创建订单表，新订单将作为表中第一笔订单。

创建订单的合约 MarketSellAsset，该合约有4个参数：
- sellTokenId:卖出token id，TRX以"_"表示
- sellTokenQuantity：卖出Token或TRX的数量
- buyTokenId：买入token id，TRX以"_"表示 
- buyTokenQuantity：买入Token或TRX的最少数量
    
例子：  
```text    
MarketSellAsset TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz  _ 100 1000001 200  
```

该交易会创建订单，卖出100个TRX，买入200个TokenA(Id=1000001)，
如果创建者没有足够的TokenA和TRX，则订单创建失败；创建订单后，用户账户中的余额不会马上减少。
只有当发生订单撮合的时候，用户账户中余额才会发生变化。

## 查询用户及订单状态
创建订单以后，通过用户地址查询到订单信息，包括订单的状态（未成交、已成交、已取消），订单详情，订单已经完成量等。

例子：       
查询我们刚刚创建的TokenA与TRX的订单，接口 GetMarketOrderByAccount ownerAddress。
例子：
```text  
GetMarketOrderByAccount TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz     
```

```text  
{
  "orders": [
    {
      "order_id": "e7e283c2066f6b82850dfb82d34fd9ec5ac2f70ae31b0669e96c1a9ad810a748",
      "owner_address": "TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz",
      "create_time": 1578302082000,
      "sell_token_id": "_",
      "buy_token_id": "1000001",
      "sell_token_quantity": 100,
      "buy_token_quantity": 200,
      "sell_token_quantity_remain": 100
    }
  ]
}
```     
除了用户创建订单时的参数外，还增加了sell_token_quantity_remain， 表示剩余待卖出的数量。
订单信息中还包含state字段，表示当前订单的状态，有active、inactive、cancel，默认是active，则不显示。
active,表示当前有效的订单。inactive，表示订单已经撮合完成。cancel，表示订单已经被取消。

## 查询订单表状态
除了查询账户中包含的订单以外，还可以查询到订单表的状态，包括存在的交易对，指定交易对中所有的订单，交易对中的价格等。

#### 查询存在的交易对
通过 getMarketPairList 接口，查询存在的交易对
例子：
```text  
getMarketPairList
```
```text  
{
  "orderPair": [
    {
      "sell_token_id": "_",
      "buy_token_id": "1000001"
    }
  ]
}
```  
从返回的结果中看到，之前创建的第一笔订单，系统自动增加了一个TokenA和TRX的交易对。

#### 查询指定交易对的所有的订单
通过 GetMarketOrderListByPair sell_token_id buy_token_id 接口，查询交易对的所有的订单。
例子：
```text  
getMarketOrderListByPair _ 1000001
```
```text  
{
    "orders": [
        {
            "order_id": "fc9c64dfd48ae58952e85f05ecb8ec87f55e19402493bb2df501ae9d2da75db0",
            "owner_address": "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW",
            "create_time": 1578983490000,
            "sell_token_id": "_",
            "sell_token_quantity": 100,
            "buy_token_id": "1000001",
            "buy_token_quantity": 200,
            "sell_token_quantity_remain": 100
        }
    ]
}
``` 
#### 查询指定交易对的价格表
通过 GetMarketPriceByPair sell_token_id buy_token_id 接口，查询交易对的所有的价格。
例子：
```text  
GetMarketPriceByPair _ 1000001
```
```text  

{
  "sell_token_id": "_",
  "buy_token_id": "1000001",
  "prices": [
    {
      "sell_token_quantity": 1,
      "buy_token_quantity": 2
    }
  ]
}
``` 
其中prices列表，表示该交易对有的所有价格。

#### 根据OrderId查询订单详情
也可以通过 getMarketOrderById orderId 接口，直接查询订单详情。
例子：
```text  
getMarketOrderById e7e283c2066f6b82850dfb82d34fd9ec5ac2f70ae31b0669e96c1a9ad810a748
```
```text  
{
    "order_id": "e7e283c2066f6b82850dfb82d34fd9ec5ac2f70ae31b0669e96c1a9ad810a748",
    "owner_address": "TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz",
    "create_time": 1581344955000,
    "sell_token_id": "_",
    "sell_token_quantity": 100,
    "buy_token_id": "1000001",
    "buy_token_quantity": 200,
    "sell_token_quantity_remain": 100
}
``` 

## 创建第二笔订单，并发生撮合
在第一笔订单中，卖出TRX买入TokenA。在我们的第二笔订单中，用与第一笔订单相同的命令，但是这一次卖出TokenA买入的TRX，
也就是交换了买入卖出的Token。
例子：
```text  
MarketSellAsset TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz 1000001 400 _ 200
```
这里，订单中，卖出400个TokenA，买入200个TRX。第一笔订单中，卖出200个TRX，买入100个TokenA。
两个订单的价格是相同，发生撮合。其实，只要第二笔订单的价格高于第一笔订单，就能够发生撮合，这里为了方便计算数量，采用相同价格。
发生撮合后，可以查询transactionInfo中，来获得具体撮合信息。
```text  
gettransactioninfobyid 461276fcceb73760578a96692778918560d599fa7b71b3545c924e2518d5733b
```
```text  
{
...
"orderId": "5c83953fd64af67cb452171df5e0ff90ae8f348a6f5ba0c664613d21599dfb89",
    "orderDetails": [
        {
            "makerOrderId": "e7e283c2066f6b82850dfb82d34fd9ec5ac2f70ae31b0669e96c1a9ad810a748",
            "takerOrderId": "5c83953fd64af67cb452171df5e0ff90ae8f348a6f5ba0c664613d21599dfb89",
            "fillSellQuantity": 200,
            "fillBuyQuantity": 100
        }
    ]
}
```
其中，makerOrderId是第一笔订单的id，takerOrderId表示本次订单的id，fillSellQuantity表示撮合完成的卖出量，
这里是TokenA的卖出量，fillBuyQuantity表示撮合完成的买入量，这里是TRX的买入量。fillSellQuantity和fillBuyQuantity，也构成了本次撮合的价格。
如果本次订单和之前的多个订单发生了撮合，那么这里的orderDetails将是个列表，包含多个撮合信息。

再次使用 GetMarketOrderByAccount 接口查看账户拥有订单。

```text  
{
  "orders": [    
    {
      "order_id": "5c83953fd64af67cb452171df5e0ff90ae8f348a6f5ba0c664613d21599dfb89",
      "owner_address": "TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz",
      "create_time": 1578302487000,
      "sell_token_id": "1000001",
      "buy_token_id": "_",
      "sell_token_quantity": 400,
      "buy_token_quantity": 200,
      "sell_token_quantity_remain": 200
    }
  ]
}
```
这里只能看到第二笔订单的信息，第一个订单已经完全被撮合，不在账户订单中记录，可以通过getOrderById查看。
第二个订单部分被撮合，sell_token_quantity_remain为200


## 取消订单
使用 MarketCancelOrder ownerAddress orderId 接口，来取消订单，这里我们取消第二笔订单。
```text  
marketcancelorder  TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz 5c83953fd64af67cb452171df5e0ff90ae8f348a6f5ba0c664613d21599dfb89
```
此时，再次查询账户中的将返回空，表示账户中已经不包含正在进行的订单。

## 其他注意事项

1.撮合的价格。撮合的价格以之前存在的挂单为准，如上面的示例中，在发起第二笔订单时，撮合价格是按照第一笔价格。
如果第二笔订单的价格高于第一笔价格，第二笔订单实际获得token >= 订单中的buy_token数目。\
2、一个账户拥有的最大active订单数为100。\
3.由于链上合约执行时间的限制，无法在一笔交易中完成大量的撮合交易交易，所以有最大撮合数的限制，目前是20，超过这个数目的交易会执行错误。\
4.交易费。除了创建交易时消耗的带宽，其他的手续费为0，未来可通过提案修改。


相关api详情，请查询[http api](../api/http.md)。  