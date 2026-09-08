# wallet-cli asset info

完整显示一个 TRC10。

## 用法

```
wallet-cli asset info (<asset> | --issuer <address>) [options]
```

## 说明

报告一个 token 的发行记录：发行方、总供应量、精度、ICO 比率与窗口、冻结批次、描述、URL，以及两项免费带宽限额。只读，不需要账户。

可以通过三种方式查询：按 id（全数字参数）、按名称，或按 `--issuer` 地址。`<asset>` 与 `--issuer` 必须且只能提供其一；两者均未提供或同时提供时会返回 `invalid_value`。由于每个账户只能发行一个 TRC10，按发行方查询最多返回一个结果。

链上不保证名称唯一。如果名称匹配到多个 token，命令不会直接返回列表，而是以退出码 `1` 和错误码 `ambiguous_asset_name` 失败，同时打印候选项，便于改用 id 重新查询。参见[下面的示例](#a-name-that-is-not-unique)。

空的小节会被整体省略：没有冻结批次的 token 完全不会显示 `Frozen` 块。

这里的时间戳精确到秒（`2026-08-01 00:00:00 UTC`），而不是 CLI 中其他地方那样精确到分。

它是 [`token info`](../token/info.md) 在 TRC10 上的专用对应命令；后者报告与 TRC20 共有的通用元数据（名称、符号、精度），且只能用 `--asset-id` 选择 TRC10。

输出不包含“已售数量”“剩余供应量”或持有人数，因为节点无法可靠计算这些数据：仅凭链上结果无法区分发行方的普通转账和 ICO 销售。要查看发行方当前持有量，请使用 [`account balance`](../account/balance.md) 查询其余额。

## 选项

| 选项 | 说明 |
|---|---|
| `<asset>` | token id 或名称；全数字的值按 id 解析。`<asset>` / `--issuer` 二选一 |
| `--issuer <address>` | 由该地址发行的 token。`<asset>` / `--issuer` 二选一 |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

按 id 查询：

```bash
wallet-cli asset info 1000123 --network tron:3448148188
```

```console
Asset MyToken (id 1000123)
  Issuer            TQkXm4vN...5Zt7Uw
  Total supply      1,000,000,000
  Precision         6
  Price             1 TRX = 100 MyToken
  ICO start time    2026-08-01 00:00:00 UTC
  ICO end time      2026-08-31 00:00:00 UTC
  Url               https://mytoken.io
  Description       Demo TRC10
  Free net/account  0
  Public free net   0
  Frozen (2)
    100,000,000  until 2026-08-31 00:00:00 UTC
    50,000,000   until 2026-10-30 00:00:00 UTC
```

### 名称不唯一的情况 {#a-name-that-is-not-unique}

```bash
wallet-cli asset info MyToken --network tron:3448148188
```

命令以退出码 `1` 失败；消息和候选表输出到 **stderr**：

```console
error [ambiguous_asset_name]: 2 TRC10 tokens are named MyToken; re-run with the id
| ID      | Issuer                             | Total supply  | Precision |
| ------- | ---------------------------------- | ------------- | --------- |
| 1000123 | TQkXm4vN2f8LrQ5tYc7bWmXe3sVd9Zt7Uw | 1,000,000,000 | 6         |
| 1000488 | TZx9kP2mR4nJ6vLc8dHqYe1tWbXs5f7bWq | 50,000,000    | 2         |
```

在 json 中，同样的信息位于 `error.details`——参见[输出](#output)。

按发行方查询——这里是别人的 token，且没有冻结批次：

```bash
wallet-cli asset info --issuer TZx9kP2m...7bWq --network tron:3448148188
```

```console
Asset MyToken (id 1000488)
  Issuer            TZx9kP2m...7bWq
  Total supply      50,000,000
  Precision         2
  Price             1 TRX = 5 MyToken
  ICO start time    2026-07-15 00:00:00 UTC
  ICO end time      2026-09-15 00:00:00 UTC
  Url               https://beta.example
  Description       Another TRC10
  Free net/account  0
  Public free net   0
```

```bash
wallet-cli asset info 1000123 --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"asset.info","data":{"kind":"asset-info","assetId":"1000123","name":"MyToken","abbr":"MTK","issuerAddress":"TQkXm4vN...","totalSupply":"1000000000000000","precision":6,"price":"1:100","trxNum":1,"num":100,"startTime":1785542400000,"endTime":1788134400000,"url":"https://mytoken.io","description":"Demo TRC10","freeAssetNetLimit":0,"publicFreeAssetNetLimit":0,"frozenSupply":[{"amount":"100000000000000","days":30,"expireTime":1788134400000},{"amount":"50000000000000","days":90,"expireTime":1793318400000}]},"meta":{"durationMs":26,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

名称歧义失败在 json 中的形式：

```bash
wallet-cli asset info MyToken --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":false,"command":"asset.info","error":{"code":"ambiguous_asset_name","message":"2 TRC10 tokens are named MyToken; re-run with the id","details":{"name":"MyToken","assetIds":["1000123","1000488"],"matches":[{"assetId":"1000123","issuerAddress":"TQkXm4vN...","totalSupply":"1000000000000000","precision":6},{"assetId":"1000488","issuerAddress":"TZx9kP2m...","totalSupply":"5000000000","precision":2}]}},"meta":{"durationMs":29,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出 {#output}

`data.kind` is `asset-info`.

| 字段 | 类型 | 含义 |
|---|---|---|
| `assetId` | string | Token id |
| `name` / `abbr` | string | 发行时的名称和缩写。`abbr` 仅在 json 中——text 没有对应行 |
| `issuerAddress` | string | 发行方，base58 |
| `totalSupply` | string | 总供应量，原始值（完整 token × 10^`precision`）。是**字符串**：供应量会达到 int64，作为 JSON number 会损失精度 |
| `precision` | number | 小数位数，0–6 |
| `price` | string | 发行比率，形如 `trx:tokens`，以完整单位计——text 渲染为 `1 TRX = 100 MyToken` |
| `trxNum` / `num` | number | 与链上存储完全一致的比率，以 sun 和最小单位表示，并在发行时约分为最简形式。当 `precision` 为 6 时，`1:100` 存储为 `trxNum=1` / `num=100` |
| `startTime` / `endTime` | number | ICO 窗口，epoch 以来的毫秒数 |
| `url` / `description` | string | 项目页面和描述 |
| `freeAssetNetLimit` / `publicFreeAssetNetLimit` | number | 每位持有人的免费带宽，以及共享池 |
| `frozenSupply[]` | array | `amount`（原始值，**字符串**）、`days`、`expireTime`（epoch 以来的毫秒数）。没有时为空数组 |

不存在 `remainingSupply` 字段。

匹配到多个 token 的名称会失败，而不是返回数据。此时 `error.details` 携带 `name`、`assetIds[]`（可用于重跑的 id）以及 `matches[]`——每个候选一行扁平记录，含 `assetId`、`issuerAddress`、`totalSupply`（原始值，字符串）和 `precision`。text 模式把 `matches[]` 渲染成上面所示的表格，并按各自的 `precision` 缩放 `totalSupply`。

## 退出码

`0` 成功 · `1` 执行失败（`asset_not_found`——没有这个 token；`ambiguous_asset_name`——名称匹配到多个 token；`rpc_error`） · `2` 用法错误（`invalid_value`——`<asset>` 与 `--issuer` 都没给或都给了；或 `--issuer` 不是有效的 base58 TRON 地址）。

## 另请参见

[`asset list`](list.md) · [`token info`](../token/info.md) · [`asset participate`](participate.md)
