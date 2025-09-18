# jsonRPC API

## 概述

JSON-RPC 是一种无状态、轻量级的远程过程调用（RPC）协议，TRON 网络提供了一套与以太坊兼容的 JSON-RPC API。

尽管 API 在设计上保持了高度兼容性，但由于 TRON 与以太坊在底层账户模型、资源模型和共识机制上存在差异，部分接口的行为会有所不同。同时，TRON 也扩展了部分自定义接口以支持其特有的交易类型。

### 如何启用或禁用节点的 JSON-RPC 服务

默认情况下，java-tron 节点的 JSON-RPC 服务是禁用的。您必须在节点的 [配置文件](https://github.com/tronprotocol/java-tron/blob/develop/framework/src/main/resources/config.conf) 中明确启用它。  
```
node.jsonrpc {  
    httpFullNodeEnable = true  
    httpFullNodePort = 8545  
    httpSolidityEnable = true  
    httpSolidityPort = 8555  
}
```

### HEX 值编码

在 JSON-RPC 交互中，所有数据均通过十六进制字符串传递，但遵循两种不同的格式化规则：

* **QUANTITIES (数值类型)**

   - 描述: 用于表示整数，如区块号、余额、数量等。
   - 格式: 以 `0x` 为前缀的十六进制，采用最紧凑的表示法（即没有前导零）。唯一的例外是零，必须表示为 `0x0`.
   - 示例:
       -  `0x41` (十进制 65)
       -  `0x400` (十进制 1024)
       -  错误: `0x0400` (不允许前导零)
       -  错误: `ff` (必须有 `0x` 前缀)

* **UNFORMATTED DATA (非格式化数据)**

  - 描述: 用于表示字节数组，如地址、哈希、字节码等。
  - 格式: 以 `0x` 为前缀，每个字节由两个十六进制字符表示。
  - 示例:
       -  `0x41` (1 字节数据)
       -  `0x004200` (3 字节数据)
       -  `0x` (0 字节数据)
       -  错误: `0xf0f0f` (必须是偶数位)
       -  错误: `004200` (必须有 `0x` 前缀)

## eth

### eth_accounts

*返回客户端拥有的地址列表。*

**参数：**  无

**返回值：**  空列表

**注意**: 与 Geth 等以太坊客户端不同，TRON 节点不负责管理私钥或账户。因此，此接口仅为兼容性而存在，不具备实际功能。
 
**示例**

``` curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '
{"jsonrpc": "2.0", "id": 1, "method": "eth_accounts", "params": []}'

#返回
{"jsonrpc":"2.0","id":1,"result":[]}
```


### eth_blockNumber

*返回节点已同步的最新区块的高度。*

**参数：**  无

**返回值：** QUANTITY - 最新的区块号。

**示例**
```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":64}'

#返回
{"jsonrpc":"2.0","id":64,"result":"0x20e0cf0"}

```

### eth_call

*在节点上本地模拟执行一笔交易，但不会将其广播上链。主要用于调用智能合约的view或pure函数，或在发送前预估交易结果。*

**参数：**

1. Object - 交易调用对象，包含以下字段：

| 项名称 | 数据类型      | 描述                                                   |
| :-------- | :------------- | :------------------------------------------------------------ |
| from      | DATA, 20 Bytes | 调用者地址。十六进制格式地址，为了兼容eth，所有地址既可以是TRON 十六进制地址，也可以是eth地址    |
| to        | DATA, 20 Bytes | 合约地址。十六进制格式地址 |
| gas       | QUANTITY       | 不支持。值为 0x0                               |
| gasPrice  | QUANTITY       | 不支持。值为 0x0                               |
| value     | QUANTITY       | 不支持。值为 0x0                               |
| data      | DATA           | 方法签名和编码参数的哈希。          |

2. QUANTITY|TAG - 区块标识符，目前仅支持 "latest"。

**返回值：** DATA - 合约函数执行的返回值，经过ABI编码。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
	"jsonrpc": "2.0",
	"method": "eth_call",
	"params": [{
		"from": "0xF0CC5A2A84CD0F68ED1667070934542D673ACBD8",
		"to": "0x70082243784DCDF3042034E7B044D6D342A91360",
		"gas": "0x0",
		"gasPrice": "0x0",
		"value": "0x0",
		"data": "0x70a08231000000000000000000000041f0cc5a2a84cd0f68ed1667070934542d673acbd8"
	}, "latest"],
	"id": 1
}'

#返回
{"jsonrpc":"2.0","id":1,"result":"0x"}

```


### eth_chainId

*返回TRON网络的chainId，即创世区块哈希的最后四个字节。*

**参数：**  无

**返回值：**  DATA - TRON网络的chainId

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":79}'

#返回
{"jsonrpc":"2.0","id":79,"result":"0x2b6653dc"}

```


### eth_coinbase

*返回当前节点的超级代表地址。*

**参数：**  无

**返回值：**  DATA - 节点的超级代表地址。（注意：如果配置了多个超级代表地址，则返回第一个地址；如果没有有效地址或地址未生成任何区块，则返回错误，错误信息为“etherbase must be explicitly specified”。）

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc": "2.0", "id": 1, "method": "eth_coinbase", "params": []}'

#返回
{"jsonrpc":"2.0","id":1,"error":{"code":-32000,"message":"etherbase must be explicitly specified","data":"{}"}}
```


### eth_estimateGas

*预估执行一笔交易所需要消耗的能量 (Energy)。*

**参数**  

1. object - 交易调用对象，包含以下项：

| 项名称 | 数据类型      | 描述                                          |
| :-------- | :------------- | :--------------------------------------------------- |
| from      | DATA, 20 Bytes | 发送方地址                                |
| to        | DATA, 20 Bytes | 接收方地址或合约地址                              |
| gas       | QUANTITY       | 未使用                                              |
| gasPrice  | QUANTITY       | 未使用                                              |
| value     | QUANTITY       | 交易发送的TRX数量 (单位: sun)。      |
| data      | DATA           | 方法签名和编码参数的哈希 |

**返回值：**  QUANTITY - 预估消耗的能量 (Energy) 数量。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
	"jsonrpc": "2.0",
	"id": 1,
	"method": "eth_estimateGas",
	"params": [{
		"from": "0x41F0CC5A2A84CD0F68ED1667070934542D673ACBD8",
		"to": "0x4170082243784DCDF3042034E7B044D6D342A91360",
		"gas": "0x01",
		"gasPrice": "0x8c",
		"value": "0x01",
		"data": "0x70a08231000000000000000000000041f0cc5a2a84cd0f68ed1667070934542d673acbd8"
	}]
}'

#返回
{"jsonrpc":"2.0","id":1,"result":"0x0"}
```


### eth_gasPrice

*返回当前网络中能量 (Energy) 的价格（单位：sun）。*

**参数：**  无

**返回值：**  QUANTITY - 当前的能量价格，单位为 sun。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc": "2.0", "id": 1, "method": "eth_gasPrice", "params": []}'

#返回
{"jsonrpc":"2.0","id":1,"result":"0x8c"}
```

### eth_getBalance

*返回指定地址的TRX余额。*

**参数：**

1. DATA, 20 Bytes - 要查询余额的账户地址。
2. QUANTITY|TAG - 区块标识符，目前仅支持 "latest"。

**返回值：** QUANTITY - 指定地址的 TRX 余额，单位为 sun。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
	"jsonrpc": "2.0",
	"method": "eth_getBalance",
	"params": ["0x41f0cc5a2a84cd0f68ed1667070934542d673acbd8", "latest"],
	"id": 64
}'

#返回
{"jsonrpc":"2.0","id":64,"result":"0x492780"}
```


### eth_getBlockByHash

*通过区块哈希返回区块的详细信息。*

**参数：**

1. DATA, 32 Bytes - 区块的哈希。
2. Boolean - `true` 表示返回完整的交易对象列表；`false` 表示仅返回交易的哈希列表。

**返回值：** `Object` - 区块对象。如果未找到区块，则返回 `null`。
区块对象包含以下项:

| 项名称        | 数据类型       | 描述                                                                                         |
| :--------------- | :-------------- | :-------------------------------------------------------------------------------------------------- |
| number           | QUANTITY        | 区块号                                                                                        |
| hash             | DATA, 32 Bytes  | 区块哈希                                                                                   |
| parentHash       | DATA, 32 Bytes  | 父区块哈希                                                                            |
| nonce            | QUANTITY        | 未使用                                                                                              |
| sha3Uncles       | DATA, 32 Bytes  | 仅用于兼容以太坊 JSON-RPC 接口，无实际意义 |
| logsBloom        | DATA, 256 Bytes | 仅用于兼容以太坊 JSON-RPC 接口，无实际意义                  |
| transactionsRoot | DATA, 32 Bytes  | 区块交易树的根                                                       |
| stateRoot        | DATA, 32 Bytes  | 目前无实际意义                                                      |
| receiptsRoot     | DATA, 32 Bytes  | 目前无实际意义                                                       |
| miner            | DATA, 20 Bytes  | 生产这个区块的 SR 地址                               |
| difficulty       | QUANTITY        | 目前无实际意义                                                       |
| totalDifficulty  | QUANTITY        | 目前无实际意义                                      |
| extraData        | DATA            | 目前无实际意义                                                                |
| size             | QUANTITY        | 该区块的大小（单位：字节）                                                             |
| gasLimit         | QUANTITY        | 该区块允许的最大 gas                                                               |
| gasUsed          | QUANTITY        | 该区块中所有交易使用的总 gas                                                |
| timestamp        | QUANTITY        | 区块创建时的 Unix 时间戳，单位为秒。                              |
| transactions     | Array           | 交易对象数组，或根据最后一个参数返回的 32 字节交易哈希。 |
| uncles           | Array           | 目前无实际意义                                                                             |

**示例**
```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
	"jsonrpc": "2.0",
	"method": "eth_getBlockByHash",
	"params": ["0x00000000035dc7288bbde648318b5e42fcd3301ab1a4d12c853910af0ab214d2", false],
	"id": 1
}'

#返回
{"jsonrpc":"2.0","id":1,"result":null}
```


### eth_getBlockByNumber

*通过区块高度返回区块的详细信息。*

**参数：**

1. QUANTITY|TAG - 区块高度，或标签 "earliest", "latest"。
2. Boolean - true 表示返回完整的交易对象列表；false 表示仅返回交易的哈希列表。

**返回值：**  Object - 区块对象。如果未找到区块，则返回 null。结构参见 [eth_getBlockByHash](https://developers.tron.network/reference#eth_getblockbyhash)

**示例**
```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
	"jsonrpc": "2.0",
	"method": "eth_getBlockByNumber",
	"params": ["0xF9CC56", true],
	"id": 1
}'

#返回
{"jsonrpc":"2.0","id":1,"result":null}
```


### eth_getBlockTransactionCountByHash

*返回指定区块哈希中的交易数量。*

**参数：** DATA, 32 Bytes - 区块的哈希。

**返回值：** QUANTITY - 该区块中的交易数量。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
	"jsonrpc": "2.0",
	"id": 1,
	"method": "eth_getBlockTransactionCountByHash",
	"params": ["0x00000000020ef11c87517739090601aa0a7be1de6faebf35ddb14e7ab7d1cc5b"]
}'

#返回
{"jsonrpc":"2.0","id":1,"result":"0x39"}
```


### eth_getBlockTransactionCountByNumber

*返回指定区块高度中的交易数量。*

**参数：**  QUANTITY|TAG - 区块高度，或标签 `"earliest"`, `"latest"`。

**返回值：**  QUANTITY - 该区块中的交易数量。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
	"jsonrpc": "2.0",
	"method": "eth_getBlockTransactionCountByNumber",
	"params": ["0xF96B0F"],
	"id": 1
}'

#返回
{"jsonrpc":"2.0","id":1,"result":"0x23"}
```


### eth_getCode

*返回指定合约地址**运行时**字节码。*

**参数：**

1. `DATA, 20 Bytes` - 合约地址。
2. `QUANTITY|TAG` - 区块标识符，目前仅支持 `"latest"`。

**返回值：** 
`DATA` - 运行时字节码。如果地址不是合约，则返回 `0x`。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
	"jsonrpc": "2.0",
	"method": "eth_getCode",
	"params": ["0x4170082243784DCDF3042034E7B044D6D342A91360", "latest"],
	"id": 64
}'

#返回
{"jsonrpc":"2.0","id":64,"result":"0x"}
```

### eth_getStorageAt

*返回给定地址的存储位置的值。可用于获取合约中变量的值。*

**参数：**

1. `DATA, 20 Bytes` - 合约地址。
2. `QUANTITY` - 存储槽的位置索引。
3. `QUANTITY|TAG` - 区块标识符，目前仅支持 `"latest"`。

**返回值：**
`DATA` - 该存储槽位置的32字节数据。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
	"jsonrpc": "2.0",
	"method": "eth_getStorageAt",
	"params": ["0xE94EAD5F4CA072A25B2E5500934709F1AEE3C64B", "0x29313b34b1b4beab0d3bad2b8824e9e6317c8625dd4d9e9e0f8f61d7b69d1f26", "latest"],
	"id": 1
}'

#返回
{"jsonrpc":"2.0","id":1,"result":"0x0000000000000000000000000000000000000000000000000000000000000000"}
```


### eth_getTransactionByBlockHashAndIndex

*通过区块哈希和交易在区块中的索引，返回交易的详细信息。*

**参数：**

1. `DATA, 32 Bytes` - 区块的哈希。
2. `QUANTITY` - 交易在区块中的索引。

**返回值：**
`Object` - 交易对象。如果未找到，则返回 `null`。
交易对象包含以下项：

| 项名称        | 数据类型      | 描述                                             |
| :--------------- | :------------- | :------------------------------------------------------ |
| blockHash        | DATA, 32 Bytes | 交易所在区块的哈希        |
| blockNumber      | QUANTITY       | 交易所在区块的区块号             |
| from             | DATA, 20 Bytes | 发送方地址                                   |
| gas              | QUANTITY       | 交易消耗的能量（Energy）                                                |
| gasPrice         | QUANTITY       | 能量 (Energy)价格                                            |
| hash             | DATA, 32 Bytes | 交易哈希                                 |
| input            | DATA           | 随交易发送的数据                |
| nonce            | QUANTITY       | 未使用                                                  |
| to               | DATA, 20 Bytes | 接收方地址                                 |
| transactionIndex | QUANTITY       | 交易在区块中的索引位置 |
| type | QUANTITY       | 交易类型，当前TRON网络上的交易都是普通交易，值为0  |
| value            | QUANTITY       | 转账金额（单位：sun）                                |
| v                | QUANTITY       | ECDSA 恢复 id                                       |
| r                | DATA, 32 Bytes | ECDSA 签名 r                                       |
| s                | DATA, 32 Bytes | ECDSA 签名 s                                       |

**示例**

```
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
	"jsonrpc": "2.0",
	"method": "eth_getTransactionByBlockHashAndIndex",
	"params": ["00000000020ef11c87517739090601aa0a7be1de6faebf35ddb14e7ab7d1cc5b", "0x0"],
	"id": 64
}'

#返回
{
	"jsonrpc": "2.0",
	"id": 64,
	"result": {
		"blockHash": "0x00000000020ef11c87517739090601aa0a7be1de6faebf35ddb14e7ab7d1cc5b",
		"blockNumber": "0x20ef11c",
		"from": "0xb4f1b6e3a1461266b01c2c4ff9237191d5c3d5ce",
		"gas": "0x0",
		"gasPrice": "0x8c",
		"hash": "0x8dd26d1772231569f022adb42f7d7161dee88b97b4b35eeef6ce73fcd6613bc2",
		"input": "0x",
		"nonce": null,
		"r": "0x6212a53b962345fb8ab02215879a2de05f32e822c54e257498f0b70d33825cc5",
		"s": "0x6e04221f5311cf2b70d3aacfc444e43a5cf14d0bf31d9227218efaabd9b5a812",
		"to": "0x047d4a0a1b7a9d495d6503536e2a49bb5cc72cfe",
		"transactionIndex": "0x0",
		"type": "0x0",
		"v": "0x1b",
		"value": "0x203226"
	}
}
```


### eth_getTransactionByBlockNumberAndIndex

*通过区块高度和交易在区块中的索引，返回交易的详细信息。*

**参数：**

1. `QUANTITY|TAG` - 区块高度，或标签 `"earliest"`, `"latest"`。
2. `QUANTITY` - 交易在区块中的索引。

**返回值：**
`Object` - 交易对象。如果未找到，则返回 `null`。交易对象结构参见 [eth_getTransactionByBlockHashAndIndex](#eth_gettransactionbyblockhashandindex)

**示例**
```
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
	"jsonrpc": "2.0",
	"method": "eth_getTransactionByBlockNumberAndIndex",
	"params": ["0xfb82f0", "0x0"],
	"id": 64
}'

#返回
{"jsonrpc":"2.0","id":64,"result":null}
```


### eth_getTransactionByHash

*通过交易哈希返回交易的详细信息。*

**参数：**
`DATA, 32 Bytes` - 交易的哈希。

**返回值：**
`Object` - 交易对象。如果未找到，则返回 `null`。交易对象结构参见 [eth_getTransactionByBlockHashAndIndex](#eth_gettransactionbyblockhashandindex)

**示例**
```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
	"jsonrpc": "2.0",
	"method": "eth_getTransactionByHash",
	"params": ["c9af231ad59bcd7e8dcf827afd45020a02112704dce74ec5f72cb090aa07eef0"],
	"id": 64
}'

#返回
{
	"jsonrpc": "2.0",
	"id": 64,
	"result": {
		"blockHash": "0x00000000020ef11c87517739090601aa0a7be1de6faebf35ddb14e7ab7d1cc5b",
		"blockNumber": "0x20ef11c",
		"from": "0x6eced5214d62c3bc9eaa742e2f86d5c516785e14",
		"gas": "0x0",
		"gasPrice": "0x8c",
		"hash": "0xc9af231ad59bcd7e8dcf827afd45020a02112704dce74ec5f72cb090aa07eef0",
		"input": "0x",
		"nonce": null,
		"r": "0x433eaf0a7df3a08c8828a2180987146d39d44de4ac327c4447d0eeda42230ea8",
		"s": "0x6f91f63b37f4d1cd9342f570205beefaa5b5ba18d616fec643107f8c1ae1339d",
		"to": "0x0697250b9d73b460a9d2bbfd8c4cacebb05dd1f1",
		"transactionIndex": "0x6",
		"type": "0x0",
		"v": "0x1b",
		"value": "0x1cb2310"
	}
}
```


### eth_getTransactionReceipt

*通过交易哈希返回交易的收据信息。收据包含了交易的执行结果、事件日志、消耗的资源等。请参考 http api: [wallet/gettransactioninfobyid](#walletgettransactioninfobyid)*

**参数：**
`DATA, 32 Bytes` - 交易的哈希。

**返回值：**
`Object` - 交易收据对象。如果交易未确认或不存在，则返回 `null`。
交易收据对象包含以下项：

| 项名称         | 数据类型       | 描述                                                                               |
| :---------------- | :-------------- | :---------------------------------------------------------------------------------------- |
| transactionHash   | DATA, 32 Bytes  | 交易哈希                                                                   |
| transactionIndex  | QUANTITY        | 交易在区块中的索引位置                                   |
| blockHash         | DATA, 32 Bytes  | 交易所在区块的哈希                                          |
| blockNumber       | QUANTITY        | 交易所在区块的区块号                                               |
| from              | DATA, 20 Bytes  | 发送方地址                                                                     |
| to                | DATA, 20 Bytes  | 接收方地址                                                                   |
| cumulativeGasUsed | QUANTITY        | 当前区块在执行完该交易时，当前区块所消耗的总能量             |
| gasUsed           | QUANTITY        | 该交易消耗的能量(Energy)总量                                |
| contractAddress   | DATA, 20 Bytes  | 如果交易是合约创建，则为创建的合约地址，否则为 `null`。 |
| logs              | Array           | 该交易生成的日志对象数组                                   |
| logsBloom         | DATA, 256 Bytes | 用于轻客户端快速检索相关日志的布隆过滤器                          |
| root              | DATA            | 交易后的状态根（Byzantium 之前）                                    |
| status            | QUANTITY        | 1（成功）或 0（失败）                                                         |
| type            | QUANTITY        | 交易类型，当前 TRON 网络上的交易都是普通交易，值为 0                   |

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
	"jsonrpc": "2.0",
	"method": "eth_getTransactionReceipt",
	"params": ["c9af231ad59bcd7e8dcf827afd45020a02112704dce74ec5f72cb090aa07eef0"],
	"id": 64
}'

#返回
{
	"jsonrpc": "2.0",
	"id": 64,
	"result": {
		"blockHash": "0x00000000020ef11c87517739090601aa0a7be1de6faebf35ddb14e7ab7d1cc5b",
		"blockNumber": "0x20ef11c",
		"contractAddress": null,
		"cumulativeGasUsed": "0x646e2",
		"effectiveGasPrice": "0x8c",
		"from": "0x6eced5214d62c3bc9eaa742e2f86d5c516785e14",
		"gasUsed": "0x0",
		"logs": [],
		"logsBloom": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
		"status": "0x1",
		"to": "0x0697250b9d73b460a9d2bbfd8c4cacebb05dd1f1",
		"transactionHash": "0xc9af231ad59bcd7e8dcf827afd45020a02112704dce74ec5f72cb090aa07eef0",
		"transactionIndex": "0x6",
		"type": "0x0"
	}
}
```


### eth_getWork

*返回当前区块的哈希。*

**参数：**  无

**返回值：**  
`Array` - 包含三个元素的数组，只有第一个元素（区块哈希）有效。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
	"jsonrpc": "2.0",
	"method": "eth_getWork",
	"params": [],
	"id": 73
}'

#返回
{
	"jsonrpc": "2.0",
	"id": 73,
	"result": ["0x00000000020e73915413df0c816e327dc4b9d17069887aef1fff0e854f8d9ad0", null, null]
}
```


### eth_protocolVersion

*返回节点的TRON协议版本。*

**参数：**  无

**返回值：**  `String` - 当前协议的版本号。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_protocolVersion","params":[],"id":64}'

#返回
{"jsonrpc":"2.0","id":64,"result":"0x16"}
```


### eth_syncing

*返回节点的同步状态。*

**参数：**  无

**返回值：**  

`Object` 或 `Boolean` -  如果节点正在同步，返回一个包含 `startingBlock`, `currentBlock`, 和 `highestBlock` 的对象。如果已同步完成，返回 `false`，详细项介绍：

|               |          |                                                                                             |
| :------------ | :------- | :------------------------------------------------------------------------------------------ |
| startingBlock | QUANTITY | 当前开始同步的起始区块 |
| currentBlock  | QUANTITY | 当前区块                                                                           |
| highestBlock  | QUANTITY | 预估的最高区块                                                                 |

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_syncing","params":[],"id":64}'

#返回
{
    "jsonrpc": "2.0",
	"id": 64,
	"result": {
		"startingBlock": "0x20e76cc",
		"currentBlock": "0x20e76df",
		"highestBlock": "0x20e76e0"
	}
}
```


### eth_newFilter

*创建一个用于监听事件日志（Event Logs）的过滤器。*

**参数：**  

1. `Object` - 过滤器选项对象:

| 字段     | 类型                  | 描述                                                               |
| :-------- | :-------------------- | :------------------------------------------------------------------------ |
| fromBlock | QUANTITY\|TAG         | 整数区块号，或 "latest"，或 "earliest"                                         |
| toBlock   | QUANTITY\|TAG         | 整数区块号，或 "latest"，或 "earliest"                                         |
| address   | DATA\|Array, 20 Bytes | 要监听的合约地址，可以是单个地址或地址数组，用于过滤来源于这些地址的日志 |
| topics    | Array of DATA         | 用于过滤事件的主题数组，每个主题为 32 字节的 DATA。主题的顺序很重要。每个主题位置也可以是一个 DATA 数组，表示"或"的关系（匹配数组中任意一个值）                                                                 |

**返回值：**  
`QUANTITY` - 新创建的过滤器 ID。

**示例**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_newFilter","params":[{"address":["cc2e32f2388f0096fae9b055acffd76d4b3e5532","E518C608A37E2A262050E10BE0C9D03C7A0877F3"],"fromBlock":"0x989680","toBlock":"0x9959d0","topics":["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",null,["0x0000000000000000000000001806c11be0f9b9af9e626a58904f3e5827b67be7","0x0000000000000000000000003c8fb6d064ceffc0f045f7b4aee6b3a4cefb4758"]]}],"id":1}'

#返回
{"jsonrpc":"2.0","id":1,"result":"0x2bab51aee6345d2748e0a4a3f4569d80"}
```


### eth_newBlockFilter

*创建一个用于监听新区块的过滤器。*

**参数：**  无。

**返回值：**  
`QUANTITY` - 新创建的过滤器 ID。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_newBlockFilter","params":[],"id":1}'

#返回
{"jsonrpc":"2.0","id":1,"result":"0x2bab51aee6345d2748e0a4a3f4569d80"}
```


### eth_getFilterChanges

*轮询过滤器，返回自上次轮询以来发生的日志或者区块数组。*

**参数**  
`QUANTITY` - 由 `eth_newFilter` 或 `eth_newBlockFilter` 创建的过滤器ID。

**返回值**
- 对于使用 `eth_newFilter` 创建的过滤器，返回日志对象列表，每个日志对象包含以下参数：

| 字段            | 类型           | 描述                                                                                 |
| :--------------- | :------------- | :------------------------------------------------------------------------------------------ |
| removed          | TAG            | 如果日志由于链重组被移除则为 true。如果是有效日志则为 false。     |
| logIndex         | QUANTITY       | 日志在区块中的索引位置。如果是待处理日志则为 null。                  |
| transactionIndex | QUANTITY       | 创建日志的交易索引位置。如果是待处理日志则为 null。 |
| transactionHash  | DATA, 32Bytes  | 创建日志的交易哈希。                                         |
| blockHash        | DATA, 32 Bytes | 日志所在区块的哈希。如果是待处理日志则为 null。                             |
| blockNumber      | QUANTITY       | 日志所在区块的区块号。                                                     |
| address          | DATA, 32 Bytes | 日志来源的地址。                                                     |
| data             | DATA           | 包含一个或多个 32 字节的非索引日志参数。                             |
| topics           | DATA\[]        | 事件主题和索引参数。                                                          |

- 对于使用 `eth_newBlockFilter` 创建的过滤器，返回区块哈希列表。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
    "jsonrpc": "2.0",
    "method": "eth_getFilterChanges",
    "params": [     "0xc11a84d5e906ecb9f5c1eb65ee940b154ad37dce8f5ac29c80764508b901d996"
    ],
    "id": 71
}'

#返回
{
    "jsonrpc": "2.0",
    "id": 71,
    "error": {
        "code": -32000,
        "message": "filter not found",
        "data": "{}"
    }
}
```


### eth_getFilterLogs

*返回指定日志过滤器的所有历史匹配日志。*

**参数**  
`QUANTITY` - 由 `eth_newFilter` 创建的过滤器ID。

**返回值**
`Array` - 事件日志对象数组，参见 [eth_getFilterChanges](#eth_getfilterchanges)。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
    "jsonrpc": "2.0",
    "method": "eth_getFilterLogs",
    "params": [      "0xc11a84d5e906ecb9f5c1eb65ee940b154ad37dce8f5ac29c80764508b901d996"
    ],
    "id": 71
}'

#返回
{
    "jsonrpc": "2.0",
    "id": 71,
    "error": {
        "code": -32000,
        "message": "filter not found",
        "data": "{}"
    }
}
```


### eth_uninstallFilter

*卸载给定 ID 的过滤器。当不再需要监视时应始终调用此方法。此外，如果过滤器在一段时间内未通过 `eth_getFilterChanges` 请求，则会超时。*

**参数：**  
`QUANTITY` - 要卸载的过滤器 ID。

**返回值：**
`Boolean` - 如果成功卸载，返回 `true`，否则返回 `false`。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
    "jsonrpc": "2.0",
    "method": "eth_uninstallFilter",
    "params": [     "0xc11a84d5e906ecb9f5c1eb65ee940b154ad37dce8f5ac29c80764508b901d996"
 ],
    "id": 71
}'

#返回
{
    "jsonrpc": "2.0",
    "id": 71,
    "result": true
}
```


### eth_getLogs

*返回与给定过滤器对象匹配的所有日志数组。*

**参数**  
`Object` - 过滤器选项对象，与 `eth_newFilter` 相同，但可以额外包含 `blockhash` 字段以查询特定区块。包括以下字段：

| 字段     | 类型                  | 描述                                                                                                                      |
| :-------- | :-------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| fromBlock | QUANTITY\|TAG         | （可选，默认："latest"）整数区块号，或 "latest" 表示最新的区块                                          |
| toBlock   | QUANTITY\|TAG         | （可选，默认："latest"）整数区块号，或 "latest" 表示最新的区块                                          |
| address   | DATA\|Array, 20 Bytes | （可选）合约地址或日志应源自的地址列表。                                             |
| topics    | Array of DATA         | （可选）32 字节 DATA 主题数组。主题是顺序相关的。每个主题也可以是具有 "or" 选项的 DATA 数组。 |
| blockhash | DATA, 32 Bytes        | （可选）区块哈希 ，注意：blockHash和fromBlock/toBlock不可以同时指定，否则报错：`cannot specify both BlockHash and FromBlock/ToBlock, choose one or the other`                                                                                                          |

**返回值**
`Array` - 事件日志对象数组，参见 [eth_getFilterChanges](#eth_getfilterchanges)。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_getLogs","params":[{"address":["cc2e32f2388f0096fae9b055acffd76d4b3e5532","E518C608A37E2A262050E10BE0C9D03C7A0877F3"],"fromBlock":"0x989680","toBlock":"0x9959d0","topics":["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",null,["0x0000000000000000000000001806c11be0f9b9af9e626a58904f3e5827b67be7","0x0000000000000000000000003c8fb6d064ceffc0f045f7b4aee6b3a4cefb4758"]]}],"id":1}'

#返回
{
    "jsonrpc": "2.0",
    "id": 71,
    "result": []
}
```

## net

### net_listening

*检查节点是否正在监听网络连接。*

**参数：**  无

**返回值：**  
`Boolean` - 如果正在监听，则为 `true`，否则为 `false`。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"net_listening","params":[],"id":64}'

#返回
{"jsonrpc":"2.0","id":64,"result":true}
```


### net_peerCount

*返回当前连接的对等节点（Peers）数量。*

**参数：**  无

**返回值：**  
`QUANTITY` - 已连接的对等节点数量。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"net_peerCount","params":[],"id":64}'

#返回
{"jsonrpc":"2.0","id":64,"result":"0x9"}
```


### net_version

*返回创世区块的哈希值。*

**参数：**  无

**返回值：**  
`String` - 网络ID（Chain ID）。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"net_version","params":[],"id":64}'

#返回
{"jsonrpc":"2.0","id":64,"result":"0x2b6653dc"}
```

## web3

### web3_clientVersion

*返回节点的客户端版本信息。*

**参数：**  无

**返回值：**  
`String` - 客户端版本。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc": "2.0", "id": 1, "method": "web3_clientVersion", "params": []}'

#返回
{"jsonrpc":"2.0","id":1,"result":"TRON/v4.8.0/Linux/Java1.8"}
```


### web3_sha3

*返回给定数据的 Keccak-256 哈希值（非标准化的 SHA3-256）。*

**参数**  
`DATA` - 要进行哈希运算的数据。

**返回**  
`DATA` - 32字节的Keccak-256哈希结果。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc": "2.0", "id": 1, "method": "web3_sha3", "params": ["0x68656c6c6f20776f726c64"]}'

#返回
{"jsonrpc":"2.0","id":1,"result":"0x47173285a8d7341e5e972fc677286384f802f8ef42a5ec5f03bbfa254cb01fad"}
```

## buildTransaction

*这是一个TRON**自定义**的 RPC 方法，用于便捷地创建 TRON 原生交易，返回未签名的交易对象，不同类型的交易具有不同的参数。*

### TransferContract (TRX 转账)

**参数：**  
`Object` - 包含以下字段:
| 参数名称 | 数据类型      | 描述                                 |
| :--------- | :------------- | :------------------------------------------ |
| from       | DATA, 20 字节 | 交易发送方的地址。   |
| to         | DATA, 20 字节 | 交易接收方的地址。 |
| value      | DATA           |  转账金额，单位为 sun。                        |

**返回值：**
`Object` - 包含未签名`TransferContract`交易的对象。

**示例**

```curl
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
    "id": 1337,
    "jsonrpc": "2.0",
    "method": "buildTransaction",
    "params": [
        {
            "from": "0xC4DB2C9DFBCB6AA344793F1DDA7BD656598A06D8",
            "to": "0x95FD23D3D2221CFEF64167938DE5E62074719E54",
            "value": "0x1f4"
        }]}'

#返回
{"jsonrpc":"2.0","id":1337,"result":{"transaction":{"visible":false,"txID":"ae02a80abd985a6f05478b9bbf04706f00cdbf71e38c77d21ed77e44c634cef9","raw_data":{"contract":[{"parameter":{"value":{"amount":500,"owner_address":"41c4db2c9dfbcb6aa344793f1dda7bd656598a06d8","to_address":"4195fd23d3d2221cfef64167938de5e62074719e54"},"type_url":"type.googleapis.com/protocol.TransferContract"},"type":"TransferContract"}],"ref_block_bytes":"957e","ref_block_hash":"3922d8c0d28b5283","expiration":1684469286000,"timestamp":1684469226841},"raw_data_hex":"0a02957e22083922d8c0d28b528340f088c69183315a66080112620a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412310a1541c4db2c9dfbcb6aa344793f1dda7bd656598a06d812154195fd23d3d2221cfef64167938de5e62074719e5418f40370d9bac2918331"}}}

```

### TransferAssetContract (TRC-10转账)

**参数：**  
`Object` - 包含以下字段:

| 参数名称 | 数据类型      | 描述                                 |
| :--------- | :------------- | :----------------------------------------- |
| from       | DATA, 20 字节 | 交易发送方的地址   |
| to         | DATA, 20 字节 | 交易接收方的地址 |
| tokenId    | QUANTITY       | 代币 ID                                   |
| tokenValue | QUANTITY       | TRC-10代币的转账金额。               |

**返回**
`Object` - 包含未签名`TransferAssetContract`交易的对象。

**示例**

```
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
    "method": "buildTransaction",
    "params": [
        {
            "from": "0xC4DB2C9DFBCB6AA344793F1DDA7BD656598A06D8",
            "to": "0x95FD23D3D2221CFEF64167938DE5E62074719E54",
            "tokenId": 1000016,
            "tokenValue": 20
        }
    ],
    "id": 44,
    "jsonrpc": "2.0"
}

#返回
{"jsonrpc":"2.0","id":44,"error":{"code":-32600,"message":"assetBalance must be greater than 0.","data":"{}"}}
```

### CreateSmartContract (部署合约)

**参数**  
`Object` - 包含以下字段:
| 参数名称 | 数据类型      | 描述                                 |
| :------------------------- | :------------- | :--------------------------------------- |
| from                       | DATA, 20 字节 | 交易发送方的地址 |
| name                       | DATA           | 智能合约的名称         |
| gas                        | DATA           | 费用限制                                |
| abi                        | DATA           | 智能合约的 ABI           |
| data                       | DATA           | 智能合约的字节码     |
| consumeUserResourcePercent | QUANTITY       | 用户资源消耗百分比       |
| originEnergyLimit          | QUANTITY       | 初始能量限制               |
| value                      | DATA           | 转入合约的TRX数额      |
| tokenId                    | QUANTITY       | 代币 ID                                 |
| tokenValue                 | QUANTITY       | TRC-10 代币的转账金额             |

**返回**
`Object` - 未签名的 `CreateSmartContract` 交易或错误

**示例：**
```
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{
    "id": 1337,
    "jsonrpc": "2.0",
    "method": "buildTransaction",
    "params": [
        {
            "from": "0xC4DB2C9DFBCB6AA344793F1DDA7BD656598A06D8",
            "name": "transferTokenContract",
            "gas": "0x245498",
            "abi": "[{\"constant\":false,\"inputs\":[],\"name\":\"getResultInCon\",\"outputs\":[{\"name\":\"\",\"type\":\"trcToken\"},{\"name\":\"\",\"type\":\"uint256\"},{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"toAddress\",\"type\":\"address\"},{\"name\":\"id\",\"type\":\"trcToken\"},{\"name\":\"amount\",\"type\":\"uint256\"}],\"name\":\"TransferTokenTo\",\"outputs\":[],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[],\"name\":\"msgTokenValueAndTokenIdTest\",\"outputs\":[{\"name\":\"\",\"type\":\"trcToken\"},{\"name\":\"\",\"type\":\"uint256\"},{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"function\"},{\"inputs\":[],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"constructor\"}]\n",
            "data": "6080604052d3600055d2600155346002556101418061001f6000396000f3006080604052600436106100565763ffffffff7c010000000000000000000000000000000000000000000000000000000060003504166305c24200811461005b5780633be9ece71461008157806371dc08ce146100aa575b600080fd5b6100636100b2565b60408051938452602084019290925282820152519081900360600190f35b6100a873ffffffffffffffffffffffffffffffffffffffff600435166024356044356100c0565b005b61006361010d565b600054600154600254909192565b60405173ffffffffffffffffffffffffffffffffffffffff84169082156108fc029083908590600081818185878a8ad0945050505050158015610107573d6000803e3d6000fd5b50505050565bd3d2349091925600a165627a7a72305820a2fb39541e90eda9a2f5f9e7905ef98e66e60dd4b38e00b05de418da3154e7570029",
            "consumeUserResourcePercent": 100,
            "originEnergyLimit": 11111111111111,
            "value": "0x1f4",
            "tokenId": 1000033,
            "tokenValue": 100000
        }
    ]
}

#返回
{"jsonrpc":"2.0","id":1337,"result":{"transaction":{"visible":false,"txID":"598d8aafbf9340e92c8f72a38389ce9661b643ff37dd2a609f393336a76025b9","contract_address":"41dfd93697c0a978db343fe7a92333e11eeb2f967d","raw_data":{"contract":[{"parameter":{"value":{"token_id":1000033,"owner_address":"41c4db2c9dfbcb6aa344793f1dda7bd656598a06d8","call_token_value":100000,"new_contract":{"bytecode":"6080604052d3600055d2600155346002556101418061001f6000396000f3006080604052600436106100565763ffffffff7c010000000000000000000000000000000000000000000000000000000060003504166305c24200811461005b5780633be9ece71461008157806371dc08ce146100aa575b600080fd5b6100636100b2565b60408051938452602084019290925282820152519081900360600190f35b6100a873ffffffffffffffffffffffffffffffffffffffff600435166024356044356100c0565b005b61006361010d565b600054600154600254909192565b60405173ffffffffffffffffffffffffffffffffffffffff84169082156108fc029083908590600081818185878a8ad0945050505050158015610107573d6000803e3d6000fd5b50505050565bd3d2349091925600a165627a7a72305820a2fb39541e90eda9a2f5f9e7905ef98e66e60dd4b38e00b05de418da3154e7570029","consume_user_resource_percent":100,"name":"transferTokenContract","origin_address":"41c4db2c9dfbcb6aa344793f1dda7bd656598a06d8","abi":{"entrys":[{"outputs":[{"type":"trcToken"},{"type":"uint256"},{"type":"uint256"}],"payable":true,"name":"getResultInCon","stateMutability":"Payable","type":"Function"},{"payable":true,"inputs":[{"name":"toAddress","type":"address"},{"name":"id","type":"trcToken"},{"name":"amount","type":"uint256"}],"name":"TransferTokenTo","stateMutability":"Payable","type":"Function"},{"outputs":[{"type":"trcToken"},{"type":"uint256"},{"type":"uint256"}],"payable":true,"name":"msgTokenValueAndTokenIdTest","stateMutability":"Payable","type":"Function"},{"payable":true,"stateMutability":"Payable","type":"Constructor"}]},"origin_energy_limit":11111111111111,"call_value":500}},"type_url":"type.googleapis.com/protocol.CreateSmartContract"},"type":"CreateSmartContract"}],"ref_block_bytes":"80be","ref_block_hash":"ac7c3d59c55ac92c","expiration":1634030190000,"fee_limit":333333280,"timestamp":1634030131693},"raw_data_hex":"0a0280be2208ac7c3d59c55ac92c40b0fba79ec72f5ad805081e12d3050a30747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e437265617465536d617274436f6e7472616374129e050a1541c4db2c9dfbcb6aa344793f1dda7bd656598a06d812fc040a1541c4db2c9dfbcb6aa344793f1dda7bd656598a06d81adb010a381a0e676574526573756c74496e436f6e2a0a1a08747263546f6b656e2a091a0775696e743235362a091a0775696e743235363002380140040a501a0f5472616e73666572546f6b656e546f22141209746f416464726573731a0761646472657373220e120269641a08747263546f6b656e22111206616d6f756e741a0775696e743235363002380140040a451a1b6d7367546f6b656e56616c7565416e64546f6b656e4964546573742a0a1a08747263546f6b656e2a091a0775696e743235362a091a0775696e743235363002380140040a0630013801400422e0026080604052d3600055d2600155346002556101418061001f6000396000f3006080604052600436106100565763ffffffff7c010000000000000000000000000000000000000000000000000000000060003504166305c24200811461005b5780633be9ece71461008157806371dc08ce146100aa575b600080fd5b6100636100b2565b60408051938452602084019290925282820152519081900360600190f35b6100a873ffffffffffffffffffffffffffffffffffffffff600435166024356044356100c0565b005b61006361010d565b600054600154600254909192565b60405173ffffffffffffffffffffffffffffffffffffffff84169082156108fc029083908590600081818185878a8ad0945050505050158015610107573d6000803e3d6000fd5b50505050565bd3d2349091925600a165627a7a72305820a2fb39541e90eda9a2f5f9e7905ef98e66e60dd4b38e00b05de418da3154e757002928f40330643a157472616e73666572546f6b656e436f6e747261637440c7e3d28eb0c30218a08d0620e1843d70edb3a49ec72f9001a086f99e01"}}}
```


### TriggerSmartContract (调用合约)

**参数:** 
`Object` - 包含以下字段:

| 参数名称 | 类型      | 描述                                |
| :------------------------- | :------------- | :--------------------------------------- |
| from | DATA, 20 Bytes | 交易发送方的地址 |
| to | DATA, 20 Bytes | 智能合约的地址 |
| data | DATA | 调用的合约函数和参数|
| gas | DATA | Fee limit|
| value | DATA |转入合约的 TRX 数额 |
| tokenId | QUANTITY | 代币 ID |
| tokenValue | QUANTITY | TRC-10 代币的转账金额 |

**返回值:** 
`Object` - 未签名的 `TriggerSmartContract` 交易或者错误。

**示例**
```
curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"id": 1337,
    "jsonrpc": "2.0",
    "method": "buildTransaction",
    "params": [
        {
            "from": "0xC4DB2C9DFBCB6AA344793F1DDA7BD656598A06D8",
            "to": "0xf859b5c93f789f4bcffbe7cc95a71e28e5e6a5bd",
            "data": "0x3be9ece7000000000000000000000000ba8e28bdb6e49fbb3f5cd82a9f5ce8363587f1f600000000000000000000000000000000000000000000000000000000000f42630000000000000000000000000000000000000000000000000000000000000001",
            "gas": "0x245498",
            "value": "0xA",
            "tokenId": 1000035,
            "tokenValue": 20
        }
    ]
    }
'

# 返回
{"jsonrpc":"2.0","id":1337,"result":{"transaction":{"visible":false,"txID":"c3c746beb86ffc366ec0ff8bf6c9504c88f8714e47bc0009e4f7e2b1d49eb967","raw_data":{"contract":[{"parameter":{"value":{"amount":10,"owner_address":"41c4db2c9dfbcb6aa344793f1dda7bd656598a06d8","to_address":"41f859b5c93f789f4bcffbe7cc95a71e28e5e6a5bd"},"type_url":"type.googleapis.com/protocol.TransferContract"},"type":"TransferContract"}],"ref_block_bytes":"958c","ref_block_hash":"9d8c6bae734a2281","expiration":1684469328000,"timestamp":1684469270364},"raw_data_hex":"0a02958c22089d8c6bae734a22814080d1c89183315a65080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541c4db2c9dfbcb6aa344793f1dda7bd656598a06d8121541f859b5c93f789f4bcffbe7cc95a71e28e5e6a5bd180a70dc8ec5918331"}}}
```

