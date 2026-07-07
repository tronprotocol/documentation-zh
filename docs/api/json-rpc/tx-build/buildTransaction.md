# buildTransaction

Tron 私有扩展。构造一条**未签名**的 Tron 交易；签名后通过 HTTP [`/wallet/broadcasttransaction`](../../http/tx-build-and-broadcast/broadcasttransaction.md) 或 [`/wallet/broadcasthex`](../../http/tx-build-and-broadcast/broadcasthex.md) 广播（JSON-RPC 自身不提供广播接口）。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#buildTransaction`
- 端口：**仅 FullNode `8545`**（Solidity 端口抛 `-32601`）

## 请求参数

| 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `params[0]` | object | 是 | `BuildArguments`（继承 `CallArguments`，字段见下） |

`BuildArguments` 字段（`framework/src/main/java/org/tron/core/services/jsonrpc/types/BuildArguments.java`）：

| 字段 | 默认 | 说明 |
|---|---|---|
| `from` | 必填 | 发送方地址（hex 或 base58check） |
| `to` | 视情况 | 目标地址；合约部署时为空 |
| `gas` | `0x0` | 交易最大消耗 energy；最终 `feeLimit = gas × eth_gasPrice`（sun） |
| `value` | null | TRX 金额（sun，hex） |
| `data` | null | 合约 bytecode（部署）或 calldata（trigger） |
| `input` | null | `data` 的别名；hex 校验更严格，适合 execution-API 兼容客户端使用 |
| `tokenId` | `0` | TRC-10 token id（用于 `TransferAssetContract`） |
| `tokenValue` | `0` | TRC-10 数量 |
| `abi` | `""` | 部署合约时的 ABI JSON 字符串（如 `[{...}]`） |
| `name` | `""` | 部署合约名 |
| `consumeUserResourcePercent` | `0` | 用户分担资源百分比（0–100） |
| `originEnergyLimit` | `0` | 部署者每笔最大 energy |
| `permissionId` | `0` | 多签 permission id |
| `extraData` | `""` | 写入交易的备注数据 |
| `visible` | `false` | 输出地址/字符串是否使用 base58/UTF-8 |

合约类型推断（`BuildArguments.getContractType`）：

| 条件 | ContractType |
|---|---|
| `to` 为空 + calldata 非空 | `CreateSmartContract` |
| `to` 是合约地址 | `TriggerSmartContract` |
| `to` 是普通账户 + `tokenId>0` + `tokenValue>0` + `value` 为空 | `TransferAssetContract` |
| `to` 是普通账户 + `value` 非空 | `TransferContract` |
| 其它 | 抛 `-32600 invalid json request` |

```bash
# 例：构造一笔 TRX 转账（1 TRX = 1e6 sun）
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc":"2.0","id":1,"method":"buildTransaction",
    "params":[{
      "from":"0x41a614f803b6fd780986a42c78ec9c7f77e6ded13c",
      "to":"0x4112ab345eafdc9af9eaad7c97a2e9c3d4ddc0d7e1",
      "value":"0xf4240"
    }]
  }'
```

## 响应

`{"transaction": {...}}` —— 直接对应 Tron `protocol.Transaction`（hex 字段编码同 HTTP `/wallet/createtransaction` 返回的格式）。下例为上面 curl 调用 Nile testnet 抓回的真实响应：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "transaction": {
      "visible": false,
      "txID": "231371e531760758ea3a74dd4bce4934ad6d4cc71dfae1907f072c39de4c0c2f",
      "raw_data": {
        "contract": [
          {
            "parameter": {
              "value": {
                "amount": 1000000,
                "owner_address": "41a614f803b6fd780986a42c78ec9c7f77e6ded13c",
                "to_address": "4112ab345eafdc9af9eaad7c97a2e9c3d4ddc0d7e1"
              },
              "type_url": "type.googleapis.com/protocol.TransferContract"
            },
            "type": "TransferContract"
          }
        ],
        "ref_block_bytes": "1d00",
        "ref_block_hash": "081a3fe1f1440f1d",
        "expiration": 1777438164000,
        "timestamp": 1777438106738
      },
      "raw_data_hex": "0a021d002208081a3fe1f1440f1d40a088c8bcdd335a67080112630a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412320a1541a614f803b6fd780986a42c78ec9c7f77e6ded13c12154112ab345eafdc9af9eaad7c97a2e9c3d4ddc0d7e118c0843d70f2c8c4bcdd33"
    }
  }
}
```

> `ref_block_bytes` / `ref_block_hash` 取自构造时的最新块；`expiration` = `timestamp` + 60s；`txID` 是 `raw_data` 的 SHA256 hash，因此随上述字段变化，同一请求两次得到的 `txID` 不同。
>
> `feeLimit` = `gas × wallet.getEnergyFee()`，仅 `CreateSmartContract` / `TriggerSmartContract` 自动覆写到 `raw_data.fee_limit`；`TransferContract` / `TransferAssetContract` 不需要 feeLimit（上例 `raw_data` 中无 `fee_limit` 字段即此原因）。

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| 当前节点不是 FullNode（Solidity） | `-32601` | `the method buildTransaction does not exist/is not available in SOLIDITY` |
| `from` 缺失 / 非法 | `-32600` | `invalid json request` |
| 合约类型推断失败（如 `to` + `data` + `value` 同时为空） | `-32600` | `invalid json request` |
| `to` 非空但非法 hex / 长度不对 | `-32602` | 透传 `addressCompatibleToByteArray` 异常 message |
| `input` 不是严格 hex | `-32602` | 透传 `JsonRpcApiUtil.requireValidHex` 校验信息 |
| `data` 和 `input` 都设置但解析出的 bytes 不一致 | `-32602` | `both "data" and "input" are set and not equal. Please use "input" to pass transaction call data` |
| `value` 不是合法 hex | `-32602` | `invalid param value: invalid hex number` |
| `gas` 不是合法 hex | `-32602` | `invalid param value: invalid hex number` |
| `tokenId` 转字符串后非法（仅 TRC-10 路径） | `-32602` | `invalid param value: invalid tokenId` |
| 合约校验失败（`ContractValidateException`） | `-32600` | 透传 message |
| 内部异常 | `-32000` | 透传 message |
