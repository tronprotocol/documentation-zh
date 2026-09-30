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

| `data.state` | 含义 | 是否终态？ |
|---|---|---|
| `confirmed` | 已入块，且能拿到执行结果 / 回执；带有 `blockNumber` | 是 |
| `failed` | 已入块但被 revert / 拒绝 | 是 |
| `pending` | 节点已看到，但尚无执行结果 / 回执 | 否——继续轮询 |
| `not_found` | 所查询的端点不认识它（网络选错、尚未传播、被丢弃或已被裁剪）；结果未知 | 否——继续轮询并对账；不要臆断为失败 |

> `confirmed` 表示的是「已入块且已拿到回执」，而不是最终性保证。如果你的流程需要最终性，请另行核验——TRON 上查 SolidityNode 视图，EVM 上做 finalized 区块检查。

> 轮询到截止时间仍停在 `pending` 或 `not_found`，结果依然是未知。不要把它记录为失败，也不要用它作为自动重发的触发条件；请先按目标网络和端点核对该 txid。

## 选项

| 选项 | 说明 |
|---|---|
| `--txid <string>` | **必填。** 交易 id / 哈希——TRON 上是不带前缀的 hex，EVM 上是 `0x…` |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli tx status --txid 1789b6e3d420d84f21013fa4e18ecd2c60df1accb7101fd71c2511b75835c0cd --network nile
```

```console
TxID           1789b6e3d420d84f21013fa4e18ecd2c60df1accb7101fd71c2511b75835c0cd
Status         confirmed ✅
Block          #70,604,611
Confirmations  19
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"tx.status","data":{"txid":"1789b6e3d420d84f21013fa4e18ecd2c60df1accb7101fd71c2511b75835c0cd","state":"confirmed","confirmed":true,"failed":false,"blockNumber":70604611,"confirmations":19},"meta":{"durationMs":1817,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

同一个查询在 EVM 网络上，用 `0x` 哈希：

```bash
wallet-cli tx status --txid 0x55b0068ef31bce39bbf5b06d456eaef307fd77f96d85ea291f48c1ae4b900d80 --network sepolia -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"tx.status","data":{"txid":"0x55b0068ef31bce39bbf5b06d456eaef307fd77f96d85ea291f48c1ae4b900d80","state":"confirmed","confirmed":true,"failed":false,"blockNumber":11576586,"confirmations":0},"meta":{"durationMs":408,"warnings":[]},"chain":{"family":"evm","network":"eip155:11155111","chainId":"11155111"}}
```

未知的 txid 会返回**成功**，`state: "not_found"`（退出码 0）——查询本身是成功的，答案是「不存在」：

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"tx.status","data":{"txid":"0000…0000","state":"not_found","confirmed":false,"failed":false},"meta":{"durationMs":1022,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

在 EVM 上，`not_found` 还会带一条 `meta.warnings`，因为一个裁剪过历史的公共端点，和一个从未存在过的哈希，是无法区分的：

```json
{"…":"…","data":{"txid":"0x0000…0000","state":"not_found","confirmed":false,"failed":false},"meta":{"durationMs":407,"warnings":["0x0000…0000 is unknown to this endpoint. Public nodes often prune history, so this may mean the node has no record of it rather than that it never existed; try an archival endpoint."]},"chain":{"family":"evm","network":"eip155:11155111","chainId":"11155111"}}
```

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
