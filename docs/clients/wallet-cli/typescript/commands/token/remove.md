# wallet-cli token remove

从地址簿中删除一条自行添加的 token。

## 用法

```
wallet-cli token remove (--contract <address> | --asset-id <id>) [options]
```

## 说明

把你添加的某个 token 从地址簿的 user 层中删除（作用范围与 [`token add`](add.md) 一样，按网络 + 账户划分）。official 层的 token 无法删除——尝试删除会返回 `token_is_official`。

纯本地操作——链上的 token 和你的余额都不受影响，消失的只是本地的符号映射。

## 选项

| 选项 | 说明 |
|---|---|
| `--contract <string>` | 要删除的 token 合约地址——TRON 上为 TRC20，EVM 上为 ERC20 |
| `--asset-id <string>` | **仅限 TRON。** 要删除的 TRC10 数字资产 id；`--asset-id` / `--contract` 二者必选其一 |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli token remove --contract TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf --network tron:3448148188
```

```console
✅ Removed from token book
  Name    Tether USD
  Symbol  USDT
```

```bash
wallet-cli token remove --contract TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"token.remove","data":{"network":"tron:3448148188","account":"wlt_b2.0","removed":{"kind":"trc20","id":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf","symbol":"USDT","decimals":6,"name":"Tether USD"}},"meta":{"durationMs":15,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `network` | string | 该条目原先所属的网络 |
| `account` | string | 该条目原先所属的账户 |
| `removed` | object | 被删除的 token 条目（`kind`——`trc20`/`trc10`/`erc20`——以及 `id`、`symbol`、`decimals`、`name`） |

## 退出码

`0` 已删除 · `1` 执行失败（`encoding_error` / `io_error`——本地 token 地址簿无法解码或写入） · `2` 用法错误（`token_is_official`——official 层的 token 不能删除；`token_not_in_book`——user 层中没有这条；`invalid_value`；`invalid_option`——在 EVM 网络上使用了 `--asset-id`）。

## 另请参见

[`token add`](add.md) · [`token list`](list.md)
