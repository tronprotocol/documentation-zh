# wallet-cli networks

列出已知网络。

## 用法

```
wallet-cli networks [options]
```

## 说明

列出 wallet-cli 已知的每一个网络，以及 `--network` 同样接受的简短别名。纯本地操作——不访问任何节点。

**Network** 是规范的 CAIP-2 id，形如 `namespace:reference`；**Alias** 是你可以改用的简称。两者解析到同一个网络，而下游任何环节都看不到别名。CAIP-2 之前使用的那几个 TRON id（`tron:mainnet`、`tron:nile`、`tron:shasta`）同样仍可作为别名解析，只是列表中只列出简称形式。

端点只显示**主机名**——商用 RPC 端点可能把 API key 放在 URL 路径里。`config networks.<id>.httpEndpoint` 会给出完整 URL。

## 选项

仅[全局选项](index.md)。

## 示例

```bash
wallet-cli networks
```

```console
| Network         | Alias        | Family | Chain id   | Fee model     | Endpoint                            |
| --------------- | ------------ | ------ | ---------- | ------------- | ----------------------------------- |
| tron:728126428  | tron         | tron   | 728126428  | tron-resource | api.trongrid.io                     |
| tron:3448148188 | nile         | tron   | 3448148188 | tron-resource | nile.trongrid.io                    |
| tron:2494104990 | shasta       | tron   | 2494104990 | tron-resource | api.shasta.trongrid.io              |
| eip155:1        | ethereum     | evm    | 1          | evm-gas       | ethereum-rpc.publicnode.com         |
| eip155:11155111 | sepolia      | evm    | 11155111   | evm-gas       | ethereum-sepolia-rpc.publicnode.com |
| eip155:56       | bsc          | evm    | 56         | evm-gas       | bsc-dataseed.bnbchain.org           |
| eip155:97       | bsc-testnet  | evm    | 97         | evm-gas       | bsc-testnet-dataseed.bnbchain.org   |
| eip155:8453     | base         | evm    | 8453       | evm-gas       | mainnet.base.org                    |
| eip155:84532    | base-sepolia | evm    | 84532      | evm-gas       | sepolia.base.org                    |
```

```bash
wallet-cli networks -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"networks","data":[{"id":"tron:728126428","alias":"tron","family":"tron","chainId":"728126428","feeModel":"tron-resource","endpoint":"api.trongrid.io"},{"id":"tron:3448148188","alias":"nile","family":"tron","chainId":"3448148188","feeModel":"tron-resource","endpoint":"nile.trongrid.io"},{"id":"tron:2494104990","alias":"shasta","family":"tron","chainId":"2494104990","feeModel":"tron-resource","endpoint":"api.shasta.trongrid.io"},{"id":"eip155:1","alias":"ethereum","family":"evm","chainId":"1","feeModel":"evm-gas","endpoint":"ethereum-rpc.publicnode.com"},{"id":"eip155:11155111","alias":"sepolia","family":"evm","chainId":"11155111","feeModel":"evm-gas","endpoint":"ethereum-sepolia-rpc.publicnode.com"},{"id":"eip155:56","alias":"bsc","family":"evm","chainId":"56","feeModel":"evm-gas","endpoint":"bsc-dataseed.bnbchain.org"},{"id":"eip155:97","alias":"bsc-testnet","family":"evm","chainId":"97","feeModel":"evm-gas","endpoint":"bsc-testnet-dataseed.bnbchain.org"},{"id":"eip155:8453","alias":"base","family":"evm","chainId":"8453","feeModel":"evm-gas","endpoint":"mainnet.base.org"},{"id":"eip155:84532","alias":"base-sepolia","family":"evm","chainId":"84532","feeModel":"evm-gas","endpoint":"sepolia.base.org"}],"meta":{"durationMs":2,"warnings":[]}}
```

## 输出

`data` 是一个数组，每个已知网络对应一项。本地命令——没有 `chain` 块。

| 字段 | 类型 | 含义 |
|---|---|---|
| `id` | string | 规范的 CAIP-2 网络 id，形如 `namespace:reference` |
| `alias` | string | `--network` 同样接受的简称 |
| `family` | string | 链家族——`tron` 或 `evm` |
| `chainId` | string | 规范 id 的第二段——EVM 上是 EIP-155 数字，TRON 上是十进制的创世哈希前缀 |
| `feeModel` | string | `tron-resource` 或 `evm-gas` |
| `endpoint` | string | 所配置端点的**主机名**；完整 URL 请用 `config networks.<id>.httpEndpoint` 读取 |

## 退出码

`0` 成功 · `1` 执行失败 · `2` 用法错误。参见 [machine-interface](../machine-interface.md)。

## 另请参见

[网络概念](../concepts/networks.md) · [`config`](config.md)
