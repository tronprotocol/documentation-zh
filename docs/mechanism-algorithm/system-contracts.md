# 系统合约


TRON 网络支持多种不同类型的交易，比如 TRX 转账交易、TRC-10 转账交易、创建智能合约交易、触发智能合约交易、质押 TRX 交易等等。创建不同类型的交易，需要调用不同的 API 接口，例如部署合约交易的类型是 `CreateSmartContract`，需要调用 `wallet/deploycontract` API 来创建交易；质押 TRX 获取资源交易的类型是 `FreezeBalanceV2Contract`，需要调用 `wallet/freezebalancev2` API 来创建交易，我们将这些不同的交易类型的实现统称为系统合约，下面为系统合约类型及其包含的内容：

## ContractType 总览

每个系统合约都通过 [`Tron.proto`](https://github.com/tronprotocol/java-tron/blob/master/protocol/src/main/protos/core/Tron.proto) 中定义的 `ContractType` 枚举值进行标识。下表列出了每个 `ContractType` 对应的 Proto Message、Actuator、当前状态以及触发的业务。

| # | ContractType | Proto Message(消息名) | Actuator(执行器) | 状态 | 触发的业务 |
|---|---|---|---|---|---|
| 0 | AccountCreateContract | AccountContract.AccountCreateContract | CreateAccountActuator | ✅ 启用 | 创建一个链上账户 |
| 1 | TransferContract | BalanceContract.TransferContract | TransferActuator | ✅ 启用 | TRX 转账 |
| 2 | TransferAssetContract | AssetIssueContractOuterClass.TransferAssetContract | TransferAssetActuator | ✅ 启用 | TRC-10 token 转账 |
| 3 | VoteAssetContract |  |  | 🚫 禁用(未实现Actuator)  |  |
| 4 | VoteWitnessContract | WitnessContract.VoteWitnessContract | VoteWitnessActuator | ✅ 启用 | 用账户的 TronPower 为超级代表投票,刷新投票记录(下次 maintenance 生效) |
| 5 | WitnessCreateContract | WitnessContract.WitnessCreateContract | WitnessCreateActuator | ✅ 启用 | 申请成为超级代表 |
| 6 | AssetIssueContract | AssetIssueContractOuterClass.AssetIssueContract | AssetIssueActuator | ✅ 启用 | 发行 TRC-10 token,按 ICO 规则冻结募集期余额 |
| 8 | WitnessUpdateContract | WitnessContract.WitnessUpdateContract | WitnessUpdateActuator | ✅ 启用 | 更新超级代表的官网 URL |
| 9 | ParticipateAssetIssueContract | AssetIssueContractOuterClass.ParticipateAssetIssueContract | ParticipateAssetIssueActuator | ✅ 启用 | 在 ICO 期间用 TRX 参与 TRC-10 token 发行 |
| 10 | AccountUpdateContract | AccountContract.AccountUpdateContract | UpdateAccountActuator | ✅ 启用 | 修改账户名(受 AllowUpdateAccountName 约束) |
| 11 | FreezeBalanceContract | BalanceContract.FreezeBalanceContract | FreezeBalanceActuator | 🚫 禁用(`supportUnfreezeDelay` 启用后链拒绝) | Stake 1.0:质押 TRX 换取 Bandwidth/Energy,并可代理给他人 |
| 12 | UnfreezeBalanceContract | BalanceContract.UnfreezeBalanceContract | UnfreezeBalanceActuator | ✅ 启用 | Stake 1.0:到期后解质押 TRX,释放对应资源、清除得票 |
| 13 | WithdrawBalanceContract | BalanceContract.WithdrawBalanceContract | WithdrawBalanceActuator | ✅ 启用 | 领取 SR 出块 / 投票奖励到余额 |
| 14 | UnfreezeAssetContract | AssetIssueContractOuterClass.UnfreezeAssetContract | UnfreezeAssetActuator | ✅ 启用 | 解冻 ICO 时冻结的 TRC-10 token 份额 |
| 15 | UpdateAssetContract | AssetIssueContractOuterClass.UpdateAssetContract | UpdateAssetActuator | ✅ 启用 | 更新 TRC-10 token 的 description / url / 免费带宽配额 |
| 16 | ProposalCreateContract | ProposalContract.ProposalCreateContract | ProposalCreateActuator | ✅ 启用 | 发起链上参数提案,写入 ProposalStore 等待投票 |
| 17 | ProposalApproveContract | ProposalContract.ProposalApproveContract | ProposalApproveActuator | ✅ 启用 | 对提案投赞成/取消票 |
| 18 | ProposalDeleteContract | ProposalContract.ProposalDeleteContract | ProposalDeleteActuator | ✅ 启用 | 撤回创建的提案 |
| 19 | SetAccountIdContract | AccountContract.SetAccountIdContract | SetAccountIdActuator | ✅ 启用 | 为账户设置唯一 account_id(仅可设置一次) |
| 20 | CustomContract  |  |  | 🚫 禁用(未实现Actuator)  |  |
| 30 | CreateSmartContract | SmartContractOuterClass.CreateSmartContract | VMActuator | ✅ 启用 | 部署智能合约 |
| 31 | TriggerSmartContract | SmartContractOuterClass.TriggerSmartContract | VMActuator | ✅ 启用 | 调用智能合约 |
| 32 | GetContract |  |  | 🚫 禁用(未实现Actuator)  |  |
| 33 | UpdateSettingContract | SmartContractOuterClass.UpdateSettingContract | UpdateSettingContractActuator | ✅ 启用 | 修改合约的 consume_user_resource_percent(用户承担能量比例) |
| 41 | ExchangeCreateContract | ExchangeContract.ExchangeCreateContract | ExchangeCreateActuator | ✅ 启用 | 创建 Bancor 交易对, 为两种资产初始注入流动性 |
| 42 | ExchangeInjectContract | ExchangeContract.ExchangeInjectContract | ExchangeInjectActuator | ✅ 启用 | 向已有交易对继续注入流动性, 按 Bancor 算法扣减双方资产 |
| 43 | ExchangeWithdrawContract | ExchangeContract.ExchangeWithdrawContract | ExchangeWithdrawActuator | ✅ 启用 | 按比例撤回交易对中双方资产 |
| 44 | ExchangeTransactionContract | ExchangeContract.ExchangeTransactionContract | ExchangeTransactionActuator | 🚫 禁用 | 通过 Bancor 交易对进行资产兑换 |
| 45 | UpdateEnergyLimitContract | SmartContractOuterClass.UpdateEnergyLimitContract | UpdateEnergyLimitContractActuator | ✅ 启用 | 更新合约的 origin_energy_limit(每次合约调用愿意承担的能量消耗上限) |
| 46 | AccountPermissionUpdateContract | AccountContract.AccountPermissionUpdateContract | AccountPermissionUpdateActuator | ✅ 启用 | 更新账户权限:owner/witness/active |
| 48 | ClearABIContract | SmartContractOuterClass.ClearABIContract | ClearABIContractActuator | ✅ 启用 | 清空合约 ABI |
| 49 | UpdateBrokerageContract | StorageContract.UpdateBrokerageContract | UpdateBrokerageActuator | ✅ 启用 | 调整对投票者的分成比例(0-100%) |
| 51 | ShieldedTransferContract | ShieldContract.ShieldedTransferContract | ShieldedTransferActuator | 🚫 禁用(`getAllowShieldedTransaction` 未开启) | ZK-SNARK 匿名转账(透明 in + 匿名 spend/receive + 透明 out) |
| 52 | MarketSellAssetContract | MarketContract.MarketSellAssetContract | MarketSellAssetActuator | 🚫 禁用(`getAllowMarketTransaction` 未开启) | 内置订单簿挂限价卖单(sell / buy 两种资产 + 价格) |
| 53 | MarketCancelOrderContract | MarketContract.MarketCancelOrderContract | MarketCancelOrderActuator | 🚫 禁用(`getAllowMarketTransaction` 未开启) | 撤销自己挂出的未成交订单,退回剩余资产 |
| 54 | FreezeBalanceV2Contract | BalanceContract.FreezeBalanceV2Contract | FreezeBalanceV2Actuator | ✅ 启用 | Stake 2.0:冻结 TRX 得到 Bandwidth/Energy, 资源与 TronPower 分离 |
| 55 | UnfreezeBalanceV2Contract | BalanceContract.UnfreezeBalanceV2Contract | UnfreezeBalanceV2Actuator | ✅ 启用 | Stake 2.0:发起解质押,进入解质押等待期 |
| 56 | WithdrawExpireUnfreezeContract | BalanceContract.WithdrawExpireUnfreezeContract | WithdrawExpireUnfreezeActuator | ✅ 启用 | 提取已过等待期的解质押 TRX 到账户余额 |
| 57 | DelegateResourceContract | BalanceContract.DelegateResourceContract | DelegateResourceActuator | ✅ 启用 | Stake 2.0:把自己已质押的 Bandwidth/Energy 代理给其他地址(可设锁定期) |
| 58 | UnDelegateResourceContract | BalanceContract.UnDelegateResourceContract | UnDelegateResourceActuator | ✅ 启用 | Stake 2.0:从他人处回收先前代理的资源 |
| 59 | CancelAllUnfreezeV2Contract | BalanceContract.CancelAllUnfreezeV2Contract | CancelAllUnfreezeV2Actuator | ✅ 启用 | 一次性取消账户所有处于等待期的 V2 解质押,剩余份额重新质押 |

下面分章节列出每个合约的 protobuf 消息定义和字段说明。

## 创建账户 AccountCreateContract

```protobuf
    message AccountCreateContract {
       bytes owner_address = 1;
       bytes account_address = 2;
       AccountType type = 3;
    }
```

* `owner_address`：创建账户的发起账户地址。
* `account_address`： 将要创建的账户地址。
* `type`：账户类型。0代表普通账户，1代表创世块中初始账号，2代表智能合约账户。

## TRX转账 TransferContract

```protobuf
      message TransferContract {
       bytes owner_address = 1;
       bytes to_address = 2;
       int64 amount = 3;
     }
```

* `owner_address`：TRX 转出账户地址。
* `to_address`： 目标账户地址。
* `amount`：转账金额，单位为 sun。


## TRC-10 token 转账 TransferAssetContract

```protobuf
      message TransferAssetContract {
       bytes asset_name = 1;
       bytes owner_address = 2;
       bytes to_address = 3;
       int64 amount = 4;
     }
```

* `asset_name`：TRC-10 的 id。
* `owner_address`：TRC-10 token 转出账户地址。
* `to_address`： 目标账户地址。
* `amount`：转账 token 的数量。

## 投票超级代表  VoteWitnessContract

```protobuf
      message VoteWitnessContract {
       message Vote {
         bytes vote_address = 1;
         int64 vote_count = 2;
       }
       bytes owner_address = 1;
       repeated Vote votes = 2;
       bool support = 3;
     }
```

* `owner_address`：为超级代表投票的账户地址。
* `vote_address`：超级代表的地址。
* `vote_count`：投给超级代表的票数。
* `support`：是否支持，这里应该是恒为true，暂未使用该参数。

## 创建超级代表 WitnessCreateContract

```protobuf
      message WitnessCreateContract {
       bytes owner_address = 1;
       bytes url = 2;
     }
```

* `owner_address`：申请成为超级代表的账户地址。
* `url`：超级代表的网址。

## 发行 TRC-10 token AssetIssueContract

```protobuf
    message AssetIssueContract {
       message FrozenSupply {
         int64 frozen_amount = 1;
         int64 frozen_days = 2;
       }
       bytes owner_address = 1;
       bytes name = 2;
       bytes abbr = 3;
       int64 total_supply = 4;
       repeated FrozenSupply frozen_supply = 5;
       int32 trx_num = 6;
       int32 precision = 7;
       int32 num = 8;
       int64 start_time = 9;
       int64 end_time = 10;
       int64 order = 11; // useless
       int32 vote_score = 16;
       bytes description = 20;
       bytes url = 21;
       int64 free_asset_net_limit = 22;
       int64 public_free_asset_net_limit = 23;
       int64 public_free_asset_net_usage = 24;
       int64 public_latest_free_net_time = 25;
       string id = 41;
     }
```

* `owner_address`：发行 TRC-10 token 的账户地址。
* `name`：发行 token 的名称。
* `abbr`：token 缩写。
* `total_supply`：发行总的 token 数量。
* `frozen_supply`：质押 token 的数量和质押时间列表。
* `trx_num`：对应 TRX 数量。
* `num`：对应的自定义资产数目。
* `start_time`：ICO 开始时间。
* `end_time`：ICO 结束时间。
* `order`：已废弃。
* `vote_score`：已废弃。
* `description`：token 的描述。
* `url`：token 的 URL 地址链接。
* `free_asset_net_limit`：每个账户可以使用的免费带宽（转移该资产时使用）。
* `public_free_asset_net_limit`：所有账户可以使用的免费带宽（转移该资产时使用）。
* `public_free_asset_net_usage`：所有账户使用免费带宽（转移该资产时使用）。
* `public_latest_free_net_time`：最近一次转移该 token 使用免费带宽的时间。
* `id`：token 的唯一 ID，由系统在发行时按顺序生成（从 1000001 起递增）。

## 更新超级代表 URL WitnessUpdateContract

```protobuf
      message WitnessUpdateContract {
       bytes owner_address = 1;
       bytes update_url = 12;
     }
```

* `owner_address`：更新 URL 的超级代表地址。
* `update_url`：超级代表网站的 URL。

## 参与 TRC-10 token 发行 ParticipateAssetIssueContract

```protobuf
      message ParticipateAssetIssueContract {
       bytes owner_address = 1;
       bytes to_address = 2;
       bytes asset_name = 3;
       int64 amount = 4;
     }
```

* `owner_address`：参与 TRC-10 token 发行的账户地址。
* `to_address`：发行 token 所有者地址。
* `asset_name`：发行 token 的 ID。
* `amount`：购买发行 token 使用 TRX 的数量，单位是 sun。

## 更新账户 AccountUpdateContract

```protobuf
      // Update account name. Account name is unique now.
     message AccountUpdateContract {
       bytes account_name = 1;
       bytes owner_address = 2;
     }
```

* `owner_address`：待更新账户的地址。
* `account_name`： 账户名称。

## 解质押 Stake 1.0 阶段质押的资产 UnfreezeBalanceContract

```protobuf
      message UnfreezeBalanceContract {
       bytes owner_address = 1;
       ResourceCode resource = 10;
       bytes receiver_address = 15;
     }
```

* `owner_address`：解质押 TRX 的账户地址。
* `resource`： 解质押资源的类型。
* `receiver_address`：接收资源的账户。

## 提取奖励 WithdrawBalanceContract

```protobuf
      message WithdrawBalanceContract {
       bytes owner_address = 1;
     }
```

* `owner_address`：提取奖励的账户地址。

## 解锁发行的 token UnfreezeAssetContract

```protobuf
      message UnfreezeAssetContract {
       bytes owner_address = 1;
     }
```

* `owner_address`：token 发行方账户地址。

## 更新 token 参数 UpdateAssetContract

```protobuf
      message UpdateAssetContract {
       bytes owner_address = 1;
       bytes description = 2;
       bytes url = 3;
       int64 new_limit = 4;
       int64 new_public_limit = 5;
     }
```

* `owner_address`：token 发行方账户地址。
* `description`： token 的描述。
* `url`：token 的网址。
* `new_limit`：每个调用者可以消耗 Bandwidth point 的限制。
* `new_public_limit`：所有调用者可以消耗 Bandwidth points 的限制。

## 创建提案  ProposalCreateContract

```protobuf
      message ProposalCreateContract {
       bytes owner_address = 1;
       map<int64, int64> parameters = 2;
     }
```

* `owner_address`：创建提案的账户地址。
* `parameters`： 提案。

## 赞成提案 ProposalApproveContract

```protobuf
      message ProposalApproveContract {
       bytes owner_address = 1;
       int64 proposal_id = 2;
       bool is_add_approval = 3; // add or remove approval
     }
```

* `owner_address`：赞成提案的账户地址。
* `proposal_id`： 提案的Id。
* `is_add_approval`：是否赞成提案。

## 删除提案 ProposalDeleteContract

```protobuf
     message ProposalDeleteContract {
       bytes owner_address = 1;
       int64 proposal_id = 2;
     }
```

* `owner_address`：删除提案的账户地址。
* `proposal_id`： 提案ID。

## 设置账户ID SetAccountIdContract

```protobuf
      // Set account id if the account has no id. Account id is unique and case insensitive.
     message SetAccountIdContract {
       bytes account_id = 1;
       bytes owner_address = 2;
     }
```

* `owner_address`：设置 account id 的账户地址。
* `account_id`： 账户Id。

## 创建智能合约 CreateSmartContract

```protobuf
     message CreateSmartContract {
       bytes owner_address = 1;
       SmartContract new_contract = 2;
       int64 call_token_value = 3;
       int64 token_id = 4;
     }
```

* `owner_address`：部署智能合约的账户地址。
* `new_contract`： 智能合约。
* `call_token_value`：转入 TRC-10 数目。
* `token_id`：转入 TRC-10 的 id。

## 触发智能合约 TriggerSmartContract

```protobuf
      message TriggerSmartContract {
       bytes owner_address = 1;
       bytes contract_address = 2;
       int64 call_value = 3;
       bytes data = 4;
       int64 call_token_value = 5;
       int64 token_id = 6;
     }
```

* `owner_address`：调用智能合约的账户地址。
* `contract_address`： 合约地址。
* `call_value`：传入合约的TRX的值。
* `data`：操作参数。
* `call_token_value`：转入 TRC-10 数目。
* `token_id`：转入 TRC-10 的 id。

## 更新合约 UpdateSettingContract

```protobuf
      message UpdateSettingContract {
       bytes owner_address = 1;
       bytes contract_address = 2;
       int64 consume_user_resource_percent = 3;
     }
```

* `owner_address`：智能合约部署者账户地址。
* `contract_address`： 合约地址。
* `consume_user_resource_percent`：将要更新的账户消耗资源的百分比。

## 创建交易对 ExchangeCreateContract

```protobuf
      message ExchangeCreateContract {
       bytes owner_address = 1;
       bytes first_token_id = 2;
       int64 first_token_balance = 3;
       bytes second_token_id = 4;
       int64 second_token_balance = 5;
     }
```

* `owner_address`：创建交易对的账户地址。
* `first_token_id`：第 1 种 token 的 id。
* `first_token_balance`：第 1 种 token 的 balance。
* `second_token_id`：第 2 种 token 的 id。
* `second_token_balance`：第 2 种 token 的 balance。

## 向交易对注入流动性 ExchangeInjectContract

```protobuf
      message ExchangeInjectContract {
       bytes owner_address = 1;
       int64 exchange_id = 2;
       bytes token_id = 3;
       int64 quant = 4;
     }
```

* `owner_address`：向交易对注入流动性的账户地址（必须为该交易对的创建者）。
* `exchange_id`： 交易对的id。
* `token_id`：要注资的 token 的 id。
* `quant`：要注资的 token 的数量。

## 从交易对撤出流动性 ExchangeWithdrawContract

```protobuf
      message ExchangeWithdrawContract {
       bytes owner_address = 1;
       int64 exchange_id = 2;
       bytes token_id = 3;
       int64 quant = 4;
     }
```

* `owner_address`：从交易对撤出流动性的账户地址（必须为该交易对的创建者）。
* `exchange_id`： 交易对的id。
* `token_id`：要撤资的 token 的 id。
* `quant`：要撤资的 token 的数量。

## 调整能量上限 UpdateEnergyLimitContract

```protobuf
     message UpdateEnergyLimitContract {
       bytes owner_address = 1;
       bytes contract_address = 2;
       int64 origin_energy_limit = 3;
     }
```

* `owner_address`：智能合约部署者账户地址。
* `contract_address`：需要调整的合约地址。
* `origin_energy_limit`：调整后智能合约部署者提供的能量上限值。

## 更新账户权限 AccountPermissionUpdateContract

```protobuf
    message AccountPermissionUpdateContract {
      bytes owner_address = 1;
      Permission owner = 2;             //Empty is invalidate
      Permission witness = 3;           //Can be empty
      repeated Permission actives = 4;  //Empty is invalidate
    }
```

* `owner_address`：待更新权限的账户地址。
* `owner`：账户的 owner 权限，不能为空。
* `witness`：witness 权限。超级代表必填；非超级代表必须为空。
* `actives`：active 权限列表，不能为空，且最多 8 个。

更多说明请参见[账户权限管理](./multi-signatures.md)。

## 清除合约 ABI ClearABIContract

```protobuf
     message ClearABIContract {
       bytes owner_address = 1;
       bytes contract_address = 2;
     }
```

* `owner_address`：智能合约部署者账户地址。
* `contract_address`：需要清除 ABI 的合约。

## 更新分成比例 UpdateBrokerageContract

```protobuf
     message UpdateBrokerageContract {
       bytes owner_address = 1;
       int32 brokerage = 2;
     }
```

* `owner_address`：调整分成比例的超级代表地址。
* `brokerage`：分成比例，从 0 到 100，1 代表 1%。

## 质押资产 FreezeBalanceV2Contract

```protobuf
     message FreezeBalanceV2Contract {
      bytes owner_address = 1;
      int64 frozen_balance = 2;
      ResourceCode resource = 3;
      }
```

* `owner_address`：质押 TRX 的账户地址。
* `frozen_balance`：质押资产的数量。
* `resource`：质押 TRX 获取资源的类型。

## 解质押资产 UnfreezeBalanceV2Contract

```protobuf
      message UnfreezeBalanceV2Contract {
       bytes owner_address = 1;
       int64 unfreeze_balance = 2;
       ResourceCode resource = 3;
      }
```

* `owner_address`：解质押 TRX 的账户地址。
* `unfreeze_balance`：解质押数额。
* `resource`： 解质押资源的类型。
   

## 提取解质押本金 WithdrawExpireUnfreezeContract

```protobuf
      message WithdrawExpireUnfreezeContract {
        bytes owner_address = 1;
      }
```

* `owner_address`：提取已到期解质押 TRX 的账户地址。
   
## 资源代理 DelegateResourceContract

```protobuf
      message DelegateResourceContract {
      bytes owner_address = 1;
      ResourceCode resource = 2;
      int64 balance = 3;
      bytes receiver_address = 4;
      bool  lock = 5;
      int64 lock_period = 6;
      }
```

* `owner_address`：资源代理方账户地址。
* `resource`： 代理的资源的类型。
* `balance`： 代理的资源的份额，单位为sun。
* `receiver_address`：资源接收者地址。
* `lock`：是否锁定本次代理。
* `lock_period`：当 `lock=true` 时的锁定时长，单位为块（每块 3 秒）。仅在 `MAX_DELEGATE_LOCK_PERIOD` 提案生效后才接受用户传入值，此时取 0 表示使用默认 86400 块（3 天），取值上限由链参数 `getMaxDelegateLockPeriod` 决定；提案未生效时该字段被忽略，锁定时长固定为 86400 块。
   
   
## 回收先前代理的资源 UnDelegateResourceContract

```protobuf
      message UnDelegateResourceContract {
      bytes owner_address = 1;
      ResourceCode resource = 2;
      int64 balance = 3;
      bytes receiver_address = 4;
      }
```

* `owner_address`：回收已代理资源的账户地址。
* `resource`： 回收代理资源的类型。
* `balance`：回收代理资源的份额。
* `receiver_address`：资源接收地址。

## 取消所有 V2 解质押 CancelAllUnfreezeV2Contract

```protobuf
      message CancelAllUnfreezeV2Contract {
        bytes owner_address = 1;
      }
```

* `owner_address`：取消全部待解质押操作的账户地址。





