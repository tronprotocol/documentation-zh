# wallet-cli tx status

查看交易的确认状态。

## 用法

```
wallet-cli tx status --txid <id> [options]
```

## 说明

通过**四种状态**报告交易进度，TRON 与 EVM 网络都适用。发送后，脚本和智能体可以轮询该命令，判断交易是否已经入块及执行成功。
这四个状态值属于稳定接口，在兼容版本中不会改名或删除，因此程序可以直接据此分支处理（参见
[machine-interface](../../machine-interface.md) 中的 `wallet-cli.result.v1` 输出规范）。

| `data.state` | 含义 | 能否停止轮询？ |
|---|---|---|
| `confirmed` | 已入块，且已经能取到执行结果/回执；存在 `blockNumber` | 可以 |
| `failed` | 已入块，但链上执行失败 | 可以——视为失败 |
| `pending` | 节点已经看到，但还没有执行结果/回执 | 不能——继续轮询 |
| `not_found` | 查询端点尚未找到该交易（可能是网络选择错误、交易尚未传播、交易被丢弃，或端点未保留相关历史）；结果未知 | 不能——继续轮询/对账；不要据此判定失败 |

> `confirmed` 是一个「已入块且已取到回执」的状态，不是最终性保证。如果某个流程需要最终性，请另行验证——TRON 上查询 SolidityNode 视图，EVM 上检查 finalized 区块。

## 选项

| 选项 | 说明 |
|---|---|
| `--txid <string>` | **必填。** 交易 id / 哈希——TRON 上是不带前缀的 hex，EVM 上是 `0x…` |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli tx status --txid 34d9da372cd7fa9d4e7384744c0925af9d682eef4c9410fb831e0b87b355171b --network tron:3448148188
```

```console
TxID           34d9da372cd7fa9d4e7384744c0925af9d682eef4c9410fb831e0b87b355171b
Status         confirmed ✅
Block          #70,433,563
Confirmations  1
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"tx.status","data":{"txid":"34d9da372cd7fa9d4e7384744c0925af9d682eef4c9410fb831e0b87b355171b","state":"confirmed","confirmed":true,"failed":false,"blockNumber":70433563,"confirmations":1},"meta":{"durationMs":732,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

同一个查询在 EVM 网络上，用 `0x` 哈希：

```bash
wallet-cli tx status --txid 0x55b0068ef31bce39bbf5b06d456eaef307fd77f96d85ea291f48c1ae4b900d80 --network eip155:11155111 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"tx.status","data":{"txid":"0x55b0068ef31bce39bbf5b06d456eaef307fd77f96d85ea291f48c1ae4b900d80","state":"confirmed","confirmed":true,"failed":false,"blockNumber":11576586,"confirmations":0},"meta":{"durationMs":408,"warnings":[]},"chain":{"family":"evm","network":"eip155:11155111","chainId":"11155111"}}
```

未知的 txid 属于**成功**，返回 `state: "not_found"`（退出码 0）——查询本身是成功的，只是这个端点没有该哈希的任何记录：

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"tx.status","data":{"txid":"0000…0000","state":"not_found","confirmed":false,"failed":false},"meta":{"durationMs":1022,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

在 EVM 上，`not_found` 还会带一条 `meta.warnings`，因为一个裁剪过历史的公共端点，和一个从未存在过的哈希，是无法区分的：

```json
{"…":"…","data":{"txid":"0x0000…0000","state":"not_found","confirmed":false,"failed":false},"meta":{"durationMs":407,"warnings":["0x0000…0000 is unknown to this endpoint. Public nodes often prune history, so this may mean the node has no record of it rather than that it never existed; try an archival endpoint."]}}
```

> 轮询到截止时间仍停在 `pending` 或 `not_found`，结果依然是未知。不要把它当成失败，也不要拿它当作自动重发的触发条件；先把这个 txid 对照目标网络和端点的历史记录核对清楚。

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `txid` | string | 回显所查询的 id |
| `state` | string | `confirmed` / `failed` / `pending` / `not_found` |
| `confirmed` / `failed` | boolean | 与 `state` 对应的布尔值，便于直接分支判断 |
| `blockNumber` | number | 状态为已确认时才有 |
| `confirmations` | number | 在所在区块之上又叠加了多少个块；已确认时才有 |

## 退出码

`0` 查询已作答（包括 `not_found`） · `1` 执行失败（节点不可达、超时） · `2` 用法错误。

## 另请参见

[`tx info`](info.md)——完整详情和交易回执 · [`tx send`](send.md) · [脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)
