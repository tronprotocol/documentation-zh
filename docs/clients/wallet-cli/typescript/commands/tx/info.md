# wallet-cli tx info

查看交易的完整详情和交易回执。

## 用法

```
wallet-cli tx info --txid <id> [options]
```

## 说明

获取完整的交易对象及其执行回执，适用于 TRON 和 EVM 网络。该命令适合取证和费用分析；如果只需判断交易是否成功，[`tx status`](status.md) 更轻量，其四个稳定状态值可直接用于程序分支。

顶层摘要在两个家族之间是归一化的；而嵌套在下面的原始对象不是。在 TRON 上，它们是 `transaction`（节点给出的交易对象）和 `info`（其执行回执）；在 EVM 上，它们是 `transaction`（`eth_getTransactionByHash` 的结果）和 `receipt`。

注意两者失败方式的差别：`tx status` 遇到未知 txid 时返回 `not_found` 且退出码为 0，而 `tx info` 则直接**报错**——因为没有任何详情可以展示。两个家族在错误码和退出码上都不同：TRON 把节点自己的拒绝原样呈现为 `rpc_error`，退出码 **1**；EVM 则报 `not_found`，退出码 **2**——它把这次查询视作一次错误的调用，因为这个哈希什么也指不到。请先按退出码分支，再看 `error.code`。

## 选项

| 选项 | 说明 |
|---|---|
| `--txid <string>` | **必填。** 交易 id / 哈希——TRON 上是不带前缀的 hex，EVM 上是 `0x…` |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli tx info --txid 52332505ab6b605aff626aaef2b07f3718d4bac8f45cdab1c0ea9465eb98e065 --network nile
```

```console
TxID    52332505ab6b605aff626aaef2b07f3718d4bac8f45cdab1c0ea9465eb98e065
From    TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ
To      TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH
Amount  1 TRX
Status  success
Block   #69,084,269
```

`-o json` 返回完整详情（`transaction` 是原始交易，`info` 是回执；此处以空对象示意）：

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"tx.info","data":{"txid":"52332505ab6b605aff626aaef2b07f3718d4bac8f45cdab1c0ea9465eb98e065","from":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ","to":"TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH","amount":"1","symbol":"TRX","status":"success","blockNumber":69084269,"transaction":{},"info":{}},"meta":{"durationMs":1396,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

在 EVM 网络上，摘要中多了 `type` 和 `nonce`，费用以 wei 计价，并且嵌套的是 `receipt` 而不是 `info`：

```bash
wallet-cli tx info --txid 0x55b0068ef31bce39bbf5b06d456eaef307fd77f96d85ea291f48c1ae4b900d80 --network sepolia -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"tx.info","data":{"txid":"0x55b0068ef31bce39bbf5b06d456eaef307fd77f96d85ea291f48c1ae4b900d80","type":"contract-call","from":"0x88878d9250e68C574912f5618ad3b43f675B8888","nonce":342,"to":"0x1b853EbA683A7C0b691256124392F3b922771869","status":"success","blockNumber":11576586,"confirmations":0,"gasUsed":"46231","feeWei":"43850186538","effectiveGasPriceWei":"948493","transaction":{},"receipt":{}},"meta":{"durationMs":455,"warnings":[]},"chain":{"family":"evm","network":"eip155:11155111","chainId":"11155111"}}
```

未知的 txid 会直接报错——这与 `tx status` 返回 `not_found`（退出码 0）不同。错误码和退出码按家族而异（TRON 为 `rpc_error`、退出码 1；EVM 为 `not_found`、退出码 2）：

```json
{"schema":"wallet-cli.result.v1","success":false,"command":"tx.info","error":{"code":"rpc_error","message":"TRON getTransaction failed: Transaction not found"},"meta":{"durationMs":1033,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

```json
{"schema":"wallet-cli.result.v1","success":false,"command":"tx.info","error":{"code":"not_found","message":"no transaction with hash 0x0000…0000 on eip155:11155111"},"meta":{"durationMs":412,"warnings":[]},"chain":{"family":"evm","network":"eip155:11155111","chainId":"11155111"}}
```

## 输出

`data` 是结构化的交易详情：顶层是归一化的摘要，下面嵌套着该链自身的原始对象。只有摘要部分保证稳定——嵌套的对象遵循节点的模型，可能随之变化。

两个家族共有的摘要字段：

| 字段 | 类型 | 含义 |
|---|---|---|
| `txid` | string | 交易 id |
| `from` | string | 发送方地址 |
| `to` | string | 收款方地址 |
| `amount` | string | 转账金额（人类可读单位） |
| `symbol` | string | 原生币或 token 符号 |
| `status` | string | 一律小写，因此匹配时用 `"success"`，绝不要用 `"SUCCESS"`。EVM 上取值为 `success` 或 `revert`；TRON 上则是节点自身 `contractRet` 的小写形式——`success`、`revert`、`out_of_energy` 等。它绝不会是 `failed` |
| `blockNumber` | number | 区块高度 |
| `confirmations` | number | 该区块之上又出了多少个块 |

TRON 额外提供：

| 字段 | 类型 | 含义 |
|---|---|---|
| `feeSun` | number | 实际收取的手续费，单位 SUN |
| `transaction` | object | 原始 TRON 交易对象（`raw_data`、`signature`、`txID` 等） |
| `info` | object | 执行回执（`receipt` 资源消耗、`contractResult`、`blockTimeStamp` 等） |

EVM 额外提供：

| 字段 | 类型 | 含义 |
|---|---|---|
| `type` | string | `transfer`（原生转账，或解码出的 ERC20 转账）、`contract-creation`（没有 `to`），或 `contract-call` |
| `nonce` | number | 发送方在这笔交易上的 nonce |
| `rawAmount` | string | 转移的金额，单位 wei |
| `blockTime` | number | 出块时间戳，epoch 秒；尽力而为——区块读取失败时会省略 |
| `gasUsed` | string | 实际消耗的 gas |
| `feeWei` | string | 实际收取的手续费，单位 wei |
| `effectiveGasPriceWei` | string | 实际支付的每单位 gas 价格 |
| `transaction` | object | `eth_getTransactionByHash` 的返回结果，原样给出 |
| `receipt` | object | 解码后的回执（`success`、`gasUsed`、`feeWei`、`effectiveGasPriceWei`、`blockNumber`），节点自身的响应保存在 `raw` 中 |

## 退出码

`0` 已找到 · `1` 执行失败——在 TRON 上包括*未找到*（`rpc_error`） · `2` 用法错误，在 EVM 上包括*未找到*（`not_found`）。

## 另请参见

[`tx status`](status.md) · [`account history`](../account/history.md) · [费用模型](../../concepts/networks.md#fees-the-tron-resource-model)
