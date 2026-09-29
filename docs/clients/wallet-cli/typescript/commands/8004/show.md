# wallet-cli 8004 show

直接从身份注册表加载单个 Agent。

## 用法

```
wallet-cli 8004 show <id> [options]
```

## 说明

从所选网络的注册表读取该 Agent 的所有者、URI 和针对该 Agent 已批准的操作者，然后加载 URI 指向的注册文档。不需要钱包，也不需要密码。

链上字段总是会返回。加载文档则是尽力而为，而且**只会抓取 `https://` 和 `http://` 的 URI**。响应必须是 JSON（`application/json`，UTF-8），最大 1 MiB，且必须是一个 JSON 对象；重定向以及指向本地或私有网络的地址都会被拒绝，请求最多 10 秒后放弃。

其他任何情况都只产生警告而不是错误，文档则被略去。这包括 `data:` 和 `ipfs://` 形式的 URI：[`8004 register`](register.md) 和 [`8004 update`](update.md) 接受它们，但 `show` 不会读取。警告放在 `meta.warnings` 中（文本输出会打印为 `warning: …`）。

成功加载的文档会完整放在 `data.metadata` 下；文本输出显示它的 `name`、`description`、`image`，以及 `services`（或 `endpoints`）的名称。

没有批准任何操作者时，`approved` 是零地址——TRON 上为 `T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb`，EVM 上为 `0x0000000000000000000000000000000000000000`——文本输出会显示为 `None`。

可在部署了 ERC-8004 身份注册表的网络上运行：`tron`、`nile`、`shasta`、`bsc`、`bsc-testnet`、`base`、`base-sepolia`。见 [`8004`](index.md)。

## 参数

- `id`——Agent ID，十进制数字。可以带上它的规范网络 id 前缀，形如 `<network-id>:<id>`（例如 `tron:3448148188:172` 或 `eip155:97:42`）；该网络必须就是当前所选网络，且不接受 `nile:172` 这样的别名形式

## 选项

没有本命令特有的选项；仅[全局选项](../index.md#global-options-every-command)。

## 示例

显示 Base 上的 Agent 55，它的注册文档通过 HTTPS 提供：

```bash
wallet-cli 8004 show 55 --network base
```

```console
Agent ID     55
Owner        0x67722c823010ceb4bed5325fe109196c0f67d053
URI          https://marketplace.olas.network/erc8004/base/ai-agents/53
Approved     None
Registry     0x8004A169FB4a3325136EB29fA0ceB6D2e539a432
Name         garnor-tarko73 by Olas
Description  An optimism liquidity trader service.
Image        https://gateway.autonolas.tech/ipfs/bafybeiaakdeconw7j5z76fgghfdjmsr6tzejotxcwnvmp3nroaw3glgyve
Endpoints    web
```

```bash
wallet-cli 8004 show 55 --network base -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"8004.show","data":{"agentId":"55","owner":"0x67722c823010ceb4bed5325fe109196c0f67d053","uri":"https://marketplace.olas.network/erc8004/base/ai-agents/53","approved":"0x0000000000000000000000000000000000000000","registry":"0x8004A169FB4a3325136EB29fA0ceB6D2e539a432","metadata":{"type":"https://eips.ethereum.org/EIPS/eip-8004#registration-v1","name":"garnor-tarko73 by Olas","description":"An optimism liquidity trader service.","image":"https://gateway.autonolas.tech/ipfs/bafybeiaakdeconw7j5z76fgghfdjmsr6tzejotxcwnvmp3nroaw3glgyve","services":[{"name":"web","endpoint":"https://marketplace.olas.network/base/ai-agents/53"}],"x402Support":false,"active":true,"registrations":[{"agentId":55,"agentRegistry":"eip155:8453:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"}],"supportedTrust":["reputation"]}},"meta":{"durationMs":1602,"warnings":[]},"chain":{"family":"evm","network":"eip155:8453","chainId":"8453"}}
```

从 `Name` 到 `Endpoints` 都来自加载到的注册文档，JSON 会把它完整放在 `metadata` 下。`Approved None`（JSON 中是零地址）表示该 Agent 没有批准任何操作者。

用 `data:` URI 注册的 Agent（例如 Nile 上的 Agent 173）只会显示它的链上字段，外加一条警告：

```bash
wallet-cli 8004 show 173 --network nile
```

```console
warning: Registration metadata URI is invalid or unsupported
Agent ID  173
Owner     TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH
URI       data:application/json;base64,eyJuYW1lIjoiV2VhdGhlciBBZ2VudCIsImRlc2NyaXB0aW9uIjoiUmV0dXJucyB3ZWF0aGVyIGZvcmVjYXN0cyBhbmQgYWxlcnRzIGZvciBhIGNpdHkifQ==
Approved  None
Registry  TDDk4vc69nzBCbsY4kfu7gw2jmvbinirj5
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `agentId` | string | Agent ID，十进制 |
| `owner` | string | 当前所有者地址 |
| `uri` | string | 链上存储的注册 URI |
| `approved` | string | 针对该 Agent 已批准的操作者；没有时为零地址 |
| `registry` | string | 身份注册表的合约地址 |
| `metadata` | object | 加载到的注册文档；无法加载时没有该字段，原因在 `meta.warnings` 中 |

## 退出码

`0` 成功 · `1` 执行失败（`agent_not_found`——不存在该 id 的 Agent；`chain_id_mismatch`——id 前缀指向的是另一个网络；`rpc_error`、`timeout`） · `2` 用法错误（`unsupported_network_capability`——所选网络上没有注册表；`invalid_value`——id 不是无符号十进制数）。

## 另请参见

[`8004 update`](update.md) · [`8004 approve`](approve.md) · [`8004 operator-check`](operator-check.md)
