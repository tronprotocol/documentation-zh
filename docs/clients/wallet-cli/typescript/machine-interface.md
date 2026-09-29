# 机器接口

本页定义脚本、CI 流水线和 AI 智能体调用 wallet-cli 时应遵循的接口规范，包括 JSON 响应结构、
退出码、错误码和敏感信息处理方式。除非另有说明，这些约定均受 `wallet-cli.result.v1` 的稳定性承诺保护。

## 调用约定 {#calling-convention}

```bash
wallet-cli <command> -o json [--network <id|alias>] [--timeout <ms>] [--account <id|label>]
```

- 始终传 `-o json`。文本输出是给人看的，不提供任何稳定性承诺。
- JSON 模式下，stdout 上**只有一个终态帧**——也就是结果响应体。除此之外绝不会有任何东西写到 stdout。诊断信息一律走 stderr。
- 运行时间较长的 `x402` 和 `bai` 命令还会在 stderr 上报告进度：text 模式下是 `⏳ …` 行，JSON 模式下每一步一行 `{"type":"activity","message":"…"}`。它们只是提示性的——可以忽略，也可以展示给用户，但绝不要用它们来判断结果。
- 每一次 RPC / 设备调用都受 `--timeout` 限制（毫秒，默认取 `config.timeoutMs`，内置 60000）。
- `--network` 接收规范的 **CAIP-2** id（`tron:3448148188`、`eip155:11155111`）或简短别名（`nile`、`sepolia`、`bsc`）。namespace 不等于链家族：`eip155` 寻址的是 `evm` 家族。别名只在选择网络的那一刻解析一次；下游任何环节都看不到它，响应中的 `chain.network` 始终报告规范 id。脚本里请优先用规范 id——别名只是本地配置项，随时可能被重新指向。
- CAIP-2 之前使用的那几个 TRON id（`tron:mainnet`、`tron:nile`、`tron:shasta`）作为永久别名保留，因此既有的调用方式仍然可用。**但输出是另一回事**：`chain.network`、`chain.chainId`、`networks` 列表中的 `id`，以及各 `config` 键，现在报告的都是 CAIP-2 id，所以凡是按字符串匹配、或用 `tron:nile` 作 map 键的使用方都需要更新。

### 能力发现

```bash
wallet-cli --json-schema
```

```bash
wallet-cli --json-schema tron
```

```bash
wallet-cli tx send --json-schema
```

一次调用就返回整个接口面：`tool`、`version`、`globalFlags`、`errorCodes` 和 `commands[]`。每个命令条目带有 `id`、`kind`、`path`、`usage`、`summary`、`requires`（network / auth / wallet）、`capability`、`examples`，以及描述其输入的 JSON Schema `inputSchema`；链上命令还会声明 `families`。这是了解本 CLI 的推荐方式；请不要去抓 `--help`。带上家族参数可以把目录限定到某一个链家族。

### 链家族

一个网络属于某一个**链家族**——`tron` 或 `evm`，而正是它决定了哪些命令、哪些参数适用：

- 命令会声明它服务于哪些家族（目录中的 `families`）。在另一个家族的网络上调用它，会在任何节点调用之前就以 **`family_mismatch`** 失败，退出码 `2`。
- 参数也可能只属于某一个家族（`--asset-id` 和 `--permission-id` 是 TRON 的，`--gas-limit` 和 `--nonce` 是 EVM 的）。把其中之一用在另一个家族上是 **`invalid_option`**，退出码 `2`。`--help` 会给它们打上 `(TRON only)` / `(EVM only)` 标记。
- 只要**账户**持有密钥，它就不绑定家族——seed 账户或私钥账户同时拥有 TRON 和 EVM 两个地址。仅观察账户和 Ledger 账户只有一个地址，因此也只属于一个家族；在不匹配的网络上选中它，同样是 `family_mismatch`。

命令家族与参数家族的校验是静态的——它们只取决于命令、参数和所选网络——因此智能体可以直接从目录判断，无需发起调用。而账户家族是否兼容还取决于所选的钱包账户：持有密钥的账户两个家族都能用，仅观察账户和 Ledger 账户则绑定在其中一个上。

### 启动时的钱包数据升级 {#startup-wallet-data-upgrades}

每条命令在运行前都会检查持久化的钱包 schema。`--help`、`--version`、`--json-schema` 以及不带参数的 `wallet-cli` 是例外：它们从不读取钱包数据，因此跳过该检查。如果 schema 已经过时，启动关卡会先完成升级，而**你输入的那条命令会被刻意跳过、不予执行**。过程写入 stderr；结果是一个退出码为 `0` 的成功响应，其 `command` 为 `migration`：

| 字段 | 含义 |
|---|---|
| `upgraded` | 文件被改写时为 `true`，用户拒绝时为 `false` |
| `cancelled` | 仅在用户拒绝升级时为 `true` |
| `files[]` | 含 `path`、`from`、`to` 和 `backup`（用户拒绝升级时没有 `backup`，因为什么都没写） |
| `originalCommandExecuted` | 恒为 `false`——查看这个结果之后，请重新执行你原来的命令 |

在这个边界上结束本次调用，正是为了避免脚本化命令或动用资金的命令，在一次预料之外的持久状态变更之后继续往下跑。

在交互式终端里，升级会先征求同意。随后，seed 和私钥类的迁移会要求输入 master password；Ledger 和仅观察类的迁移则不需要。非交互式的 Ledger / 仅观察迁移是自动进行的，而需要密码的那一类必须提供 `--password-stdin`，否则以 `migration_required` 失败、退出码 `2`——因为需要改变的是这次调用本身，所以它属于用法错误；该错误码专门保留给**无法**进行的升级。拒绝升级不算失败：它是退出码 `0`，带 `upgraded: false`、`cancelled: true`，且不写入任何文件或备份。

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
| `error.message`   | string | 仅出错时 | 面向人类可读；**不**稳定——绝不要解析它。当一次链上拒绝被归类到某个错误码时，它的内容形如 `<category>: <what the node said>`，因此终端里能看到节点自己给出的数字或 revert 原因；同一段节点原文也会出现在 `details.nodeMessage`（TRON，已脱敏）或 `details.providerMessage`（TronLink）中，并与 `details.nodeCode` / `details.providerCode` 一同给出 |
| `error.details`   | object | 可选 | 可用时提供的结构化附加信息 |
| `meta.durationMs` | number | 始终 | 实际耗时（毫秒） |
| `meta.warnings`   | `(string \| {code, message})[]` | 始终 | 非致命提示；**元素类型并不统一**——见下文 |
| `meta.pagination` | object | 仅返回窗口的命令 | `offset` / `limit` / `total`；当命令返回一个分页窗口时出现——见[分页](#pagination) |
| `chain`           | object | 选定了网络时 | `family` / `network` / `chainId`。每条链上命令都有；本地命令若其策略会解析出一个网络，也会有——目前是 `backup`、`current` 和 `list`，它们把选定网络或默认网络当作链家族/展示用的选择器，并不访问节点。`network: "none"` 的命令（`config`、`networks`、`contact`、`encoding`、`address`、`create`、`import` 等）不带它；它的存在**并不**意味着访问过节点 |

编码规则：`bigint` 值序列化为十进制**字符串**（例如 `"balance": "1976489000"`），二进制序列化为 hex。以 `bigint` 或协议 int64 表示的金额是字符串，但 `feeSun`、`multiSignFeeSun`、`energyUsed`、`netUsed` 这类有界的计数和费用可能以 JSON 数字返回。请以各命令的字段表为准，不要把所有金额强行当成同一种类型。

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

返回 offset/limit 窗口的命令会把它放在 `meta.pagination` 中报告，绝不会塞进 `data` 里。目前这类命令有 `asset list`、`exchange list`、`proposal list`、`backup --records`、`x402 provider-list`、`bai recharge-orders` 和 `bai usage-records`；某条命令也可能只是把 `--limit` 当作结果条数上限，从而不给出分页元数据：

| 键 | 类型 | 含义 |
|---|---|---|
| `offset` | number | 本页的起始索引——回显 `--offset` |
| `limit` | number \| **null** | 每页大小；`null` = 不限（未给 `--limit`） |
| `total` | number \| **null** | 匹配记录的总数；`null` 表示**不存在这个计数**，而不是"被省略了" |

这三个键始终存在，因此 `null` 是唯一的「未知」信号，也就不必再去区分「字段缺席」和「值为 null」。按游标翻页的服务还可能多出两个：`hasMore`（布尔）和 `nextCursor`（字符串，用 `--cursor` 传回）——目前只有 [`bai usage-records`](commands/bai/usage-records.md)，它的 `total` 恒为 `null`。

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

**持续维护的错误码索引是公开的**，位于能力发现目录的 `errorCodes` 下：

```bash
wallet-cli --json-schema | jq '.errorCodes'
```

每个条目都是对象，而不是单独的字符串：

```json
{ "rpc_error": { "exit": 1, "retry": "same", "meaning": "the node answered with an error" } }
```

`exit` 是某个错误码退出状态的权威来源；下面的表格是手写的，并由测试与它核对。少数错误码带的是 `"either"`：它们确实会在两侧出现，实际退出状态以进程真正返回的那个为准。

`retry` 回答的是「接下来怎么办」：`same`——立即重试完全相同的命令（节点或服务的偶发抖动）；`later`——同样的命令会成功，但现在还不行，需要先退避一段时间（锁定期、提现间隔、限流）；`changed`——必须先修改请求再重试（提高手续费、用新的 nonce 重新构建）；`never`——原样重试不可能成功，必须改变命令之外的某些东西。所有退出码为 `2` 的错误码，按定义都是 `never`。

`retry` 描述的是**错误**，而不是命令。`timeout` 和 `rpc_error` 标为 `same`，是因为对大多数调用来说这是对的——节点根本没有动作，重发不会有代价。但是，一条可能已经广播出交易的命令（`tx send` 以及提交路径上的其他命令）也可能在**节点已经受理该交易、而响应还没回来**的时候撞上 `timeout` 或 `rpc_error`。这种情况下结果是未知，而不是失败；重发并不是在重试原来那个请求：它会构建并签名一笔**新的**交易，在 TRON 上就是第二笔互不相同的转账。对于解析网络 id 或读取余额时发生的 `timeout` / `rpc_error`，`retry: "same"` 是对的；但它不是盲目重发广播的许可。做决定之前，请先用 [`tx status`](#script-safety-never-mistake-submitted-for-confirmed) 对账。

这份索引是本版本暴露出来的机器可读目录。请把它当作能力发现的辅助手段，而不是一个封闭枚举：有少数代码路径会在运行时动态选择错误码字符串，因此实际响应中仍可能出现 `errorCodes` 里没有的 code。下面的表格是高频子集，便于阅读。v1 内仍可能新增 code；有两个字符串（`invalid_value`、`aborted`）会根据抛出位置的不同而出现在两种退出码下——所以请始终兼容未知错误码，并回退到对应的退出码类别。

退出码 **2**（用法——修正调用方式）下的常见错误码：

| 错误码 | 含义 |
|---|---|
| `usage_error` | 由参数解析器本身抛出——yargs 的用法失败，或位置参数过多。更具体的问题各有自己的 code：未知参数是 `invalid_option`，缺少必填参数是 `missing_option`，取值校验或跨字段规则失败是 `invalid_value` |
| `family_mismatch` | 该命令、该账户、该收款方或该原始交易不属于所选网络所在的链家族 |
| `missing_option` | 未提供某个必填参数 |
| `invalid_option` | 某个参数被用在了非法组合中，或者它只属于另一个链家族 |
| `invalid_value` | 某个参数取值未通过校验（例如 `config defaultOutput xml`） |
| `invalid_permission` | 权限文档或所选的权限组对该操作而言不合法 |
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
| `invalid_keystore` | `import keystore`：不是合法的 Web3 V3 keystore——JSON 有误、`version` ≠ 3、使用了不支持的 cipher/KDF，或解密结果不是 32 字节私钥 |
| `invalid_config` | `config.yaml` 无法读取或不是合法的 YAML——请修复或删除该文件。具体解析错误会被隐藏，因为错误信息可能引用包含凭据的原始行 |
| `insecure_config` | `config.yaml` 保存了服务凭据，但它是符号链接或对同组/所有人可读——请对它执行 `chmod 600`（仅 POSIX；Windows 上不强制） |
| `account_not_found` | 本地没有该 id、标签或地址对应的账户 |
| `contact_not_found` / `already_exists` | 不存在该名称的联系人，或该联系人名称/地址已被占用 |
| `token_not_in_book` / `token_is_official` / `token_already_listed` | token 地址簿相关的状况 |
| `unsupported_token` | 所选服务方或该命令不支持这个 token |
| `insufficient_voting_power` | 请求的票数超出该账户可用的投票权 |
| `gasfree_credentials_missing` / `tronlink_credentials_missing` | 未配置所需的服务凭据（用 `config` 设置） |
| `unknown_parameter` | 不存在该名称或 id 的链参数（`proposal create --set`） |
| `invalid_asset_name` | TRC10 名称或缩写不在 1–32 个可见 ASCII 字符范围内 |
| `migration_required` | 持久化的钱包数据需要升级，但本次调用因无法获得 master password 而不能完成升级——请在终端中重新运行，或用 `--password-stdin` 管道传入。参见[启动时的钱包数据升级](#startup-wallet-data-upgrades) |
| `seed_not_found` | `derive` 指向的账户或 id 不是 HD 钱包——而是私钥、Ledger 或仅观察账户 |
| `bai_credentials_missing` | 未配置 B.AI API key。请用 `config baiApiKey --api-key-stdin` 设置 |
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
| `provider_rate_limited` | 某个外部服务返回了 HTTP 429。GasFree：若它发送了 `Retry-After` 头，`error.details.retryAfter` 会带上它。x402 facilitator 或 endpoint：对方发送时给出 `error.details.retryAfterSeconds`，并附带下文的付款明细——结算过程中的 429 是 `paymentStatus: "unknown"`。B.AI：`error.details.httpStatus: 429`。TronLink 的 429 则归为 `provider_error` |
| `tx_expired` | 签名收齐之前交易就已过期（TRON） |
| `chain_id_mismatch` | 该 EVM 交易是为另一条链构建的，与所选网络不符 |
| `nonce_too_low` | 该 EVM 交易的 nonce 已经被一笔已入块的交易用掉了 |
| `history_not_supported` | 该端点不支持 TronGrid 历史查询（`account history`，TRON） |
| `not_found` | 所寻址的对象不存在——例如未激活的账户、交易、区块，或 GasFree / TronLink 资源 |
| `proposal_not_found` / `contract_not_found` / `asset_not_found` / `exchange_not_found` | 链上不存在与该提案 ID、合约地址、TRC10 引用或交易对 ID 对应的对象 |
| `ambiguous_asset_name` | 某个 TRC10 名称匹配到多个 token；`error.details` 中带有候选项——见 [`error.details.matches`](#errordetailsmatches) |
| `ledger_unsupported` | 所选的 Ledger app 无法为该交易类型签名——请求会在访问设备前被拒绝（TRON 的账户激活、账户 id、`asset` 写操作、合约部署与治理、`witness` 写操作，以及 `stake cancel-unfreeze`） |
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
| `legacy_derivation` | 4.13.1 之前创建的钱包中，1 号或更靠后的 TRON 账户使用的派生路径，本版本已不再用于签名。以该 TRON 地址签名、或用 `derive` 向其钱包添加账户时抛出。参见[出现 `legacy_derivation` 后如何找回地址](troubleshooting/legacy-derivation-recovery.md) |
| `derivation_mismatch` | 某账户存储的地址与其种子的任何派生路径都对不上——`wallets.json` 与加密保险库互相矛盾 |
| `execution_reverted` | 合约 revert 了该调用；原始 revert 数据在 `error.details.revertData` 中 |
| `not_authorized` | 该账户无权执行此操作。`8004 update` / `transfer` / `approve`：该账户既不是 Agent 的所有者，也不是被允许执行此操作的操作者——这是在签名之前由注册表的 revert 解码得出的 |
| `agent_not_found` | 所选网络的注册表中没有该 id 的 Agent——用于 `8004 show`，以及 `8004` 的各写入命令（在签名之前由注册表的 revert 解码得出） |
| `amount_exceeds_limit` / `no_matching_requirement` | `x402 pay`，无论是否加 `--dry-run`：价格高于 `--max-amount` / `--max-raw-amount`，或端点给出的支付路由中没有一条与所选网络、`--token`、`--asset` 或 `--scheme` 匹配。均在签名之前抛出（`details.paymentStatus: "not_sent"`） |
| `gasfree_insufficient_balance` / `gasfree_not_activated` / `gasfree_asset_unsupported` | 一笔 `exact_gasfree` 的 x402 付款：GasFree 账户不足以覆盖付款额加最高手续费、尚未激活，或不持有所选的 token 合约（请检查网络、token 和 `--gasfree-relay`）。在发出任何东西之前就抛出（`details.paymentStatus: "not_sent"`） |
| `permit2_allowance_required` / `approval_reset_required` | x402 付款需要先有 token 授权额度，或者该 token 需要先把额度重置为零才能设置新值 |
| `fee_cap_exceeded` / `payer_mismatch` / `signed_payload_mismatch` | x402 授权在签名前或签名后被拒绝：GasFree 手续费超过上限、载荷中的付款方是另一个地址，或签名覆盖的结构与请求的不一致 |
| `invalid_settlement` / `invalid_x402_response` | 付费后的响应带有无效的结算回执，或某个 x402 响应无法解码 |
| `provider_not_found` / `catalog_schema_unsupported` | `x402 provider-show` / `endpoint-list`：没有该名称的服务方；或下载到的目录使用了本版本无法读取的版本 |
| `port_in_use` | `x402 serve` / `roundtrip`：请求的本地端口已被占用。`x402 serve --daemon` 下，后台服务器启动失败（含端口被占用的情形）会报告为 `provider_error`，并带上 `error.details.logFile` |
| `response_too_large` | 远端响应超过了 CLI 的大小上限 |
| `bai_auth_failed` / `bai_rejected` | B.AI 拒绝了该 API key，或出于可识别的业务原因拒绝了某项操作（`error.details.reason`） |
| `internal_error` | 预期之外的内部失败；消息刻意保持通用 |

预期之外的异常会先经过**脱敏处理**，再以 `internal_error` 和通用消息返回，避免第三方库回显的敏感信息
进入响应。上面两张表仅用于方便阅读；持续维护的能力发现索引是 `--json-schema` 返回的 `errorCodes`，
但该索引也不保证列出解析器可能返回的所有错误码。

### x402 与 B.AI 的支付细节 {#x402-and-bai-payment-details}

付款失败时，`error.details` 中会带上额外字段，便于脚本判断钱是否可能已经出去了：

| 字段 | 含义 |
|---|---|
| `phase` | 失败发生在哪一步：`request`、`challenge`、`create_payment`、`sign`、`payment_request`、`verify` 或 `settle` |
| `httpStatus` | 失败请求的 HTTP 状态码（如果有的话） |
| `paymentStatus` | `not_sent`——什么都没发出去；`unknown`——无法确认结果，因此再次付款前请先对账；`settled`——收到了结算回执，但所购买的资源未能交付 |
| `settled` / `delivered` | 付款是否已结算，以及资源是否已送达 |
| `retryPayment` | `false` 表示**不要**为了补救而再付一次。它优先于错误码自带的通用 `retry` 值 |
| `candidateTxHash` / `candidateNetwork` | 一笔可能就是该付款的交易。它是对账用的线索，而不是付款已完成的证据 |
| `approval` | TRON：失败前已签名的那笔一次性 Permit2 approve——`{txId, token, spender, allowance, feeLimitSun, status}`，其中 `status` 为 `submitted`、`confirmed` 或 `exported`。它不是付款，不要当作付款上报。如果它旁边还有 `paymentStatus: "not_sent"`，则说明链上已存在该授权额度，但并未生成任何付款授权 |

**请把 `paymentStatus: "unknown"` 当作可能已付。** 举例来说，从一个没有 token 余额的账户发起 `exact` 付款，当前会以 `provider_error` 失败，带 `phase: "create_payment"` 和 `paymentStatus: "unknown"`——尽管实际上什么都没发出去。

### `error.details.matches` {#errordetailsmatches}

部分错误表示输入存在歧义，需要调用方从多个候选项中选择，而不是简单重试。这类错误会把候选项放在
`error.details.matches` 中，其值是字段结构一致的对象数组：

```json
{"code":"ambiguous_asset_name","message":"2 TRC10 tokens are named MyToken; re-run with the id","details":{"name":"MyToken","assetIds":["1000123","1000488"],"matches":[{"assetId":"1000123","issuerAddress":"TQkXm4vN...","totalSupply":"1000000000000000","precision":6},{"assetId":"1000488","issuerAddress":"TZx9kP2m...","totalSupply":"5000000000","precision":2}]}}
```

`ambiguous_account` 是这套约定的第二位成员，也是更常遇到的那个——任何 `--account <address>` 只要在当前操作所属的家族下无法解析为唯一一个可互换的签名者，都会返回它：

```json
{"code":"ambiguous_account","message":"address T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb matches 2 accounts; address it by accountId","details":{"address":"T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb","accountIds":["wlt_a1b2c.0","wlt_d3e4f.0"],"matches":[{"accountId":"wlt_a1b2c.0","label":"main","type":"seed","index":0},{"accountId":"wlt_d3e4f.0","label":"cold","type":"watch","index":null}]}}
```

`matches` 是通用字段，并不限定于某个错误码。任何带有该字段的错误都应按相同方式处理。text 模式会在
stderr 的 `error [...]` 行下方以表格显示候选项。`matches` 中的数量保留最小单位，与对应成功响应的
表示方式一致；某行包含 `precision` 时，text 表格会换算为便于阅读的数值。

与它并列，错误还可能携带一个只包含标识符的标量列表，供你据此重试——就是上面的 `assetIds`。脚本请优先用它；`matches` 的存在是为了让人能分辨这些候选项。

## 敏感信息处理 {#secret-handling}

wallet-cli 绝不从命令行参数、也不从专用的敏感信息环境变量中读取密码、助记词或私钥：参数和导出的变量会泄漏进 shell 历史、进程列表和 CI 日志。只有两条通道：

1. **stdin 标志**——`--password-stdin` 用于 master password，`--tx-stdin` / `--message-stdin` 用于较大的载荷。**每次运行只能有一个 `*-stdin` 标志消费 stdin。**（助记词和私钥没有 stdin 通道——`import mnemonic` / `import private-key` / `change-password` 只能交互执行，走隐藏的 TTY 输入。）
2. **交互式 TTY 提示**——只出现在那些自己声明为交互式的命令上：`create`、各个 `import` 子命令、`backup`、`change-password`，以及 `delete` 的确认。其他地方有没有终端都一样：`tx send`、`contract *`、`stake *`、`message sign` 之类从不弹出提示，缺少 master password 一律是 `auth_required`（退出码 `1`），与是否挂载 TTY 无关。

示例中的 shell 变量只是 shell 一侧为管道准备的数据来源；wallet-cli 并不会去读它们。请让它们保持在进程内、生命周期尽量短，也不要长期 export。

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

   Agent id 同理：`8004 register` 会立刻把请求的 `uri` 放进 `data.identity`，而只有在能读到已确认的注册事件时，才补上 `identity.agentId`（十进制字符串）。`8004 update` 报告 `identity.agentId`、`oldURI` 和 `requestedURI`，确认之后再加上 `newURI`；`8004 transfer` 报告 `agentId`、`oldOwner` 和 `requestedOwner`，确认之后再加上 `newOwner`。`8004 approve` 报告 `agentId` 和 `operator`（使用 `--revoke` 时为零地址）。`8004 add-operator` 和 `remove-operator` 报告 `operator` 和 `requestedApproval`，确认之后再加上从注册表读回的 `approved`。

2. 想阻塞到结果已知为止，请传 `--wait`（轮询直到 confirmed/failed，上限由 `--wait-timeout` 控制，默认 60000 毫秒；触及上限时返回提交回执）。

   **`--wait` 通过 `data.stage` 报告交易结果，而不是通过 `success`。** 如果交易已提交并入块，但链上执行失败，CLI 调用本身仍算成功：响应中的 `success` 为 `true`、退出码为 `0`，而 `data.stage` 为 `"failed"`。退出码表示 CLI 是否完成了请求，并不表示链上执行是否成功。因此使用 `--wait` 后，程序必须检查 `data.stage`（`confirmed` / `failed` / `submitted`），再决定如何记录本次操作。

3. 或者你自己用 `tx status` 轮询，它有一个**四状态模型**：

   | `data.state` | 含义 | 是否终态？ |
   |---|---|---|
   | `confirmed` | 已入块，且能拿到执行结果 / 回执（带有 `blockNumber`） | 是 |
   | `failed` | 已入块但被 revert / 拒绝 | 是 |
   | `pending` | 节点已看到，但尚无执行结果 / 回执 | 否——继续轮询 |
   | `not_found` | 所查询的端点不认识它 | 否——继续轮询并对账；不要臆断为失败 |

   `data.confirmed` 和 `data.failed` 以布尔值提供，便于直接分支。

   > `confirmed` 表示已入块并取得回执，不表示已最终确定。当这个区别重要时，请另行验证——TRON 上查询 SolidityNode 视图，EVM 上检查 finalized 区块。

   > 如果截止时间到达时状态仍为 `pending` 或 `not_found`，交易结果仍然未知。不要将其记录为失败；在通过外部方式对账之前，不要自动重发。

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
    confirmed) exit 0 ;;
    failed)
      echo "transaction failed: $txid" >&2
      exit 1
      ;;
    pending|not_found) sleep 3 ;;
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
- 规范命令 id 和网络 id（`tron:728126428`、`tron:3448148188`、`tron:2494104990`、`eip155:1`、`eip155:56`、`eip155:11155111`、`eip155:97`、`eip155:8453`、`eip155:84532`）。

网络**别名**属于配置，不属于接口约定：它们可以在本地被重新指向，因此脚本应当传规范 id。

不在承诺范围内：text 模式输出、`error.message` 的措辞、字段顺序、`meta.durationMs` 的取值，以及任何在命令参考页上标记为尽力而为（best-effort）的字段（例如 `account portfolio` 中的 `priceUsd`）。

## 另请参见

- [脚本编写指南](guide/scripting.md)——更通俗的入门
- [命令参考](commands/index.md)——每条命令的 `data` 返回数据
- [故障排查](troubleshooting.md)——按上述错误码组织的、面向人的处理办法
