# TronGrid

最新官方 TronGrid 文档位于 [https://developers.tron.network/docs/tron-grid-intro](https://developers.tron.network/docs/tron-grid-intro).

TronGrid提供运行在云端的客户端, 因而你自己本地不需要运行节点。TronGrid提供负载均衡的，安全的，可靠的的节点访问API。

TronGrid支持两种类型的API调用：

- FullNode & SolidityNode api

TronGrid支持所有的FullNode和SolidityNode的api调用，你只需要加上前缀：`https://api.trongrid.io/`，例如：

`https://api.trongrid.io/wallet/getnowblock`

- TronGrid v3 (TG3) api

示例：`https://api.trongrid.io/v1`

## 参数, 查询以及返回值

- TG3类型接口调用地址可以按照base58或者hex形式
- 查询参数可以按照驼峰或者下划线形式
- 所有返回的json数据按照下划线形式
- 在本文档中，我们优先使用base58和下划线形式

## 账户接口

1. 通过地址查询账户
*接口：*
`https://api.trongrid.io/v1/accounts/:address`
*参数：*
address: 账户的地址
*选项：*
`only_confirmed` 只查询已经被确认的区块。`true` | `false` 默认为false。
*示例：*
`https://api.trongrid.io/v1/accounts/TLCuBEirVzB6V4menLZKw1jfBTFMZbuKq7?only_confirmed=false`

2. 查询账户的交易信息
*接口：*
`https://api.trongrid.io/v1/accounts/:address/transactions`
*参数：*
address: 账户的地址
*选项：*
`only_confirmed` 只查询已经被确认的交易。 `true` | `false` 默认为false。
`only_unconfirmed` 只查询未被确认的交易。 `true` | `false` 默认为false。
`only_to` 只查询与目标地址相关的交易。 `true` | `false` 默认为false。
`only_from` 只查询与源地址相关的交易。 `true` | `false` 默认为false。
`limit` 分页查询交易，每页的数目。默认`20`。最大`200`。
`fingerprint` 上一页返回的最后一笔交易的指纹。
`order_by` 排序方案。`order_by=block_number,asc`, `order_by=block_timestamp,desc`。`min_block_timestamp` 交易时间戳最小值为`0`。 `max_block_timestamp` 交易时间戳最大值为`now`。

*示例：*
`https://api.trongrid.io/v1/accounts/TLCuBEirVzB6V4menLZKw1jfBTFMZbuKq/transactions?only_to=true&only_from=true`

3. 查询账户资源信息
*接口：*
`https://api.trongrid.io/v1/accounts/:address/resources`
*参数：*
address: 账户的地址
*示例：*
`https://api.trongrid.io/v1/accounts/TLCuBEirVzB6V4menLZKw1jfBTFMZbuKq/resources`

## 通证接口

1. 查询所有通证信息
*接口：*
`https://api.trongrid.io/v1/assets`
*选项：*
`order_by` 排序方案。支持字段：`total_supply,asc` | `total_supply,desc`, `start_time,asc` | `start_time,desc`, `end_time,asc` | `end_time,desc`, `id,asc` | `id,desc`. 例如：`order_by=total_supply,asc`。

2. 按照标识符查询通证信息
*接口：*
`https://api.trongrid.io/v1/assets/:identifier`
*参数：*
identifier: 可以为通证id或者发行者的地址

3. 按照通证名称查询通证信息
*接口：*
`https://api.trongrid.io/v1/assets/:name/list`
*参数：*
name: 通证名称。
*选项：*
`limit` 分页查询交易，每页的数目。默认`20`。最大`200`。
`fingerprint` 上一页返回的最后一笔交易的指纹。
`order_by` 排序方案。支持字段 `order_by=total_supply,asc`，`order_by=start_time,desc`。

## 区块接口

1.&nbsp;查询一个区块中的事件信息
*接口：*
`https://api.trongrid.io/v1/blocks/:identifier/events`
*参数：*
identifier: 区块高度。

## 合约接口

1. 根据合约地址查询事件信息
*接口：*
`https://api.trongrid.io/v1/contracts/:address/events`
*参数：*
address: 合约地址。
*选项：*
`only_confirmed` 只显示已经确认过的事件。`true` | `false` 默认为`false`。
`only_unconfirmed` 只显示未确认过的事件。`true` | `false` 默认为`false`。
`event_name` 事件的名称。
`block_number` 事件所在的区块高度。
`min_block_timestamp` 区块时间戳最小值。默认为`0`。
`max_block_timestamp` 区块时间戳最大值。默认为`now`。
`limit` 分页查询交易，每页的数目。默认`20`。最大`200`。
`fingerprint` 上一页返回的最后一笔交易的指纹。
`order_by` 排序方案。自持字段 `block_timestamp,asc`, `block_timestamp,desc`。

2. 查询合约地址的交易信息
*接口：*
`https://api.trongrid.io/v1/contracts/:address/transactions`
*参数：*
address: 合约地址。
*选项：*
`only_confirmed` 只显示已经确认过的交易。 `true` | `false` 默认为 `false`。
`only_unconfirmed` 只显示未确认过的交易。 `true` | `false` 默认为 `false`。
`min_block_timestamp` 区块时间戳最小值。默认为 `0`。
`max_block_timestamp` 区块时间戳最大值。默认为 `now`。
`limit` 分页查询交易，每页的数目。默认`20`。最大`200`。
`fingerprint` 上一页返回的最后一笔交易的指纹。
`order_by` 排序方案。自持字段 `block_timestamp,asc`, `block_timestamp,desc`。

## 交易接口

1. 根据交易ID查询交易信息
*接口：*
`https://api.trongrid.io/v1/transactions/:id`
*参数：*
id: 交易ID。

2. 根据交易ID查询交易中的事件
*A接口：*
`https://api.trongrid.io/v1/transactions/:id/events`
*参数：*
id: 交易ID。
