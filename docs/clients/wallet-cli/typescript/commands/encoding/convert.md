# wallet-cli encoding convert

自动识别输入，并打印它的所有等价表示。

## 用法

```
wallet-cli encoding convert <input>
```

## 说明

自动识别输入的编码，打印它的所有等价表示，并校验 checksum。命令会根据输入是否具有地址的形态，自动归入以下两个族之一：

- **地址族**——输入 TRON Base58Check 地址、TRON 41-hex 地址、EVM `0x` 地址或公钥 hex 后，命令会显示对应的全部地址形式。TRON 地址和 EVM 地址是**同一个 20 字节公钥哈希**的两种编码：`TRON` 使用 Base58Check 编码（带 `0x41` 前缀），`TRON hex` 是 `41` 加上这 20 个字节（共 21 个原始字节），`EVM` 则是 `0x` 加上同样的 20 个字节，并采用 EIP-55 大小写混合格式。因此，`TRON hex` 与 `EVM` 中间的 20 个字节完全相同，区别只在于 `41` 前缀和编码形式。输入公钥时（65 字节非压缩格式或 33 字节压缩格式），命令会先计算 Keccak 哈希并取末 20 字节，再进行地址编码。
- **编码族**——任何不具备地址形态的字节串（任意 hex / Base64 / Base58Check）都会被打印成它的 `Hex`、`Base64` 和 `Base58Check` 形式（Base58Check 输出带有 4 字节 checksum）。

该命令完全在本地运行，不访问节点，也**不**接受私钥或助记词。把敏感信息写在命令行参数中可能导致其
出现在 shell 历史和进程列表中。需要从私钥取得地址时，请使用
[`import private-key`](../import/private-key.md) 导入。

## 选项

没有命令专属选项；`input` 是位置参数。纯本地操作，因此没有 `--network`。此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

一个 TRON 地址会打印出它的全部地址形式：

```bash
wallet-cli encoding convert TBhCfAytTEh52WFL6HYr64i2nmc3u3TCUp
```

```console
TRON      TBhCfAytTEh52WFL6HYr64i2nmc3u3TCUp
TRON hex  4112e94f5a3c88b17d2f6e0b9a45cd310f8e7a6d29
EVM       0x12E94f5a3c88b17d2F6E0b9a45Cd310f8E7a6D29
```

```bash
wallet-cli encoding convert TBhCfAytTEh52WFL6HYr64i2nmc3u3TCUp -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"encoding.convert","data":{"input":"TBhCfAytTEh52WFL6HYr64i2nmc3u3TCUp","inputType":"tron-base58","valid":true,"tron":"TBhCfAytTEh52WFL6HYr64i2nmc3u3TCUp","tronHex":"4112e94f5a3c88b17d2f6e0b9a45cd310f8e7a6d29","evm":"0x12E94f5a3c88b17d2F6E0b9a45Cd310f8E7a6D29"},"meta":{"durationMs":2,"warnings":[]}}
```

公钥 hex 会解析出同一个地址：

```bash
wallet-cli encoding convert 04a1b2c3d4e5...f6a7b8c9d0
```

```console
TRON      TBhCfAytTEh52WFL6HYr64i2nmc3u3TCUp
TRON hex  4112e94f5a3c88b17d2f6e0b9a45cd310f8e7a6d29
EVM       0x12E94f5a3c88b17d2F6E0b9a45Cd310f8E7a6D29
```

不具备地址形态的输入会在各种编码之间互相转换，双向均可：

```bash
wallet-cli encoding convert deadbeef0102
```

```console
Hex          deadbeef0102
Base64       3q2+7wEC
Base58Check  DWcJPafcQr2coF
```

```bash
wallet-cli encoding convert 3q2+7wEC      # Base64 转回 hex
```

```console
Hex          deadbeef0102
Base64       3q2+7wEC
Base58Check  DWcJPafcQr2coF
```

checksum 校验失败时会给出具体原因：

```bash
wallet-cli encoding convert TBhCfAytTEh52WFL6HYr64i2nmc3u3TCUX
```

```console
error [invalid_value]: base58 checksum mismatch (typo in the address?)
```

## 输出

`data` 的结构取决于输入所属的族：

| 族 | 字段 |
|---|---|
| address | `input`、`inputType`（`tron-base58` / `tron-hex` / `evm` / `public-key`）、`valid`、`tron`、`tronHex`、`evm` |
| encoding | `input`、`inputType`（`hex` / `base64` / `base58check`）、`valid`、`hex`、`base64`、`base58check` |

## 退出码

`0` 成功 · `2` 用法错误（`invalid_value`——无法识别的输入或 checksum 不匹配；提示文本会给出具体原因）。

## 另请参见

[`address generate`](../address/generate.md) · [`import private-key`](../import/private-key.md)
