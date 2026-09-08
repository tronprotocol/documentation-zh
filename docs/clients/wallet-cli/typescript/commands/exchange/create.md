# wallet-cli exchange create

创建一个 Bancor 交易对，并为两侧注入初始资金。

## 用法

```
wallet-cli exchange create --pair <tokenA>:<tokenB>
                           (--amounts <a>:<b> | --raw-amounts <a>:<b>)
                           [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]]
                           [--permission-id <n>] [options]
```

## 说明

在同一笔交易中创建交易对并放入初始流动性。两侧都可以是 TRX 或某个 TRC10 asset id，但两者必须不同。任何账户都可以创建交易对。

**创建者绑定是永久的。** 从此以后，只有创建它的那个账户才能对这个交易对[注资](inject.md)或[撤资](withdraw.md)，链上也没有任何办法把这项权利转移给别的账户。用错账户创建，流动性就会永远留在那个账户名下。

创建费用会被**燃烧**——它是链参数 `getExchangeCreateFee`，目前约 1,024 TRX，可用 [`chain params`](../chain/params.md) 读取——而两侧的初始金额还要在此之外一并从你的账户扣走。

`--pair` 和 `--amounts` 按位置一一对应：`--pair TRX:1000123 --amounts 10000:500000` 会在 TRX 一侧放入 10,000，在 asset 1000123 一侧放入 500,000。这个比例就是交易对的初始报价——这里大约是 1 TRX 兑 50 个 token——此后每一笔交易都会改变它。

**只用 id 指代 token**——`TRX`（或它的链上 id `_`）以及数字形式的 TRC10 id。TRC10 名称本身可能含有 `:`，那会让 `--pair` 产生歧义；用 [`asset info <name>`](../asset/info.md) 查出 id。

`--amounts` 以完整 token 计，并按各侧的精度换算；`--raw-amounts` 则以最小单位给出同样的两个数字。两者必须且只能给其中一个。

**该命令默认在交易提交后返回**（`stage: "submitted"`），不会等待确认。使用 `--wait` 可阻塞至交易确认或失败。命令需要一个账户；仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回 `watch_only_no_signer`。

## 选项

| 选项 | 说明 |
|---|---|
| `--pair <tokenA>:<tokenB>` | **必填。** 交易对的两侧——`TRX` 或某个 TRC10 asset id；两者必须不同 |
| `--amounts <a>:<b>` | 两侧各自的金额，以完整 token 计，顺序与 `--pair` 一致；都必须 > 0。它们会从你的账户扣除，并成为该交易对的储备。`--amounts` / `--raw-amounts` 二选一 |
| `--raw-amounts <a>:<b>` | 同样的两个金额，以最小单位表示。`--amounts` / `--raw-amounts` 二选一 |
| `--dry-run` | 只构建和估算，不签名/不广播；与 `--sign-only` / `--build-only` 互斥 |
| `--sign-only` | 只签名不广播，输出已签名的 hex；与 `--dry-run` / `--build-only` 互斥；配合 `--expiration` 使用 |
| `--build-only` | 构建并估算，输出**未签名**的 hex；与 `--dry-run` / `--sign-only` 互斥；配合 `--expiration` 使用 |
| `--expiration <ms>` | 交易过期时间（毫秒），最大 `86400000`（24 小时）；仅可与 `--sign-only` 或 `--build-only` 同用；省略时使用节点默认值（约 60 秒） |
| `--permission-id <n>` | 用于签名的权限组（0=owner，1=witness，2-9=active）；默认 `0` |
| `--wait` / `--wait-timeout <ms>` | 广播后轮询直到已确认/失败（上限默认取配置 `waitTimeoutMs`，内置 60000） |
| `--password-stdin` | 从 stdin（fd 0）读取 master password |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

示例中的 `$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入。

```bash
echo "$PW" | wallet-cli exchange create --pair TRX:1000123 --amounts 10000:500000 --network tron:3448148188 --wait --password-stdin
```

```console
✅ Exchange created
  Exchange id  12
  Creator      TQkXm4vN...5Zt7Uw
  Reserves     10,000 TRX / 500,000 MyToken
  TxID         2b7...
  Block        #57,884,020
  Fee          1,024 TRX
  Status       success
```

```bash
echo "$PW" | wallet-cli exchange create --pair TRX:1000123 --amounts 10000:500000 --network tron:3448148188 --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"exchange.create","data":{"kind":"exchange-create","stage":"confirmed","txId":"2b7...","confirmed":true,"blockNumber":57884020,"failed":false,"exchangeId":12,"pair":"TRX:1000123","creatorAddress":"TQkXm4vN...","firstTokenId":"_","firstTokenQuant":"10000000000","firstTokenLabel":"TRX","firstTokenDecimals":6,"secondTokenId":"1000123","secondTokenQuant":"500000000000","secondTokenLabel":"MyToken","secondTokenDecimals":6,"feeSun":1024000000},"meta":{"durationMs":6680,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交） | `kind: "exchange-create"`、`stage: "submitted"`、`txId`、`pair`、`creatorAddress`，以及两侧各自的 `…TokenId` / `…TokenQuant` / `…TokenLabel` / `…TokenDecimals` |
| `--wait`（已确认） | 同上，另加 `stage: "confirmed"`、`confirmed`（boolean）、`blockNumber`、`feeSun`、`failed`，以及 `exchangeId`——它由链分配，因此只有确认之后才能知道 |

`firstTokenId` / `secondTokenId` 是链上 id，因此 TRX 显示为 `"_"`。数量是各 token 最小单位下的**字符串**；text 输出正是靠 `…TokenLabel` 和 `…TokenDecimals` 把它们按完整 token 打印出来。

## 退出码

`0` 已提交（早退模式下为已构建/已签名） · `1` 执行失败（`same_token`——两侧是同一个 token、`asset_not_found`——没有这个 id 的 TRC10、`transaction_rejected`——节点拒绝了它，例如余额不足或某侧储备超过 `getExchangeBalanceLimit`、`watch_only_no_signer`、`auth_failed`） · `2` 用法错误（`missing_option`——没给 `--pair`；`invalid_option`——`--amounts` / `--raw-amounts` 两个都给了或都没给；`invalid_amount`——某一侧不是十进制数字，或小数位数超过该 token 允许的位数；`invalid_value`——`<a>:<b>` 格式非法，或某一侧 ≤ 0）。

## 另请参见

[`exchange inject`](inject.md) · [`exchange trade`](trade.md) · [`exchange show`](show.md) · [`chain params`](../chain/params.md) · [脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)
