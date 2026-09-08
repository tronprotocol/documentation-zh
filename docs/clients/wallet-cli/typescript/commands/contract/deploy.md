# wallet-cli contract deploy

部署合约字节码。

## 用法

```
wallet-cli contract deploy (--artifact <path> | --code <hex> | --code-file <path>)
                           [--constructor-args <json> | --constructor-params <json>]
                           [--constructor-signature <sig>]
                           [--dry-run | --sign-only | --build-only | --wait [--wait-timeout <ms>]]
                           [--abi <json>] [--fee-limit <sun>] [--permission-id <n>] [--expiration <ms>]   # TRON
                           [--gas-limit <n>] [--max-fee <gwei>] [--priority-fee <gwei>] [--nonce <n>]     # EVM
                           [options]
```

## 说明

以当前账户（或 `--account`）部署合约的 creation 字节码，并报告新合约的地址；TRON 与 EVM 网络都适用。

**字节码从哪里来**——三选一，必须且只能给一个，否则报 `invalid_value`：

| 来源 | 适用场景 |
|---|---|
| `--artifact <path>` | **首选。** 编译器产物（Foundry、Hardhat/sunhat、TronBox），其中*同时*包含字节码和 ABI，因此构造函数的参数类型来自编译器，而不是你手写 |
| `--code-file <path>` | 你只有字节码，且放在文件里——creation 字节码经常超出 shell 的参数长度上限 |
| `--code <hex>` | 你只有字节码，而且短到可以直接写在命令行里 |

读取 artifact 时会依次尝试 `.bytecode.object`、`.bytecode`、`.evm.bytecode.object`，并在存在时读取其 `abi`。若 artifact 中没有 creation 字节码，或只有 `"0x"`（接口或抽象合约），会被直接拒绝，而不是当成空合约部署出去。

**构造函数的参数类型从哪里来。** `--constructor-args` 接收的是裸值（`["18","MyToken"]`），因此类型必须另有来源：`--artifact` 里的 ABI、显式的 `--constructor-signature`，或者在 TRON 上用 `--abi`。三者都没有时报 `invalid_value`。`--constructor-params` 接收的是自带类型信息的 `{"type","value"}` 条目，因此不需要类型来源——但它不能与 `--artifact` 同用，因为后者的 ABI 已经声明了这些类型。`--constructor-signature` 同样不能与 `--artifact` 同用，而且**在 TRON 上完全不被接受**：TRON 节点需要的是完整 ABI，而不只是构造函数的类型。

**TRON 必须有 ABI。** 传 `--artifact` 或 `--abi`；两个都传是错误。`--abi` 仅限 TRON，且 ABI 中的 `constructor` 条目必须带有字符串形式的 `stateMutability`（`"nonpayable"` / `"payable"`）——`solc` 会输出它，但手工裁剪过的 ABI，或由 0.5 之前版本的 `solc` 生成的 ABI，可能没有。EVM 部署在类型来自 `--constructor-signature`、或参数本身自带类型时，不需要任何 ABI。

执行模式与其他交易写入命令一致：`--dry-run` 用于预览，`--sign-only` 输出可交给 [`tx broadcast`](../tx/broadcast.md) 的已签名交易，`--build-only` 输出未签名交易。默认在交易提交后返回；`--wait` 则阻塞至交易确认或失败。

费用相关的参数跟随链家族——`--fee-limit`（TRON，默认 `100000000` SUN），或 `--gas-limit` / `--max-fee` / `--priority-fee` / `--nonce`（EVM）。`--help` 会为每组打上标记，把其中一组用在另一个家族上会以 `invalid_option` 被拒绝。

命令需要一个账户。仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。
`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回
`watch_only_no_signer`。

在 TRON 上，Ledger 应用无法对 `CreateSmartContract` 签名；Ledger 账户可以做试运行或构建，但签名模式会以 `ledger_unsupported` 失败。通过以太坊应用进行的 EVM 部署不受此限制。

## 选项

| 选项 | 说明 |
|---|---|
| `--artifact <path>` | **必填**（三选一）。同时包含字节码和 ABI 的编译器产物 |
| `--code <hex>` | **必填**（三选一）。creation 字节码，十六进制编码 |
| `--code-file <path>` | **必填**（三选一）。存放 creation 字节码的文件 |
| `--constructor-args <json>` | 构造函数参数，JSON 数组形式的裸值，例如 `["18","MyToken"]` |
| `--constructor-params <json>` | 构造函数参数，`{"type","value"}` 条目形式；与 `--artifact` 互斥 |
| `--constructor-signature <sig>` | 没有 ABI 时用它给出构造函数的类型，例如 `constructor(uint256,string)`；与 `--artifact` 互斥，且在 TRON 上不被接受 |
| `--dry-run` | 只做估算；与 `--sign-only` / `--build-only` 互斥 |
| `--sign-only` | 只签名不广播，输出已签名的 hex；与 `--dry-run` / `--build-only` 互斥 |
| `--build-only` | 构建并估算，输出**未签名**的 hex；与 `--dry-run` / `--sign-only` 互斥 |
| `--wait` / `--wait-timeout <ms>` | 广播后轮询直到已确认/失败（上限默认取配置 `waitTimeoutMs`，内置 60000） |
| `--password-stdin` | 从 stdin 读取 master password |

仅限 TRON：

| 选项 | 说明 |
|---|---|
| `--abi <json>` | 合约 ABI，JSON 数组字符串；除非由 `--artifact` 提供，否则必填 |
| `--fee-limit <sun>` | 允许燃烧的最大能量费用，单位 SUN（默认 100000000） |
| `--permission-id <n>` | 用于签名的权限组（0=owner，1=witness，2-9=active）；默认 `0` |
| `--expiration <ms>` | 交易过期时间（毫秒），最大 `86400000`（24 小时）；仅可与 `--sign-only` 或 `--build-only` 同用；省略时使用节点默认值（约 60 秒） |

仅限 EVM：

| 选项 | 说明 |
|---|---|
| `--gas-limit <n>` | 授权的 gas 单位数；默认取节点的估算值，不做冗余放大 |
| `--max-fee <gwei>` | 每单位 gas 的最高总费用（仅 EIP-1559 链） |
| `--priority-fee <gwei>` | 每单位 gas 的小费（仅 EIP-1559 链） |
| `--nonce <n>` | 交易 nonce；默认取该账户的 pending nonce |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

示例中的 `$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入。

使用编译器产物——因为 artifact 自带 ABI，两个家族上的命令写法完全相同：

```bash
echo "$PW" | wallet-cli contract deploy --artifact ./build/contracts/Token.json --constructor-args '["18","MyToken"]' --network tron:3448148188 --password-stdin
echo "$PW" | wallet-cli contract deploy --artifact ./out/Token.sol/Token.json --constructor-args '["18","MyToken"]' --network eip155:11155111 --password-stdin
```

```console
⏳ Contract deployed
  Address  TXg3jWThoa5AxuwRA4aRyFAhmRN9hjhQFU
  TxID     b7c...
  Status   pending — not yet on-chain
! Track it: wallet-cli tx info --network tron:3448148188 --txid b7c...
```

在 EVM 上使用裸字节码，并自行给出构造函数的类型：

```bash
echo "$PW" | wallet-cli contract deploy --code-file ./Token.bin --constructor-signature 'constructor(uint8,string)' --constructor-args '["18","MyToken"]' --network eip155:11155111 --password-stdin
```

演练一次 EVM 部署——地址此时已经可知，费用则是一个 gas 上限：

```bash
wallet-cli contract deploy --code 0x60006000f3 --network eip155:11155111 --dry-run
```

```console
⏳ Dry run contract deploy
  Address  0xF3741D160A1E64A8D71fFE64CC0F111ddC7720E5
  Fee      ≤ 0.000117 ETH  (53,857 gas × 2.186156 gwei max)
  Tx       {"data":"0...000000"}
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"contract.deploy","data":{"kind":"contract-deploy","mode":"dry-run","fee":{"feeModel":"eip1559","maxCostWei":"117739814894256","gasLimit":"53857","maxPerGasWei":"2186156208"},"tx":{"data":"0x60006000f3","value":"0","chainId":11155111,"nonce":0,"gasLimit":"53857","type":2,"maxFeePerGas":"2186156208","maxPriorityFeePerGas":"1000000"},"nonce":0,"contractAddress":"0xF3741D160A1E64A8D71fFE64CC0F111ddC7720E5"},"meta":{"durationMs":565,"warnings":[]},"chain":{"family":"evm","network":"eip155:11155111","chainId":"11155111"}}
```

```bash
echo "$PW" | wallet-cli contract deploy --artifact ./build/contracts/Token.json --network tron:3448148188 --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"contract.deploy","data":{"kind":"contract-deploy","contractAddress":"TXg3jWThoa5AxuwRA4aRyFAhmRN9hjhQFU","stage":"submitted","txId":"b7c..."},"meta":{"durationMs":15,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交） | `kind: "contract-deploy"`、`contractAddress`（确定性得出的新地址）、`stage: "submitted"`、`txId` |
| `--wait`（已确认） | 以上内容，外加 `confirmed`、`blockNumber`、`failed`，以及实际发生的成本——TRON 上是 `feeSun`，EVM 上是 `gasUsed` / `feeWei` / `effectiveGasPriceWei` |
| `--dry-run` | `kind`、`mode: "dry-run"`、`contractAddress`、`fee`，以及未签名的 `tx`（EVM 上还有 `nonce`） |
| `--sign-only` / `--build-only` | `kind`、`mode`、`hex`、`fee`，以及交易对象 |

`contractAddress` 在交易确认之前就已知，但两个家族的推导方式不同。EVM 上它由部署者地址和 nonce 在本地算出。TRON 上地址由最终的 txID 推导而来，因此它是从已准备好的交易中读回的——要等 `--permission-id` / `--expiration` 绑定完毕、txID 定下来之后——而不是从构建器的输出直接算出。

## 退出码

`0` 已提交（早退模式下为已构建/已签名/试运行） · `1` 执行失败（`watch_only_no_signer`、`ledger_unsupported`——仅 TRON 签名、`auth_failed`、`rpc_error`、`timeout`） · `2` 用法错误——`file_not_found`（该路径下没有 artifact / 字节码文件），或以下情形报 `invalid_value`：`--artifact` / `--code` / `--code-file` 一个都没给或给了多个；artifact 不是合法 JSON、没有 creation 字节码，或只有 `"0x"`；用了 `--constructor-args` 却没有任何类型来源；`--constructor-params` 或 `--constructor-signature` 与 `--artifact` 同用；TRON 部署既没给 `--abi` 也没给 `--artifact`，或两个都给了；在 TRON 上使用 `--constructor-signature`；ABI 的构造函数缺少字符串形式的 `stateMutability`。

## 另请参见

[`contract info`](info.md) · [`contract send`](send.md) · [`contract create2`](create2.md) · [`tx status`](../tx/status.md)
