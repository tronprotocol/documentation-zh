# 机器接口

本页定义脚本、CI 流水线和 AI 智能体调用 wallet-cli 时应遵循的接口规范，包括 JSON 响应结构、
退出码、错误码和敏感信息处理方式。除非另有说明，这些约定均受 `wallet-cli.result.v1` 的稳定性承诺保护。

## 调用约定 {#calling-convention}

```bash
wallet-cli <command> -o json [--network <id|alias>] [--timeout <ms>] [--account <id|label>]
```

- 始终传 `-o json`。text 输出仅供人工阅读，不提供任何稳定性承诺。
- 在 JSON 模式下，stdout **只输出一个完整的 JSON 响应对象**，不会混入其他内容；诊断信息写入 stderr。
- 每次 RPC / 设备调用都受 `--timeout` 限制（毫秒，默认取 `config.timeoutMs`，内置默认值 60000）。
- `--network` 接受规范的 **CAIP-2** ID（`tron:3448148188`、`eip155:11155111`），也接受简短别名（`nile`、`sepolia`、`bsc`）。namespace 不等于链家族：`eip155` 对应 `evm` 家族。别名只在选择网络时解析，响应中的 `chain.network` 始终返回规范 ID。脚本应优先使用规范 ID，因为本地配置可以将别名重新指向其他网络。
- 本 CLI 在采用 CAIP-2 之前使用的 **TRON** id（`tron:mainnet`、`tron:nile`、`tron:shasta`）会永久保留为别名，因此原有调用方式仍然有效。但输出统一使用 CAIP-2 id：`chain.network`、`networks` 列表中的 `id` 和 `config` 的键均如此。依赖字符串匹配或使用 `tron:nile` 作为 map 键的调用方必须更新。别名只在选择网络时解析，不会出现在结果中。

### 能力发现

```bash
wallet-cli --json-schema                # 全部命令、它们的参数，以及错误码索引
wallet-cli --json-schema tron           # 限定到某一个链家族
wallet-cli <command> --json-schema      # 单条命令
```

一次调用即可返回完整的接口描述：`tool`、`version`、`globalFlags`、`errorCodes` 和 `commands[]`。每个命令条目都包含 `id`、`path`、`usage`、`requires`（network / auth / wallet）、`capability`、`examples`，以及描述输入的 JSON Schema；链上命令还会声明 `families`。这是智能体了解本 CLI 的推荐方式，请勿抓取 `--help` 的文本输出。

### 链家族

一个网络属于某一个**链家族**——`tron` 或 `evm`，而正是它决定了哪些命令、哪些参数适用：

- 命令会声明它服务于哪些家族（目录中的 `families`）。在另一个家族的网络上调用它，会在任何节点调用之前就以 **`family_mismatch`** 失败，退出码 `2`。
- 参数也可能只属于某一个家族（`--asset-id` 和 `--permission-id` 是 TRON 的，`--gas-limit` 和 `--nonce` 是 EVM 的）。把其中之一用在另一个家族上是 **`invalid_option`**，退出码 `2`。`--help` 会给它们打上 `(TRON only)` / `(EVM only)` 标记。
- 只要**账户**持有密钥，它就不绑定家族——seed 账户或私钥账户同时拥有 TRON 和 EVM 两个地址。仅观察账户和 Ledger 账户只有一个地址，因此也只属于一个家族；在不匹配的网络上选中它，同样是 `family_mismatch`。

命令家族和参数家族的检查是静态的，可以直接从目录中判定。而账户家族的兼容性还取决于所选的钱包账户：有密钥的账户两个家族都能服务，仅观察账户和 Ledger 账户则绑定在一个家族上。

### 启动时的钱包数据升级 {#startup-wallet-data-upgrades}

每一次调用——包括不带任何参数、`--help`、`--version` 和 `--json-schema`——都会在执行其他操作前检查持久化的钱包 schema。如果 schema 已过时，启动流程会先完成升级，并将过程写入 stderr。升级成功时返回退出码 `0` 和一个成功响应，其 `command` 为 `migration`，data 中包含 `originalCommandExecuted: false`；触发升级的原命令不会执行。请查看升级结果后重新执行原命令。这样可避免脚本命令或交易提交命令在发生意外的持久化状态变更后继续执行。

在交互式终端里，每个过时的钱包在改动文件之前都会先征求同意。用户选择 `Upgrade now` 之后，seed / 私钥类的迁移会要求输入 master password，而 Ledger / 仅观察类的迁移不需要。非交互式的 Ledger / 仅观察迁移仍然自动进行；而需要密码的迁移必须提供 `--password-stdin`，否则返回 `migration_required`，退出码 `2`——因为需要改变的是这次调用本身，所以它属于用法错误。

交互式用户也可以选择 `Exit without upgrading`。这是一次成功的取消，而不是失败：它返回退出码 `0`，带 `command: "migration"`、`upgraded: false`、`cancelled: true` 和 `originalCommandExecuted: false`。不会写入任何钱包文件或备份。`migration_required` 只保留给迁移确实无法进行的情形，例如非交互式调用且没有任何密码来源。

## 退出码 {#exit-codes}

| 退出码 | 含义 | JSON 响应 |
|---|---|---|
| `0` | 成功 | `success: true` |
| `1` | 执行失败——运行时错误：RPC 失败、超时、链上拒绝、钱包错误 | `success: false` |
| `2` | 用法错误——参数写错、缺少必填选项、取值非法、family 不匹配 | `success: false` |

退出码只有以上三种，含义固定。在 JSON 模式下，非零退出码总会同时在 stdout 输出错误响应。

## JSON 响应结构 {#the-result-envelope}

Schema id：`wallet-cli.result.v1`。

**成功：**

```json
{
  "schema": "wallet-cli.result.v1",
  "success": true,
  "command": "account.balance",
  "data": { "address": "TMSgJxtPw29AFEHMXsjGo4kWV7UwbCToHJ", "balance": "1976489000", "decimals": 6, "symbol": "TRX" },
  "meta": { "durationMs": 1114, "warnings": [] },
  "chain": { "family": "tron", "network": "tron:3448148188", "chainId": "3448148188" }
}
```

**出错：**

```json
{
  "schema": "wallet-cli.result.v1",
  "success": false,
  "command": "tx.info",
  "error": { "code": "rpc_error", "message": "TRON getTransaction failed: Transaction not found" },
  "meta": { "durationMs": 1033, "warnings": [] },
  "chain": { "family": "tron", "network": "tron:3448148188", "chainId": "3448148188" }
}
```

| 字段 | 类型 | 出现时机 | 说明 |
| ----------------- | ------------------------ | ------------------- | -------------------------------------------------------------------------------- |
| `schema`          | `"wallet-cli.result.v1"` | 始终 | schema 版本标识；调用方应据此选择解析逻辑 |
| `success`         | boolean | 始终 | 与退出码一致（`true` ⇔ 0） |
| `command`         | string | 始终 | 规范命令 id，例如 `tx.send`、`list`。它标识的是**操作**，而不是你输入的字面词：`backup --records` 报告为 `backup.records`，`import keystore` 报告为 `import.keystore` |
| `data`            | object/array | 仅成功时 | 命令返回的数据；见各命令的参考页 |
| `error.code`      | string | 仅出错时 | 机器可读；见[错误码](#error-codes) |
| `error.message`   | string | 仅出错时 | 面向人类可读；**不**稳定——绝不要解析它 |
| `error.details`   | object | 可选 | 可用时提供的结构化附加信息 |
| `meta.durationMs` | number | 始终 | 实际耗时（毫秒） |
| `meta.warnings`   | `(string \| {code, message})[]` | 始终 | 非致命提示；**元素类型并不统一**——见下文 |
| `meta.pagination` | object | 仅返回窗口的命令 | `offset` / `limit` / `total`；当命令返回一个分页窗口时出现——见[分页](#pagination) |
| `chain`           | object | 选定了网络时 | `family` / `network` / `chainId`。每条链上命令都有；本地命令若其策略会解析出一个网络，也会有。`network: "none"` 的命令不带它；它的存在**并不**意味着访问过节点 |

目前会感知网络的本地命令是 `backup`、`current` 和 `list`。它们把所选网络（或默认网络）当作家族/显示选择器使用，并不访问节点。

编码规则：`bigint` 值序列化为十进制**字符串**（例如 `"balance": "1976489000"`），二进制数据序列化为 hex。由 `bigint` 或协议 int64 表示的金额是字符串；而 `feeSun`、`multiSignFeeSun`、`energyUsed`、`netUsed` 这类有界的计数和费用可能是 JSON 数字。请以各命令的字段表为准，不要把所有金额一概强转成同一种类型。

### 读取 `meta.warnings` {#reading-metawarnings}

每个条目可能是普通字符串，也可能是 `{code, message}` 对象。需要程序据此分支处理的警告使用对象形式——
目前包括 [`permission update`](commands/permission/update.md) 的安全警告和确认后的检查；其他警告使用
普通字符串。展示前请先统一处理两种形式，不要假设所有元素类型相同：

```bash
# 供人工阅读的文本——两种形式都适用
jq -r '.meta.warnings[] | if type == "string" then . else .message end'

# 针对特定情况分支——仅对象形式适用
jq -e '.meta.warnings[] | select(type == "object" and .code == "owner_lockout")' >/dev/null && exit 1
```

假定元素是字符串的辅助写法（`.meta.warnings | join("\n")`、`Array.prototype.join`）在遇到对象形式时会报错或打印出 `[object Object]`。警告的 `code` 取值在 v1 内是稳定且只增的——可能出现新的 code，已有的 code 会保持原有含义。警告的 `message` 文本**不**稳定；请像对待 `error.message` 一样，绝不要解析它。

### 分页 {#pagination}

返回 offset/limit 窗口的命令会在 `meta.pagination` 中报告这个窗口，而不是放在 `data` 里。目前这类命令是 `asset list`、`exchange list`、`proposal list` 和 `backup --records`；某些命令只是把 `--limit` 当作结果条数上限，因此并不会给出分页元数据。

| 键 | 类型 | 含义 |
|---|---|---|
| `offset` | number | 本页的起始索引——回显 `--offset` |
| `limit` | number \| **null** | 每页大小；`null` = 不限（未给 `--limit`） |
| `total` | number \| **null** | 匹配记录的总数；`null` 表示**不存在这个计数**，而不是"被省略了" |

这三个键始终存在，因此 `null` 是唯一的"未知"信号，也就不需要把"缺失"和 null 区分开。

对于由 TRON 分页节点端点提供的命令——[`asset list`](commands/asset/list.md) 和 [`exchange list`](commands/exchange/list.md)——`total` 永久为 `null`。这些端点不返回计数，而要算出一个计数就意味着传输全部记录（主网上有 5,187 个资产，2.7 MB）。请一直翻页直到返回一个不足整页的结果为止，而不要去和总数比较：

```bash
offset=0
while :; do
  page=$(wallet-cli asset list --limit 50 --offset "$offset" -o json)
  n=$(jq '.data.assets | length' <<<"$page")
  jq -c '.data.assets[]' <<<"$page"
  [ "$n" -lt 50 ] && break
  offset=$((offset + 50))
done
```

对本地有限数据集分页的命令（[`backup --records`](commands/backup.md)），以及先取回全部数据再在客户端分页的命令（[`proposal list`](commands/proposal/list.md)），会报告 `total`。

text 模式会为同一页数据添加标题（`Assets (limit 50, offset 0)`、`Proposals (showing 2 of 4)`、`Backup records (showing 3 of 12)`），但 text 输出不属于稳定接口，请使用并解析 `-o json`。

## 错误码 {#error-codes}

**退出码是稳定接口**：`2` 表示命令参数或调用方式有误（直接重试仍会失败），`1` 表示执行过程中发生
网络、设备、链或钱包错误。`error.code` 用于进一步区分具体原因；程序应先按退出码分类，再按需要处理 `error.code`。

**持续维护的错误码索引是公开的**，每个 code 一行，位于能力发现目录的 `errorCodes` 下：

```bash
wallet-cli --json-schema | jq '.errorCodes'
```

每个条目都是对象，而不是单独的字符串：

```json
{ "rpc_error": { "exit": 1, "retry": "same", "meaning": "the node answered with an error" } }
```

`exit` 是该错误码退出状态的权威定义。下表由人工维护，并通过测试与索引核对：表中每个错误码的退出
状态必须与索引中的 `exit` 一致；测试不检查表里的含义说明，也不要求表格覆盖索引中的所有错误码。
少数错误码的 `exit` 为 `"either"`，表示两种退出状态都有可能，具体以进程实际返回值为准。

`retry` 表示建议的重试策略：

- `same`——可以立即重试同一条命令，通常适用于节点或服务的偶发故障；
- `later`——请求本身无须修改，但要等待一段时间后再试，例如等待锁定期、提现间隔或限流结束；
- `changed`——必须修改请求后再试，例如提高手续费，或使用新的 nonce 重新构建交易；
- `never`——原样重试不会成功，需要先改变命令之外的条件。

按照定义，退出码为 `2` 的错误，其 `retry` 均为 `never`。

`retry` 描述的是**错误类型通常采用的处理方式**，并不保证整条命令可以安全重试。`timeout` 和
`rpc_error` 被标记为 `same`，是因为大多数读取类请求在这两种情况下可以直接重试。但交易提交命令
（包括 `tx send`）可能在**节点已经接收交易、但响应尚未返回**时发生 `timeout` 或 `rpc_error`。
此时交易结果是未知，而不是已失败；再次执行命令会重新构建并签名一笔**新交易**，在 TRON 上可能形成
第二笔独立转账。

因此，解析网络 ID 或读取余额时可以按照 `retry: "same"` 直接重试，但它不代表可以盲目重新广播交易。
提交结果不确定时，应先通过 [`tx status`](#script-safety-never-mistake-submitted-for-confirmed) 核对链上
状态，再决定是否重试。这也符合下文的四状态模型。

该索引是当前版本提供的机器可读错误码目录，可用于能力发现，但不应视为封闭枚举。少数代码路径会在
运行时动态选择错误码，因此实际响应中仍可能出现 `errorCodes` 未列出的值。下表仅收录常见错误码，
v1 版本内仍可能新增条目。`invalid_value` 和 `aborted` 可能根据错误发生阶段对应两种不同的退出码；
调用方应兼容未知错误码，并在无法识别时按退出码类别处理。

退出码 **2**（用法——修正调用方式）下的常见错误码：

| 错误码 | 含义 |
|---|---|
| `usage_error` | 由参数解析器本身抛出——yargs 的用法失败，或位置参数过多。更具体的问题各有自己的 code：未知参数是 `invalid_option`，缺少必填参数是 `missing_option`，取值校验或跨字段规则失败是 `invalid_value` |
| `family_mismatch` | 该命令、该账户、该收款方或该原始交易不属于所选网络所在的链家族 |
| `missing_option` | 未提供某个必填参数 |
| `invalid_option` | 某个参数被用在了非法组合中，或者它只属于另一个链家族 |
| `invalid_permission` | 权限文档或所选的权限组对该操作而言不合法 |
| `invalid_value` | 某个参数取值未通过校验（例如 `config defaultOutput xml`） |
| `invalid_amount` | 金额格式错误或超出范围 |
| `weak_password` | master password 未达策略要求（≥8 个字符；大写 + 小写 + 数字 + 特殊字符） |
| `tty_required` | 需要交互式提示，但没有挂载 TTY——请在终端中运行，或在该命令提供 stdin 标志时改用它 |
| `missing_network` / `unsupported_network` | 调用方显式要求注册表解析一个空的网络 id，或者给出的规范 id / 别名未知。普通链上命令在省略 `--network` 时使用 `config.defaultNetwork`，其内置值为 `tron:728126428` |
| `unsupported_network_capability` | 所选网络不提供该命令所需的能力 |
| `limit_exceeded` | 某个有界输入（文件大小、列表长度、分页大小）超出了上限 |
| `unknown_command` | 没有这条命令 |
| `output_exists` | 目标文件已存在且绝不会被覆盖（`backup --out`、`address generate --out`）。这是确定性的——用同一路径重试永远会失败 |
| `file_not_found` | 某个参数指定的输入文件不存在（`contract deploy --artifact` / `--code-file`、`contract create2 --code-file`） |
| `keystore_not_found` | `import keystore`：给定路径上没有文件 |
| `migration_required` | 持久化的钱包数据需要升级，但本次调用因无法获得 master password 而不能完成升级——请在终端中重新运行，或用 `--password-stdin` 管道传入。参见[启动时的钱包数据升级](#startup-wallet-data-upgrades) |
| `invalid_keystore` | `import keystore`：不是合法的 Web3 V3 keystore——JSON 有误、`version` ≠ 3、使用了不支持的 cipher/KDF，或解密结果不是 32 字节私钥 |
| `invalid_config` | `config.yaml` 无法读取或不是合法的 YAML——请修复或删除该文件。具体解析错误会被隐藏，因为错误信息可能引用包含凭据的原始行 |
| `insecure_config` | `config.yaml` 保存了服务凭据，但它是符号链接或对同组/所有人可读——请对它执行 `chmod 600`（仅 POSIX；Windows 上不强制） |
| `contact_not_found` / `already_exists` | 不存在该名称的联系人，或该联系人名称/地址已被占用 |
| `token_not_in_book` / `token_is_official` / `token_already_listed` | token 地址簿相关的状况 |
| `unsupported_token` | 所选服务方或该命令不支持这个 token |
| `insufficient_voting_power` | 请求的票数超出该账户可用的投票权 |
| `gasfree_credentials_missing` / `tronlink_credentials_missing` | 未配置所需的服务凭据（用 `config` 设置） |
| `unknown_parameter` | 不存在该名称或 id 的链参数（`proposal create --set`） |
| `invalid_asset_name` | TRC10 名称或缩写不在 1–32 个可见 ASCII 字符范围内 |
| `ambiguous_account` | `--account <address>` 匹配到多个账户，且这些账户在当前链家族中无法归并为同一个等效签名者；`error.details` 中包含候选项——参见 [`error.details.matches`](#errordetailsmatches) |

退出码 **1**（执行——运行时失败）下的常见错误码：

| 错误码 | 含义 |
|---|---|
| `rpc_error` | 节点拒绝了请求或请求执行失败——可能是一次 TRON API 调用，也可能是 `eth_estimateGas` 之类的 JSON-RPC 方法 |
| `invalid_node_response` | 节点响应与请求或协议不一致：TRC10/exchange 记录的 ID 不是请求值、`precision` 超出 0..6、汇率参数不是正 int32、EVM JSON-RPC 响应同时缺少 `result` 和 `error`，或最新区块查询没有返回区块。由于这些数据会影响签名金额，命令会停止执行，不会继续使用异常值；列表查询则丢弃异常记录并保留本页其他结果 |
| `timeout` | 等待网络或设备时被中止（超过 `--timeout`） |
| `auth_required` | 所需的凭据不可用——软件账户的 master password，或者 Ledger app / 设备未就绪 |
| `auth_failed` | master password 错误（解密失败） |
| `signing_rejected` / `transaction_rejected` | 签名或广播被拒绝（设备或链） |
| `watch_only_no_signer` | 该账户是仅观察账户，无法签名 |
| `invalid_mnemonic` / `invalid_private_key` | 存储层校验拒绝了格式错误的助记词或私钥；交互式导入通常会在提示处当场发现并要求重输 |
| `token_metadata_unavailable` | 无法从所选网络读取必需的 token 元数据。该错误可能对应两种退出码：大多数场景返回退出码 `1`；但在 TRON 上，如果 `tx send` 遇到合约不返回 `decimals()` 且地址簿中也没有对应条目，则返回退出码 **2**——此时必须修改调用参数或配置 |
| `wrong_device_seed` | 连接的 Ledger 与已注册的账户不匹配 |
| `tx_integrity` / `invalid_transaction` | 预签名交易未通过完整性 / 合法性检查 |
| `insufficient_balance` / `insufficient_token_balance` | TRX / token 不足以覆盖金额加手续费 |
| `provider_error` | 节点或外部服务返回了 CLI 无法安全使用的数据——例如格式错误、自相矛盾或超出取值范围的响应（TRON 权限数据、链参数、本地 TronWeb 构建未暴露的 protobuf 编解码器，以及 GasFree / TronLink 的载荷）、请求失败，或者 GasFree / TronLink 返回错误状态码。TronLink 的**所有**非 404 状态码都归到这里，包括 429 |
| `provider_rate_limited` | **仅 GasFree**——服务返回了 HTTP 429；若它发送了 `Retry-After` 头，`error.details.retryAfter` 会带上它。TronLink 的 429 归为 `provider_error` |
| `tx_expired` | 签名收齐之前交易就已过期（TRON） |
| `chain_id_mismatch` | 该 EVM 交易是为另一条链构建的，与所选网络不符 |
| `nonce_too_low` | 该 EVM 交易的 nonce 已经被一笔已入块的交易用掉了 |
| `history_not_supported` | 该端点不支持 TronGrid 历史查询（`account history`，TRON） |
| `not_found` | 所寻址的对象不存在——例如未激活的账户、交易、区块，或 GasFree / TronLink 资源 |
| `proposal_not_found` / `contract_not_found` / `asset_not_found` / `exchange_not_found` | 链上不存在与该提案 ID、合约地址、TRC10 引用或交易对 ID 对应的对象 |
| `ambiguous_asset_name` | 某个 TRC10 名称匹配到多个 token；`error.details` 中带有候选项——见 [`error.details.matches`](#errordetailsmatches) |
| `ledger_unsupported` | 所选的 Ledger app 无法为该交易类型签名——请求会在访问设备前被拒绝（TRON 的账户激活、账户 id、asset 写操作、合约部署/治理、witness 写操作，以及 cancel-unfreeze） |
| `not_a_witness` / `already_witness` / `not_proposal_owner` | 治理身份不满足该操作的规则 |
| `already_approved` / `not_approved` / `proposal_expired` / `already_canceled` | 提案投票的状态条件 |
| `account_not_active` / `account_already_active` / `name_already_set` / `id_already_set` / `chain_parameter_unavailable` | 账户激活 / 名称 / id 相关的状况，或者 `witness create` 无法读取 `getAccountUpgradeCost` |
| `not_contract_deployer` | 该账户不是目标合约的部署者 |
| `already_issued_asset` / `not_an_issuer` | 该账户已经发行过 TRC10，或者从未发行过 |
| `not_in_ico_window` / `self_participation` | TRC10 ICO 参与条件 |
| `no_frozen_supply` / `not_yet_unfreezable` | 没有冻结的部分，或还没有到期的部分（`asset unfreeze`） |
| `not_exchange_creator` / `token_not_in_exchange` / `exchange_closed` / `same_token` | 交易对的访问权限与状态条件 |
| `insufficient_reserve` | `exchange withdraw`：撤出量超过交易对对应一侧的储备 |
| `precision_loss` / `slippage_exceeded` / `exchange_trading_disabled` | 根据有限白名单识别出的节点拒绝原因——金额无法按储备比例精确换算、回报低于下限，或该网络不接受 Bancor 交易 |
| `not_exportable` | 该账户不持有可导出的密钥材料（仅观察或 Ledger）——`backup` |
| `wrong_keystore_password` | `import keystore`：文件自身的密码不对（区别于 `auth_failed`，后者指的是 master password）。`mac` 缺失或不是 hex 的文件属于 `invalid_keystore`，而不是密码错误——hex 不区分大小写 |
| `internal_error` | 预期之外的内部失败；消息刻意保持通用 |

预期之外的异常会先经过**脱敏处理**，再以 `internal_error` 和通用消息返回，避免第三方库回显的敏感信息
进入响应。上面两张表仅用于方便阅读；持续维护的能力发现索引是 `--json-schema` 返回的 `errorCodes`，
但该索引也不保证列出解析器可能返回的所有错误码。

### `error.details.matches` {#errordetailsmatches}

部分错误表示输入存在歧义，需要调用方从多个候选项中选择，而不是简单重试。这类错误会把候选项放在
`error.details.matches` 中，其值是字段结构一致的对象数组：

```json
{"code":"ambiguous_asset_name","message":"2 TRC10 tokens are named MyToken; re-run with the id","details":{"name":"MyToken","assetIds":["1000123","1000488"],"matches":[{"assetId":"1000123","issuerAddress":"TQkXm4vN...","totalSupply":"1000000000000000","precision":6},{"assetId":"1000488","issuerAddress":"TZx9kP2m...","totalSupply":"5000000000","precision":2}]}}
```

`ambiguous_account` 是另一种使用该候选项结构的常见错误。当 `--account <address>` 在当前链家族中
匹配多个账户记录，且这些记录无法视为同一个等效签名者时，会返回此错误：

```json
{"code":"ambiguous_account","message":"address T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb matches 2 accounts; address it by accountId","details":{"address":"T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb","accountIds":["wlt_a1b2c.0","wlt_d3e4f.0"],"matches":[{"accountId":"wlt_a1b2c.0","label":"main","type":"seed","index":0},{"accountId":"wlt_d3e4f.0","label":"cold","type":"watch","index":null}]}}
```

`matches` 是通用字段，并不限定于某个错误码。任何带有该字段的错误都应按相同方式处理。text 模式会在
stderr 的 `error [...]` 行下方以表格显示候选项。`matches` 中的数量保留最小单位，与对应成功响应的
表示方式一致；某行包含 `precision` 时，text 表格会换算为便于阅读的数值。

与它并列，错误还可能携带一个只包含标识符的标量列表，供你据此重试——就是上面的 `assetIds`。脚本请优先用它；`matches` 的存在是为了让人能分辨这些候选项。

## 敏感信息处理 {#secret-handling}

wallet-cli 绝不从命令行参数或专用的敏感信息环境变量读取密码、助记词和私钥。命令行参数和导出的环境变量会泄漏进 shell 历史、进程列表和 CI 日志。传递敏感信息请使用下面这些 CLI 通道：

1. **stdin 标志**——`--password-stdin` 用于 master password；`--tx-stdin` / `--message-stdin` 用于较大的载荷。**每次运行只能有一个 `*-stdin` 标志消费 stdin。**（助记词和私钥没有 stdin 路径——`import mnemonic` / `import private-key` / `change-password` 只能交互执行，使用隐藏的 TTY 输入。）
2. **交互式 TTY 提示**——仅用于明确声明为交互式的命令：`create`、各种 `import`、`backup`、`change-password`，以及 `delete` 的确认。其他命令无论是否挂载终端，行为都相同：`tx send`、`contract *`、`stake *`、`message sign` 等命令不会主动提示；缺少 master password 时一律返回 `auth_required`（退出码 `1`）。

示例中的 shell 变量只是管道输入的数据来源，并非由 wallet-cli 主动读取。应将变量限制在当前进程中，
尽量缩短其生命周期，避免长期 `export`。

```bash
# 非交互式解锁
printf '%s' "$MASTER_PASSWORD_FROM_YOUR_VAULT" | wallet-cli tx send \
  --to TSx72ViULFepRGCS4PM5dP4FqD1d8qggCc --amount 1 \
  --network tron:3448148188 --password-stdin -o json
```

## 脚本安全：绝不要把"已提交"当作"已确认" {#script-safety-never-mistake-submitted-for-confirmed}

错误判断交易是否成功可能造成资产损失。请遵循以下规则：

1. 广播类（✍️）命令**默认在提交后就返回**，而不是等待确认。`data` 是一个扁平对象，其中包含表示操作类型的 `kind`（`send`、`stake-freeze`、`permission-update`、`account-activate`、`proposal-create`、`asset-issue`、`exchange-trade` 等）、`stage` 和 `txId`；`submitted` 阶段不包含区块、手续费或执行结果（这些字段只有在 `--wait` 确认后才会出现）：

   ```json
   { "kind": "send", "stage": "submitted", "txId": "7d9b6a08…", "rawAmount": "1000000", "to": "TSx72…" }
   ```

   **由链分配的 id 只有随确认才会出现。** 新提案的 `proposalId`、TRC10 的 `assetId`、交易对的 `exchangeId` 在提交时并不存在——它们不会出现在提交回执中，而是在 `--wait`（或之后的查询）在链上看到该交易之后才出现。创建这些对象的脚本必须等待。

2. 想阻塞到结果已知为止，请传 `--wait`（轮询直到 confirmed/failed，上限由 `--wait-timeout` 控制，默认 60000 毫秒；触及上限时返回提交回执）。

   **`--wait` 通过 `data.stage` 报告交易结果，而不是通过 `success`。** 如果交易已提交并入块，但链上执行失败，CLI 调用本身仍算成功：响应中的 `success` 为 `true`、退出码为 `0`，而 `data.stage` 为 `"failed"`。退出码表示 CLI 是否完成了请求，并不表示链上执行是否成功。因此使用 `--wait` 后，程序必须检查 `data.stage`（`confirmed` / `failed` / `submitted`），再决定如何记录本次操作。

3. 或者你自己用 `tx status` 轮询，它有一个**四状态模型**：

   | `data.state` | 含义 | 能否停止轮询？ |
   |---|---|---|
   | `confirmed` | 已入块，且已经能取到执行结果/回执（存在 `blockNumber`） | 可以 |
   | `failed` | 已入块，但链上执行失败 | 可以——视为失败 |
   | `pending` | 节点已经看到，但还没有执行结果/回执 | 不能——继续轮询 |
   | `not_found` | 查询端点尚未找到该交易 | 不能——继续轮询/对账；不要据此判定失败 |

   > `confirmed` 表示已入块并取得回执，不表示已最终确定。当这个区别重要时，请另行验证——TRON 上查询 SolidityNode 视图，EVM 上检查 finalized 区块。

   > 轮询到截止时间仍停在 `pending` 或 `not_found`，结果依然是未知。不要把它记录为失败，也不要在没有外部对账的情况下自动重发。

   `data.confirmed` 和 `data.failed` 以布尔值提供，便于直接分支。

   **GasFree 转账是个例外。** `gasfree transfer` 提交给的是一个服务提供方，而不是直接提交给节点：提交回执中带的是 `traceId`（而不是 `txId`），进度遵循提供方的状态——`WAITING` → `INPROGRESS` → `CONFIRMING` → `SUCCEED` / `FAILED`。请用 `--wait` 或 [`gasfree trace <traceId>`](commands/gasfree/trace.md) 跟踪它，而不是 `tx status`；`txId` 只有在提供方把它送上链之后才会出现。

```bash
#!/usr/bin/env bash
set -euo pipefail

deadline=$((SECONDS + 90))
txid=$(
  printf '%s' "$PW" |
    wallet-cli tx send --to T... --amount 1 --network tron:3448148188 --password-stdin -o json |
    jq -er '.data.txId'
)

while (( SECONDS < deadline )); do
  state=$(
    wallet-cli tx status --txid "$txid" --network tron:3448148188 -o json |
      jq -er '.data.state'
  )

  case "$state" in
    confirmed)
      exit 0
      ;;
    failed)
      echo "transaction failed: $txid" >&2
      exit 1
      ;;
    pending|not_found)
      sleep 3
      ;;
    *)
      echo "unexpected transaction state: $state" >&2
      exit 1
      ;;
  esac
done

echo "transaction outcome unknown after deadline: $txid" >&2
exit 1
```

4. **批量操作**：每条命令对应一笔交易和一个退出码。默认的安全做法是遇到第一个失败就停止；如果选择继续，请逐项记录 txid，并在报告成功前用 `tx status` 逐一核对。

## 稳定性承诺（v1） {#stability-promise-v1}

只要 `schema` 是 `wallet-cli.result.v1`，以下内容保证稳定：

- 上表中的响应字段名称与语义；
- 0/1/2 的退出码映射；
- JSON 模式下 stdout 只输出一个完整 JSON 对象的约定；
- 已有的 `error.code` 取值保持其含义（可能新增 code）；
- 规范命令 id 和网络 id（`tron:728126428`、`tron:3448148188`、`tron:2494104990`、`eip155:1`、`eip155:56`、`eip155:11155111`、`eip155:97`）。

网络**别名**属于配置，不属于接口约定：它们可以在本地被重新指向，因此脚本应当传规范 id。

不在承诺范围内：text 模式输出、`error.message` 的措辞、字段顺序、`meta.durationMs` 的取值，以及任何在命令参考页上标记为尽力而为（best-effort）的字段（例如 `account portfolio` 中的 `priceUsd`）。

## 另请参见

- [脚本编写指南](guide/scripting.md)——更通俗的入门
- [命令参考](commands/index.md)——每条命令的 `data` 返回数据
- [故障排查](troubleshooting.md)——按上述错误码组织的、面向人的处理办法
