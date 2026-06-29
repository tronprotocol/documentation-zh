# eth_estimateGas

估算交易的 energy 消耗（即 Tron 中 gas 的对应物）。

- 源码：`framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#estimateGas`
- 端口：FullNode `8545` / Solidity `8555`

## 请求参数

| 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `params[0]` | object | 是 | `CallArguments`（同 [`eth_call`](eth_call.md)），其中 `from` / `to` / `value` / `data` 用于推断合约类型 |

`CallArguments.getContractType` 推断规则：

- `to` 为空且 `data` 非空 → `CreateSmartContract`
- `to` 是合约地址 → `TriggerSmartContract`
- `to` 是普通账户且 `value` 非空 → `TransferContract`（直接返回 `0x0`，不进入 EVM 估算）
- 其它情形 → 抛 `-32600 invalid json request[: invalid value]`

```bash
# 例：估算 Nile testnet 上一笔 TRX 转账的 energy 消耗
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc":"2.0","id":1,"method":"eth_estimateGas",
    "params":[{
      "from":"0xdd791d6b49e190062d650e6a23c575510d35f2f9",
      "to":"0xb06b4139895c9f51c967c9f3d9089ca721e8e34c",
      "value":"0xf4240"
    }]
  }'
```

## 响应

energy 用量的 hex 编码：

- 普通 TRX 转账（`TransferContract`）→ `0x0`
- 合约调用 / 部署 → 视节点配置：
    - `node.supportEstimateEnergy = true` 时返回 `EstimateEnergyMessage.energyRequired`
    - 默认（false）→ 返回 `TransactionExtention.energyUsed`（一次 constant-call 的实际用量）

下例为上面 curl 调用 Nile testnet 抓回的真实响应（TRX 转账走 `TransferContract` 路径，直接返回 `0x0`，不进入 EVM）：

```json
{ "jsonrpc": "2.0", "id": 1, "result": "0x0" }
```

### 异常响应

| 触发条件 | 错误码 | message |
|---|---|---|
| `from` 缺失 / 非法 hex / 长度不对 | `-32602` | 透传 `addressCompatibleToByteArray` 异常 message |
| `to` 非法 hex / 长度不对 | `-32602` | 透传 `addressCompatibleToByteArray` 异常 message |
| `from` 合法但 `to` + `data` 都缺失 | `-32600` | `invalid json request` |
| `to` 不是合约且 `value` 未传 | `-32600` | `invalid json request: invalid value` |
| 合约校验失败（`ContractValidateException`） | `-32600` | 透传 message（fallback `invalid contract`） |
| EVM 执行 `REVERT` | `-32000` | message + 解析后的 revert string；`error.data` 携带原始 revert hex |
| `data` / `value` hex 非法或其他内部异常 | `-32000` | 透传 message（双引号被替换为单引号） |
