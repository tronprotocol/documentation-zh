# wallet-cli token list

列出 token 地址簿（official + user）。

## 用法

```
wallet-cli token list [options]
```

## 说明

列出当前账户（或 `--account` 指定的账户）在所选网络上可见的全部 token：内置的 **official** 层，加上你自己添加的 **user** 条目。`source` 列用于区分两者。`tx send --token <symbol>` 解析符号时用的就是这张表。只读，且完全在本地完成——不需要密码，也不访问任何节点。

这张表是按网络划分的，因此同一条命令在 `tron:3448148188` 和 `eip155:11155111` 上列出的 token 并不相同。

## 选项

没有命令级选项；仅[全局选项](../index.md#global-options-every-command)（`--network` / `--account` 决定地址簿的作用范围）。

## 示例

```bash
wallet-cli token list --network tron:3448148188
```

```console
| Symbol | Name            | Source   | Contract / ID                      |
| ------ | --------------- | -------- | ---------------------------------- |
| USDT   | Tether USD      | official | TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf |
| USDD   | Usdd Stablecoin | official | TYQF9cAeJ3Faq8QXpHxTcFco72DRCQbgFt |
```

> `official` 层是按网络内置的，并非每个网络都有。没有内置条目的网络，只会列出你用 `token add` 添加的内容——在此之前是一张空表：
>
> ```console
> | Symbol | Name | Source | Contract / ID |
> | ------ | ---- | ------ | ------------- |
> ```

```bash
wallet-cli token list --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"token.list","data":{"network":"tron:3448148188","account":"wlt_n5v4r992","tokens":[{"kind":"trc20","id":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf","symbol":"USDT","decimals":6,"name":"Tether USD","source":"official"},{"kind":"trc20","id":"TYQF9cAeJ3Faq8QXpHxTcFco72DRCQbgFt","symbol":"USDD","decimals":18,"name":"Usdd Stablecoin","source":"official"}]},"meta":{"durationMs":15,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 包含 `network`、`account` 和 `tokens[]`——每个 token 一条：

| 字段 | 类型 | 含义 |
|---|---|---|
| `kind` | string | `trc20` / `trc10`（TRON）或 `erc20`（EVM） |
| `id` | string | 合约地址，或 TRC10 资产 id |
| `symbol` | string | Token 符号（`tx send --token` 用的就是它） |
| `decimals` | number | token 精度 |
| `name` | string | token 名称 |
| `source` | string | `official`（内置） / `user`（你自己添加的） |

## 退出码

`0` 成功 · `1` 执行失败 · `2` 用法错误。

## 另请参见

[`token add`](add.md) · [`token remove`](remove.md) · [发送 token](../../guide/send-tokens.md)
