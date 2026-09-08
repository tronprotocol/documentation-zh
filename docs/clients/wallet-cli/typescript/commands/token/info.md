# wallet-cli token info

查看 token 元数据。

## 用法

```
wallet-cli token info (--contract <address> | --asset-id <id>) [options]
```

## 说明

直接通过 RPC 从链上读取 token 元数据，不需要账户或密码。必须且只能指定一种查询方式：合约类 token 使用 `--contract`（TRON 上为 TRC20，EVM 上为 ERC20），TRC10 资产使用 `--asset-id`。

合约类 token（TRC20/ERC20）返回经过归一化的元数据。TRC10 的 `--asset-id` 查询则保留节点响应中以下划线命名的键，只将文本字段（`name`、`abbr`、`url`、`description`）解码为 UTF-8，并把 `total_supply` 等 int64 数量序列化为十进制字符串。因此，不应假定 TRC10 响应与合约类 token 具有相同的字段结构。

## 选项

| 选项 | 说明 |
|---|---|
| `--contract <string>` | token 合约地址——TRON 上为 TRC20，EVM 上为 ERC20 |
| `--asset-id <string>` | **仅限 TRON。** TRC10 数字资产 id；`--asset-id` / `--contract` 二者必选其一 |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli token info --contract TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf --network tron:3448148188
```

```console
Name      Tether USD
Symbol    USDT
Decimals  6
```

```bash
wallet-cli token info --contract TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"token.info","data":{"contract":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf","name":"Tether USD","symbol":"USDT","decimals":6,"totalSupply":"17600000000030000000"},"meta":{"durationMs":690,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

EVM 网络上的 ERC20 token——没有 `totalSupply`：

```bash
wallet-cli token info --contract 0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238 --network eip155:11155111 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"token.info","data":{"contract":"0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238","symbol":"USDC","decimals":6,"name":"USDC"},"meta":{"durationMs":409,"warnings":[]},"chain":{"family":"evm","network":"eip155:11155111","chainId":"11155111"}}
```

TRC10 查询保留节点自身的键名，同时把文本解码出来、并原样保留各项数量：

```bash
wallet-cli token info --asset-id 1002000 --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"token.info","data":{"id":"1002000","owner_address":"418225f3aa48a2d30643a64410abb1e914dfa0bd2f","name":"MyToken","abbr":"MTK","description":"Demo TRC10","url":"https://mytoken.example","total_supply":"1000000000","trx_num":1,"num":100,"precision":6,"start_time":1785542400000,"end_time":1788134400000,"free_asset_net_limit":0,"public_free_asset_net_limit":0,"frozen_supply":[]},"meta":{"durationMs":210,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

使用 `--contract`（TRC20/ERC20）时：

| 字段 | 类型 | 含义 |
|---|---|---|
| `contract` | string | token 合约地址 |
| `name` | string | token 名称 |
| `symbol` | string | Token 符号 |
| `decimals` | number | token 精度 |
| `totalSupply` | string | TRON 合约适配层返回时给出的总供应量；EVM 服务不返回该字段 |

使用 `--asset-id`（TRC10）时：

| 字段 | 类型 | 含义 |
|---|---|---|
| `id` / `owner_address` | string | 资产 id，以及节点给出的十六进制持有者地址 |
| `name` / `abbr` / `description` / `url` | string | 从节点响应中解码出的 UTF-8 文本 |
| `total_supply` | string | 精确的 int64 供应量，以最小单位计 |
| `trx_num` / `num` | number | 链上的 ICO 比率数对 |
| `precision` | number? | 资产精度；缺席表示 `0` |
| `start_time` / `end_time` | number | ICO 窗口，epoch 毫秒 |
| `free_asset_net_limit` / `public_free_asset_net_limit` | number? | 存在时给出的免费带宽限额 |
| `frozen_supply` | array? | 冻结批次；其中 `frozen_amount` 是十进制字符串，`frozen_days` 是数字 |

TRC10 这套结构里没有归一化的 `contract`、`symbol` 或 `decimals` 键。

## 退出码

`0` 成功 · `1` 执行失败（`token_metadata_unavailable`——该合约没有暴露 ERC20 风格的元数据；`rpc_error`） · `2` 用法错误（`invalid_value`；`invalid_option`——在 EVM 网络上使用了 `--asset-id`）。

## 另请参见

[`token add`](add.md) · [`token balance`](balance.md) · [`contract info`](../contract/info.md)
