# wallet-cli token add

向地址簿中添加 token，并从链上读取它的元数据。

## 用法

```
wallet-cli token add (--contract <address> | --asset-id <id>) [options]
```

## 说明

从合约读取该 token 的名称、符号和精度，并写入本地的 token 地址簿。TRON（TRC20/TRC10）和 EVM（ERC20）网络都可用。地址簿的作用范围是**网络 + 账户**：在 `tron:3448148188` 上为某个账户添加的 token，不会出现在其他网络或其他账户下。

添加之后，在别处就可以用符号来引用这个 token——例如 `tx send --token USDT`。地址簿分两层：**official**（内置，只读）和 **user**（你自己添加的）。如果该 token 已经内置在 official 层中，命令会以 `token_already_listed` 失败（无需重复添加）；如果你此前已经添加过，再添加一次不会报错——它会重新拉取该 token 的元数据（符号/精度/名称）并更新，返回 `action: refreshed`。

## 选项

| 选项 | 说明 |
|---|---|
| `--contract <string>` | token 合约地址——TRON 上为 TRC20，EVM 上为 ERC20 |
| `--asset-id <string>` | **仅限 TRON。** TRC10 数字资产 id；`--asset-id` / `--contract` 二者必选其一 |

此外还有[全局选项](../index.md#global-options-every-command)。

`--asset-id` 是仅限 TRON 的参数：`--help` 会给它打上 `(TRON only)` 标记，在 EVM 网络上传入它会在任何节点调用之前就以 `invalid_option` 失败。

## 示例

```bash
wallet-cli token add --contract TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf --network tron:3448148188
```

```console
✅ Added to token book
  Name      Tether USD
  Symbol    USDT
  Decimals  6
```

```bash
wallet-cli token add --contract TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"token.add","data":{"network":"tron:3448148188","account":"wlt_b2.0","action":"added","token":{"kind":"trc20","id":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf","symbol":"USDT","decimals":6,"name":"Tether USD"}},"meta":{"durationMs":15,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

EVM 网络上的 ERC20 token，此时 `token.kind` 为 `erc20`：

```bash
wallet-cli token add --contract 0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238 --network eip155:11155111
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `network` | string | 该条目所属的网络 |
| `account` | string | 该条目所属的账户 |
| `action` | string | `"added"`（首次添加） / `"refreshed"`（user 层中已存在，元数据已刷新） |
| `token.kind` | string | `trc20` / `trc10`（TRON）或 `erc20`（EVM） |
| `token.id` | string | 合约地址，或 TRC10 资产 id |
| `token.symbol` | string | 读取到的符号 |
| `token.decimals` | number | 读取到的精度 |
| `token.name` | string | 读取到的名称 |

## 退出码

`0` 已添加 · `1` 执行失败（`token_metadata_unavailable`——元数据读取失败，不会写入任何内容；`encoding_error` / `io_error`——本地 token 地址簿无法解码或写入） · `2` 用法错误（`token_already_listed`——已存在于 official 层；`invalid_value`；`invalid_option`——在 EVM 网络上使用了 `--asset-id`）。

## 另请参见

[`token list`](list.md) · [`token remove`](remove.md) · [`tx send`](../tx/send.md)
