# 故障排查

本页按照机器接口中定义的[错误码](machine-interface.md#error-codes)提供排查方法。错误码的正式定义以
机器接口为准，本页重点说明对应的处理步骤。对于本页未涵盖的错误码，可查询持续维护的能力发现索引：`wallet-cli --json-schema | jq '.errorCodes'`。如果实际响应中的 code 未收录在该索引中，请按对应的退出码类别处理。

## `usage_error` / `invalid_value`（退出码 2） {#usage_error--invalid_value-exit-2}

命令构造有误——某个参数未知、缺失、冲突，或取值非法。这些都以退出码 2 结束，但 code 各不相同：未知参数或组合错误是 `invalid_option`，缺少必填参数是 `missing_option`，取值非法是 `invalid_value`，只有解析器自身拒绝了这一行时才是 `usage_error`。

- 对具体子命令运行 `--help`，例如：`wallet-cli tx send --help`。
- 常见冲突：`--amount` 与 `--raw-amount`；`--token` 与 `--contract` 与 `--asset-id`；`--dry-run`
  与 `--sign-only`（该冲突返回 `invalid_option`，同样是退出码 2）。一次调用中出现两个 `*-stdin` 标志**不属于**这一类——它会返回退出码 **1** 的 `secret_source_error`。
- 其他常见冲突：`contract deploy` 上的 `--constructor-args` 与 `--constructor-params`，以及 `--artifact` 与 `--code` 与 `--code-file`。
- `config` 上的 `invalid_value`：检查允许的键和取值（`defaultOutput` 为 `text` 或 `json`）。可读的键有 `defaultNetwork`、`defaultOutput`、`timeoutMs`、`waitTimeoutMs`、`networks`、`aliases`、`tronlinkSecretId`、`tronlinkSecretKey`、`tronlinkChannel`、`gasfreeApiKey`、`gasfreeApiSecret`，以及 `networks.<id>.{httpEndpoint|apiKeyHeader|apiKey}` 这几条路径；其中 `networks` 和 `aliases` 是只读的，其余可写。

## `family_mismatch`（退出码 2）

该命令、该账户或该交易不属于所选网络所在的链家族——例如 `stake freeze --network sepolia`，或者把一个仅限 TRON 的仅观察账户用在 EVM 网络上。

- 确认这条命令服务于哪个家族：`wallet-cli <command> --help` 会写明，[命令参考](commands/index.md#which-commands-run-on-which-networks)则列出了全部仅限 TRON 的命令。
- 确认你实际选中的是哪个网络——省略 `--network` 时用的是 `config.defaultNetwork`，执行 `wallet-cli config defaultNetwork` 即可看到。
- 如果不匹配的是账户：seed 账户或私钥账户两个家族都能用，但**仅观察账户和 Ledger 账户只有一个地址、也只属于一个家族**。`wallet-cli list -o json` 会显示每个账户的 `addresses` 和它的 `family`。

## `invalid_option`："a tron option on this command"（退出码 2）

使用了属于另一个链家族的参数。`--asset-id`、`--fee-limit`、`--permission-id`、`--expiration`、`--transaction` 和 `--tx-stdin` 属于 TRON；`--gas-limit`、`--max-fee`、`--priority-fee` 和 `--nonce` 属于 EVM。`--help` 会为这些参数标注 `(TRON only)` / `(EVM only)`。

`--max-fee` / `--priority-fee` 还额外要求链是 **EIP-1559** 的；在仍按 `gasPrice` 计价的网络上，它们会以同一个 code 被拒绝。

## `chain_id_mismatch` / `nonce_too_low`（退出码 1）

两者都仅限 EVM，表示交易与目标网络当前的链状态不匹配。

- `chain_id_mismatch`——这笔已签名的交易是为另一条链构建的。链 id 包含在交易中，也是签名所覆盖的内容，因此无法更改目标链；请针对目标网络重新构建。该检查在签名**之前**也会执行，因此不能把 `tx sign` 指向测试网来为主网交易签名。
- `nonce_too_low`——该账户在这个 nonce 上已经有一笔入块的交易了。去掉 `--nonce` 重新构建以采用账户的 pending nonce，或者传入正确的那个。

如果 nonce *高于*账户的下一个值，`tx broadcast --dry-run` 只会在 `meta.warnings` 中给出警告——CLI 会把该值与节点返回的账户 nonce 比较；若读取失败，则将检查降级为带警告的 `skipped`。实际广播时由节点决定：如果节点拒绝 nonce 空档，会返回退出码 1 的 `nonce_too_high`；如果接受，交易将持续排队，直到缺失的 nonce 被补上。

## `weak_password`（退出码 2） {#weak_password-exit-2}

`create`（以及其他设置密码的命令）拒绝了这个 master password。它必须**至少 8 个字符**，并包含
**大写字母、小写字母、数字和特殊字符**（`!@#$%^&*()-_=+[]{};:,.?`）。错误消息会指明你没满足的
具体规则。

## `tty_required` / `auth_required`（退出码 2 / 退出码 1） {#tty_required--auth_required-exit-2--exit-1}

命令需要某项凭据、敏感信息或签名设备的确认，但未能获得。

- `tty_required`——没有挂载终端（CI、管道）。对于有 stdin 路径的命令，请提供对应的 `*-stdin` 标志
  （`--password-stdin`、`--tx-stdin`）。`import mnemonic`、`import private-key` 和
  `change-password` 只能交互执行——它们必须在真实 TTY 中运行；不存在非交互的替代方案。
- `auth_required`——软件签名需要 master password，或者 Ledger 签名需要正确的 app / 设备状态。签名类命令不会主动提示，因此即使挂载终端也需要传入 `--password-stdin`。使用 Ledger 时，请解锁设备并打开与该账户家族相符的 TRON 或以太坊 app。
- `auth_failed`——密码错误（解密失败）；请重新输入。

## `timeout`（退出码 1） {#timeout-exit-1}

节点或 Ledger 设备在 `--timeout`（默认 60000 毫秒）内没有响应。

- 检查到该网络的基本连通性；如果处在代理之后，请确认 CLI 的流量确实经过了代理。
- 放宽上限：`--timeout 120000`。
- Ledger：确认设备已解锁，且已打开与该账户家族相符的 app（TRON app 或以太坊 app），然后重试。
- **如果这发生在 `tx send` 上**：交易可能仍然已经提交。如果你有 txid，请先找回它并查 `tx status`，
  再决定是否重发。

## `rpc_error`（退出码 1） {#rpc_error-exit-1}

节点接受了连接，但拒绝了请求。消息中带有节点给出的原因——可能来自一次 TRON API 调用（`TRON getTransaction failed: Transaction not found`），也可能来自一个 JSON-RPC 方法（`eth_estimateGas failed: …`）。

- *Transaction not found*：`--txid` 写错、`--network` 选错（拿 Nile 的 txid 去主网查），或者交易
  尚未传播开——过几秒后重试。
- *Insufficient balance / bandwidth / energy*：给账户充值，或质押以获得资源（`stake freeze`）
  ——资源的工作方式参见[网络](concepts/networks.md)；在 Nile 上请使用水龙头。
- TRC20 发送回滚：只有在确认收款方/合约无误之后，才考虑调高 `--fee-limit`（默认 100000000 SUN）。
- *`eth_estimateGas` failed*：节点模拟了这笔交易，结果 revert——最常见的是账户没有余额，或者合约本身拒绝了这次调用。请先解决根因；`--gas-limit` 可以在没有估算的情况下继续，但在模拟中就 revert 的交易，上链后通常照样 revert，而 gas 还是要付。

## `internal_error`（退出码 1） {#internal_error-exit-1}

未预期的失败。为避免泄露敏感信息，返回消息会保持概括。添加 `--verbose` 重试可在 stderr 获取更多
诊断信息；如果问题能够稳定复现，请在 issue 中提供命令结构，但**不要**包含任何密码、助记词或私钥。

## 不属于错误码，但经常被问到 {#not-an-error-code-but-frequently-asked}

- **`tx status` 长时间显示 `pending`**——节点已看到交易，但暂时无法获取执行结果或回执；请继续轮询。如果超过设定的截止时间后仍为 `pending`/`not_found`，结果仍是未知，而不是失败。请先在目标网络上核对交易，再考虑重发；建议使用区块浏览器或归档节点。
- **"only one *-stdin flag can consume stdin per run"**——每次调用只能通过管道传入一项敏感信息；带密码发送
  时请用 `--password-stdin`，把助记词/私钥留在加密存储中。
- **忘记 master password**——没有恢复途径；请用你的 BIP39 助记词（`import mnemonic`）恢复到一个新
  钱包，并设置新密码。
- **`account history` 失败但其他查询正常**——历史查询需要 TronGrid 端点；普通的节点 RPC 不够。它同时也仅限 TRON：在 EVM 网络上会以 `family_mismatch` 失败。
- **`list` 没有显示我确定存在的某个账户**——文本输出一次只显示一个链家族，并会提示略去了多少个。请传 `--network` 切到另一个家族，或者用 `-o json`，它会列出全部账户及其全部地址。
- **EVM 上某笔确实发生过的交易，`tx status` 却返回 `not_found`**——公共 RPC 端点通常不保留完整历史数据。`meta.warnings` 中的警告会说明这一点；请换用归档节点（`config networks.<id>.httpEndpoint`）。
- **某条命令以退出码 0 返回 `command: "migration"`，但未执行原操作**——CLI 先升级了持久化的钱包数据，并有意跳过原命令。请再次执行原命令。参见[启动时的钱包数据升级](machine-interface.md#startup-wallet-data-upgrades)。
