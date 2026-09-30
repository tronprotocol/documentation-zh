# wallet-cli 8004 update

修改某个 Agent 的注册 URI。

## 用法

```
wallet-cli 8004 update <id> <uri>
                  [--wait [--wait-timeout <ms>] | --sign-only | --build-only | --dry-run]
                  [--fee-limit <sun>] [--permission-id <n>] [--expiration <ms>] [options]
```

## 说明

调用注册表的 `setAgentURI(uint256,string)`。只有该 Agent 的所有者、它已批准的操作者，或所有者通过 [`8004 add-operator`](add-operator.md) 添加的操作者才能执行；其他任何人都会在手续费估算阶段、签名之前被以 `not_authorized` 拒绝。不存在的 Agent ID 同样在此阶段以 `agent_not_found` 失败。

URI 的规则与 [`8004 register`](register.md) 相同：`https://`、`ipfs://` 或 base64 JSON 的 `data:`，最长 2048 个字符。[`8004 show`](show.md) 只加载 `https://` 和 `http://` 的文档，因此用 `ipfs://` 或 `data:` URI 注册的 Agent 在那里不会显示注册详情；若希望能用 wallet-cli 读到这些内容，请优先使用 `https://`。

回执中会给出变更前读到的 URI（`oldURI`）和你请求设置的那个。加上 `--wait` 时，它会在确认之后再读一次 URI，并补上 `newURI`。

需要一个账户。只有会签名的模式才需要通过 `--password-stdin` 提供 master password。

可在部署了 ERC-8004 身份注册表的网络上运行：`tron`、`nile`、`shasta`、`bsc`、`bsc-testnet`、`base`、`base-sepolia`。见 [`8004`](index.md)。

## 参数

- `id`——Agent ID，可选地带上它的规范网络 id 前缀（`<network-id>:<id>`，例如 `tron:3448148188:172`；不接受 `nile:172` 这样的别名形式）
- `uri`——新的注册 URI

## 选项

| 选项 | 说明 |
|---|---|
| `--wait` / `--wait-timeout <ms>` | 广播后轮询直到已确认/失败（上限默认取配置 `waitTimeoutMs`，内置 60000） |
| `--sign-only` | 只签名不广播，输出已签名的 hex；与 `--dry-run` / `--build-only` 互斥 |
| `--build-only` | 构建并估算，输出**未签名**的 hex，且不解锁钱包；与 `--dry-run` / `--sign-only` 互斥 |
| `--dry-run` | 只做估算，不签名/不广播；与 `--sign-only` / `--build-only` 互斥 |
| `--password-stdin` | 从 stdin 读取 master password |

仅限 TRON：

| 选项 | 说明 |
|---|---|
| `--fee-limit <sun>` | 允许燃烧的最高能量费用，单位 SUN（默认 100000000） |
| `--permission-id <n>` | 签名所用的权限组（0=owner，1=witness，2-9=active）；默认 `0` |
| `--expiration <ms>` | 交易过期时间（毫秒），最大 `86400000`（24 小时）；仅可与 `--sign-only` 或 `--build-only` 同用；省略时使用节点默认值（约 60 秒） |

没有 EVM 侧的费用参数：在 EVM 上，gas 上限和费用均取自节点的估算，`--gas-limit` 之类会被当作未知选项拒绝。

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

把 Agent 173 指向一份新的注册文档，并等待确认。 `$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入。

```bash
printf '%s' "$PW" | wallet-cli 8004 update 173 "data:application/json;base64,eyJuYW1lIjoiV2VhdGhlciBBZ2VudCIsImRlc2NyaXB0aW9uIjoiUmV0dXJucyB3ZWF0aGVyIGZvcmVjYXN0cyBhbmQgYWxlcnRzIGZvciBhIGNpdHkifQ==" --network nile --wait --password-stdin
```

```console
✅ Called setAgentURI
  Contract       TDDk4vc69nzBCbsY4kfu7gw2jmvbinirj5
  Agent ID       173
  Previous URI   data:application/json;base64,eyJuYW1lIjoiV2VhdGhlciBBZ2VudCIsImRlc2NyaXB0aW9uIjoiUmV0dXJucyB3ZWF0aGVyIGZvcmVjYXN0cyBmb3IgYSBjaXR5In0=
  Requested URI  data:application/json;base64,eyJuYW1lIjoiV2VhdGhlciBBZ2VudCIsImRlc2NyaXB0aW9uIjoiUmV0dXJucyB3ZWF0aGVyIGZvcmVjYXN0cyBhbmQgYWxlcnRzIGZvciBhIGNpdHkifQ==
  Current URI    data:application/json;base64,eyJuYW1lIjoiV2VhdGhlciBBZ2VudCIsImRlc2NyaXB0aW9uIjoiUmV0dXJucyB3ZWF0aGVyIGZvcmVjYXN0cyBhbmQgYWxlcnRzIGZvciBhIGNpdHkifQ==
  TxID           ea234c8c75d336e75d53cde5966b570912a2267979a8c3a4a0a817aab7820ee0
  Block          #71,015,905
  Energy         36,791
  Fee            4.218 TRX
  Status         success
```

```bash
printf '%s' "$PW" | wallet-cli 8004 update 173 "data:application/json;base64,eyJuYW1lIjoiV2VhdGhlciBBZ2VudCIsImRlc2NyaXB0aW9uIjoiUmV0dXJucyB3ZWF0aGVyIGZvcmVjYXN0cyBhbmQgYWxlcnRzIGZvciBhIGNpdHkifQ==" --network nile --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"8004.update","data":{"kind":"contract-send","stage":"confirmed","txId":"b6231d3f66e5c8d58a82318e76bb2ab4a7f6a96f731db80043e86d64f49470fe","confirmed":true,"blockNumber":71015908,"feeSun":4218000,"energyUsed":36791,"energyFeeSun":3679000,"netFeeSun":539000,"result":"SUCCESS","failed":false,"method":"setAgentURI(uint256,string)","contract":"TDDk4vc69nzBCbsY4kfu7gw2jmvbinirj5","identity":{"agentId":"173","oldURI":"data:application/json;base64,eyJuYW1lIjoiV2VhdGhlciBBZ2VudCIsImRlc2NyaXB0aW9uIjoiUmV0dXJucyB3ZWF0aGVyIGZvcmVjYXN0cyBmb3IgYSBjaXR5In0=","requestedURI":"data:application/json;base64,eyJuYW1lIjoiV2VhdGhlciBBZ2VudCIsImRlc2NyaXB0aW9uIjoiUmV0dXJucyB3ZWF0aGVyIGZvcmVjYXN0cyBhbmQgYWxlcnRzIGZvciBhIGNpdHkifQ==","newURI":"data:application/json;base64,eyJuYW1lIjoiV2VhdGhlciBBZ2VudCIsImRlc2NyaXB0aW9uIjoiUmV0dXJucyB3ZWF0aGVyIGZvcmVjYXN0cyBhbmQgYWxlcnRzIGZvciBhIGNpdHkifQ=="}},"meta":{"durationMs":6539,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

`Previous URI` 是变更前的 URI，`Requested URI` 是你提交的那个，`Current URI` 则是确认之后读回来的。

## 输出

`data` 随阶段而异：

| 模式 | 字段 |
|---|---|
| 默认（提交） | `kind: "contract-send"`、`stage: "submitted"`、`txId`、`method`、`contract`、`identity` |
| `--wait`（已确认/失败） | 同上，但 `stage` 为 `"confirmed"` 或 `"failed"`，另加 `confirmed`、`blockNumber`、`failed`，以及实际开销——TRON 上是 `feeSun` / `energyUsed` / `energyFeeSun` / `netFeeSun` / `result`，EVM 上是 `gasUsed` / `feeWei` / `effectiveGasPriceWei` |
| `--sign-only` | `kind`、`mode: "sign-only"`、`hex`、`signed`、`address`（签名者）、`txId`、`fee`、`method`、`contract`、`identity` |
| `--build-only` | `kind`、`mode: "build-only"`、`hex`（**未签名**）、`tx`、`fee`、`method`、`contract`、`identity` |
| `--dry-run` | `kind`、`mode: "dry-run"`、`fee`、未签名的 `tx`、`method`、`contract`，EVM 上另加 `nonce`，以及 `identity` |

`identity` 中有 `agentId`、`oldURI` 和 `requestedURI`；在 `--wait` 确认之后还会有 `newURI`。

## 退出码

`0` 已提交（提前退出的模式下则为已构建/已签名） · `1` 执行失败（`not_authorized`——该账户既不是本 Agent 的所有者，也不是它的操作者；`agent_not_found`——不存在该 id 的 Agent；`execution_reverted`——注册表因其他原因拒绝了该调用，原始 revert 数据在 `error.details.revertData` 中；`auth_required`——签名模式下未给出 `--password-stdin`；`watch_only_no_signer`、`auth_failed`、`rpc_error`、`timeout`——超时后交易仍可能在途，请用 [`tx status`](../tx/status.md) 查询） · `2` 用法错误（`invalid_value`——id 或 URI 格式错误，或选项组合不当，例如 `--expiration` 没有配 `--sign-only` / `--build-only`；`family_mismatch`——地址属于另一个链家族；`invalid_option`——`--wait` 与提前退出的模式同用；`unsupported_network_capability`——所选网络上没有注册表）

## 另请参见

[`8004 show`](show.md) · [`8004 register`](register.md)
