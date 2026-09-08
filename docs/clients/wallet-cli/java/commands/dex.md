# TRON-DEX 市场

链上订单市场——创建和取消卖单，以及查询订单、交易对和价格。

## MarketSellAsset

创建一个卖出资产的订单。

```console
> MarketSellAsset owner_address sell_token_id sell_token_quantity buy_token_id buy_token_quantity
```

- `ownerAddress`——发起交易的账户地址。
- `sell_token_id`、`sell_token_quantity`——要卖出的 token ID 和数量。
- `buy_token_id`、`buy_token_quantity`——要买入的 token ID 和数量。

示例：

```console
MarketSellAsset TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW  1000001 200 _ 100

用 getTransactionInfoById 命令获取合约执行结果：
getTransactionInfoById 10040f993cd9452b25bf367f38edadf11176355802baf61f3c49b96b4480d374

{
	"id": "10040f993cd9452b25bf367f38edadf11176355802baf61f3c49b96b4480d374",
	"blockNumber": 669,
	"blockTimeStamp": 1578983493000,
	"contractResult": [
		""
	],
	"receipt": {
		"net_usage": 264
	}
}
```

## GetMarketOrderByAccount

获取某个账户创建的订单（仅包含 active 状态）。

```console
> GetMarketOrderByAccount ownerAddress
```

`ownerAddress`——创建市场订单的账户地址。

示例：

```console
GetMarketOrderByAccount TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW
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

## GetMarketOrderById

按 `order_id` 获取指定订单。

```console
> GetMarketOrderById orderId
```

示例：

```console
GetMarketOrderById fc9c64dfd48ae58952e85f05ecb8ec87f55e19402493bb2df501ae9d2da75db0
{
	"order_id": "fc9c64dfd48ae58952e85f05ecb8ec87f55e19402493bb2df501ae9d2da75db0",
	"owner_address": "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW",
	"create_time": 1578983490000,
	"sell_token_id": "_",
	"sell_token_quantity": 100,
	"buy_token_id": "1000001",
	"buy_token_quantity": 200,
}
```

## GetMarketPairList

获取市场交易对列表。

```console
GetMarketPairList
{
	"orderPair": [
		{
			"sell_token_id": "_",
			"buy_token_id": "1000001"
		}
	]
}
```

## GetMarketOrderListByPair

按交易对获取订单列表。

```console
> GetMarketOrderListByPair sell_token_id buy_token_id
```

- `sell_token_id`——要卖出的 token ID。
- `buy_token_id`——要买入的 token ID。

示例：

```console
GetMarketOrderListByPair _ 1000001
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

## GetMarketPriceByPair

按交易对获取市场价格。

```console
> GetMarketPriceByPair sell_token_id buy_token_id
```

- `sell_token_id`——要卖出的 token ID。
- `buy_token_id`——要买入的 token ID。

示例：

```console
GetMarketPriceByPair _ 1000001
{
	"sell_token_id": "_",
	"buy_token_id": "1000001",
	"prices": [
		{
			"sell_token_quantity": 100,
			"buy_token_quantity": 200
		}
	]
}
```

## MarketCancelOrder

取消订单。

```console
> MarketCancelOrder owner_address order_id
```

- `owner_address`——创建该订单的账户地址。
- `order_id`——要取消的订单 ID。

示例：

```console
MarketCancelOrder TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW fc9c64dfd48ae58952e85f05ecb8ec87f55e19402493bb2df501ae9d2da75db0
```

用 `getTransactionInfoById` 命令获取合约执行结果：

```console
getTransactionInfoById b375787a098498623403c755b1399e82910385251b643811936d914c9f37bd27
{
	"id": "b375787a098498623403c755b1399e82910385251b643811936d914c9f37bd27",
	"blockNumber": 1582,
	"blockTimeStamp": 1578986232000,
	"contractResult": [
		""
	],
	"receipt": {
		"net_usage": 283
	}
}
```

## 另请参见

- [proposals](proposals.md)——链上治理提案
- [exchange](exchange.md)——内置的 Bancor 交易所
- [transfer-trc10](transfer-trc10.md)——发行被交易的 TRC10 资产
