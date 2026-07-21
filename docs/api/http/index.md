# java-tron HTTP API 文档

本目录收录 `framework/src/main/java/org/tron/core/services/http/` 下 FullNode HTTP 接口的请求/响应文档。每个接口一个 markdown 文件，命名规则同 URL 末段（例如 `/wallet/getnodeinfo` → `getnodeinfo.md`）。

未收录接口主要包括以下三个类别：

- Exchange（DEX）类接口
- Market（订单簿）类接口
- Shielded（匿名交易）类接口

## 通用约定

- **Method**：除少量纯查询接口同时支持 `GET`，多数 POST 接口仅接受 `POST`，请求体为 JSON。
- **GET / POST 边界**：同时支持两种方法的接口会在请求表和异常表中标明适用方法。GET 通常从 URL 查询参数读取，POST 通常读取 JSON 请求体；如果 POST 复用查询参数或忽略请求体，对应接口页面会单独说明。
- **`visible`**：`true` 时地址使用 base58check 字符串形式，URL/描述等文本字段使用 UTF-8 字符串；`false`（默认）时使用 hex 字符串。
- **构造类接口**返回未签名的 `protocol.Transaction`，需调用方本地签名后通过 [`/wallet/broadcasttransaction`](tx-build-and-broadcast/broadcasttransaction.md) 或 [`/wallet/broadcasthex`](tx-build-and-broadcast/broadcasthex.md) 广播。
- **`Permission_id`**：交易构造接口可选；用于多签账户指定使用哪个 `Permission`。字段名区分大小写。
- **金额单位**：除 TRC-10 数量按发行精度外，其他金额一律为 sun（1 TRX = 1e6 sun）。
- **`int64_as_string`**：GET 请求可在 URL 查询参数中添加 `int64_as_string=true`。启用后，protobuf JSON 响应中的 int64 / uint64 字段会序列化为 JSON 字符串，避免 JavaScript 等客户端出现精度损失。该参数只对 GET 请求生效，不影响 POST 请求体。
- **请求体大小**：HTTP 请求体受 `config.conf` 中 `node.http.maxMessageSize` 限制（默认 `4194304`，约 4 MiB；`0` 表示拒绝所有非空 body）。JSON-RPC 有独立的 `node.jsonrpc.maxMessageSize`。
- **限流**：HTTP 单接口限流在 `rate.limiter.http` 中配置。全局开关 `rate.limiter.apiNonBlocking` 控制超限行为：`true` 表示立即拒绝，并返回 HTTP 200 和 `{"Error":"class java.lang.IllegalAccessException : lack of computing resources"}`；`false` 表示排队并阻塞调用方直到获得 permit。

!!! warning "XSS 安全提示"

    尽管 HTTP API 通过将 `Content-Type` 设置为 `application/json` 降低了浏览器直接将响应解析为 HTML 的风险，但这并不等于完全避免 XSS。部分接口对入参并无严格校验，响应中可能回显用户可控内容（尤其当 `visible=true` 时，地址、备注等字段可能以 UTF-8 字符串原样返回）。在将 API 返回的数据渲染到页面之前，应根据输出上下文进行安全处理。

    正确做法是根据输出位置选择合适的编码方式：在 HTML 文本上下文中使用 HTML 实体编码（如将 `<` 转成 `&lt;`、`>` 转成 `&gt;`、`"` 转成 `&quot;`），或直接使用前端框架自带的默认输出转义机制（如 React JSX、Vue 模板的默认转义）。如果数据被放入 URL 参数中，才应使用 `encodeURIComponent()` 这类 URL 编码方法。注意 `encodeURIComponent()` / `escape()` 属于 URL 编码或旧式编码方式，不能替代 HTML 上下文中的输出转义。

    更多防护指引请参考 [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)。

## 异常响应

HTTP 状态码在**绝大多数情况下都是 200**（业务错误也通过响应体表达），客户端必须解析响应体判断成败。已知例外：

- 接口被节点配置 `disabledApiList` 显式禁用时，由 `HttpApiAccessFilter` 直接返回 **HTTP 404**，响应体 `{"Error": "this API is unavailable due to config"}`。
- 请求体超过 `node.http.maxMessageSize` 时，共享 HTTP `SizeLimitHandler` 可能会在目标 servlet 处理请求前直接返回 **HTTP 413**（`Payload Too Large`）。如果请求已经进入 servlet，并由 servlet 内部的 `Util.checkBodySize` 检查到 body 超限，则接口会按自身的异常响应格式返回；部分接口仍可能是 **HTTP 200** 加错误响应体。
- 启用非阻塞限流且共享 `RateLimiterServlet` 无法获得 permit 时，会在目标 servlet 运行前返回 **HTTP 200**，响应体为 `{"Error":"class java.lang.IllegalAccessException : lack of computing resources"}`。这是共享层错误，而非接口业务错误。
- 节点以 lite fullnode 模式启动且未开启 `openHistoryQueryWhenLiteFN` 时，由 `LiteFnQueryHttpFilter` 对约 24 个历史查询接口（`getblockbynum` / `gettransactionbyid` / `gettransactioninfobyid` / `gettransactioninfobyblocknum` / `getblockbyid` / `getblockbylatestnum` / `getblockbylimitnext` / `gettransactioncountbyblocknum` 等）返回 **HTTP 200**，但响应体是裸字符串 `this API is closed because this node is a lite fullnode`（**非 JSON**），客户端朴素 `JSON.parse` 会抛错，需先按字符串前缀识别。
- 其它由 servlet 容器/反向代理产生的网络层错误（502、504、连接拒绝等）不在本文档范围。

<!-- BEGIN GENERATED HTTP ERROR CATALOG -->
### HTTP 错误目录

Catalog ID 和重试分类由 `openapi.yaml` 的 `x-tron-error-model` 定义。它们是机器可读的文档分类，不是 java-tron 在线上响应中返回的字段。

`自动重试` 与 catalog 的 `retryable` 完全对应：只有“是”才允许自动重放同一逻辑操作。有条件的重试类别在满足“范围 / 操作”的前置条件之前仍为“否”。

| Catalog ID | 线上信号 | 含义 | 自动重试 | 重试类别 | 范围 / 操作 |
|---|---|---|---|---|---|
| `HTTP_RATE_LIMITED` | HTTP 200 且 `$.Error` 包含 `lack of computing resources` | 共享 servlet 限流器拒绝了请求。 | 是 | `SAFE_WITH_BACKOFF` | 使用带抖动的指数退避自动重试；响应不包含 Retry-After header。 |
| `HTTP_SERVLET_EXCEPTION` | HTTP 200 加自由文本 `$.Error` | servlet 在 JavaTronError 中返回了异常类和消息。 | 否 | `UNKNOWN` | 检查具体 Error 文本和接口上下文；不得仅根据该兜底分类自动重试。 |
| `HTTP_API_DISABLED` | HTTP 404 且 `$.Error` = `this API is unavailable due to config` | 节点配置禁用了该接口。 | 否 | `AFTER_STATE_CHANGE` | 使用已启用该接口的节点，或等待节点配置变更。 |
| `HTTP_LITE_FULLNODE_HISTORY_DISABLED` | HTTP 200 加裸文本 `this API is closed because this node is a lite fullnode` | lite FullNode 拒绝了历史区块或交易查询。 | 否 | `AFTER_STATE_CHANGE` | 使用 full node，或等待 `openHistoryQueryWhenLiteFN` 配置变更。 |
| `HTTP_REQUEST_TOO_LARGE` | HTTP 413（`text/html`） | 请求超过 `node.http.maxMessageSize`。 | 否 | `AFTER_REQUEST_REBUILD` | 缩小请求体后重新提交。 |
| `RETURN_SIGERROR` | `$.code` 或 `$.result.code` = `SIGERROR` | 交易签名无效。 | 否 | `NEVER` | 修正签名并重新签名。 |
| `RETURN_CONTRACT_VALIDATE_ERROR` | `$.code` 或 `$.result.code` = `CONTRACT_VALIDATE_ERROR` | 合约校验失败。 | 否 | `AFTER_REQUEST_REBUILD` | 修正参数、余额或权限后重构请求。 |
| `RETURN_CONTRACT_EXE_ERROR` | `$.code` 或 `$.result.code` = `CONTRACT_EXE_ERROR` | 合约执行失败。 | 否 | `AFTER_STATE_CHANGE` | 检查 message；仅在相关合约或链状态变更后重试。 |
| `RETURN_BANDWITH_ERROR` | `$.code` 或 `$.result.code` = `BANDWITH_ERROR` | 账户带宽不足，或其余额不足以支付带宽、多签、备注或其他交易相关费用。 | 否 | `AFTER_STATE_CHANGE` | 在带宽恢复，或账户余额足以支付相应的带宽、多签、备注或其他交易相关费用后重试；如果交易过期，则需重新构建并签名。 |
| `RETURN_DUP_TRANSACTION_ERROR` | `$.code` 或 `$.result.code` = `DUP_TRANSACTION_ERROR` | 节点已知该交易。 | 否 | `VERIFY_BEFORE_RETRY` | 先按 txid 查询，再决定是否需要新交易。 |
| `RETURN_TAPOS_ERROR` | `$.code` 或 `$.result.code` = `TAPOS_ERROR` | 交易引用的区块无效或过旧。 | 否 | `AFTER_REQUEST_REBUILD` | 使用较新的引用区块重构并重新签名。 |
| `RETURN_TOO_BIG_TRANSACTION_ERROR` | `$.code` 或 `$.result.code` = `TOO_BIG_TRANSACTION_ERROR` | 交易过大。 | 否 | `AFTER_REQUEST_REBUILD` | 缩小或拆分交易后重新提交。 |
| `RETURN_TRANSACTION_EXPIRATION_ERROR` | `$.code` 或 `$.result.code` = `TRANSACTION_EXPIRATION_ERROR` | 交易已过期。 | 否 | `AFTER_REQUEST_REBUILD` | 使用新的 expiration 重构并重新签名。 |
| `RETURN_SERVER_BUSY` | `$.code` 或 `$.result.code` = `SERVER_BUSY` | 节点待处理交易过多。 | 是 | `SAFE_WITH_BACKOFF` | 使用带抖动的指数退避自动重试，或使用其它健康节点。 |
| `RETURN_NO_CONNECTION` | `$.code` 或 `$.result.code` = `NO_CONNECTION` | 节点没有活跃对等连接。 | 是 | `SAFE_WITH_BACKOFF` | 等待连接恢复后退避重试，或使用其它已连接节点。 |
| `RETURN_NOT_ENOUGH_EFFECTIVE_CONNECTION` | `$.code` 或 `$.result.code` = `NOT_ENOUGH_EFFECTIVE_CONNECTION` | 节点的有效对等连接过少。 | 是 | `SAFE_WITH_BACKOFF` | 等待有效对等连接恢复后退避重试，或使用其它节点。 |
| `RETURN_BLOCK_UNSOLIDIFIED` | `$.code` 或 `$.result.code` = `BLOCK_UNSOLIDIFIED` | 节点暂时处于未固化区块状态。 | 是 | `SAFE_WITH_BACKOFF` | 等待区块固化后退避重试，或使用其它已同步节点。 |
| `RETURN_OTHER_ERROR` | `$.code` 或 `$.result.code` = `OTHER_ERROR` | Return 响应报告未分类失败。 | 否 | `UNKNOWN` | 检查 message；如无更具体的瞬时原因，不得自动重试。 |
| `SIGN_WEIGHT_NOT_ENOUGH_PERMISSION` | `$.result.code` = `NOT_ENOUGH_PERMISSION` | 累计签名权重不足。 | 否 | `AFTER_REQUEST_REBUILD` | 在再次尝试前，为所选权限补充有效签名。 |
| `SIGN_WEIGHT_SIGNATURE_FORMAT_ERROR` | `$.result.code` = `SIGNATURE_FORMAT_ERROR` | 签名格式无效。 | 否 | `NEVER` | 修正签名格式并重新签名。 |
| `SIGN_WEIGHT_COMPUTE_ADDRESS_ERROR` | `$.result.code` = `COMPUTE_ADDRESS_ERROR` | 无法从签名恢复地址。 | 否 | `NEVER` | 修正签名，使其可恢复签名者地址。 |
| `SIGN_WEIGHT_PERMISSION_ERROR` | `$.result.code` = `PERMISSION_ERROR` | 账户、所选权限、操作或提供的签名的权限评估失败。 | 否 | `UNKNOWN` | 检查 `result.message`；修正 `Permission_id`/签名，或等待账户权限状态变更。不得自动重试。 |
| `SIGN_WEIGHT_OTHER_ERROR` | `$.result.code` = `OTHER_ERROR` | 签名权重评估返回了未分类失败。 | 否 | `UNKNOWN` | 检查 `result.message`；如无更具体的瞬时原因，不得自动重试。 |
| `APPROVED_LIST_SIGNATURE_FORMAT_ERROR` | `$.result.code` = `SIGNATURE_FORMAT_ERROR` | 签名格式无效。 | 否 | `NEVER` | 修正签名格式并重新签名。 |
| `APPROVED_LIST_COMPUTE_ADDRESS_ERROR` | `$.result.code` = `COMPUTE_ADDRESS_ERROR` | 无法从签名恢复地址。 | 否 | `NEVER` | 修正签名，使其可恢复签名者地址。 |
| `APPROVED_LIST_OTHER_ERROR` | `$.result.code` = `OTHER_ERROR` | 批准列表评估返回了未分类失败。 | 否 | `UNKNOWN` | 检查 `result.message`；如无更具体的瞬时原因，不得自动重试。 |
| `TRANSACTION_RESULT_FAILED` | `$.transaction.ret[0].ret` = `FAILED` | 生成的交易结果报告 FAILED。 | 否 | `AFTER_STATE_CHANGE` | 检查交易结果，并修正或重构交易。 |
| `INVALID_ADDRESS` | `wallet_validateaddress_get` 或 `wallet_validateaddress_post`：`$.result` = `false` | 地址校验返回 `result=false`。 | 否 | `NEVER` | 修正地址编码或 `visible` 模式后重新校验。 |
<!-- END GENERATED HTTP ERROR CATALOG -->
## 账户

| 接口 | 说明 |
|---|---|
| [`/wallet/getaccount`](account/getaccount.md) | 按地址查询账户 |
| [`/wallet/getaccountbalance`](account/getaccountbalance.md) | 查询账户在指定区块的余额 |
| [`/wallet/getaccountnet`](account/getaccountnet.md) | 查询账户带宽资源 |
| [`/wallet/getaccountresource`](account/getaccountresource.md) | 查询账户带宽+能量+TronPower |
| [`/wallet/createaccount`](account/createaccount.md) | 链上创建账户（需消耗 1 TRX） |
| [`/wallet/updateaccount`](account/updateaccount.md) | 修改账户名 |
| [`/wallet/accountpermissionupdate`](account/accountpermissionupdate.md) | 配置多签权限 |
| [`/wallet/validateaddress`](account/validateaddress.md) | 校验地址合法性 |

## 区块 / 交易查询

| 接口 | 说明 |
|---|---|
| [`/wallet/getnowblock`](block-and-tx-query/getnowblock.md) | 当前最新区块 |
| [`/wallet/getblock`](block-and-tx-query/getblock.md) | 通用区块查询（按 num/hash） |
| [`/wallet/getblockbynum`](block-and-tx-query/getblockbynum.md) | 按高度查询区块 |
| [`/wallet/getblockbyid`](block-and-tx-query/getblockbyid.md) | 按 hash 查询区块 |
| [`/wallet/getblockbylimitnext`](block-and-tx-query/getblockbylimitnext.md) | 按区间查询区块 |
| [`/wallet/getblockbylatestnum`](block-and-tx-query/getblockbylatestnum.md) | 查询最近 N 个区块 |
| [`/wallet/getblockbalance`](block-and-tx-query/getblockbalance.md) | 查询区块的账户余额变更 |
| [`/wallet/gettransactioncountbyblocknum`](block-and-tx-query/gettransactioncountbyblocknum.md) | 区块内交易数 |
| [`/wallet/gettransactionbyid`](block-and-tx-query/gettransactionbyid.md) | 按 txid 查询交易 |
| [`/wallet/gettransactioninfobyid`](block-and-tx-query/gettransactioninfobyid.md) | 按 txid 查询交易回执 |
| [`/wallet/gettransactioninfobyblocknum`](block-and-tx-query/gettransactioninfobyblocknum.md) | 按区块查询交易回执 |
| [`/wallet/getpendingsize`](block-and-tx-query/getpendingsize.md) | 待打包交易池大小 |
| [`/wallet/gettransactionfrompending`](block-and-tx-query/gettransactionfrompending.md) | 查询单条 pending 交易 |
| [`/wallet/gettransactionlistfrompending`](block-and-tx-query/gettransactionlistfrompending.md) | 全部 pending 交易 ID |

## 交易构造 / 广播

| 接口 | 说明 |
|---|---|
| [`/wallet/createtransaction`](tx-build-and-broadcast/createtransaction.md) | 构造 TRX 转账交易 |
| [`/wallet/getsignweight`](tx-build-and-broadcast/getsignweight.md) | 查询多签当前权重 |
| [`/wallet/getapprovedlist`](tx-build-and-broadcast/getapprovedlist.md) | 查询多签已签署地址 |
| [`/wallet/broadcasttransaction`](tx-build-and-broadcast/broadcasttransaction.md) | 广播签名后的交易（JSON） |
| [`/wallet/broadcasthex`](tx-build-and-broadcast/broadcasthex.md) | 广播签名后的交易（hex） |

## TRC-10 资产

| 接口 | 说明 |
|---|---|
| [`/wallet/createassetissue`](asset/createassetissue.md) | 发行 TRC-10 通证 |
| [`/wallet/updateasset`](asset/updateasset.md) | 修改 TRC-10 描述/URL/限额 |
| [`/wallet/transferasset`](asset/transferasset.md) | 转账 TRC-10 |
| [`/wallet/participateassetissue`](asset/participateassetissue.md) | 参与 TRC-10 募资 |
| [`/wallet/unfreezeasset`](asset/unfreezeasset.md) | 解锁发行方冻结的 TRC-10 |
| [`/wallet/getassetissuebyid`](asset/getassetissuebyid.md) | 按 id 查询 TRC-10（推荐） |
| [`/wallet/getassetissuebyname`](asset/getassetissuebyname.md) | 按名查询 TRC-10（重名报错） |
| [`/wallet/getassetissuelistbyname`](asset/getassetissuelistbyname.md) | 同名 TRC-10 列表 |
| [`/wallet/getassetissuebyaccount`](asset/getassetissuebyaccount.md) | 账户发行的 TRC-10 |
| [`/wallet/getassetissuelist`](asset/getassetissuelist.md) | 全网 TRC-10 列表 |
| [`/wallet/getpaginatedassetissuelist`](asset/getpaginatedassetissuelist.md) | 分页 TRC-10 列表 |

## 智能合约

| 接口 | 说明 |
|---|---|
| [`/wallet/deploycontract`](smart-contract/deploycontract.md) | 部署合约 |
| [`/wallet/triggersmartcontract`](smart-contract/triggersmartcontract.md) | 触发合约（写） |
| [`/wallet/triggerconstantcontract`](smart-contract/triggerconstantcontract.md) | 只读调用合约 |
| [`/wallet/estimateenergy`](smart-contract/estimateenergy.md) | 预估调用能量消耗 |
| [`/wallet/getcontract`](smart-contract/getcontract.md) | 查询合约元信息 |
| [`/wallet/getcontractinfo`](smart-contract/getcontractinfo.md) | 查询合约完整运行信息 |
| [`/wallet/clearabi`](smart-contract/clearabi.md) | 清空合约 ABI |
| [`/wallet/updatesetting`](smart-contract/updatesetting.md) | 修改用户能量百分比 |
| [`/wallet/updateenergylimit`](smart-contract/updateenergylimit.md) | 修改部署者能量上限 |

## 超级代表 / 治理

| 接口 | 说明 |
|---|---|
| [`/wallet/createwitness`](witness-and-governance/createwitness.md) | 申请成为 SR 候选人 |
| [`/wallet/updatewitness`](witness-and-governance/updatewitness.md) | 修改 SR URL |
| [`/wallet/listwitnesses`](witness-and-governance/listwitnesses.md) | 所有 SR 候选人列表 |
| [`/wallet/getpaginatednowwitnesslist`](witness-and-governance/getpaginatednowwitnesslist.md) | 分页 SR 列表 |
| [`/wallet/votewitnessaccount`](witness-and-governance/votewitnessaccount.md) | 给 SR 投票 |
| [`/wallet/getBrokerage`](witness-and-governance/getBrokerage.md) | SR 当前佣金比例 |
| [`/wallet/updateBrokerage`](witness-and-governance/updateBrokerage.md) | SR 修改佣金 |
| [`/wallet/getReward`](witness-and-governance/getReward.md) | 查询可领取分红 |
| [`/wallet/withdrawbalance`](witness-and-governance/withdrawbalance.md) | 提取出块奖励/分红 |
| [`/wallet/proposalcreate`](witness-and-governance/proposalcreate.md) | 创建链参数提案 |
| [`/wallet/proposalapprove`](witness-and-governance/proposalapprove.md) | SR 对提案投票 |
| [`/wallet/proposaldelete`](witness-and-governance/proposaldelete.md) | 撤销自己的提案 |
| [`/wallet/listproposals`](witness-and-governance/listproposals.md) | 提案列表 |
| [`/wallet/getproposalbyid`](witness-and-governance/getproposalbyid.md) | 按 ID 查询提案 |
| [`/wallet/getpaginatedproposallist`](witness-and-governance/getpaginatedproposallist.md) | 分页提案列表 |
| [`/wallet/getchainparameters`](witness-and-governance/getchainparameters.md) | 链参数当前值 |
| [`/wallet/getnextmaintenancetime`](witness-and-governance/getnextmaintenancetime.md) | 下次维护期时间 |

## 质押 1.0（仅保留解冻与查询）

提案 #70 `UNFREEZE_DELAY_DAYS` 通过后（主网已生效），新的 V1 冻结会被链拒绝；解冻与查询接口保留，用于处理存量仓位。

| 接口 | 说明 |
|---|---|
| [`/wallet/freezebalance`](stake-v1/freezebalance.md) | 冻结 TRX 获取资源（V1，**链已拒绝新请求**） |
| [`/wallet/unfreezebalance`](stake-v1/unfreezebalance.md) | 解冻已到期资源（V1，仍可用于存量解冻） |
| [`/wallet/getdelegatedresource`](stake-v1/getdelegatedresource.md) | 查询代理记录（V1，只读） |
| [`/wallet/getdelegatedresourceaccountindex`](stake-v1/getdelegatedresourceaccountindex.md) | 查询代理对手地址（V1，只读） |

## 质押 2.0

| 接口 | 说明 |
|---|---|
| [`/wallet/freezebalancev2`](stake-v2/freezebalancev2.md) | 冻结 TRX 获取资源 |
| [`/wallet/unfreezebalancev2`](stake-v2/unfreezebalancev2.md) | 发起解冻（14 天等待） |
| [`/wallet/withdrawexpireunfreeze`](stake-v2/withdrawexpireunfreeze.md) | 提取已到期解冻 |
| [`/wallet/cancelallunfreezev2`](stake-v2/cancelallunfreezev2.md) | 取消所有未到期解冻 |
| [`/wallet/delegateresource`](stake-v2/delegateresource.md) | 资源代理给他人 |
| [`/wallet/undelegateresource`](stake-v2/undelegateresource.md) | 撤销资源代理 |
| [`/wallet/getdelegatedresourcev2`](stake-v2/getdelegatedresourcev2.md) | 查询代理记录 |
| [`/wallet/getdelegatedresourceaccountindexv2`](stake-v2/getdelegatedresourceaccountindexv2.md) | 查询代理对手地址 |
| [`/wallet/getcandelegatedmaxsize`](stake-v2/getcandelegatedmaxsize.md) | 当前可代理上限 |
| [`/wallet/getavailableunfreezecount`](stake-v2/getavailableunfreezecount.md) | 剩余可解冻次数 |
| [`/wallet/getcanwithdrawunfreezeamount`](stake-v2/getcanwithdrawunfreezeamount.md) | 指定时间可提取金额 |

## 节点 / 价格 / 工具

| 接口 | 说明 |
|---|---|
| [`/wallet/getnodeinfo`](node-and-tools/getnodeinfo.md) | 节点状态（亦 `/monitor/getnodeinfo`） |
| [`/wallet/listnodes`](node-and-tools/listnodes.md) | 已知对等节点（亦 `/net/listnodes`） |
| [`/wallet/getenergyprices`](node-and-tools/getenergyprices.md) | 能量历史单价 |
| [`/wallet/getbandwidthprices`](node-and-tools/getbandwidthprices.md) | 带宽历史单价 |
| [`/wallet/getburntrx`](node-and-tools/getburntrx.md) | 累计销毁 TRX |
