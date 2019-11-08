    
 <h2 id="1">1.创建账户 AccountCreateContract</h2>  

    message AccountCreateContract {
       bytes owner_address = 1;
       bytes account_address = 2;
       AccountType type = 3;
    }
 
   `owner_address`：合约持有人地址。     
   `account_address`： 将要创建的账户地址。    
   `type`：账户类型。0代表普通账户，1代表智能合约账户。  
     
 <h2 id="2">2.转账 TransferContract</h2>  

      message TransferContract {
       bytes owner_address = 1;
       bytes to_address = 2;
       int64 amount = 3;
     }
 
   `owner_address`：合约持有人地址。  
   `to_address`： 目标账户地址。     
   `amount`：转账金额，单位为 sun。  
     

 <h2 id="3">3.转账发布的Token TransferAssetContract</h2>  

      message TransferAssetContract {
       bytes asset_name = 1;
       bytes owner_address = 2;
       bytes to_address = 3;
       int64 amount = 4;
     }

   `asset_name`：发布Token的id。  
   `owner_address`：合约持有人地址。  
   `to_address`： 目标账户地址。  
   `amount`：转账Token的数量。  
     

 <h2 id="4">4.投票超级节点  VoteWitnessContract</h2>  

      message VoteWitnessContract {
       message Vote {
         bytes vote_address = 1;
         int64 vote_count = 2;
       }
       bytes owner_address = 1;
       repeated Vote votes = 2;
       bool support = 3;
     }
 
   `owner_address`：合约持有人地址。    
   `vote_address`： 超级节点候选人的地址。      
   `vote_count`：投给超级节点候选人的票数。      
   `support`：是否支持，这里应该是恒为true，暂未使用该参数。    


 <h2 id="5">5.创建超级节点候选人 WitnessCreateContract</h2>  

      message WitnessCreateContract {
       bytes owner_address = 1;
       bytes url = 2;
     }
   
   `owner_address`：合约持有人地址。    
   `url`：超级节点的网址。    
    
     
 <h2 id="6">6.发布Token AssetIssueContract</h2>  

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
 
   `owner_address`：合约持有人地址。     
   `name`：发布Token的名称。 
   `abbr`：Token缩写。    
   `total_supply`：发行总的token数量。     
   `frozen_supply`：冻结Token的数量和冻结时间列表。   
   `trx_num`：对应TRX数量。  
   `num`： 对应的自定义资产数目。  
   `start_time`：ICO开始时间。  
   `end_time`：ICO结束时间。  
   `order`：已废弃。    
   `vote_score`：已废弃。 
   `description`：Token的描述。  
   `url`：Token的url地址链接。  
   `free_asset_net_limit`：每个账户可以使用的免费带宽（转移该资产时使用）。  
   `public_free_asset_net_limit`：所有账户可以使用的免费带宽（转移该资产时使用）。  
   `public_free_asset_net_usage`：所有账户使用免费带宽（转移该资产时使用）。  
   `public_latest_free_net_time`：最近一次转移该Token使用免费带宽的时间。  
    
     
 <h2 id="7">7.更新超级节点候选人URL WitnessUpdateContract</h2>  

      message WitnessUpdateContract {
       bytes owner_address = 1;
       bytes update_url = 12;
     }
    
   `owner_address`：合约持有人地址。  
   `update_url`：超级节点网站的url。  
     
 <h2 id="8">8.购买发行的Token ParticipateAssetIssueContract</h2>  

      message ParticipateAssetIssueContract {
       bytes owner_address = 1;
       bytes to_address = 2;
       bytes asset_name = 3;
       int64 amount = 4;
     }
 
   `owner_address`：合约持有人地址。   
   `to_address`：发行Token所有者地址。  
   `asset_name`： 发行Token的id。    
   `amount`：购买发行Token使用TRX的数量，单位是 sun。  

     
 <h2 id="9">9.更新账户 AccountUpdateContract</h2> 

      // Update account name. Account name is unique now.
     message AccountUpdateContract {
       bytes account_name = 1;
       bytes owner_address = 2;
     }
 
   `owner_address`：合约持有人地址。     
   `account_name`： 账户名称。   
     
 <h2 id="10">10.冻结资产 FreezeBalanceContract</h2>  

      message FreezeBalanceContract {
       bytes owner_address = 1;
       int64 frozen_balance = 2;
       int64 frozen_duration = 3;
       ResourceCode resource = 10;
       bytes receiver_address = 15;
     }
   
   `owner_address`：合约持有人地址。  
   `frozen_balance`：冻结资产的数量。  
   `frozen_duration`：冻结资产的时间段。  
   `resource`： 冻结TRX获取资源的类型。   
   `receiver_address`：接收资源的账户。    

     
 <h2 id="11">11.解冻资产 UnfreezeBalanceContract</h2>  

      message UnfreezeBalanceContract {
       bytes owner_address = 1;
       ResourceCode resource = 10;
       bytes receiver_address = 13;
     }
  
   `owner_address`：合约持有人地址。    
   `resource`： 解冻资源的类型。      
   `receiver_address`：接收资源的账户。  

     
 <h2 id="12">12.提取奖励 WithdrawBalanceContract</h2>  

      message WithdrawBalanceContract {
       bytes owner_address = 1;
     }

   `owner_address`：合约持有人地址。    

     
 <h2 id="13">13.解冻发布的Token UnfreezeAssetContract</h2>  

      message UnfreezeAssetContract {
       bytes owner_address = 1;
     }

   `owner_address`：合约持有人地址。   

     
 <h2 id="14">14.更新通证参数 UpdateAssetContract</h2>  

      message UpdateAssetContract {
       bytes owner_address = 1;
       bytes description = 2;
       bytes url = 3;
       int64 new_limit = 4;
       int64 new_public_limit = 5;
     }
 
   `owner_address`：合约持有人地址。  
   `description`： 通证的描述。  
   `url`：通证的网址的Url。  
   `new_limit`：每个调用者可以消耗Bandwidth point的限制。  
   `new_public_limit`： 所有调用者可以消耗Bandwidth points的限制。  

     
 <h2 id="15">15.创建提议  ProposalCreateContract</h2>  

      message ProposalCreateContract {
       bytes owner_address = 1;
       map<int64, int64> parameters = 2;
     }
 
   `owner_address`：合约持有人地址。    
   `parameters`： 提议。  

     
 <h2 id="16">16.赞成提议 ProposalApproveContract</h2>  

      message ProposalApproveContract {
       bytes owner_address = 1;
       int64 proposal_id = 2;
       bool is_add_approval = 3; // add or remove approval
     }
 
   `owner_address`：合约持有人地址。  
   `proposal_id`： 提议的Id。  
   `is_add_approval`：是否赞成提议。  

     
 <h2 id="17">17.删除提议 ProposalDeleteContract</h2>  

     message ProposalDeleteContract {
       bytes owner_address = 1;
       int64 proposal_id = 2;
     }
 
   `owner_address`：合约持有人地址。    
   `proposal_id`： 提议ID。  
     
 <h2 id="18">18.设置账户ID SetAccountIdContract</h2>  

      // Set account id if the account has no id. Account id is unique and case insensitive.
     message SetAccountIdContract {
       bytes account_id = 1;
       bytes owner_address = 2;
     }
  
   `owner_address`：合约持有人地址。    
   `account_id`： 账户Id。  
     
     
 <h2 id="19">19.创建智能合约 CreateSmartContract</h2>  

     message CreateSmartContract {
       bytes owner_address = 1;
       SmartContract new_contract = 2;
     }

   `owner_address`：合约持有人地址。  
   `new_contract`： 智能合约。  

     
 <h2 id="20">20.触发智能合约 TriggerSmartContract</h2>  

      message TriggerSmartContract {
       bytes owner_address = 1;
       bytes contract_address = 2;
       int64 call_value = 3;
       bytes data = 4;
     }
 
   `owner_address`：合约持有人地址。  
   `contract_address`： 合约地址。   
   `call_value`：传入合约的TRX的值。     
   `data`：操作参数。   

     
 <h2 id="21">21.更新合约 UpdateSettingContract</h2>  

      message UpdateSettingContract {
       bytes owner_address = 1;
       bytes contract_address = 2;
       int64 consume_user_resource_percent = 3;
     }
  
   `owner_address`：合约持有人地址。    
   `contract_address`： 合约地址。    
   `consume_user_resource_percent`：将要更新的账户消耗资源的百分比。  

     
 <h2 id="22">22.创建交易所 ExchangeCreateContract</h2>  

      message ExchangeCreateContract {
       bytes owner_address = 1;
       bytes first_token_id = 2;
       int64 first_token_balance = 3;
       bytes second_token_id = 4;
       int64 second_token_balance = 5;
     }
 
   `owner_address`：合约持有人地址。  
   `first_token_id`： 第1种token的id。   
   `first_token_balance`：第1种token的balance。  
   `second_token_id`：第2种token的id。  
   `second_token_balance`：第2种token的balance。  
   
     
 <h2 id="23">23.给交易所注资 ExchangeInjectContract</h2>  

      message ExchangeInjectContract {
       bytes owner_address = 1;
       int64 exchange_id = 2;
       bytes token_id = 3;
       int64 quant = 4;
     }
  
   `owner_address`：合约持有人地址。  
   `exchange_id`： 交易对的id。   
   `token_id`：要注资的token的id。   
   `quant`：要注资的token的金额。   

     
 <h2 id="24">24.从交易所撤资 ExchangeWithdrawContract</h2>  

      message ExchangeWithdrawContract {
       bytes owner_address = 1;
       int64 exchange_id = 2;
       bytes token_id = 3;
       int64 quant = 4;
     }
  
   `owner_address`：合约持有人地址。  
   `exchange_id`： 交易对的id。   
   `token_id`：要撤资的token的id。   
   `quant`：要撤资的token的金额。   

     
 <h2 id="25">25.在交易所交易 ExchangeTransactionContract</h2>  

      message ExchangeTransactionContract {
       bytes owner_address = 1;
       int64 exchange_id = 2;
       bytes token_id = 3;
       int64 quant = 4;
     }
 
   `owner_address`：合约持有人地址。  
   `exchange_id`： 交易对的id。   
   `token_id`：要卖出的token的id。   
   `quant`：要卖出的token的金额。    

  
 <h2 id="26">26.匿名交易 ShieldedTransferContract</h2>
   
    message ShieldedTransferContract {
       bytes transparent_from_address = 1; 
       int64 from_amount = 2;
       repeated SpendDescription spend_description = 3;
       repeated ReceiveDescription receive_description = 4;
       bytes binding_signature = 5;
       bytes transparent_to_address = 6; 
       int64 to_amount = 7; 
    }  

   `transparent_from_address`：交易发送方透明地址，如果交易发送方是匿名的，则该参数为空。  
   `from_amount`：交易发送方转账金额，正整数；如果交易发送方是匿名的，则该参数为0。  
   `spend_description`：交易发送方note的SpendDescription，最多一个，该参数类型具体描述见下文；如果发送方是透明地址，则该参数为空。  
   `receive_description`：交易接收方note的ReceiveDescription，最多两个，该参数类型具体描述见下文。  
   `binding_signature`：交易的绑定签名，证明交易双方金额平衡。  
   `transparent_to_address`：交易接收方透明地址，如果交易接收方都是匿名的，则该参数为空。 
   `to_amount`：交易接收方转账金额，正整数；如果交易接收方是匿名的，则该参数为0。


     message SpendDescription {
       bytes value_commitment = 1;
       bytes anchor = 2;
       bytes nullifier = 3; 
       bytes rk = 4; 
       bytes zkproof = 5;
       bytes spend_authority_signature = 6;
     }   
     
   `value_commitment`：对交易发送方转账金额的承诺。  
   `anchor`：交易发送方note commitment所在Merkle树的根hash。  
   `nullifier`：交易发送方note的作废证明，防止双花。  
   `rk`：验证交易发送方Spend Authorization签名的公钥。  
   `zkproof`：交易发送方note的零知识证明，证明要花费的note存在，且可以被花费。  
   `spend_authority_signature`：交易发送方的Spend Authorization签名。  


     message ReceiveDescription {
       bytes value_commitment = 1;
       bytes note_commitment = 2;
       bytes epk = 3; 
       bytes c_enc = 4;
       bytes c_out = 5;
       bytes zkproof = 6;
     }

   `value_commitment`：对交易接收方转账金额的承诺。  
   `note_commitment`：对交易接收方note的承诺。  
   `epk`：临时公钥，用于生成解密note密钥。  
   `c_enc`：note加密结果的一部分，是对（Diversifier, 转账金额v, 生成note_commitment的随机数rcm, Memo）的加密结果。  
   `c_out`：note加密结果的另一部分，是对（接收方公钥，临时私钥）的加密结果。  
   `zkproof`：交易接收方note存在的零知识证明。   