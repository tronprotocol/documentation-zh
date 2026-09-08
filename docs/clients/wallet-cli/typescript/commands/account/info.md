# wallet-cli account info

显示账户的链上状态。

## 用法

```
wallet-cli account info [options]
```

## 说明

返回链上对该地址的已知信息。**字段集合**本身——而不只是取值——取决于所选网络所属的链家族：

- **TRON**——节点提供的完整账户对象（余额、权限、质押信息），外加规范化的带宽与能量 `resources` 摘要。可以通过它检查账户是否有足够资源，从而预估交易是否需要燃烧 TRX。
- **EVM**——余额、交易 `nonce`，以及该地址是否部署了代码（`type`：`eoa` 或 `contract`）。EVM 没有资源模型可供报告。

## 选项

仅[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli account info --network tron:3448148188
```

```console
Label        demo
Address      TNmoJ3Be59WFEq5dsW6eCkZjveiL3G8HVB
Balance      9,915.80311 TRX
Energy       used 0 / 0
Bandwidth    used 325 / 600
Created      2025-07-30
Permissions  owner 1-of-2, 1 active group
```

```bash
wallet-cli account info --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"account.info","data":{"address":"TNmoJ3Be59WFEq5dsW6eCkZjveiL3G8HVB","account":{"account_name":"71612d74657374","balance":"9915803110","create_time":1753860222000,"owner_permission":{"threshold":1,"keys":[{},{}]},"active_permission":[{}],"frozenV2":[{},{"type":"ENERGY"},{"type":"TRON_POWER"}]},"resources":{"bandwidth":{"used":325,"limit":600},"energy":{"used":0,"limit":0}}},"meta":{"durationMs":746,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

在 EVM 网络上，同一条命令报告的是 EVM 账户状态：

```bash
wallet-cli account info --network eip155:11155111
```

```console
Label    test1
Address  0x541B10b92b45C08513e67bb8209f035D810212B6
Balance  0 ETH
Nonce    0
Type     EOA
```

```bash
wallet-cli account info --network eip155:11155111 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"account.info","data":{"address":"0x541B10b92b45C08513e67bb8209f035D810212B6","balance":"0","nonce":0,"decimals":18,"symbol":"ETH","type":"eoa"},"meta":{"durationMs":402,"warnings":[]},"chain":{"family":"evm","network":"eip155:11155111","chainId":"11155111"}}
```

## 输出

`address` 始终存在；`data` 的其余部分则因链家族而异。

TRON：

| 字段 | 类型 | 含义 |
|---|---|---|
| `address` | string | 被查询的 base58 地址 |
| `account` | object | 由 TRON 节点原样返回的账户对象：`balance`（SUN 字符串）、各类时间戳、`owner_permission` / `active_permission`（多签密钥与阈值）、`frozenV2`（按类型的质押金额）等；字段由节点决定，wallet-cli 不做重塑 |
| `resources.bandwidth` | object | `used` / `limit`（字节） |
| `resources.energy` | object | `used` / `limit` |

EVM：

| 字段 | 类型 | 含义 |
|---|---|---|
| `address` | string | 被查询的 `0x` 地址，采用 EIP-55 校验和格式 |
| `balance` | string | 以 wei 计的原生余额 |
| `nonce` | number | 该地址已发出的交易数；也就是下一笔交易的 nonce |
| `decimals` | number | `18` |
| `symbol` | string | 该网络的原生币——`ETH`、`BNB` |
| `type` | string | `eoa`（无代码）或 `contract`（该地址上部署了代码） |

`resources` 块由 wallet-cli 规范化——稳定，可安全地编程依赖；`account` 由节点原样返回，其字段随节点/协议而变，不保证稳定。

## 退出码

`0` · `1` 执行失败 · `2` 用法错误。

## 另请参见

[`account balance`](balance.md) · `stake freeze`——获取资源（TRON） · [资源模型](../../concepts/networks.md#fees-the-tron-resource-model)
