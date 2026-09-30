# wallet-cli config

查看 / 读取 / 设置配置项。

## 用法

```
wallet-cli config [<key>] [<value>] [options]
```

## 参数

- `key`——要读取或设置的配置键；省略则显示完整的生效配置
- `value`——新值；省略则表示读取该键

## 选项

| 选项 | 说明 |
|---|---|
| `--api-key-stdin` | 从 stdin（fd 0）读取 B.AI API key。只有 `config baiApiKey` 接受该选项 |

此外还有[全局选项](index.md)。

## 注意事项

已知的配置键：

| 键 | 取值 | 内置默认值 | 含义 |
|---|---|---|---|
| `defaultNetwork` | 网络 id | `tron:728126428` | 省略 `--network` 时使用的网络 |
| `defaultOutput` | `text` \| `json` | `text` | 省略 `-o` 时使用的输出格式 |
| `timeoutMs` | 毫秒，任意大于 0 的有限数 | `60000` | 单次节点、服务或设备调用的默认超时（`--timeout` 可覆盖）。与 `waitTimeoutMs` 不同，它不要求是整数 |
| `waitTimeoutMs` | 整数毫秒 ≥ 0 | `60000` | 广播类命令 `--wait` 轮询的默认时间上限 |
| `gasfreeApiKey` | string | （未设置） | GasFree API key（[`gasfree`](gasfree/index.md)）。**敏感信息** |
| `gasfreeApiSecret` | string | （未设置） | GasFree API secret。**敏感信息** |
| `tronlinkSecretId` | string | （未设置） | TronLink 多签服务的 secretId（[`tx multisig`](tx/multisig.md)）。**敏感信息** |
| `tronlinkSecretKey` | string | （未设置） | TronLink 多签服务的 secretKey。**敏感信息** |
| `tronlinkChannel` | string | （未设置） | TronLink 多签服务的 channel |
| `baiApiKey` | string | （未设置） | B.AI 个人 API key，供 `bai` 系列命令使用。**敏感信息**——只能通过 `--api-key-stdin` 设置 |
| `aliases` | —— | —— | 简称 → 规范 id 的映射（只读） |
| `networks` | —— | —— | 已知网络及其可配置字段（作为整体只读） |
| `networks.<id>` | —— | —— | 某个网络的可配置字段；`<id>` 可以是规范 id，也可以是别名 |
| `networks.<id>.httpEndpoint` | URL | 每个网络各自的值 | 要使用的节点 / RPC 端点 |
| `networks.<id>.apiKeyHeader` | header 名 | （未设置） | 商用端点用于认证的 header，例如 `TRON-PRO-API-KEY` |
| `networks.<id>.apiKey` | string | （未设置） | 通过该 header 发送的凭据。**敏感信息**——读取时始终以掩码显示 |

`networks` 和 `aliases` 作为整体是只读的；可写的网络设置就是 `networks.<id>.…` 那三个叶子键。其他任何子键都会返回 `invalid_value`，错误信息会列出受支持的键。

同时存在命令行选项和配置键时的优先级（从高到低）：命令行选项 > 配置值 > 内置默认值——例如 `--timeout` > 配置 `timeoutMs` > 内置的 60000。

**敏感信息绝不会以明文呈现。** `tronlinkSecretId`、`tronlinkSecretKey`、`gasfreeApiKey`、`gasfreeApiSecret`、`baiApiKey` 和 `networks.<id>.apiKey` 在任何读取中都返回 `********`，设置它们时回显的 `value` 和 `input` 也都是 `"********"`。

**列表中的端点会被隐藏部分内容，只有按名称读取时才显示完整值。** `config` 和 `config networks` 只将 `httpEndpoint` 显示为主机名，因为商用端点可能把 key 放在 URL 路径中。只有明确查询某个网络（`config networks.tron:3448148188`）或其叶子键（`config networks.tron:3448148188.httpEndpoint`）时，CLI 才会显示完整 URL。

未设置的字段在视图中是**缺席**的，而不是存在但为空——这个视图说明的是「哪些*已经*配置了」。按名称读取一个未设置的键，只会返回 `key`（文本形式为 `<key>  Not configured`）。

外部服务的凭据是**按环境区分的**：GasFree（`gasfreeApiKey` / `gasfreeApiSecret`）和 TronLink（`tronlinkSecretId` / `tronlinkSecretKey` / `tronlinkChannel`）的凭据必须与当前 `--network` 所属的服务环境（主网 vs 测试网）匹配；不匹配会以 `provider_error` 失败，所以切换环境时记得同步更换。某个键未设置时，需要它的命令会给出明确的错误——[`gasfree`](gasfree/index.md) 报 `gasfree_credentials_missing`，[`tx multisig`](tx/multisig.md) 报 `tronlink_credentials_missing`。

**`baiApiKey` 的设置方式与其他所有键都不同。** 它绝不接受以命令行取值传入——`config baiApiKey <key>` 会以 `invalid_option` 失败——必须通过 `--api-key-stdin` 用管道送入。设置它只是把 key 保存到本地：不会访问 B.AI，不需要网络、账户或 master password，既不校验该 key，也不绑定任何钱包。[`bai recharge`](bai/recharge.md) 每次运行时都会检查付款地址的绑定情况，必要时先完成绑定。

取值非法时返回 `invalid_value`（退出码 2）。

## 示例

查看完整的生效配置：

```bash
wallet-cli config
```

```console
defaultNetwork     tron:728126428
defaultOutput      text
timeoutMs          60000
waitTimeoutMs      60000
networks
  tron:728126428
    httpEndpoint  api.trongrid.io
    apiKeyHeader  TRON-PRO-API-KEY
    apiKey        ********
  tron:3448148188
    httpEndpoint  nile.trongrid.io
  tron:2494104990
    httpEndpoint  api.shasta.trongrid.io
  eip155:1
    httpEndpoint  ethereum-rpc.publicnode.com
  eip155:11155111
    httpEndpoint  ethereum-sepolia-rpc.publicnode.com
  eip155:56
    httpEndpoint  bsc-dataseed.bnbchain.org
  eip155:97
    httpEndpoint  bsc-testnet-dataseed.bnbchain.org
  eip155:8453
    httpEndpoint  mainnet.base.org
  eip155:84532
    httpEndpoint  sepolia.base.org
aliases
  tron          tron:728126428
  tron:mainnet  tron:728126428
  nile          tron:3448148188
  tron:nile     tron:3448148188
  shasta        tron:2494104990
  tron:shasta   tron:2494104990
  ethereum      eip155:1
  sepolia       eip155:11155111
  bsc           eip155:56
  bsc-testnet   eip155:97
  base          eip155:8453
  base-sepolia  eip155:84532
tronlinkSecretId   ********
tronlinkSecretKey  ********
tronlinkChannel    test
gasfreeApiKey      ********
gasfreeApiSecret   ********
```

先读取某个键，再设置它：

```bash
wallet-cli config timeoutMs
```

```console
timeoutMs  60000
```

```bash
wallet-cli config timeoutMs 120000
```

```console
✅ Set config
  Key    timeoutMs
  Value  120000
```

```bash
wallet-cli config timeoutMs 120000 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"config","data":{"key":"timeoutMs","value":120000,"input":"120000"},"meta":{"durationMs":3,"warnings":[]}}
```

把某个网络指向你自己的节点，或指向一个通过 header 认证的商用端点：

```bash
wallet-cli config networks.tron:3448148188.httpEndpoint http://127.0.0.1:8090
```

```bash
wallet-cli config networks.tron:728126428.apiKeyHeader TRON-PRO-API-KEY
```

```bash
wallet-cli config networks.tron:728126428.apiKey <your-key>
```

保存 B.AI API key，从 stdin 读取：

```bash
printf '%s\n' "$BAI_KEY" | wallet-cli config baiApiKey --api-key-stdin
```

指名读取某个网络时，端点会完整给出，与上面的列表不同：

```bash
wallet-cli config networks.tron:3448148188
```

```console
networks.tron:3448148188
  httpEndpoint  https://nile.trongrid.io
```

```bash
wallet-cli config networks.tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"config","data":{"key":"networks.tron:3448148188","value":{"httpEndpoint":"https://nile.trongrid.io"}},"meta":{"durationMs":14,"warnings":[]}}
```

## 输出

`data` 随使用模式而异。本地命令——没有 `chain` 块。

| 模式 | `data` 字段 |
|---|---|
| 全部显示（无参数） | 每个配置键一个字段：`defaultNetwork`、`defaultOutput`、`timeoutMs`、`waitTimeoutMs`、`networks`（id → `{httpEndpoint, apiKeyHeader?, apiKey?}`，端点裁剪为主机名）、`aliases`（别名 → id）、`tronlinkSecretId`、`tronlinkSecretKey`、`tronlinkChannel`、`gasfreeApiKey`、`gasfreeApiSecret`、`baiApiKey`——各项仅在已设置时出现，敏感信息以掩码显示 |
| 读取（`<key>`） | `key`、`value`；该键未设置时只有 `key` |
| 设置（`<key> <value>`） | `key`、`value`、`input`（用户输入的原始字符串）；该键为敏感信息时两者均为 `"********"` |

## 退出码

`0` 成功 · `1` 执行失败（`io_error`——原子写入配置失败） · `2` 用法错误（`invalid_config`——`config.yaml` 不可读或不是合法 YAML；`insecure_config`——文件中存有服务凭据，却是符号链接或对同组/其他用户可读，请对其执行 `chmod 600`；`invalid_value`——未知的键、给只读键传了值，或使用了不受支持的 `networks.<id>.<field>`；`invalid_option`——在命令行上给出了 `baiApiKey`）。参见 [machine-interface](../machine-interface.md)。

## 另请参见

[网络](../concepts/networks.md) · [machine-interface](../machine-interface.md)
