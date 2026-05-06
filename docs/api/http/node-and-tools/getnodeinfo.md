# /wallet/getnodeinfo

获取本节点运行状态、版本、内存、磁盘、最新区块、对等节点统计等信息。

- 源码：`framework/src/main/java/org/tron/core/services/http/GetNodeInfoServlet.java`
- Method：`GET` / `POST`
- 别名路径：`/monitor/getnodeinfo`
- 响应处理：servlet 调 `JSON.toJSONString(NodeInfo)` 直接序列化 Java 实体（`common/src/main/java/org/tron/common/entity/NodeInfo.java`），**不走 `JsonFormat`**——字段名以 Java POJO 为准（与 `Tron.proto` 中的 `NodeInfo` proto 不完全一致）。`visible` 不影响响应。
- 支持固化接口：`/walletsolidity/getnodeinfo`

## 请求参数

无。

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getnodeinfo \
     --header 'accept: application/json'
```

## 响应

主要字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `beginSyncNum` | int64 | 开始同步的区块高度 |
| `block` | string | 当前最新区块（"Num:height,ID:hash"） |
| `solidityBlock` | string | 当前已固化区块 |
| `currentConnectCount` | int32 | 当前对等连接数 |
| `activeConnectCount` | int32 | 主动连接数 |
| `passiveConnectCount` | int32 | 被动连接数 |
| `totalFlow` | int64 | 总流量 |
| `peerList` | repeated PeerInfo | 各 peer 详情 |
| `configNodeInfo` | ConfigNodeInfo | 配置（`codeVersion`、`versionNum`、`p2pVersion`、`listenPort` 等） |
| `machineInfo` | MachineInfo | 机器信息（CPU、内存、磁盘） |
| `cheatWitnessInfoMap` | map<string,string> | SR 作弊统计（key 为见证人 hex 地址，含 `41` 前缀） |

响应示例（截取关键字段，省略 `peerList`、`memoryDescInfoList` 完整内容、`cheatWitnessInfoMap` 等）：

```json
{
  "activeConnectCount": 3,
  "beginSyncNum": 66987546,
  "block": "Num:66987565,ID:0000000003fe262d52bfa4b2814f816fd2e57af5b98a33d60d8630a03a908e0e",
  "solidityBlock": "Num:66987547,ID:0000000003fe261b9e6e8091f5bd92dc67816890ec4739f6fe5109ad7779120c",
  "currentConnectCount": 60,
  "passiveConnectCount": 57,
  "totalFlow": 0,
  "configNodeInfo": {
    "codeVersion": "4.8.1",
    "versionNum": "18636",
    "p2pVersion": "201910292",
    "listenPort": 18888,
    "discoverEnable": true,
    "maxConnectCount": 60,
    "supportConstant": true,
    "dbVersion": 2
  },
  "machineInfo": {
    "cpuCount": 16,
    "cpuRate": 0.06666666666666667,
    "totalMemory": 32726257664,
    "freeMemory": 232448000,
    "jvmTotalMemory": 18683133952,
    "jvmFreeMemory": 7802853696,
    "javaVersion": "1.8.0_291",
    "osName": "Linux 3.10.0-1160.49.1.el7.x86_64",
    "threadCount": 361,
    "deadLockThreadCount": 0
  }
}
```

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 节点内部异常（采集节点信息或序列化失败） | `{"Error": "<exceptionClass> : <message>"}` |
