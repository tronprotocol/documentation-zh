# wallet-cli contract info

查看合约 ABI 与元数据。

## 用法

```
wallet-cli contract info --contract <address> [options]
```

## 说明

获取已部署合约的 ABI 与元数据（合并了 `getContract` 与 `getContractInfo`），包括名称、方法列表、`origin` 地址、`bytecode` 和能量相关设置。在使用 [`contract call`](call.md) 或 [`contract send`](send.md) 前，可通过 ABI 确认准确的方法签名。该命令只读，不涉及账户或密码。

**仅限 TRON。** 链上 ABI 登记表是 TRON 的协议特性；EVM 链不在链上保存 ABI，因此在 EVM 网络上本命令会以 `family_mismatch` 失败。

## 选项

| 选项 | 说明 |
|---|---|
| `--contract <string>` | **必填。** 合约地址 |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli contract info --contract TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf --network tron:3448148188
```

```console
Contract  TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf
Name      TetherToken
Methods   33 (name / deprecate / approve …)
```

```bash
wallet-cli contract info --contract TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"contract.info","data":{"address":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf","name":"TetherToken","functionCount":33,"methods":["name","deprecate","approve","deprecated","addBlackList","totalSupply","transferFrom","…"],"contract":{"origin_address":"41…","contract_address":"41…","abi":{},"bytecode":"…","name":"TetherToken"},"info":{"smart_contract":{},"runtimecode":"…","contract_state":{}}},"meta":{"durationMs":15,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `address` | string | 合约地址 |
| `name` | string | 合约名称 |
| `functionCount` | number | ABI 中的函数数量 |
| `methods` | string[] | 函数名列表 |
| `contract` | object | `getContract` 原始返回（ABI、`bytecode`、`origin`）——仅 json |
| `info` | object | `getContractInfo` 原始返回（运行时代码、合约状态）——仅 json |

text 输出只给出便于阅读的摘要；`contract` / `info` 两项原始明细仅在 json 中提供。

## 退出码

`0` 成功 · `1` 执行失败（`rpc_error`；或该地址不是合约） · `2` 用法错误。

## 另请参见

[`contract call`](call.md) · [`contract deploy`](deploy.md) · [`token info`](../token/info.md)
