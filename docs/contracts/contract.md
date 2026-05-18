# 智能合约

## 介绍

智能合约是一种能自动执行其条款的计算化交易协议。智能合约和普通合约一样，定义了参与者相关的条款和奖惩机制。一旦合约被启动，便能按照设定的条款执行，并自动检查所承诺的条款实施情形。
TRON 兼容以太坊（Ethereum）上采用 Solidity 编写的智能合约。你可以在 [TRON solidity 代码库](https://github.com/tronprotocol/solidity/releases) 中了解最新的版本。合约编写、编译完成后，部署到 TRON 公链上。部署后的合约，被触发时，就会在公链的各个节点上自动执行。

## 特性

TRON virtual machine 基于以太坊 solidity 语言实现，兼容以太坊虚拟机的特性，但基于 TRON 自身属性也有部分的区别。

### 智能合约的定义

波场虚拟机运行的智能合约兼容以太坊智能合约特性，以 protobuf 的形式定义合约内容：

```solidity
message SmartContract {
  message ABI {
    message Entry {
      enum EntryType {
        UnknownEntryType = 0;
        Constructor = 1;
        Function = 2;
        Event = 3;
        Fallback = 4;
        Receive = 5;
        Error = 6;
      }
      message Param {
        bool indexed = 1;
        string name = 2;
        string type = 3;
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
  string name = 7;
  int64 origin_energy_limit = 8;
  bytes code_hash = 9;
  bytes trx_hash = 10;
  int32 version = 11;
}
```

- `origin_address`：合约创建者地址
- `contract_address`：合约地址
- `abi`：合约所有函数的接口信息
- `bytecode`：合约字节码
- `call_value`：随合约调用传入的 TRX 金额
- `consume_user_resource_percent`：开发者设置的调用者的资源扣费百分比
- `name`：合约名称
- `origin_energy_limit`：开发者设置的在一次合约调用过程中自己消耗的 energy 的上限，必须大于 0。对于之前老的合约，deploy 的时候没有提供设置该值的参数，会存成 0，但是会按照 1000 万 energy 上限计算，开发者可以通过 `updateEnergyLimit` 接口重新设置该值，设置新值时也必须大于 0
- `code_hash`：合约 runtime bytecode 的哈希
- `trx_hash`：合约部署的根交易 id。仅对通过 `CREATE2` 操作码部署的合约填充该字段；通过 `CREATE` 操作码或 gRPC `deployContract` 部署的合约该字段为空
- `version`：合约版本号。当网络激活了 `ALLOW_TVM_COMPATIBLE_EVM` 提案后，新部署的合约会被标记为 version 1，使运行时可以仅对这些合约启用 EVM 兼容行为；激活前部署的旧合约保持 version 0，沿用原 TVM 语义。截至撰写时该提案在主网尚未激活，因此主网上所有合约的 version 都是 0

通过另外两个 grpc message 类型 `CreateSmartContract` 和 `TriggerSmartContract` 来创建和使用 smart contract

### 合约函数的使用

#### constant function 和非 constant function

函数调用从对链上属性是否有更改可分为两种：constant function 和非 constant function。
Constant function 是指用 `view`/`pure`/`constant` 修饰的函数。会在调用的节点上直接返回结果，并不以一笔交易的形式广播出去。
非 constant function 是指需要依托一笔交易的形式被广播的方法调用。函数会改变链上数据的内容，比如转账，改变合约内部变量的值等等。

注意：如果在合约内部使用 create 指令（`CREATE` 指令），即使用 `view`/`pure`/`constant` 来修饰这个动态创建的合约方法，这个合约方法仍会被当作非 constant function，以交易的形式来处理。

#### 消息调用（message calls）

消息调用可以向其他的合约发起函数调用，也可以向合约的账户或非合约的账户转账 TRX。与普通的波场 `TriggerContract` 类似，消息调用也有调用的发起者、接受者、数据、转账金额、扣费以及返回值等属性。每一个消息调用都可以递归地生成新的消息调用。
合约可以决定在其内部的消息调用中，对于剩余的 energy 应发送和保留多少。如果在内部消息调用时发生了 `OutOfEnergyException` 异常（或其他任何异常），会返回 false，但不会以异常的形式抛出。此时，只有与该内部消息调用一起发送的 gas 会被消耗掉，如果不表明消息调用所传入的费用 `call.value(energy)`，则会扣掉所有的剩余 energy。

#### 委托调用 / 代码调用 / 库（delegatecall/callcode/library）

有一种特殊类型的消息调用，被称为委托调用（`delegatecall`）。它和一般消息调用的区别在于，目标地址的代码将在发起调用的合约的上下文中执行，并且 `msg.sender` 和 `msg.value` 不变。这意味着一个合约可以在运行时从另外一个地址动态加载代码。存储、当前地址和余额都指向发起调用的合约，只有代码是从被调用地址获取的。这使得 Solidity 可以实现"库"能力：可复用的代码库可以放在一个合约的存储上，如用来实现复杂的数据结构的库。

#### CREATE 指令

该指令会创建一个新的合约并生成一个新的地址。与以太坊的主要区别在于：TRON 新合约地址的推导方式为 `sha3omit12(rootTransactionId || nonce)`——即把根交易 id 与 8 字节的 nonce 拼接后再做哈希（nonce 本身**不**预先哈希）；最终的 21 字节地址首字节为 `0x41` TRON 地址前缀。与以太坊不同（以太坊中 nonce 是发起账户的交易 nonce），TRON 这里的 `nonce` 是每个根交易范围内的计数器，每次内部动作（internal call、transfer、`CREATE`、suicide 等）都会自增，不只是在 `CREATE` 时才增。具体实现见 `TransactionUtil.generateContractAddress(byte[], long)`。

注意：与通过 gRPC `deployContract` 创建合约不同，由 `CREATE` 指令创建的合约不会保存合约的 abi。

#### 内置功能与内置函数属性

1. TVM 兼容 Solidity 语言的转账形式，包括：

    - 在 constructor 中调用转账
    - 在合约内函数中调用转账
    - 通过 `transfer`/`send`/`call`/`callcode`/`delegatecall` 函数调用转账

    注意：TRON 的智能合约与 TRON 的系统合约不同。在 SOLIDITY_059 升级（链参数 `ALLOW_TVM_SOLIDITY_059`，由委员会 [提案 #29](https://tronscan.io/#/proposal/29) 激活）之前，从智能合约向不存在的账户转账会失败；激活之后，TVM 会在转账时自动创建目标账户，与系统合约行为一致。

2. 在合约内为超级节点投票以及提取投票奖励。由链参数 `ALLOW_TVM_VOTE` 启用，由委员会 [提案 #84](https://tronscan.io/#/proposal/84) 在主网激活。提供 `VOTEWITNESS` / `WITHDRAWREWARD` 操作码以及相关的只读预编译合约。

3. TRC10 代币操作：向目标地址发送 TRC10、查询某地址的 TRC10 余额。由链参数 `ALLOW_TVM_TRANSFER_TRC10` 启用，由委员会 [提案 #15](https://tronscan.io/#/proposal/15) 在主网激活。

4. 在合约内质押 TRX 获取资源（Stake 2.0）、代理/取消代理资源、查询代理余额。当网络支持解冻延迟模型（Stake 2.0）时启用，目前已在主网激活。

5. 兼容大多数以太坊内置函数和预编译合约（覆盖 Constantinople、Istanbul、London、Shanghai、Cancun 升级，每个升级由独立的 `ALLOW_TVM_*` 链参数控制——已全部在主网激活，分别对应委员会提案 [#18](https://tronscan.io/#/proposal/18)、[#44](https://tronscan.io/#/proposal/44)、[#72](https://tronscan.io/#/proposal/72)、[#89](https://tronscan.io/#/proposal/89) 和 [#103](https://tronscan.io/#/proposal/103)）。`ALLOW_TVM_COMPATIBLE_EVM` 链参数从未提案，因此以太坊标准的 `RIPEMD160` 和 `BLAKE2F` 预编译合约尚未启用。

注意：不推荐使用以太坊的 `RIPEMD160` 函数，因为 TRON 上的返回结果是基于 TRON 的 `sha256` 计算得到的哈希，并非准确的以太坊 `RIPEMD160`。

### 合约地址在solidity语言的使用

以太坊虚拟机地址为20字节，而波场虚拟机解析地址为21字节。

#### 地址转换

在solidity中使用的时候需要对波场地址做如下处理（推荐）：

```solidity
/**
  *  @dev    convert uint256 (HexString add 0x at beginning) TRON address to solidity address type
  *  @param  tronAddress uint256 tronAddress, begin with 0x, followed by HexString
  *  @return Solidity address type
  */

    function convertFromTronInt(uint256 tronAddress) public view returns(address){
        return address(tronAddress);
    }
```

这个和在以太坊中其他类型转换成address类型语法相同。

#### 地址判断

solidity中有地址常量判断，如果写的是21字节地址编译器会报错，只用写20字节地址即可，如：

```solidity
function compareAddress(address tronAddress) public view returns (uint256){
        // if (tronAddress == 0x41ca35b7d915458ef540ade6068dfe2f44e8fa733c) { // compile error
        if (tronAddress == 0xca35b7d915458ef540ade6068dfe2f44e8fa733c) { // right
            return 1;
        } else {
            return 0;
        }
    }
```

tronAddress 从 wallet-cli 传入是 0000000000000000000041ca35b7d915458ef540ade6068dfe2f44e8fa733c 这个 21 字节地址，即正常的波场地址时，是会返回1的，判断正确。

#### 地址赋值

solidity中有地址常量的赋值，如果写的是21字节地址编译器会报错，只用写20字节地址即可，solidity中后续操作直接利用这个20位地址，波场虚拟机内部做了补位操作。如：

```solidity
function assignAddress() public view {
        // address newAddress = 0x41ca35b7d915458ef540ade6068dfe2f44e8fa733c; // compile error
        address newAddress = 0xca35b7d915458ef540ade6068dfe2f44e8fa733c;
        // do something
    }
```

如果想直接使用string 类型的波场地址（如TLLM21wteSPs4hKjbxgmH1L6poyMjeTbHm）请参考内置函数的两种地址转换方式（见II-4-7,II-4-8）。

### 与以太坊有区别的特殊常量

#### 货币

类似于 Solidity 对 `ether` 的支持，波场虚拟机的代码支持的货币单位有 `trx` 和 `sun`，其中 1 `trx` = 1000000 `sun`，大小写敏感，只支持小写。目前 tron-studio 支持 `trx` 和 `sun`，在 remix 中，不支持 `trx` 和 `sun`，如果使用 `ether`、`finney` 等单位时，注意换算（可能会发生溢出错误）。
我们推荐使用 tron-studio 代替 remix 进行 TRON 智能合约的编写。

#### 区块相关

- `blockhash(uint blockNumber) returns (bytes32)`：指定区块的区块哈希——仅可用于最新的 256 个区块且不包括当前区块。注意：`block.blockhash(uint)` 形式在上游 Solidity 0.4.22 中已被弃用，并在 0.5.0 中被移除（TRON 的 Solidity fork 自 `tv_0.4.24` 起继承了这两项变更）；请改用顶层的 `blockhash(...)`
- `block.basefee` (uint)：返回链参数中的网络能量费（`getEnergyFee`）；与以太坊基于每个区块的 EIP-1559 base fee 不同，该值只在委员会提案修改时才会变化。自 London 升级（`ALLOW_TVM_LONDON`）起可用，由委员会 [提案 #72](https://tronscan.io/#/proposal/72) 在主网激活
- `block.coinbase` (address)：产当前区块的超级节点地址
- `block.difficulty` (uint)：当前区块难度，波场不推荐使用，设置恒为 0
- `block.gaslimit` (uint)：当前区块 gas 限额，波场暂时不支持使用，暂时设置为 0
- `block.number` (uint)：当前区块号
- `block.timestamp` (uint)：当前区块以秒计的时间戳
- `gasleft() returns (uint256)`：剩余的 gas
- `msg.data` (bytes)：完整的 calldata
- `msg.gas` (uint)：剩余 gas，自 0.4.21 版本开始已经不推荐使用，由 `gasleft()` 代替
- `msg.sender` (address)：消息发送者（当前调用）
- `msg.sig` (bytes4)：calldata 的前 4 字节（也就是函数标识符）
- `msg.value` (uint)：随消息发送的 sun 的数量
- `now` (uint)：`block.timestamp` 的别名。在上游 Solidity 0.7.0 中已被移除（TRON 的 Solidity fork 自 `tv_0.7.0` 起继承该移除）；请改用 `block.timestamp`
- `tx.gasprice` (uint)：交易的 gas 价格，波场不推荐使用，设置值恒为 0
- `tx.origin` (address)：交易发起者


### Energy

智能合约的每条指令在运行时都会消耗系统资源，我们以 `Energy` 作为资源消耗的单位。
