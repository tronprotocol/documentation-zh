# 系统合约


TRON网络支持多种不同类型的交易，比如TRX转账交易、TRC10转账交易、创建智能合约交易、触发智能合约交易、质押TRX交易等等。创建不同类型的交易，需要调用不同的API接口， 例如部署合约交易的类型是`CreateSmartContract`，需要调用`wallet/deploycontractAPI`来创建交易；质押TRX获取资源交易的类型是`FreezeBalanceV2Contract`，需要调用 `wallet/freezebalancev2API`来创建交易，我们将这些不同的交易类型的实现统称为系统合约，下面为系统合约类型及其包含的内容：


## 创建账户 AccountCreateContract

```protobuf
    message AccountCreateContract {
       bytes owner_address = 1;
       bytes account_address = 2;
       AccountType type = 3;
    }
```

* `owner_address`：合约持有人地址。
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

* `owner_address`：合约持有人地址。
* `to_address`： 目标账户地址。
* `amount`：转账金额，单位为 sun。


## TRC-10代币转账 TransferAssetContract

```protobuf
      message TransferAssetContract {
       bytes asset_name = 1;
       bytes owner_address = 2;
       bytes to_address = 3;
       int64 amount = 4;
     }
```

* `asset_name`：TRC-10的id。
* `owner_address`：合约持有人地址。
* `to_address`： 目标账户地址。
* `amount`：转账代币的数量。

## 投票超级节点  VoteWitnessContract

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

* `owner_address`：合约持有人地址。
* `vote_address`： 超级节点候选人的地址。
* `vote_count`：投给超级节点候选人的票数。
* `support`：是否支持，这里应该是恒为true，暂未使用该参数。

## 创建超级节点候选人 WitnessCreateContract

```protobuf
      message WitnessCreateContract {
       bytes owner_address = 1;
       bytes url = 2;
     }
```

* `owner_address`：合约持有人地址。
* `url`：超级节点的网址。

## 发布TRC-10代币 AssetIssueContract

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
       int32 num = 8;
       int64 start_time = 9;
       int64 end_time = 10;
       int64 order = 11; // the order of tokens of the same name
       int32 vote_score = 16;
       bytes description = 20;
       bytes url = 21;
       int64 free_asset_net_limit = 22;
       int64 public_free_asset_net_limit = 23;
       int64 public_free_asset_net_usage = 24;
       int64 public_latest_free_net_time = 25;
     }
```

* `owner_address`：合约持有人地址。
* `name`：发布Token的名称。
* `abbr`：Token缩写。
* `total_supply`：发行总的token数量。
* `frozen_supply`：质押Token的数量和质押时间列表。
* `trx_num`：对应TRX数量。
* `num`： 对应的自定义资产数目。
* `start_time`：ICO开始时间。
* `end_time`：ICO结束时间。
* `order`：已废弃。
* `vote_score`：已废弃。
* `description`：Token的描述。
* `url`：Token的url地址链接。
* `free_asset_net_limit`：每个账户可以使用的免费带宽（转移该资产时使用）。
* `public_free_asset_net_limit`：所有账户可以使用的免费带宽（转移该资产时使用）。
* `public_free_asset_net_usage`：所有账户使用免费带宽（转移该资产时使用）。
* `public_latest_free_net_time`：最近一次转移该Token使用免费带宽的时间。

## 更新超级节点候选人URL WitnessUpdateContract

```protobuf
      message WitnessUpdateContract {
       bytes owner_address = 1;
       bytes update_url = 12;
     }
```

* `owner_address`：合约持有人地址。
* `update_url`：超级节点网站的url。

## 购买TRC-10代币 ParticipateAssetIssueContract

```protobuf
      message ParticipateAssetIssueContract {
       bytes owner_address = 1;
       bytes to_address = 2;
       bytes asset_name = 3;
       int64 amount = 4;
     }
```

* `owner_address`：合约持有人地址。
* `to_address`：发行Token所有者地址。
* `asset_name`： 发行Token的id。
* `amount`：购买发行Token使用TRX的数量，单位是 sun。

## 更新账户 AccountUpdateContract

```protobuf
      // Update account name. Account name is unique now.
     message AccountUpdateContract {
       bytes account_name = 1;
       bytes owner_address = 2;
     }
```

* `owner_address`：合约持有人地址。
* `account_name`： 账户名称。

## （已废弃）Stake1.0质押 FreezeBalanceContract


```protobuf
      message FreezeBalanceContract {
       bytes owner_address = 1;
       int64 frozen_balance = 2;
       int64 frozen_duration = 3;
       ResourceCode resource = 10;
       bytes receiver_address = 15;
     }
```

* `owner_address`：合约持有人地址。
* `frozen_balance`：质押资产的数量。
* `frozen_duration`：质押资产的时间段。
* `resource`： 质押TRX获取资源的类型。
* `receiver_address`：接收资源的账户。

## 解质押Stake1.0阶段质押的资产 UnfreezeBalanceContract

```protobuf
      message UnfreezeBalanceContract {
       bytes owner_address = 1;
       ResourceCode resource = 10;
       bytes receiver_address = 13;
     }
```

* `owner_address`：合约持有人地址。
* `resource`： 解锁资源的类型。
* `receiver_address`：接收资源的账户。

## 提取奖励 WithdrawBalanceContract

```protobuf
      message WithdrawBalanceContract {
       bytes owner_address = 1;
     }
```

* `owner_address`：合约持有人地址。

## 解锁发布的Token UnfreezeAssetContract

```protobuf
      message UnfreezeAssetContract {
       bytes owner_address = 1;
     }
```

* `owner_address`：合约持有人地址。

## 更新通证参数 UpdateAssetContract

```protobuf
      message UpdateAssetContract {
       bytes owner_address = 1;
       bytes description = 2;
       bytes url = 3;
       int64 new_limit = 4;
       int64 new_public_limit = 5;
     }
```

* `owner_address`：合约持有人地址。
* `description`： 通证的描述。
* `url`：通证的网址的Url。
* `new_limit`：每个调用者可以消耗Bandwidth point的限制。
* `new_public_limit`： 所有调用者可以消耗Bandwidth points的限制。

## 创建提议  ProposalCreateContract

```protobuf
      message ProposalCreateContract {
       bytes owner_address = 1;
       map<int64, int64> parameters = 2;
     }
```

* `owner_address`：合约持有人地址。
* `parameters`： 提议。

## 赞成提议 ProposalApproveContract

```protobuf
      message ProposalApproveContract {
       bytes owner_address = 1;
       int64 proposal_id = 2;
       bool is_add_approval = 3; // add or remove approval
     }
```

* `owner_address`：合约持有人地址。
* `proposal_id`： 提议的Id。
* `is_add_approval`：是否赞成提议。

## 删除提议 ProposalDeleteContract

```protobuf
     message ProposalDeleteContract {
       bytes owner_address = 1;
       int64 proposal_id = 2;
     }
```

* `owner_address`：合约持有人地址。
* `proposal_id`： 提议ID。

## 设置账户ID SetAccountIdContract

```protobuf
      // Set account id if the account has no id. Account id is unique and case insensitive.
     message SetAccountIdContract {
       bytes account_id = 1;
       bytes owner_address = 2;
     }
```

* `owner_address`：合约持有人地址。
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

* `owner_address`：合约持有人地址。
* `new_contract`： 智能合约。
* `call_token_value`：转入TRC-10数目。
* `token_id`：转入TRC-10的id。

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

* `owner_address`：合约持有人地址。
* `contract_address`： 合约地址。
* `call_value`：传入合约的TRX的值。
* `data`：操作参数。
* `call_token_value`：转入TRC-10数目。
* `token_id`：转入TRC-10的id。

## 更新合约 UpdateSettingContract

```protobuf
      message UpdateSettingContract {
       bytes owner_address = 1;
       bytes contract_address = 2;
       int64 consume_user_resource_percent = 3;
     }
```

* `owner_address`：合约持有人地址。
* `contract_address`： 合约地址。
* `consume_user_resource_percent`：将要更新的账户消耗资源的百分比。

## 创建交易所 ExchangeCreateContract

```protobuf
      message ExchangeCreateContract {
       bytes owner_address = 1;
       bytes first_token_id = 2;
       int64 first_token_balance = 3;
       bytes second_token_id = 4;
       int64 second_token_balance = 5;
     }
```

* `owner_address`：合约持有人地址。
* `first_token_id`： 第1种token的id。
* `first_token_balance`：第1种token的balance。
* `second_token_id`：第2种token的id。
* `second_token_balance`：第2种token的balance。

## 给交易所注资 ExchangeInjectContract

```protobuf
      message ExchangeInjectContract {
       bytes owner_address = 1;
       int64 exchange_id = 2;
       bytes token_id = 3;
       int64 quant = 4;
     }
```

* `owner_address`：合约持有人地址。
* `exchange_id`： 交易对的id。
* `token_id`：要注资的token的id。
* `quant`：要注资的token的数量。

## 从交易所撤资 ExchangeWithdrawContract

```protobuf
      message ExchangeWithdrawContract {
       bytes owner_address = 1;
       int64 exchange_id = 2;
       bytes token_id = 3;
       int64 quant = 4;
     }
```

* `owner_address`：合约持有人地址。
* `exchange_id`： 交易对的id。
* `token_id`：要撤资的token的id。
* `quant`：要撤资的token的数量。

## 在交易所交易 ExchangeTransactionContract

```protobuf
      message ExchangeTransactionContract {
       bytes owner_address = 1;
       int64 exchange_id = 2;
       bytes token_id = 3;
       int64 quant = 4;
       int64 expected = 5;
     }
```

* `owner_address`：合约持有人地址。
* `exchange_id`： 交易对的id。
* `token_id`：要卖出的token的id。
* `quant`：要卖出的token的数量。
* `expected`：期望买入token的数量

## 匿名交易 ShieldedTransferContract

```protobuf
    message ShieldedTransferContract {
       bytes transparent_from_address = 1;
       int64 from_amount = 2;
       repeated SpendDescription spend_description = 3;
       repeated ReceiveDescription receive_description = 4;
       bytes binding_signature = 5;
       bytes transparent_to_address = 6;
       int64 to_amount = 7;
    }
```

* `transparent_from_address`：交易发送方透明地址，如果交易发送方是匿名的，则该参数为空。
* `from_amount`：交易发送方转账金额，正整数；如果交易发送方是匿名的，则该参数为0。
* `spend_description`：交易发送方note的SpendDescription，最多一个，该参数类型具体描述见下文；如果发送方是透明地址，则该参数为空。
* `receive_description`：交易接收方note的ReceiveDescription，最多两个，该参数类型具体描述见下文。
* `binding_signature`：交易的绑定签名，证明交易双方金额平衡。
* `transparent_to_address`：交易接收方透明地址，如果交易接收方都是匿名的，则该参数为空。
* `to_amount`：交易接收方转账金额，正整数；如果交易接收方是匿名的，则该参数为0。

```
     message SpendDescription {
       bytes value_commitment = 1;
       bytes anchor = 2;
       bytes nullifier = 3;
       bytes rk = 4;
       bytes zkproof = 5;
       bytes spend_authority_signature = 6;
     }
```

* `value_commitment`：对交易发送方转账金额的承诺。
* `anchor`：交易发送方note commitment所在Merkle树的根hash。
* `nullifier`：交易发送方note的作废证明，防止双花。
* `rk`：验证交易发送方Spend Authorization签名的公钥。
* `zkproof`：交易发送方note的零知识证明，证明要花费的note存在，且可以被花费。
* `spend_authority_signature`：交易发送方的Spend Authorization签名。

```
     message ReceiveDescription {
       bytes value_commitment = 1;
       bytes note_commitment = 2;
       bytes epk = 3;
       bytes c_enc = 4;
       bytes c_out = 5;
       bytes zkproof = 6;
     }
```

* `value_commitment`：对交易接收方转账金额的承诺。
* `note_commitment`：对交易接收方note的承诺。
* `epk`：临时公钥，用于生成解密note密钥。
* `c_enc`：note加密结果的一部分，是对（Diversifier, 转账金额v, 生成note_commitment的随机数rcm, Memo）的加密结果。
* `c_out`：note加密结果的另一部分，是对（接收方公钥，临时私钥）的加密结果。
* `zkproof`：交易接收方note存在的零知识证明。


## 账户权限管理

  [账户权限管理](./multi-signatures.md)

##  清除ABI合约

```protobuf
     message ClearABIContract {
       bytes owner_address = 1;
       bytes contract_address = 2;
     }

```

* `owner_address`：合约持有人地址。
* `contract_address`：需要清除ABI的合约。

##  更新分红比例合约

```protobuf
     message UpdateBrokerageContract {
       bytes owner_address = 1;
       int32 brokerage = 2;
     }
```

* `owner_address`：合约持有人地址。
* `brokerage`: 分红比例，从0到100，1代表1%。

##  调整能量上限合约

```protobuf
     message UpdateEnergyLimitContract {
       bytes owner_address = 1;
       bytes contract_address = 2;
       int64 origin_energy_limit = 3;
     }
```
* `owner_address`：合约持有人地址。
* `contract_address`：需要调整的合约地址。
* `origin_energy_limit`：调整后智能合约部署者提供的能量上限值。

## 质押资产 FreezeBalanceV2Contract

```protobuf
     message FreezeBalanceV2Contract {
      bytes owner_address = 1;
      int64 frozen_balance = 2;
      ResourceCode resource = 3;
      }
```

* `owner_address`：质押者地址。
* `frozen_balance`：质押资产的数量。
* `resource`： 质押TRX获取资源的类型。

## 解质押资产 UnfreezeBalanceV2Contract

```protobuf
      message UnfreezeBalanceV2Contract {
       bytes owner_address = 1;
       int64 unfreeze_balance = 2;
       ResourceCode resource = 3;
      }
```

* `owner_address`：解质押者地址。
* `unfreeze_balance`：解质押数额。
* `resource`： 解锁资源的类型。
   

## 提取解质押本金 WithdrawExpireUnfreezeContract

```protobuf
      message WithdrawExpireUnfreezeContract {
        bytes owner_address = 1;
      }
```

* `owner_address`：提取本金账户地址。
   
## 资源代理 DelegateResourceContract

```protobuf
      message DelegateResourceContract {
      bytes owner_address = 1;
      ResourceCode resource = 2;
      int64 balance = 3;
      bytes receiver_address = 4;
      bool  lock = 5;
      }
```

* `owner_address`：代理人地址。
* `resource`： 代理的资源的类型。
* `balance`： 代理的资源的份额，单位为sun。
* `receiver_address`：资源接收者地址。
* `lock`：是否将代理操作锁定3天。
   
   
## 取消资源代理 UnDelegateResourceContract

```protobuf
      message UnDelegateResourceContract {
      bytes owner_address = 1;
      ResourceCode resource = 2;
      int64 balance = 3;
      bytes receiver_address = 4;
      }
```

* `owner_address`：解代理发起地址
* `resource`： 解锁资源的类型。
* `balance`：解代理资源份额。
* `receiver_address`：资源接收地址。
   







