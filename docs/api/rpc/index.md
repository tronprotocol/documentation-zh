# java-tron gRPC API

java-tron 节点对外提供 gRPC 接口。本目录按业务分类列出 82 个常用 gRPC 方法的简要文档。

## 服务与默认端口

| 服务 | 默认端口 | 说明 | 源码 |
|---|---|---|---|
| `protocol.Wallet` | `50051` | FullNode 全功能服务（含写交易） | `framework/src/main/java/org/tron/core/services/RpcApiService.java` |
| `protocol.WalletSolidity` | `50061` | 仅返回已固化数据，只读 | `framework/src/main/java/org/tron/core/services/interfaceOnSolidity/RpcApiServiceOnSolidity.java` |

端口可通过节点配置项 `node.rpc.port` / `node.rpc.solidityPort` 覆盖（参见 `framework/src/main/resources/config.conf`）。

proto 定义位于 `protocol/src/main/protos/api/api.proto`。

## 调用方式

gRPC 不使用 URL 路径区分 `wallet` 与 `walletsolidity` —— 二者是两个独立的服务桩，连接到不同端口即可：

```text
# Wallet
grpc://<host>:50051   protocol.Wallet/<Method>

# WalletSolidity（只读）
grpc://<host>:50061   protocol.WalletSolidity/<Method>
```

每个方法文档包含：

- 方法名（一级标题，PascalCase，与 proto 完全一致）
- 功能描述
- 服务支持情况（`Wallet` / `WalletSolidity` / 二者皆支持）
- 对应 protobuf 签名

## 账户

| 方法 | 描述 |
|---|---|
| [GetAccount](account/GetAccount.md) | 按地址查询账户 |
| [GetAccountBalance](account/GetAccountBalance.md) | 查询账户在指定区块的余额 |
| [GetAccountNet](account/GetAccountNet.md) | 查询账户带宽资源 |
| [GetAccountResource](account/GetAccountResource.md) | 查询账户带宽+能量+TronPower |
| [CreateAccount2](account/CreateAccount2.md) | 链上创建账户（需消耗 1 TRX） |
| [UpdateAccount2](account/UpdateAccount2.md) | 修改账户名 |
| [AccountPermissionUpdate](account/AccountPermissionUpdate.md) | 配置多签权限 |

## 区块 / 交易查询

| 方法 | 描述 |
|---|---|
| [GetNowBlock2](block-and-tx-query/GetNowBlock2.md) | 当前最新区块 |
| [GetBlock](block-and-tx-query/GetBlock.md) | 通用区块查询（按 num/hash） |
| [GetBlockByNum2](block-and-tx-query/GetBlockByNum2.md) | 按高度查询区块 |
| [GetBlockById](block-and-tx-query/GetBlockById.md) | 按 hash 查询区块 |
| [GetBlockByLimitNext2](block-and-tx-query/GetBlockByLimitNext2.md) | 按区间查询区块 |
| [GetBlockByLatestNum2](block-and-tx-query/GetBlockByLatestNum2.md) | 查询最近 N 个区块 |
| [GetBlockBalanceTrace](block-and-tx-query/GetBlockBalanceTrace.md) | 查询区块的账户余额变更 |
| [GetTransactionCountByBlockNum](block-and-tx-query/GetTransactionCountByBlockNum.md) | 区块内交易数 |
| [GetTransactionById](block-and-tx-query/GetTransactionById.md) | 按 txid 查询交易 |
| [GetTransactionInfoById](block-and-tx-query/GetTransactionInfoById.md) | 按 txid 查询交易回执 |
| [GetTransactionInfoByBlockNum](block-and-tx-query/GetTransactionInfoByBlockNum.md) | 按区块查询交易回执 |
| [GetPendingSize](block-and-tx-query/GetPendingSize.md) | 待打包交易池大小 |
| [GetTransactionFromPending](block-and-tx-query/GetTransactionFromPending.md) | 查询单条 pending 交易 |
| [GetTransactionListFromPending](block-and-tx-query/GetTransactionListFromPending.md) | 全部 pending 交易 ID |

## 交易构造 / 广播

| 方法 | 描述 |
|---|---|
| [CreateTransaction2](tx-build-and-broadcast/CreateTransaction2.md) | 构造 TRX 转账交易 |
| [GetTransactionSignWeight](tx-build-and-broadcast/GetTransactionSignWeight.md) | 查询多签当前权重 |
| [GetTransactionApprovedList](tx-build-and-broadcast/GetTransactionApprovedList.md) | 查询多签已签署地址 |
| [BroadcastTransaction](tx-build-and-broadcast/BroadcastTransaction.md) | 广播签名后的交易（JSON） |

## TRC10 资产

| 方法 | 描述 |
|---|---|
| [CreateAssetIssue2](asset/CreateAssetIssue2.md) | 发行 TRC10 通证 |
| [UpdateAsset2](asset/UpdateAsset2.md) | 修改 TRC10 描述/URL/限额 |
| [TransferAsset2](asset/TransferAsset2.md) | 转账 TRC10 |
| [ParticipateAssetIssue2](asset/ParticipateAssetIssue2.md) | 参与 TRC10 募资 |
| [UnfreezeAsset2](asset/UnfreezeAsset2.md) | 解锁发行方冻结的 TRC10 |
| [GetAssetIssueById](asset/GetAssetIssueById.md) | 按 id 查询 TRC10（推荐） |
| [GetAssetIssueByName](asset/GetAssetIssueByName.md) | 按名查询 TRC10（重名报错） |
| [GetAssetIssueListByName](asset/GetAssetIssueListByName.md) | 同名 TRC10 列表 |
| [GetAssetIssueByAccount](asset/GetAssetIssueByAccount.md) | 账户发行的 TRC10 |
| [GetAssetIssueList](asset/GetAssetIssueList.md) | 全网 TRC10 列表 |
| [GetPaginatedAssetIssueList](asset/GetPaginatedAssetIssueList.md) | 分页 TRC10 列表 |

## 智能合约

| 方法 | 描述 |
|---|---|
| [DeployContract](smart-contract/DeployContract.md) | 部署合约 |
| [TriggerContract](smart-contract/TriggerContract.md) | 触发合约（写） |
| [TriggerConstantContract](smart-contract/TriggerConstantContract.md) | 只读调用合约 |
| [EstimateEnergy](smart-contract/EstimateEnergy.md) | 预估调用能量消耗 |
| [GetContract](smart-contract/GetContract.md) | 查询合约元信息 |
| [GetContractInfo](smart-contract/GetContractInfo.md) | 查询合约完整运行信息 |
| [ClearContractABI](smart-contract/ClearContractABI.md) | 清空合约 ABI |
| [UpdateSetting](smart-contract/UpdateSetting.md) | 修改用户能量百分比 |
| [UpdateEnergyLimit](smart-contract/UpdateEnergyLimit.md) | 修改部署者能量上限 |

## 见证人 / 治理

| 方法 | 描述 |
|---|---|
| [CreateWitness2](witness-and-governance/CreateWitness2.md) | 申请成为 SR 候选人 |
| [UpdateWitness2](witness-and-governance/UpdateWitness2.md) | 修改 SR URL |
| [ListWitnesses](witness-and-governance/ListWitnesses.md) | 所有 SR 候选人列表 |
| [GetPaginatedNowWitnessList](witness-and-governance/GetPaginatedNowWitnessList.md) | 分页 SR 列表 |
| [VoteWitnessAccount2](witness-and-governance/VoteWitnessAccount2.md) | 给 SR 投票 |
| [GetBrokerageInfo](witness-and-governance/GetBrokerageInfo.md) | SR 当前佣金比例 |
| [UpdateBrokerage](witness-and-governance/UpdateBrokerage.md) | SR 修改佣金 |
| [GetRewardInfo](witness-and-governance/GetRewardInfo.md) | 查询可领取分红 |
| [WithdrawBalance2](witness-and-governance/WithdrawBalance2.md) | 提取出块奖励/分红 |
| [ProposalCreate](witness-and-governance/ProposalCreate.md) | 创建链参数提案 |
| [ProposalApprove](witness-and-governance/ProposalApprove.md) | SR 对提案投票 |
| [ProposalDelete](witness-and-governance/ProposalDelete.md) | 撤销自己的提案 |
| [ListProposals](witness-and-governance/ListProposals.md) | 提案列表 |
| [GetProposalById](witness-and-governance/GetProposalById.md) | 按 ID 查询提案 |
| [GetPaginatedProposalList](witness-and-governance/GetPaginatedProposalList.md) | 分页提案列表 |
| [GetChainParameters](witness-and-governance/GetChainParameters.md) | 链参数当前值 |
| [GetNextMaintenanceTime](witness-and-governance/GetNextMaintenanceTime.md) | 下次维护期时间 |

## 质押 1.0（仅保留解冻与查询）

提案 #70 `UNFREEZE_DELAY_DAYS` 通过后（主网已生效），新的 V1 冻结会被链拒绝；解冻与查询方法保留，用于处理存量仓位。

> 文件名末尾的 `2`（如 `FreezeBalance2`）是 proto 历史命名后缀（返回 `TransactionExtention` 的 V1 方法），与质押 2.0 的 `FreezeBalanceV2` 不是同一个方法。

| 方法 | 描述 |
|---|---|
| [FreezeBalance2](stake-v1/FreezeBalance2.md) | 冻结 TRX 获取资源（V1，**链已拒绝新请求**） |
| [UnfreezeBalance2](stake-v1/UnfreezeBalance2.md) | 解冻已到期资源（V1，仍可用于存量解冻） |
| [GetDelegatedResource](stake-v1/GetDelegatedResource.md) | 查询代理记录（V1，只读） |
| [GetDelegatedResourceAccountIndex](stake-v1/GetDelegatedResourceAccountIndex.md) | 查询代理对手地址（V1，只读） |

## 质押 2.0

| 方法 | 描述 |
|---|---|
| [FreezeBalanceV2](stake-v2/FreezeBalanceV2.md) | 冻结 TRX 获取资源 |
| [UnfreezeBalanceV2](stake-v2/UnfreezeBalanceV2.md) | 发起解冻（14 天等待） |
| [WithdrawExpireUnfreeze](stake-v2/WithdrawExpireUnfreeze.md) | 提取已到期解冻 |
| [CancelAllUnfreezeV2](stake-v2/CancelAllUnfreezeV2.md) | 取消所有未到期解冻 |
| [DelegateResource](stake-v2/DelegateResource.md) | 资源代理给他人 |
| [UnDelegateResource](stake-v2/UnDelegateResource.md) | 撤销资源代理 |
| [GetDelegatedResourceV2](stake-v2/GetDelegatedResourceV2.md) | 查询代理记录 |
| [GetDelegatedResourceAccountIndexV2](stake-v2/GetDelegatedResourceAccountIndexV2.md) | 查询代理对手地址 |
| [GetCanDelegatedMaxSize](stake-v2/GetCanDelegatedMaxSize.md) | 当前可代理上限 |
| [GetAvailableUnfreezeCount](stake-v2/GetAvailableUnfreezeCount.md) | 剩余可解冻次数 |
| [GetCanWithdrawUnfreezeAmount](stake-v2/GetCanWithdrawUnfreezeAmount.md) | 指定时间可提取金额 |

## 节点 / 价格 / 工具

| 方法 | 描述 |
|---|---|
| [GetNodeInfo](node-and-tools/GetNodeInfo.md) | 节点状态 |
| [ListNodes](node-and-tools/ListNodes.md) | 已知对等节点 |
| [GetEnergyPrices](node-and-tools/GetEnergyPrices.md) | 能量历史单价 |
| [GetBandwidthPrices](node-and-tools/GetBandwidthPrices.md) | 带宽历史单价 |
| [GetBurnTrx](node-and-tools/GetBurnTrx.md) | 累计销毁 TRX |
