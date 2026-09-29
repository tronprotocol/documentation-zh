# 故障排查

本页按照机器接口中定义的[错误码](machine-interface.md#error-codes)提供排查方法。错误码的正式定义以
机器接口为准，本页重点说明对应的处理步骤。对于本页未涵盖的错误码，可查询持续维护的能力发现索引：`wallet-cli --json-schema | jq '.errorCodes'`。如果实际响应中的 code 未收录在该索引中，请按对应的退出码类别处理。

## `migration_required`（退出码 2） {#migration_required-exit-2}

你本地的钱包数据是由较早的版本写下的，必须先升级，依赖它的命令才能运行。升级关卡先于你输入的命令执行，而**那条命令会被刻意跳过、不予执行**。`--help`、`--version`、`--json-schema` 以及不带任何参数的 `wallet-cli` 从不读取钱包数据，因此不经过该关卡。

- **在终端里**：重新执行一次。关卡会先征求同意，随后在升级需要重新派生账户数据时要求输入 master password。
- **非交互式（CI、管道）**：传入 `--password-stdin`。仅含 Ledger 或仅观察账户的钱包没有需要重新加密的密钥，无需密码即可升级；而持有种子或私钥的钱包需要密码，缺少它时你看到的就是这个错误码。
- **拒绝升级并不算失败**：退出码为 `0`，带 `upgraded: false` 和 `cancelled: true`，且不会写入任何东西——既没有升级后的文件，也没有备份。
- 升级前的文件会以 `<name>.v1.bak` 的名字**永久**保留在原文件旁边。升级只会执行一次。

完整行为（包括 `migration` 的结果结构）见[启动时的钱包数据升级](machine-interface.md#startup-wallet-data-upgrades)。

## `encoding_error`：本版本无法读取的账户（退出码 1） {#encoding_error-an-account-this-build-cannot-read-exit-1}

这是 `migration_required` 的反方向——钱包注册表是由**更新版本**的 wallet-cli 写下的，其中某个账户的存储类型，本版本没有对应的读取器。

- [`list`](commands/list.md) 会降级处理而不是直接失败：它显示所有能读取的账户，并给出警告，指明跳过了哪些钱包 id。地址扫描也是同样的行为，因此你仍能看到的地址依旧可以被解析。
- 指名一个读不了的账户——无论用 `--account`、标签还是地址——都会**在命令动手之前**以 `encoding_error` 被拒绝，因此不会写入任何东西，也不会留下半成品回执。
- 解决办法是把 wallet-cli 升级到能识别该格式的版本。本地数据并没有损坏。

## `legacy_derivation`（退出码 1） {#legacy_derivation-exit-1}

该账户是 4.13.1 之前创建的钱包中 1 号或更靠后的 TRON 账户，使用的派生路径本版本已不再用于签名。同样的错误也会阻止 `derive` 向该钱包添加账户。数据没有丢失：请**在删除任何东西之前**，按[出现 `legacy_derivation` 后如何找回地址](troubleshooting/legacy-derivation-recovery.md)操作。

## `derivation_mismatch`（退出码 1） {#derivation_mismatch-exit-1}

`wallets.json` 中存放的某个地址，与其种子的任何派生路径都对不上，也就是钱包文件与加密保险库互相矛盾——通常是文件被手工编辑过，或是从别的钱包拷贝过来的。请用你自己的副本恢复这些文件，或用助记词重建该钱包。

## `usage_error` / `invalid_value`（退出码 2） {#usage_error--invalid_value-exit-2}

命令构造有误——某个参数未知、缺失、冲突，或取值非法。这些都以退出码 2 结束，但 code 各不相同：未知参数或组合错误是 `invalid_option`，缺少必填参数是 `missing_option`，取值非法是 `invalid_value`，只有解析器自身拒绝了这一行时才是 `usage_error`。

- 对具体子命令运行 `--help`，例如：`wallet-cli tx send --help`。
- 常见冲突：`--amount` 与 `--raw-amount`；`--token` 与 `--contract` 与 `--asset-id`；`--dry-run` 与 `--sign-only`；`--constructor-args` 与 `--constructor-params`；`contract deploy` 上的 `--artifact` 与 `--code` 与 `--code-file`；以及一次运行中出现两个 `*-stdin` 标志。
- `config` 上的 `invalid_value`：检查允许的键（`defaultNetwork`、`defaultOutput`、`timeoutMs`、`waitTimeoutMs`、`networks`、`aliases`、`networks.<id>.{httpEndpoint|apiKeyHeader|apiKey}`，以及凭据类的 `gasfreeApiKey`、`gasfreeApiSecret`、`tronlinkSecretId`、`tronlinkSecretKey`、`tronlinkChannel`、`baiApiKey`）和取值（`defaultOutput` 为 `text` 或 `json`）。

## `family_mismatch`（退出码 2）

该命令、该账户或该交易不属于所选网络所在的链家族——例如 `stake freeze --network sepolia`，或者把一个仅限 TRON 的仅观察账户用在 EVM 网络上。

- 确认这条命令服务于哪个家族：`wallet-cli <command> --help` 会写明，[命令参考](commands/index.md#which-commands-run-on-which-networks)则列出了全部仅限 TRON 的命令。
- 确认你实际选中的是哪个网络——省略 `--network` 时用的是 `config.defaultNetwork`，执行 `wallet-cli config defaultNetwork` 即可看到。
- 如果不匹配的是账户：seed 账户或私钥账户两个家族都能用，但**仅观察账户和 Ledger 账户只有一个地址、也只属于一个家族**。`wallet-cli list -o json` 会显示每个账户的 `addresses` 和它的 `family`。

## `invalid_option`：属于另一个链家族的参数（退出码 2） {#invalid_option-a-flag-scoped-to-the-other-family-exit-2}

该参数确实存在，但属于另一个链家族——比如在 EVM 网络上用了 `--asset-id` 或 `--permission-id`，或在 TRON 网络上用了 `--gas-limit` 或 `--nonce`。`--help` 会为每个参数标注 `(TRON only)` / `(EVM only)`。

- 费用相关：`--fee-limit` 属于 TRON；`--gas-limit` / `--max-fee` / `--priority-fee` / `--nonce` 属于 EVM。
- 在仍按单一 `gasPrice` 计价的 EVM 链上，`--max-fee` / `--priority-fee` 同样会被拒绝；可用 [`chain prices`](commands/chain/prices.md) 查看 `feeModel`。
- 交易 JSON（`--transaction`、`--tx-stdin`）属于 TRON；在可能面向任一家族的脚本里，请改用 `--file` / `--hex`。

## `chain_id_mismatch` / `nonce_too_low`（退出码 1）

在别处签好名的 EVM 交易，无法原样发到本网络。

- `chain_id_mismatch`——该交易承诺的链 id 与 `--network` 所选的不一致。签名覆盖了那个链 id，因此无法改指他链：请针对目标网络重新构建交易。
- `nonce_too_low`——该账户在这个 nonce 上已经有一笔入块的交易了。请用当前的 pending nonce 重新构建（省略 `--nonce` 时即为默认行为），或显式传入下一个可用的值。
- **构建路径上的试运行**也用同一个错误码：`tx send`、`contract send` 和 `contract deploy` 在同时使用 `--dry-run` 和显式 `--nonce` 时，会先读取账户已入块的计数，若该 nonce 已被用掉就在估算 gas 之前拒绝，而不是为一笔永远无法入块的交易给出费用方案。该读取是尽力而为的——读不到节点时试运行仍会完成构建——而且只在这一种组合下发生，因为自动推导出的 nonce 就是 pending 计数，不可能落后。低于 *pending* 但尚未入块的 nonce 是允许的：那是对仍在内存池中的交易的正当替换。
- 如果 nonce *高于*账户的下一个值，`tx broadcast --dry-run` 只会在 `meta.warnings` 中给出警告——它会把该值与节点返回的账户 nonce 比较（若读取失败，则将该检查降级为带警告的 `skipped`）。实际广播时由节点决定：节点拒绝 nonce 空档时返回退出码 1 的 `nonce_too_high`；若接受，交易将持续排队，直到缺失的 nonce 被补上。

## `weak_password`（退出码 2） {#weak_password-exit-2}

`create`（以及其他设置密码的命令）拒绝了这个 master password。它必须**至少 8 个字符**，并包含
**大写字母、小写字母、数字和特殊字符**（`!@#$%^&*()-_=+[]{};:,.?`）。错误消息会指明你没满足的
具体规则。

## `tty_required` / `auth_required`（退出码 2 / 退出码 1） {#tty_required--auth_required-exit-2--exit-1}

命令需要某项凭据、敏感信息或签名设备的确认，但未能获得。

- `tty_required`——没有挂载终端（CI、管道）。对于提供了 stdin 路径的命令，请传入对应的 `*-stdin` 标志（`--password-stdin`、`--tx-stdin`）。`import mnemonic`、`import private-key` 和 `change-password` 只能交互执行——它们必须在真正的 TTY 中运行，没有非交互的替代方案。
- `auth_required`——该命令需要 master password；请传 `--password-stdin`，或以交互方式运行。
- `auth_failed`——密码错误（解密失败）；请重新输入。

## `timeout`（退出码 1） {#timeout-exit-1}

节点或 Ledger 设备在 `--timeout`（默认 60000 毫秒）内没有响应。

- 检查到该网络的基本连通性；如果你在代理后面，请确认 CLI 的流量确实走了代理。
- 提高上限：`--timeout 120000`。
- Ledger：确认设备已解锁，且注册该账户时所用的 app（`--app tron` 或 `--app ethereum`）已打开，然后重试。
- **如果这发生在 `tx send` 上**：交易可能已经提交出去了。若你手上有 txid，请先用 `tx status` 查询，再决定是否重发。

## `rpc_error`（退出码 1） {#rpc_error-exit-1}

节点接受了连接，但拒绝了该请求——可能是一次 TRON API 调用，也可能是 `eth_estimateGas` 这类 EVM JSON-RPC 方法。消息中会带上节点给出的原因，例如 `TRON getTransaction failed: Transaction not found`。

- *Transaction not found*：`--txid` 写错、`--network` 选错（拿 Nile 的 txid 去主网查），或交易尚未传播开——过几秒再试。
- *Insufficient balance / bandwidth / energy*：给账户充值，或质押换取资源（`stake freeze`）——资源的机制见[网络](concepts/networks.md)；在 Nile 上可以用水龙头。
- *TRC20 转账 revert*（`estimateEnergy failed: REVERT opcode executed`）：请按这个顺序排查——(1) **token 余额不足**以支付你要转的数额，这是迄今为止最常见的原因：用 `token balance --contract <address>` 查一下，另外要记得 TRX 水龙头并不会给你 token；(2) 收款方或合约地址写错了；(3) 只有在前两项都排除之后，才考虑调高 `--fee-limit`（默认 100000000 SUN）——调高它并不能解决余额不足，它只是让确实昂贵的调用得以通过。

## `internal_error`（退出码 1） {#internal_error-exit-1}

未预期的失败。为避免泄露敏感信息，返回消息会保持概括。添加 `--verbose` 重试可在 stderr 获取更多
诊断信息；如果问题能够稳定复现，请在 issue 中提供命令结构，但**不要**包含任何密码、助记词或私钥。

## 不属于错误码，但经常被问到 {#not-an-error-code-but-frequently-asked}

- **`tx status` 长时间停在 `pending`**——节点已经看到这笔交易，但还没有执行结果；继续轮询即可。轮询到截止时间仍停在 `pending` 或 `not_found`，属于*未知*结果而非失败：在重发之前，请到区块浏览器上按目标网络核对该 txid，因为重发是构建并签名一笔新交易，而不是重试原来那笔。
- **"only one *-stdin flag can consume stdin per run"**——每次调用只通过管道传一项敏感信息；带密码发送时用 `--password-stdin`，让助记词/私钥留在加密存储里。
- **忘记 master password**——无法找回；请用你的 BIP39 助记词（`import mnemonic`）恢复到一个新钱包，并设置新密码。
- **`account history` 失败而其他查询正常**——历史查询需要 TronGrid 端点，普通的节点 RPC 不够。
