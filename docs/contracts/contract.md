
## 波场智能合约介绍 

智能合约是一种能自动执行其条款的计算化交易协议。智能合约和普通合约一样，定义了参与者相关的条款和奖惩机制。一旦合约被启动，便能按照设定的条款执行，并自动检查所承诺的条款实施情形。  
Tron兼容以太坊（Ethereum）上采用Solidity编写的智能合约。当前建议的Solidity语言版本为0.4.24 ~ 0.4.25。合约编写、编译完成后，部署到Tron公链上。部署后的合约，被触发时，就会在公链的各个节点上自动执行。

## 波场智能合约特性 
Tron virtual machine 基于以太坊 solidity 语言实现，兼容以太坊虚拟机的特性，但基于tron自身属性也有部分的区别。  

<h3> 1. 智能合约 </h3>
波场虚拟机运行的智能合约兼容以太坊智能合约特性，以protobuf的形式定义合约内容：  

    message SmartContract {
      message ABI {
        message Entry {
          enum EntryType {
            UnknownEntryType = 0;
            Constructor = 1;
            Function = 2;
            Event = 3;
            Fallback = 4;
          }
          message Param {
            bool indexed = 1;
            string name = 2;
            string type = 3;
            // SolidityType type = 3;
          }
          enum StateMutabilityType {
            UnknownMutabilityType = 0;
            Pure = 1;
            View = 2;
            Nonpayable = 3;
            Payable = 4;
          }

          bool anonymous = 1;
          bool constant = 2;
          string name = 3;
          repeated Param inputs = 4;
          repeated Param outputs = 5;
          EntryType type = 6;
          bool payable = 7;
          StateMutabilityType stateMutability = 8;
        }
        repeated Entry entrys = 1;
      }
      bytes origin_address = 1;
      bytes contract_address = 2;
      ABI abi = 3;
      bytes bytecode = 4;
      int64 call_value = 5;
      int64 consume_user_resource_percent = 6;
      string name = 7；
      int64 origin_energy_limit = 8;
    }
    
origin_address: 合约创建者地址  
contract_address: 合约地址  
abi:合约所有函数的接口信息  
bytecode：合约字节码  
call_value：随合约调用传入的trx金额  
consume_user_resource_percent：开发者设置的调用者的资源扣费百分比  
name：合约名称  
origin_energy_limit: 开发者设置的在一次合约调用过程中自己消耗的energy的上限，必须大于0。对于之前老的合约，deploy的时候没有提供设置该值的参数，会存成0，但是会按照1000万energy上限计算，开发者可以通过updateEnergyLimit接口重新设置该值，设置新值时也必须大于0  

通过另外两个grpc message类型 CreateSmartContract 和 TriggerSmartContract 来创建和使用smart contract  


<h3> 2. 合约函数的使用 </h3>

1.&nbsp;constant function和非constant function

函数调用从对链上属性是否有更改可分为两种：constant function 和 非constant function。
Constant function 是指用 view/pure/constant 修饰的函数。会在调用的节点上直接返回结果，并不以一笔交易的形式广播出去。
非constant function是指需要依托一笔交易的形式被广播的方法调用。函数会改变链上数据的内容，比如转账，改变合约内部变量的值等等。

注意: 如果在合约内部使用create指令（CREATE instruction），即使用view/pure/constant来修饰这个动态创建的合约合约方法，这个合约方法仍会被当作非constant function，以交易的形式来处理。

2.&nbsp;消息调用（message calls）

消息调用可以向其他的合约发起函数调用，也可以向合约的账户或非合约的账户转帐trx。 与普通的波场triggercontract类似， 消息调用也有调用的发起者，接受者，数据，转账金额，扣费，以及返回值等属性。每一个消息调用都可以递归的生成新的消息调用。
合约可以决定在其内部的消息调用中，对于剩余的 energy ，应发送和保留多少。如果在内部消息调用时发生了OutOfEnergyException
异常（或其他任何异常）,会返回false，但不会以异常的形式抛出。此时，只有与该内部消息调用一起发送的gas会被消耗掉，如果不表明消息调用所传入的费用call.value(energy)，则会扣掉所有的剩余energy。 


3.&nbsp;委托调用/代码调用和库 (delegatecall/callcode/libary)

有一种特殊类型的消息调用，被称为 委托调用(delegatecall) 。它和一般的消息调用的区别在于，目标地址的代码将在发起调用的合约的上下文中执行，并且msg.sender 和msg.value 不变。 这意味着一个合约可以在运行时从另外一个地址动态加载代码。存储、当前地址和余额都指向发起调用的合约，只有代码是从被调用地址获取的。 这使得 Solidity 可以实现”库“能力：可复用的代码库可以放在一个合约的存储上，如用来实现复杂的数据结构的库。

4.&nbsp;CREATE 指令（CREATE instruction）

另一个与合约调用相关的是调用指令集的时候使用CREATE指令。这个指令将会创建一个新的合约并生成新的地址。与以太坊的创建唯一的不同在于波场新生成的地址使用的是传入的本次智能合约交易id与调用的nonce的哈希组合。和以太坊不同，这个nonce的定义为本次根调用开始创建的合约序号。即如果有多次的 CREATE指令调用，从1开始，顺序编号每次调用的合约。详细请参考代码。还需注意，与deploycontract的grpc调用创建合约不同，CREATE的合约并不会保存合约的abi。

5.&nbsp;内置功能属性及内置函数 (Odyssey-v3.1.1及之后的版本暂时不支持TVM内置函数)

1）TVM兼容solidity语言的转账形式，包括：
伴随constructor调用转账
伴随合约内函数调用转账
transfer/send/call/callcode/delegatecall函数调用转账

注意，波场的智能合约与波场系统合约的逻辑不同，如果转账的目标地址账户不存在，不能通过智能合约转账的形式创建目标地址账户。这也是与以太坊的不同点。  

2）不同账户为超级节点投票 (Odyssey-v3.1.1及之后的版本暂时不支持)
3）超级节点获取所有奖励 (Odyssey-v3.1.1及之后的版本暂时不支持)
4）超级节点通过或否定提案 (Odyssey-v3.1.1及之后的版本暂时不支持)
5）超级节点提出提案 (Odyssey-v3.1.1及之后的版本暂时不支持)
6）超级节点删除提案 (Odyssey-v3.1.1及之后的版本暂时不支持)
7）波场byte地址转换为solidity地址 (Odyssey-v3.1.1及之后的版本暂时不支持)
8）波场string地址转换为solidity地址 (Odyssey-v3.1.1及之后的版本暂时不支持)
9）向目标账户地址发送token转账 (Odyssey-v3.1.1及之后的版本暂时不支持)
10）查询目标账户地址的指定token的数量 (Odyssey-v3.1.1及之后的版本暂时不支持)
11）兼容所有以太坊内置函数

注意：  
波场2）- 10）为波场自己的内置函数 具体中文文档请参看：https://github.com/tronprotocol/Documentation/blob/master/中文文档/虚拟机/虚拟机内置函数.md

以太坊 RIPEMD160 函数不推荐使用，波场返回的是一个自己的基于sha256的hash结果，并不是准确的以太坊RIPEMD160。以后会考虑删除这个函数。
 
<h3> 3. 合约地址在solidity语言的使用 </h3>

以太坊虚拟机地址为是20字节，而波场虚拟机解析地址为21字节。  
1.&nbsp;地址转换  
在solidity中使用的时候需要对波场地址做如下处理（推荐）：
```text    
/**
  *  @dev    convert uint256 (HexString add 0x at beginning) tron address to solidity address type
  *  @param  tronAddress uint256 tronAddress, begin with 0x, followed by HexString
  *  @return Solidity address type
  */
     
    function convertFromTronInt(uint256 tronAddress) public view returns(address){
        return address(tronAddress);
    }
```

这个和在以太坊中其他类型转换成address类型语法相同。
2.&nbsp;地址判断   
solidity中有地址常量判断，如果写的是21字节地址编译器会报错，只用写20字节地址即可，如：  
```text
function compareAddress(address tronAddress) public view returns (uint256){
        // if (tronAddress == 0x41ca35b7d915458ef540ade6068dfe2f44e8fa733c) { // compile error
        if (tronAddress == 0xca35b7d915458ef540ade6068dfe2f44e8fa733c) { // right
            return 1;
        } else {
            return 0;
        }
    }
```
tronAddress从wallet-cli传入是0000000000000000000041ca35b7d915458ef540ade6068dfe2f44e8fa733c这个21字节地址，即正常的波场地址时，是会返回1的，判断正确。  
3.&nbsp;地址赋值  
solidity中有地址常量的赋值，如果写的是21字节地址编译器会报错，只用写20字节地址即可，solidity中后续操作直接利用这个20位地址，波场虚拟机内部做了补位操作。如：  
```text
function assignAddress() public view {
        // address newAddress = 0x41ca35b7d915458ef540ade6068dfe2f44e8fa733c; // compile error
        address newAddress = 0xca35b7d915458ef540ade6068dfe2f44e8fa733c;
        // do something
    }
```
如果想直接使用string 类型的波场地址（如TLLM21wteSPs4hKjbxgmH1L6poyMjeTbHm）请参考内置函数的两种地址转换方式（见II-4-7,II-4-8）。  

<h3> 4. 与以太坊有区别的特殊常量 </h3>

**货币**  

类似于solidity对ether的支持，波场虚拟机的代码支持的货币单位有trx和sun，其中1trx = 1000000 sun，大小写敏感，只支持小写。目前tron-studio支持trx和sun，在remix中，不支持trx和sun，如果使用ether、finney等单位时，注意换算(可能会发生溢出错误)。
我们推荐使用tron-studio代替remix进行tron智能合约的编写。

**区块相关**

- block.blockhash(uint blockNumber) returns (bytes32)：指定区块的区块哈希——仅可用于最新的 256 个区块且不包括当前区块；而 blocks 从 0.4.22 版本开始已经不推荐使用，由 blockhash(uint blockNumber) 代替
- block.coinbase (address): 产当前区块的超级节点地址
- block.difficulty (uint): 当前区块难度，波场不推荐使用，设置恒为0
- block.gaslimit (uint): 当前区块 gas 限额，波场暂时不支持使用, 暂时设置为0
- block.number (uint): 当前区块号
- block.timestamp (uint): 当前区块以秒计的时间戳
- gasleft() returns (uint256)：剩余的 gas
- msg.data (bytes): 完整的 calldata
- msg.gas (uint): 剩余 gas - 自 0.4.21 版本开始已经不推荐使用，由 gesleft() 代替
- msg.sender (address): 消息发送者（当前调用）
- msg.sig (bytes4): calldata 的前 4 字节（也就是函数标识符）
- msg.value (uint): 随消息发送的 sun 的数量
- now (uint): 目前区块时间戳（block.timestamp）
- tx.gasprice (uint): 交易的 gas 价格，波场不推荐使用，设置值恒为0
- tx.origin (address): 交易发起者


## 交易的合约类型
          
<h3 id="1">1.创建账户 AccountCreateContract</h3>  

   `AccountCreatContract`包含3种参数：    
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `account_address`： 将要创建的账户地址。    
   `type`：账户类型——比如：_0_ 代表的账户类型是`Normal`。

     message AccountCreateContract {
       bytes owner_address = 1;
       bytes account_address = 2;
       AccountType type = 3;
     }
     
 <h3 id="2">2.转账 TransferContract</h3>  

   `TransferContract`包含3种参数：    
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `to_address`： 目标账户地址。    
   `amount`：转账金额，单位为 sun。

     message TransferContract {
       bytes owner_address = 1;
       bytes to_address = 2;
       int64 amount = 3;
     }
     

 <h3 id="3">3.转账发布的Token TransferAssetContract</h3>  

   `TransferAssetContract`包含4种参数：  
   `asset_name`：发布Token的名称。  
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `to_address`： 目标账户地址。  
   `amount`：转账Token的数量。

     message TransferAssetContract {
       bytes asset_name = 1;
       bytes owner_address = 2;
       bytes to_address = 3;
       int64 amount = 4;
     }
     

<h3 id="4">4.投票超级节点  VoteWitnessContract</h3>  

   `VoteWitnessContract`包含3种参数：   
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `vote_address`： 超级节点候选人的地址。    
   `vote_count`：投给超级节点候选人的票数。  
   `votes`：超级节点候选人列表。  
   `support`：是否支持，这里应该是恒为true,暂未使用该参数。  

     message VoteWitnessContract {
       message Vote {
         bytes vote_address = 1;
         int64 vote_count = 2;
       }
       bytes owner_address = 1;
       repeated Vote votes = 2;
       bool support = 3;
     }
     

 <h3 id="5">5.创建超级节点候选人 WitnessCreateContract</h3>  

   `WitnessCreateContract`包含2种参数：    
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `url`： 超级节点后续人网址。    

     message WitnessCreateContract {
       bytes owner_address = 1;
       bytes url = 2;
     }
     
     
 <h3 id="6">6.发布Token AssetIssueContract</h3>  

   `AssetIssueContract`包含17种参数：  
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。     
   `name`：发布Token的名称——比如：_“SiCongcontract”_。 
   `abbr`： 。    
   `total_supply`：发行总的token数量——比如：_100000000_。   
   `frozen_supply`：冻结Token的数量和冻结时间列表。   
   `trx_num`：对应TRX数量——比如：_232241_。  
   `num`： 对应的自定义资产数目。  
   `start_time`：开始时间——比如：_20170312_。  
   `end_time`：结束时间——比如：_20170512_。  
   `order`：相同asset_name时，order递增，默认初始值为0。    
   `vote_score`：合约的评分——比如：_12343_。  
   `description`：Token的描述——比如：_”trondada”_。  
   `url`：Token的url地址链接。  
   `free_asset_net_limit`：每个账户可以使用的免费带宽（转移该资产时使用）。  
   `public_free_asset_net_limit`：所有账户可以使用的免费带宽（转移该资产时使用）。  
   `public_free_asset_net_usage`：所有账户使用免费带宽（转移该资产时使用）。  
   `public_latest_free_net_time`：最近一次转移该Token使用免费带宽的时间。  

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
     
     
 <h3 id="7">7.更新超级节点候选人URL WitnessUpdateContract</h3>  

   `WitnessUpdateContract`包含2种参数：    
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `update_url`： 超级节点更新后的url。  

     message WitnessUpdateContract {
       bytes owner_address = 1;
       bytes update_url = 12;
     }
     
<h3 id="8">8.购买发行的Token ParticipateAssetIssueContract</h3>  

   `ParticipateAssetIssueContract`包含4种参数：    
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。   
   `to_address`：发行Token所有者地址。  
   `account_name`： 发行Token的名称，包括Token名称和order    
   `amount`：购买发行Token使用TRX的数量，单位是 sun。  

     message ParticipateAssetIssueContract {
       bytes owner_address = 1;
       bytes to_address = 2;
       bytes asset_name = 3;
       int64 amount = 4;
     }
     
<h3 id="9">9.更新账户 AccountUpdateContract</h3> 

   `AccountUpdateContract`包含2种参数：   
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。   
   `account_name`： 账户名称——比如： _"SiCongsaccount”_。   

     // Update account name. Account name is not unique now.
     message AccountUpdateContract {
       bytes account_name = 1;
       bytes owner_address = 2;
     }
     
 <h3 id="10">10.冻结资产 FreezeBalanceContract</h3>  

   `FreezeBalanceContract`包含4种参数：    
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `frozen_balance`：冻结资产的数量。  
   `frozen_duration`：冻结资产的时间段。  
   `resource`： 冻结TRX获取资源的类型。 
   `receiver_address` ：接收资源的账户。    

     message FreezeBalanceContract {
       bytes owner_address = 1;
       int64 frozen_balance = 2;
       int64 frozen_duration = 3;
       ResourceCode resource = 10;
       bytes receiver_address = 15;
     }
     
 <h3 id="11">11.解冻资产 UnfreezeBalanceContract</h3>  

   `UnfreezeBalanceContract`包含2种参数：   
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `resource`： 解冻资源的类型。    
   `receiver_address` ：接收资源的账户。

     message UnfreezeBalanceContract {
       bytes owner_address = 1;
       ResourceCode resource = 10;
       bytes receiver_address = 13;
     }
     
 <h3 id="12">12.提取奖励 WithdrawBalanceContract</h3>  

   `WithdrawBalanceContract`包含1种参数：   
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  

     message WithdrawBalanceContract {
       bytes owner_address = 1;
     }
     
 <h3 id="13">13.解冻发布的Token UnfreezeAssetContract</h3>  

   `UnfreezeAssetContract`包含3种参数：   
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  

     message UnfreezeAssetContract {
       bytes owner_address = 1;
     }
     
 <h3 id="14">14.更新通证参数 UpdateAssetContract</h3>  

   `UpdateAssetContract`包含3种参数：   
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `description`： 通证的描述。  
   `url`：通证的Url。  
   `new_limit`：每个调用者可以消耗Bandwidth point的限制。  
   `new_public_limit`： 所有调用者可以消耗Bandwidth points的限制。  

     message UpdateAssetContract {
       bytes owner_address = 1;
       bytes description = 2;
       bytes url = 3;
       int64 new_limit = 4;
       int64 new_public_limit = 5;
     }
     
 <h3 id="15">15.创建提议  ProposalCreateContract</h3>  

   `ProposalCreateContract`包含2种参数：   
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `parameters`： 提议。  

     message ProposalCreateContract {
       bytes owner_address = 1;
       map<int64, int64> parameters = 2;
     }
     
 <h3 id="16">16.赞成提议 ProposalApproveContract</h3>  

   `ProposalApproveContract`包含3种参数：   
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `proposal_id`： 提议的Id。  
   `is_add_approval`：是否赞成提议。  

     message ProposalApproveContract {
       bytes owner_address = 1;
       int64 proposal_id = 2;
       bool is_add_approval = 3; // add or remove approval
     }
     
 <h3 id="17">17.删除提议 ProposalDeleteContract</h3>  

   `ProposalDeleteContract`包含2种参数：   
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `proposal_id`： 提议ID。  

     message ProposalDeleteContract {
       bytes owner_address = 1;
       int64 proposal_id = 2;
     }
     
<h3 id="18">18.设置账户ID SetAccountIdContract</h3>  

   `SetAccountIdContract`包含2种参数：   
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `account_id`： 账户Id。  

     // Set account id if the account has no id. Account id is unique and case insensitive.
     message SetAccountIdContract {
       bytes account_id = 1;
       bytes owner_address = 2;
     }
     
     
 <h3 id="19">19.创建智能合约 CreateSmartContract</h3>  

   `CreateSmartContract`包含2种参数：   
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `new_contract`： 智能合约。  

     message CreateSmartContract {
       bytes owner_address = 1;
       SmartContract new_contract = 2;
     }
     
<h3 id="20">20.触发智能合约 TriggerSmartContract</h3>  

   `TriggerSmartContract`包含4种参数：   
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `contract_address`： 合约地址。   
   `call_value`：TRX的值。     
   `data`：操作参数。   

     message TriggerSmartContract {
       bytes owner_address = 1;
       bytes contract_address = 2;
       int64 call_value = 3;
       bytes data = 4;
     }
     
<h3 id="21">21.更新合约 UpdateSettingContract</h3>  

   `UpdateSettingContract`包含3种参数：   
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `contract_address`： 合约地址。    
   `consume_user_resource_percent`：将要更新的账户消耗资源的百分比。  

     message UpdateSettingContract {
       bytes owner_address = 1;
       bytes contract_address = 2;
       int64 consume_user_resource_percent = 3;
     }
     
 <h3 id="22">22.创建交易所 ExchangeCreateContract</h3>  

   `ExchangeCreateContract`包含5种参数：   
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `first_token_id`： 第1种token的id 。   
   `first_token_balance`：第1种token的balance。  
   `second_token_id`：第2种token的id。  
   `second_token_balance`：第2种token的balance。  
   
     message ExchangeCreateContract {
       bytes owner_address = 1;
       bytes first_token_id = 2;
       int64 first_token_balance = 3;
       bytes second_token_id = 4;
       int64 second_token_balance = 5;
     }
     
 <h3 id="23">23.给交易所注资 ExchangeInjectContract</h3>  

   `ExchangeInjectContract`包含4种参数：   
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `exchange_id`： 交易对的id。   
   `token_id`：要注资的token的id。   
   `quant`：要注资的token的金额。   

     message ExchangeInjectContract {
       bytes owner_address = 1;
       int64 exchange_id = 2;
       bytes token_id = 3;
       int64 quant = 4;
     }
     
<h3 id="24">24.从交易所撤资 ExchangeWithdrawContract</h3>  

   `ExchangeWithdrawContract`包含4种参数：   
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `exchange_id`： 交易对的id。   
   `token_id`：要撤资的token的id。   
   `quant`：要撤资的token的金额。   

     message ExchangeWithdrawContract {
       bytes owner_address = 1;
       int64 exchange_id = 2;
       bytes token_id = 3;
       int64 quant = 4;
     }
     
<h3 id="25">25.在交易所交易 ExchangeTransactionContract</h3>  

   `ExchangeTransactionContract`包含4种参数：   
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。  
   `exchange_id`： 交易对的id。   
   `token_id`：要卖出的token的id。   
   `quant`：要卖出的token的金额。   

     message ExchangeTransactionContract {
       bytes owner_address = 1;
       int64 exchange_id = 2;
       bytes token_id = 3;
       int64 quant = 4;
     }