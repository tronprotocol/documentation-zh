# wallet-cli contract create2

计算使用 CREATE2 部署合约时生成的地址。

## 用法

```
wallet-cli contract create2 --deployer <address> (--code <hex> | --code-file <path>) --salt <n> [options]
```

## 说明

纯本地运算：不访问节点、不广播，也不涉及任何账户或密码。结果在所有 TRON 网络上都一致，因此 `--network` 对它没有影响。仅限 TRON——在 EVM 网络上本命令会以 `family_mismatch` 失败。

**TRON 的推导方式与以太坊不同**——不要拿 EVM 的计算器来算。地址为

```
sha3omit12( deployer (21 bytes, 0x41-prefixed) ‖ salt (32 bytes) ‖ keccak256(code) )
```

其中 `sha3omit12` 取 `keccak256` 摘要的 `[11:32]` 字节，把首字节改写为 `0x41`，再对结果做 `Base58Check` 编码。这里没有 `0xff` 前缀：21 字节、带 `0x41` 前缀的 `deployer` 本身已经区隔了域。因此同样的 `deployer`、`salt` 和 `code`，在 TRON 和以太坊上会得到不同的地址。

**这里的 `code` 必须是已经追加构造函数参数的 `creation bytecode`**，不能使用 `runtime bytecode`。
构造函数参数只要相差一个字节，计算出的地址就会不同。由于 `creation bytecode` 通常很长，建议使用
`--code-file`；无论采用哪种输入方式，CLI 都会自动移除 `0x` 前缀和空白字符。

`--salt` 是一个十进制整数（64 位有符号）。它会被放进 32 字节 `salt` 的低位，其余部分补零；不接受十六进制形式的 `salt`。

真正用 CREATE2 部署要求链上已启用 `TVM Constantinople`，但本命令只做算术运算，不受该限制。

## 选项

| 选项 | 说明 |
|---|---|
| `--deployer <address>` | **必填。** 执行 CREATE2 的地址——可以是工厂合约，也可以是普通账户 |
| `--code <hex>` | `creation bytecode`，含构造函数参数。`--code` / `--code-file` 二选一 |
| `--code-file <path>` | 从文件读取 `creation bytecode`——推荐用法，因为它通常非常长。`--code` / `--code-file` 二选一 |
| `--salt <n>` | **必填。** 十进制整数形式的 `salt`，补零至 32 字节 |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli contract create2 --deployer TQkXm4vN...5Zt7Uw --code-file ./MyToken.creation.hex --salt 1
```

```console
Contract address (CREATE2)
  Deployer   TQkXm4vN...5Zt7Uw
  Salt       1  (0x000000…0001)
  Code hash  c8f4a1...b91b
  Address    TXm5RQ7d...9kPa
```

较短的 `bytecode` 也可以直接内联传入：

```bash
wallet-cli contract create2 --deployer TQkXm4vN...5Zt7Uw --code 6080604052... --salt 255 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"contract.create2","data":{"deployerAddress":"TQkXm4vN...","salt":255,"saltHex":"0x00000000000000000000000000000000000000000000000000000000000000ff","codeHash":"c8f4a1...b91b","address":"TWq8dK3n...2mHb"},"meta":{"durationMs":3,"warnings":[]},"chain":{"family":"tron","network":"tron:728126428","chainId":"728126428"}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `deployerAddress` | string | 传入的 `deployer`，base58 格式 |
| `salt` | number \| string | 传入的 `salt`，十进制。当它超出安全整数范围时是**字符串**，这样完整的 int64 salt 才能在 JSON 中原样保留 |
| `saltHex` | string | 真正参与哈希计算的、补零后的 32 字节 |
| `codeHash` | string | `creation bytecode` 的 `keccak256` |
| `address` | string | 推导出的合约地址，base58 格式 |

本命令从不访问节点，但它仍然是一条 TRON 链上命令：响应中会照常带上所选网络的 `chain` 块。这里的 `--network` 是可选的，只决定这个块里写的是哪个网络。

## 退出码

`0` 成功 · `1` 执行失败 · `2` 用法错误（`missing_option`——缺少 `--deployer` 或 `--salt`；`file_not_found`——`--code-file` 不存在；`invalid_value`——两个 code 来源都没给或都给了、code 文件读不了、`deployer` 地址格式非法、`code` 不是合法 hex，或 `salt` 超出 64 位有符号范围）。

## 另请参见

[`contract deploy`](deploy.md) · [`contract info`](info.md) · [`encoding convert`](../encoding/convert.md)
