# wallet-cli 8004 operator-check

检查某个操作者是否可以管理某所有者的全部 Agent。

## 用法

```
wallet-cli 8004 operator-check <owner> <operator> [options]
```

## 说明

读取注册表中「针对该所有者全部 Agent」的批准——也就是 [`8004 add-operator`](add-operator.md) 授予、[`8004 remove-operator`](remove-operator.md) 收回的那一种。它不反映 [`8004 approve`](approve.md) 针对单个 Agent 的批准；那一种由 [`8004 show`](show.md) 显示。不需要钱包，也不需要密码。

两个地址都必须属于所选网络的链家族。

可在部署了 ERC-8004 身份注册表的网络上运行：`tron`、`nile`、`shasta`、`bsc`、`bsc-testnet`、`base`、`base-sepolia`。见 [`8004`](index.md)。

## 参数

- `owner`——拥有这些 Agent 的地址
- `operator`——要检查的地址

## 选项

没有本命令特有的选项；仅[全局选项](../index.md#global-options-every-command)。

## 示例

检查 `TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH` 是否可以管理 `TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ` 的全部 Agent：

```bash
wallet-cli 8004 operator-check TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH --network nile
```

```console
Owner                    TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ
Operator                 TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH
Approved for all Agents  No
Registry                 TDDk4vc69nzBCbsY4kfu7gw2jmvbinirj5
```

```bash
wallet-cli 8004 operator-check TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH --network nile -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"8004.operator-check","data":{"owner":"TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ","operator":"TGkbaCYB4kRBc3Q6wjqkACefUvRwf2KzkH","approved":false,"registry":"TDDk4vc69nzBCbsY4kfu7gw2jmvbinirj5"},"meta":{"durationMs":1314,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

`Approved for all Agents No`（JSON 中的 `approved: false`）表示该操作者无权管理这位所有者的 Agent；执行 [`8004 add-operator`](add-operator.md) 之后，这里会显示 `Yes`（`true`）。

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `owner` | string | 被检查的所有者地址 |
| `operator` | string | 被检查的操作者地址 |
| `approved` | boolean | `operator` 是否可以管理 `owner` 的全部 Agent |
| `registry` | string | 身份注册表的合约地址 |

## 退出码

`0` 成功 · `1` 执行失败（`rpc_error`、`timeout`） · `2` 用法错误（`family_mismatch`——地址属于另一个链家族；`unsupported_network_capability`——所选网络上没有注册表）。

## 另请参见

[`8004 add-operator`](add-operator.md) · [`8004 remove-operator`](remove-operator.md) · [`8004 show`](show.md)
