# /wallet/estimateenergy

预估调用合约所需能量。需节点开启 `vm.estimateEnergy=true`。

- 源码：`framework/src/main/java/org/tron/core/services/http/EstimateEnergyServlet.java`
- Method：`POST`
- Contract：`protocol.TriggerSmartContract`
- Response：`api.EstimateEnergyMessage`
- 支持固化接口：`/walletsolidity/estimateenergy`

## 请求参数

参数同 [`/wallet/triggerconstantcontract`](triggerconstantcontract.md)。

示例：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/estimateenergy \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "contract_address": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f",
  "function_selector": "balanceOf(address)",
  "parameter":         "000000000000000000000000dd791d6b49e190062d650e6a23c575510d35f2f9"
}
'
```

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `result` | Return | 调用结果（success/error） |
| `energy_required` | int64 | 预估所需能量 |

响应示例：

```json
{
  "result": { "result": true },
  "energy_required": 1870
}
```

未开启 `vm.estimateEnergy=true` 时调用走异常分支（见下文），通常表现为 `result.code = OTHER_ERROR`、`result.message` 含 `this node does not support estimate energy`。

### 异常响应

不会写出 `{"Error": ...}`。所有异常被 catch 后写入 `result.code`、`result.message`，HTTP 体仍是 `EstimateEnergyMessage`：

| 触发条件 | `result.result` | `result.code` | `result.message` |
|---|---|---|---|
| 合约不存在 / 校验失败（`ContractValidateException`） | false | `CONTRACT_VALIDATE_ERROR` | 校验器原始描述 |
| 节点未开启 `vm.estimateEnergy` / EVM revert / 其他 | false | `OTHER_ERROR` | `<exceptionClass> : <message>`（`"` → `'`） |

异常路径下 `energy_required` 字段不被填充（值为 0）。
