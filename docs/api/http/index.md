# java-tron HTTP API 文档

本目录收录 `framework/src/main/java/org/tron/core/services/http/` 下 FullNode HTTP 接口的请求/响应文档。每个接口一个 markdown 文件，命名规则同 URL 末段（例如 `/wallet/getnodeinfo` → `getnodeinfo.md`）。

未收录接口主要包括以下三个类别：

- Exchange（DEX）类接口
- Market（订单簿）类接口
- Shielded（匿名交易）类接口

## 通用约定

- **Method**：除少量纯查询接口同时支持 `GET`，多数 POST 接口仅接受 `POST`，请求体为 JSON。
- **`visible`**：`true` 时地址使用 base58check 字符串形式，URL/描述等文本字段使用 UTF-8 字符串；`false`（默认）时使用 hex 字符串。
- **构造类接口**返回未签名的 `protocol.Transaction`，需调用方本地签名后通过 [`/wallet/broadcasttransaction`](tx-build-and-broadcast/broadcasttransaction.md) 或 [`/wallet/broadcasthex`](tx-build-and-broadcast/broadcasthex.md) 广播。
- **`Permission_id`**：交易构造接口可选；用于多签账户指定使用哪个 `Permission`。字段名区分大小写。
- **金额单位**：除 TRC-10 数量按发行精度外，其他金额一律为 sun（1 TRX = 1e6 sun）。
- **`int64_as_string`**：GET 请求可在 URL 查询参数中添加 `int64_as_string=true`。启用后，protobuf JSON 响应中的 int64 / uint64 字段会序列化为 JSON 字符串，避免 JavaScript 等客户端出现精度损失。该参数只对 GET 请求生效，不影响 POST 请求体。
- **请求体大小**：HTTP 请求体受 `config.conf` 中 `node.http.maxMessageSize` 限制（默认 `4194304`，约 4 MiB；`0` 表示拒绝所有非空 body）。JSON-RPC 有独立的 `node.jsonrpc.maxMessageSize`。
- **限流**：HTTP 单接口限流在 `rate.limiter.http` 中配置。全局开关 `rate.limiter.apiNonBlocking` 控制超限行为：`true` 表示立即拒绝，`false` 表示排队并阻塞调用方直到获得 permit。

!!! warning "XSS 安全提示"

    尽管 HTTP API 通过将 `Content-Type` 设置为 `application/json` 降低了浏览器直接将响应解析为 HTML 的风险，但这并不等于完全避免 XSS。部分接口对入参并无严格校验，响应中可能回显用户可控内容（尤其当 `visible=true` 时，地址、备注等字段可能以 UTF-8 字符串原样返回）。在将 API 返回的数据渲染到页面之前，应根据输出上下文进行安全处理。

    正确做法是根据输出位置选择合适的编码方式：在 HTML 文本上下文中使用 HTML 实体编码（如将 `<` 转成 `&lt;`、`>` 转成 `&gt;`、`"` 转成 `&quot;`），或直接使用前端框架自带的默认输出转义机制（如 React JSX、Vue 模板的默认转义）。如果数据被放入 URL 参数中，才应使用 `encodeURIComponent()` 这类 URL 编码方法。注意 `encodeURIComponent()` / `escape()` 属于 URL 编码或旧式编码方式，不能替代 HTML 上下文中的输出转义。

    更多防护指引请参考 [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)。

## 异常响应

HTTP 状态码在**绝大多数情况下都是 200**（业务错误也通过响应体表达），客户端必须解析响应体判断成败。已知例外：

- 接口被节点配置 `disabledApiList` 显式禁用时，由 `HttpApiAccessFilter` 直接返回 **HTTP 404**，响应体 `{"Error": "this API is unavailable due to config"}`。
- 请求体超过 `node.http.maxMessageSize` 时，共享 HTTP `SizeLimitHandler` 可能会在目标 servlet 处理请求前直接返回 **HTTP 413**（`Payload Too Large`）。如果请求已经进入 servlet，并由 servlet 内部的 `Util.checkBodySize` 检查到 body 超限，则接口会按自身的异常响应格式返回；部分接口仍可能是 **HTTP 200** 加错误响应体。
- 节点以 lite fullnode 模式启动且未开启 `openHistoryQueryWhenLiteFN` 时，由 `LiteFnQueryHttpFilter` 对约 24 个历史查询接口（`getblockbynum` / `gettransactionbyid` / `gettransactioninfobyid` / `gettransactioninfobyblocknum` / `getblockbyid` / `getblockbylatestnum` / `getblockbylimitnext` / `gettransactioncountbyblocknum` 等）返回 **HTTP 200**，但响应体是裸字符串 `this API is closed because this node is a lite fullnode`（**非 JSON**），客户端朴素 `JSON.parse` 会抛错，需先按字符串前缀识别。
- 其它由 servlet 容器/反向代理产生的网络层错误（502、504、连接拒绝等）不在本文档范围。

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
