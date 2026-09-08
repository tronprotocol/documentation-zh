# wallet-cli proposal list

列出链上的治理提案。

## 用法

```
wallet-cli proposal list [--state <active|all>] [--limit <n>] [--offset <n>] [options]
```

## 说明

列出提案及其批准进度、到期时间，以及每个提案将要设置的链参数。参数按名称显示，使用与 [`chain params`](../chain/params.md) 相同的词汇表。只读，无需账户。

**`Value` 是提案要设置的目标值，而不是当前生效值。** 提案只记录目标值，链上不保存提案创建时该参数的原值。对于已结算的提案，当前值可能已发生其他变化；对于刚通过且尚未被后续提案修改的提案，当前值就是该提案设置的值。请使用 [`chain params`](../chain/params.md) 查看当前生效值。

一个提案可以一次设置多个参数。列表不会截断它们：第一个参数排在提案所在的那一行上，其余参数各占一行，左侧几列留空。参数按参数 id 排序，所以同一个提案每次打印的顺序都一样；`data.proposals[].parameters[]` 也用同一顺序。

过滤在客户端完成，且发生在分页之前：`--state` 先缩小集合，然后 `--offset` / `--limit` 从中截取一个窗口。标题里带有数量——完整集合时是 `Proposals (4)`，一旦启用窗口就变成 `Proposals (showing 2 of 4)`。精确数字在 `meta.pagination` 里。没有任何匹配项时，标题后面会跟一个 `(none)`。

## 选项

| 选项 | 说明 |
|---|---|
| `--state <active\|all>` | `active` = 仍处于投票窗口内（默认）；`all` = 同时包含已通过、未通过和已取消的提案 |
| `--limit <number>` | 最多返回多少个提案（默认：全部） |
| `--offset <number>` | 分页偏移（默认 `0`） |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli proposal list --state all --network tron:3448148188
```

```console
Proposals (4)
  ID   State         Approvals   Expiry (UTC)       Parameter                       Value
  47   voting          12 / 18   2026-07-22 08:00   getTransactionFee                  15
  46   voting           5 / 18   2026-07-22 08:00   getCreateAccountFee            200000
  45   approved        18 / 18   2026-07-21 08:00   getEnergyFee                      140
  44   disapproved      8 / 18   2026-07-20 08:00   getMaintenanceTimeInterval   10800000
                                                    getMaxCpuTimeOfOneTx               80
```

第二页——跳过前两个，每页两个：

```bash
wallet-cli proposal list --state all --offset 2 --limit 2 --network tron:3448148188
```

```console
Proposals (showing 2 of 4)
  ID   State         Approvals   Expiry (UTC)       Parameter                       Value
  45   approved        18 / 18   2026-07-21 08:00   getEnergyFee                      140
  44   disapproved      8 / 18   2026-07-20 08:00   getMaintenanceTimeInterval   10800000
                                                    getMaxCpuTimeOfOneTx               80
```

```bash
wallet-cli proposal list --state all --network tron:3448148188 -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"proposal.list","data":{"approvalThreshold":18,"proposals":[{"id":47,"proposerAddress":"TSRmq8kP...","state":"voting","approvals":12,"expirationTime":1784707200000,"parameters":[{"id":3,"name":"getTransactionFee","value":15,"unit":"sun/byte"}]},{"id":46,"proposerAddress":"TSRmq8kP...","state":"voting","approvals":5,"expirationTime":1784707200000,"parameters":[{"id":2,"name":"getCreateAccountFee","value":200000,"unit":"sun"}]},{"id":45,"proposerAddress":"TSRee5...","state":"approved","approvals":18,"expirationTime":1784620800000,"parameters":[{"id":11,"name":"getEnergyFee","value":140,"unit":"sun"}]},{"id":44,"proposerAddress":"TSRee5...","state":"disapproved","approvals":8,"expirationTime":1784534400000,"parameters":[{"id":0,"name":"getMaintenanceTimeInterval","value":10800000,"unit":"ms"},{"id":13,"name":"getMaxCpuTimeOfOneTx","value":80,"unit":"ms"}]}]},"meta":{"durationMs":31,"warnings":[],"pagination":{"offset":0,"limit":null,"total":4}},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `approvalThreshold` | number | 通过所需的批准数 = 活跃超级代表数的 70 % |
| `proposals[].id` | number | 提案 id |
| `proposals[].proposerAddress` | string | 创建者，base58 |
| `proposals[].state` | string | `voting` / `approved` / `disapproved` / `canceled` |
| `proposals[].approvals` | number | 目前已投出的批准数 |
| `proposals[].expirationTime` | number | 投票窗口结束时间，epoch 以来的毫秒数 |
| `proposals[].parameters[]` | array | `id`、`name`、`value`（提案要设置的值）、`unit`；按 `id` 排序 |
| `meta.pagination` | object | `offset`、`limit`（`null` = 不限）、按 `--state` 过滤之后的 `total` |

## 退出码

`0` 成功 · `1` 执行失败（`rpc_error`） · `2` 用法错误（`invalid_value`——`state`、`limit` 或 `offset` 取值不合法）。

## 另请参见

[`proposal show`](show.md) · [`proposal create`](create.md) · [`chain params`](../chain/params.md)
