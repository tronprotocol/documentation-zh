# eth_syncing

节点同步状态。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getSyncingStatus`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

无。

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_syncing","params":[],"id":1}'
```

## 响应

- 若 peer 列表为空：返回 `false`。
- 否则返回 `SyncingResult` 对象：

| 字段 | 类型 | 说明 |
|---|---|---|
| `startingBlock` | hex | `nodeInfoService.getNodeInfo().getBeginSyncNum()` |
| `currentBlock` | hex | 当前节点最新块高 |
| `highestBlock` | hex | **估算值**：`currentBlockNum + max(0, (now - blockTime) / 3000)`（按平均出块 3 秒外推） |

下例为上面 curl 调用 Nile testnet 抓回的真实响应：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "startingBlock": "0x3fe1dda",
    "currentBlock": "0x3fe1ded",
    "highestBlock": "0x3fe1ded"
  }
}
```

> 三个值都随节点状态实时变化；`highestBlock` 是基于本地系统时间外推得到，并非来自其他 peer 的真实最高块高，断网时仍会持续增长。

### 异常响应

无。
