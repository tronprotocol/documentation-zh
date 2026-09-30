# 命令参考

每个命令和子命令都有独立页面。大多数页面采用相同结构（用法 · 说明 · 选项 · 示例 · 输出 · 退出码 · 另请参见）；带位置参数的命令另有「参数」一节，少数简单命令则省略「说明」。命令组页面列出其下的所有子命令及相应链接。

## 哪些命令能在哪些网络上运行 {#which-commands-run-on-which-networks}

wallet-cli 支持两个链家族——**TRON** 和 **EVM**，而 `--network` 选中的是某个家族下的某一个网络。命令分为以下几类：

- **通用命令**——同一条命令在两个家族上都可用，家族相关的部分按家族各自命名：`account balance` / `info` / `portfolio`、`block`、`tx send` / `broadcast` / `status` / `info` / `sign`、`token`（全部五条）、`contract call` / `send` / `deploy`、`chain node` / `prices`、`message sign`、`typed-data sign`。
- **仅限 TRON**——该命令实现的是 TRON 独有的协议特性，EVM 上没有对应物：`account history` / `activate` / `set`、`chain params`、`contract info` / `clear-abi` / `create2` / `set-origin-energy-limit` / `set-user-resource-percent`、`tx approvals` / `multisig`，以及 `stake`、`vote`、`reward`、`proposal`、`witness`、`permission`、`asset`、`exchange` 和 `gasfree` 各组的全部命令。在 EVM 网络上运行它们，会在任何节点调用之前就以 **`family_mismatch`** 失败。
- **服务类命令**——`x402` 和 `bai` 访问的是 HTTP 服务，而不是链节点。其中会付款的那些（`x402 pay` / `roundtrip`、`bai recharge`）使用所选网络的家族；而目录、用量和上报类命令不需要网络。`8004` 在两个家族上都可运行，但仅限部署了 ERC-8004 注册表的网络——不含 `ethereum` 和 `sepolia`。
- **本地命令**——完全不联网：`create`、`import`、`use`、`current`、`list`、`derive`、`rename`、`backup`、`delete`、`change-password`、`config`、`networks`、`contact`、`encoding`、`address`。其中一部分仍然接受 `--network`，但它只作为**显示选择器**（打印哪个家族的地址、keystore 导出取哪把密钥）；无论如何都不会访问节点。

单个参数也是按家族划分的。`--help` 会给它们打上 `(TRON only)` / `(EVM only)` 标记，把其中之一用在另一个家族上属于用法错误——`invalid_option`，退出码 `2`。

这一切以能力发现目录为准：`wallet-cli --json-schema` 会为每条命令给出一个 `families` 数组。

## 钱包与账户

| 命令 | 页面 |
|---|---|
| `create` | [create.md](create.md) |
| `import`（命令组） | [import/index.md](import/index.md) |
| `import mnemonic` | [import/mnemonic.md](import/mnemonic.md) *（仅支持交互式）* |
| `import private-key` | [import/private-key.md](import/private-key.md) *（仅支持交互式）* |
| `import keystore` | [import/keystore.md](import/keystore.md) *（仅支持交互式）* |
| `import ledger` | [import/ledger.md](import/ledger.md) |
| `import watch` | [import/watch.md](import/watch.md) |
| `list` | [list.md](list.md) |
| `use` | [use.md](use.md) |
| `current` | [current.md](current.md) |
| `derive` | [derive.md](derive.md) |
| `rename` | [rename.md](rename.md) |
| `backup` | [backup.md](backup.md) |
| `delete` | [delete.md](delete.md) |
| `change-password` | [change-password.md](change-password.md) |

## 交易

| 命令 | 页面 |
|---|---|
| `tx`（命令组） | [tx/index.md](tx/index.md) |
| `tx send` | [tx/send.md](tx/send.md) |
| `tx broadcast` | [tx/broadcast.md](tx/broadcast.md) |
| `tx status` | [tx/status.md](tx/status.md) |
| `tx info` | [tx/info.md](tx/info.md) |
| `tx sign` | [tx/sign.md](tx/sign.md) |
| `tx approvals` | [tx/approvals.md](tx/approvals.md) |
| `tx multisig` | [tx/multisig.md](tx/multisig.md) |

## 链上查询

| 命令 | 页面 |
|---|---|
| `account`（命令组） | [account/index.md](account/index.md) |
| `account balance` | [account/balance.md](account/balance.md) |
| `account info` | [account/info.md](account/info.md) |
| `account history` | [account/history.md](account/history.md) |
| `account portfolio` | [account/portfolio.md](account/portfolio.md) |
| `account activate` | [account/activate.md](account/activate.md) |
| `account set` | [account/set.md](account/set.md) |
| `block` | [block.md](block.md) |
| `chain`（命令组） | [chain/index.md](chain/index.md) |
| `chain params` | [chain/params.md](chain/params.md) |
| `chain prices` | [chain/prices.md](chain/prices.md) |
| `chain node` | [chain/node.md](chain/node.md) |

## 账户权限

| 命令 | 页面 |
|---|---|
| `permission`（命令组） | [permission/index.md](permission/index.md) |
| `permission show` | [permission/show.md](permission/show.md) |
| `permission update` | [permission/update.md](permission/update.md) |

## token 与合约

| 命令 | 页面 |
|---|---|
| `token`（命令组） | [token/index.md](token/index.md) |
| `token balance` | [token/balance.md](token/balance.md) |
| `token info` | [token/info.md](token/info.md) |
| `token add` | [token/add.md](token/add.md) |
| `token list` | [token/list.md](token/list.md) |
| `token remove` | [token/remove.md](token/remove.md) |
| `contact`（命令组） | [contact/index.md](contact/index.md) |
| `contact add` | [contact/add.md](contact/add.md) |
| `contact list` | [contact/list.md](contact/list.md) |
| `contact remove` | [contact/remove.md](contact/remove.md) |
| `contract`（命令组） | [contract/index.md](contract/index.md) |
| `contract call` | [contract/call.md](contract/call.md) |
| `contract send` | [contract/send.md](contract/send.md) |
| `contract deploy` | [contract/deploy.md](contract/deploy.md) |
| `contract info` | [contract/info.md](contract/info.md) |
| `contract clear-abi` | [contract/clear-abi.md](contract/clear-abi.md) |
| `contract set-origin-energy-limit` | [contract/set-origin-energy-limit.md](contract/set-origin-energy-limit.md) |
| `contract set-user-resource-percent` | [contract/set-user-resource-percent.md](contract/set-user-resource-percent.md) |
| `contract create2` | [contract/create2.md](contract/create2.md) |
| `gasfree`（命令组） | [gasfree/index.md](gasfree/index.md) |
| `gasfree info` | [gasfree/info.md](gasfree/info.md) |
| `gasfree transfer` | [gasfree/transfer.md](gasfree/transfer.md) |
| `gasfree trace` | [gasfree/trace.md](gasfree/trace.md) |

## 质押、投票与奖励

| 命令 | 页面 |
|---|---|
| `stake`（命令组） | [stake/index.md](stake/index.md) |
| `stake freeze` | [stake/freeze.md](stake/freeze.md) |
| `stake unfreeze` | [stake/unfreeze.md](stake/unfreeze.md) |
| `stake withdraw` | [stake/withdraw.md](stake/withdraw.md) |
| `stake cancel-unfreeze` | [stake/cancel-unfreeze.md](stake/cancel-unfreeze.md) |
| `stake delegate` | [stake/delegate.md](stake/delegate.md) |
| `stake undelegate` | [stake/undelegate.md](stake/undelegate.md) |
| `stake info` | [stake/info.md](stake/info.md) |
| `stake delegated` | [stake/delegated.md](stake/delegated.md) |
| `vote`（命令组） | [vote/index.md](vote/index.md) |
| `vote cast` | [vote/cast.md](vote/cast.md) |
| `vote list` | [vote/list.md](vote/list.md) |
| `vote status` | [vote/status.md](vote/status.md) |
| `reward`（命令组） | [reward/index.md](reward/index.md) |
| `reward balance` | [reward/balance.md](reward/balance.md) |
| `reward withdraw` | [reward/withdraw.md](reward/withdraw.md) |

## 治理

| 命令 | 页面 |
|---|---|
| `proposal`（命令组） | [proposal/index.md](proposal/index.md) |
| `proposal list` | [proposal/list.md](proposal/list.md) |
| `proposal show` | [proposal/show.md](proposal/show.md) |
| `proposal create` | [proposal/create.md](proposal/create.md) |
| `proposal approve` | [proposal/approve.md](proposal/approve.md) |
| `proposal delete` | [proposal/delete.md](proposal/delete.md) |
| `witness`（命令组） | [witness/index.md](witness/index.md) |
| `witness create` | [witness/create.md](witness/create.md) |
| `witness update` | [witness/update.md](witness/update.md) |
| `witness set-brokerage` | [witness/set-brokerage.md](witness/set-brokerage.md) |

## TRC10 资产与链上交易所

| 命令 | 页面 |
|---|---|
| `asset`（命令组） | [asset/index.md](asset/index.md) |
| `asset issue` | [asset/issue.md](asset/issue.md) |
| `asset update` | [asset/update.md](asset/update.md) |
| `asset participate` | [asset/participate.md](asset/participate.md) |
| `asset unfreeze` | [asset/unfreeze.md](asset/unfreeze.md) |
| `asset info` | [asset/info.md](asset/info.md) |
| `asset list` | [asset/list.md](asset/list.md) |
| `exchange`（命令组） | [exchange/index.md](exchange/index.md) |
| `exchange create` | [exchange/create.md](exchange/create.md) |
| `exchange inject` | [exchange/inject.md](exchange/inject.md) |
| `exchange withdraw` | [exchange/withdraw.md](exchange/withdraw.md) |
| `exchange trade` | [exchange/trade.md](exchange/trade.md) |
| `exchange show` | [exchange/show.md](exchange/show.md) |
| `exchange list` | [exchange/list.md](exchange/list.md) |

## 签名

| 命令 | 页面 |
|---|---|
| `message`（命令组） | [message/index.md](message/index.md) |
| `message sign` | [message/sign.md](message/sign.md) |
| `typed-data`（命令组） | [typed-data/index.md](typed-data/index.md) |
| `typed-data sign` | [typed-data/sign.md](typed-data/sign.md) |

## 支付与 Agent 身份

| 命令 | 页面 |
|---|---|
| `x402`（命令组） | [x402/index.md](x402/index.md) |
| `x402 pay` | [x402/pay.md](x402/pay.md) |
| `x402 serve` | [x402/serve.md](x402/serve.md) |
| `x402 roundtrip` | [x402/roundtrip.md](x402/roundtrip.md) |
| `x402 provider-list` | [x402/provider-list.md](x402/provider-list.md) |
| `x402 provider-show` | [x402/provider-show.md](x402/provider-show.md) |
| `x402 endpoint-list` | [x402/endpoint-list.md](x402/endpoint-list.md) |
| `x402 update-catalog` | [x402/update-catalog.md](x402/update-catalog.md) |
| `bai`（命令组） | [bai/index.md](bai/index.md) |
| `bai usage-summary` | [bai/usage-summary.md](bai/usage-summary.md) |
| `bai usage-records` | [bai/usage-records.md](bai/usage-records.md) |
| `bai recharge-orders` | [bai/recharge-orders.md](bai/recharge-orders.md) |
| `bai recharge` | [bai/recharge.md](bai/recharge.md) |
| `bai report-recharge` | [bai/report-recharge.md](bai/report-recharge.md) |
| `8004`（命令组） | [8004/index.md](8004/index.md) |
| `8004 show` | [8004/show.md](8004/show.md) |
| `8004 operator-check` | [8004/operator-check.md](8004/operator-check.md) |
| `8004 register` | [8004/register.md](8004/register.md) |
| `8004 update` | [8004/update.md](8004/update.md) |
| `8004 transfer` | [8004/transfer.md](8004/transfer.md) |
| `8004 approve` | [8004/approve.md](8004/approve.md) |
| `8004 add-operator` | [8004/add-operator.md](8004/add-operator.md) |
| `8004 remove-operator` | [8004/remove-operator.md](8004/remove-operator.md) |

## 本地命令

| 命令 | 页面 |
|---|---|
| `encoding`（命令组） | [encoding/index.md](encoding/index.md) |
| `encoding convert` | [encoding/convert.md](encoding/convert.md) |
| `address`（命令组） | [address/index.md](address/index.md) |
| `address generate` | [address/generate.md](address/generate.md) |
| `config` | [config.md](config.md) |
| `networks` | [networks.md](networks.md) |

## 全局选项（所有命令通用） {#global-options-every-command}

```
-o, --output <text|json>   result format (default: config.defaultOutput, built-in text)
--network <string>         network id or alias, e.g. nile, sepolia, bsc, eip155:11155111
                           (falls back to config.defaultNetwork)
--account <string>         accountId, label, or address (wallet-bound commands; falls back to active)
                           an address names one chain, so use accountId or label to cross families;
                           an address matching several accounts that are not interchangeable
                           signers for the family being acted on is `ambiguous_account`
--timeout <number>         per RPC/device call timeout, ms (default: config.timeoutMs, built-in 60000)
-v, --verbose              extra diagnostic output
-h, --help / -V, --version
```

schema 中允许广播后轮询的命令接受 `--wait` / `--wait-timeout <ms>`（上限默认取配置 `waitTimeoutMs`，内置 60000）。提前退出的模式同样因命令而异：构建交易类的命令可能提供 `--dry-run` / `--sign-only` / `--build-only`，而像 `tx broadcast` 这样只负责提交的命令既不重建也不签名，因此没有 `--sign-only` / `--build-only`。

费用参数和多签参数是**按家族划分**的，因此它们不是全局选项：

| 参数 | 家族 | 出现在哪里 |
|---|---|---|
| 权限组与过期时间——见下 | TRON | 会签名、或能输出未签名 hex 的 TRON 交易构建命令；不含 `tx broadcast` 和 GasFree |
| `--fee-limit <sun>` | TRON | 会消耗能量的那些命令：`tx send`、`contract send` / `deploy` |
| `--gas-limit <n>` / `--max-fee <gwei>` / `--priority-fee <gwei>` / `--nonce <n>` | EVM | `tx send`、`contract send` / `deploy` |

`--permission-id` 选择签名所用的权限组（0=owner，1=witness，2-9=active），`--expiration` 则延长收集联署签名的时间窗。EVM 交易只带一个签名，因此两者在那边都没有对应物：在通用命令上它们会被标注 `(TRON only)`，在 EVM 上使用会以 `invalid_option` 被拒绝。

凡是三种提前退出模式都存在的地方，它们互相排斥，且 `--expiration` 只有与 `--sign-only` 或 `--build-only` 同用时才被接受。违反其中任一条都是退出码 `2` 的用法错误。具体的 code 取决于校验发生在哪里：在 `account`、`permission`、`contract`、`proposal` 和 `witness` 这几类写入命令上是 `invalid_value`，而消息里点名哪个字段则取决于规则本身。互斥性挂在整个对象上，因此它报告的是 `--input` 而不是你实际传入的那些参数（`invalid --input: choose at most one of --dry-run, --sign-only, --build-only`）；`--expiration` 的规则挂在它自己的字段上，因此会点名它（`invalid --expiration: only valid with --sign-only or --build-only`）。在其他地方，同样的冲突报告的是 `invalid_option`。请按退出码分支，而不要按 code 字符串；见[机器接口](../machine-interface.md#error-codes)。
