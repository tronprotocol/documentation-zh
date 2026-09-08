# wallet-cli chain node

所连节点的状态。

## 用法

```
wallet-cli chain node [options]
```

## 说明

显示所连接节点的版本、最新块与已固化块高度、同步状态以及对等节点数量，TRON 与 EVM 网络都适用。排查交易问题时，可以先用该命令确认节点是否已经同步。

在 TRON 上，版本、已固化块高度和对等节点数来自节点的 `getnodeinfo`，**最新块**的高度与时间戳则通过单独的 `getBlock()` 请求获取。同步状态通过比较最新块时间戳与本地时钟判断：差值不超过 3 个出块间隔（TRON 每 3 秒出一个块，即 9 秒）即视为同步。在 EVM 上，这些字段来自 `web3_clientVersion`、`eth_chainId`、`eth_syncing`、`net_peerCount` 和最新区块；同步状态直接采用节点返回的 `eth_syncing`，文本中的 `Syncing` 行是该结果的反向表述。公共网关（TronGrid、公共 RPC 服务商）可能不提供对等节点或机器信息，此时文本显示 `—`，JSON 中为 `null`。

`endpoint` 只报告**主机名**，不会显示完整 URL。商用 RPC 端点常把 API key 放在路径中，而命令输出可能被粘贴到 issue 或 CI 日志。要读取完整值，请使用 `config networks.<id>.httpEndpoint`。

## 选项

没有命令级选项；仅[全局选项](../index.md#global-options-every-command)（`--network`）。

## 示例

```bash
wallet-cli chain node --network tron:3448148188
```

```console
Endpoint     nile.trongrid.io
Version      java-tron 4.8.2.1.PQ1_build1
Head block   #70,433,707  2026-08-27 08:16:00 (~4s ago — in sync)
Solid block  #70,433,690  (17 blocks behind head)
Peers        60 connected / 3 active
```

```bash
wallet-cli chain node --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"chain.node","data":{"endpoint":"nile.trongrid.io","version":"java-tron 4.8.2.1.PQ1_build1","p2pVersion":"201910292","headBlock":{"number":70433708,"timestamp":1787818563000},"solidBlock":{"number":70433690},"lagBlocks":18,"inSync":true,"peers":{"connected":58,"active":3}},"meta":{"durationMs":752,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

在 EVM 网络上，还会加上链 id 和节点自己的同步标志：

```bash
wallet-cli chain node --network eip155:11155111
```

```console
Endpoint     ethereum-sepolia-rpc.publicnode.com
Version      Geth/v1.17.1-stable-16783c16/linux-amd64/go1.25.7
Chain id     11155111
Head block   #11,576,632  2026-08-27 08:16:00 (~6s ago — in sync)
Solid block  #11,576,563  (69 blocks behind head)
Syncing      no
Peers        25 connected / 25 active
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"chain.node","data":{"endpoint":"ethereum-sepolia-rpc.publicnode.com","version":"Geth/v1.17.1-stable-16783c16/linux-amd64/go1.25.7","chainId":"11155111","p2pVersion":null,"headBlock":{"number":11576632,"timestamp":1787818560000},"solidBlock":{"number":11576563},"lagBlocks":69,"inSync":true,"peers":{"connected":25,"active":25}},"meta":{"durationMs":389,"warnings":[]},"chain":{"family":"evm","network":"eip155:11155111","chainId":"11155111"}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `endpoint` | string | 所查询节点的主机名——只有主机名，绝不含完整 URL |
| `version` | string | 节点软件版本 |
| `chainId` | string | EIP-155 链 id；**仅 EVM** |
| `p2pVersion` | string \| null | P2P 协议版本；EVM 上为 `null` |
| `headBlock` | object | 最新块 `{number, timestamp}` |
| `solidBlock` | object \| null | TRON 上为已固化块，EVM 上为已 finalized 的区块——`{number}` |
| `lagBlocks` | number \| null | 最新块与已固化块的高度差 |
| `inSync` | boolean \| null | 节点是否已跟上。TRON 上：最新块是否新鲜（3 个出块间隔以内，即 ≤ 9 秒）。EVM 上：节点自己的 `eth_syncing` 回答取反——读不到时为 `null`，这与「未同步」不是一回事 |
| `peers` | object \| null | `{connected, active}`；端点隐藏该信息时为 `null`。EVM 只报告一个对等节点数，因此两个字段取同一个值 |

## 退出码

`0` 成功 · `1` 执行失败（`rpc_error`、`timeout`） · `2` 用法错误。

## 另请参见

[`chain params`](params.md) · [`networks`](../networks.md) · [故障排查](../../troubleshooting.md)
