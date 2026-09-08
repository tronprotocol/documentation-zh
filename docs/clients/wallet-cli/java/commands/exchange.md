# 交易所（Bancor）

内置的链上交易所。交易对的交易和由此产生的价格波动遵循 Bancor 协议。

## ExchangeCreate

创建交易对。

```console
> exchangeCreate [OwnerAddress] first_token_id first_token_balance second_token_id second_token_balance
```

- `OwnerAddress`（可选）——发起交易的账户地址。默认：登录账户的地址。
- `first_token_id`、`first_token_balance`——第一个 token 的 ID 和数量。
- `second_token_id`、`second_token_balance`——第二个 token 的 ID 和数量。ID 是已发行 TRC10 token
  的 ID。如果是 TRX，ID 为 `_`。数量必须大于 0，且小于 1,000,000,000,000,000。

示例：

```console
> exchangeCreate 1000001 10000 _ 10000
    # 创建 ID 为 1000001 与 TRX 的交易对，两者数量均为 10000。
```

## GetExchange

按 id 查询交易对（已确认状态）。

```console
> getExchange 1
```

## ExchangeInject

向交易对注入流动性。`quant` 指定其中一种 token 的注入量，另一种 token 的注入量由交易对当前的
储备比例计算；两种 token 都会从账户转入交易对。

```console
> exchangeInject [OwnerAddress] exchange_id token_id quant
```

- `OwnerAddress`（可选）——发起交易的账户地址。默认：登录账户的地址。
- `exchange_id`——要注资的交易对 ID。
- `token_id`、`quant`——注资的 tokenId 和数量（单位为基础单位）。

## ExchangeTransaction

```console
> exchangeTransaction [OwnerAddress] exchange_id token_id quant expected
```

- `OwnerAddress`（可选）——发起交易的账户地址。默认：登录账户的地址。
- `exchange_id`——交易对的 ID。
- `token_id`、`quant`——被兑换 token 的 ID 和数量，相当于卖出。
- `expected`——你愿意接受的、另一种 token 的最低到手数量。它是一个下限，而不是预测值：如果这笔兑换的实际返还低于该值，交易就会失败。它以另一种 token 计价，因此不能与 `quant` 比较大小。

示例：

```console
> ExchangeTransaction 1 1000001 100 80
```

该命令尝试在 ID 为 1 的交易对中卖出 100 个 ID 为 1000001 的 token，并至少获得 80 TRX。

## ExchangeWithdraw

从交易对撤出流动性。`quant` 指定其中一种 token 的撤出量，另一种 token 的撤出量由交易对当前的
储备比例计算；两种 token 都会从交易对转回账户。

```console
> exchangeWithdraw [OwnerAddress] exchange_id token_id quant
```

- `OwnerAddress`（可选）——发起交易的账户地址。默认：登录账户的地址。
- `Exchange_id`——要撤资的交易对 ID。
- `Token_id`、`quant`——撤资的 tokenId 和数量（单位为基础单位）。

## 获取交易对信息 {#obtain-information-on-trading-pairs}

- `ListExchanges`——列出交易对。
- `ListExchangesPaginated`——分页列出交易对。

## 另请参见

- [proposals](proposals.md)——链上治理提案
- [dex](dex.md)——TRON-DEX 订单市场
- [transfer-trc10](transfer-trc10.md)——发行被交易的 TRC10 资产
