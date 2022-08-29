# GreatVoyage-v4.0.0


4.0 版已实现匿名 TRC20 合约，可以隐藏源地址、目标地址和 TRC20 代币交易数额，并为用户提供更好的隐私性。 匿名 TRC20 合约包含三种类型的交易：

  * 公开地址到匿名地址交易(mint)： t-addr到z-addr的交易。“t-addr”的信息是公开的，“z-addr”的信息是隐藏的。
  * 完全匿名交易(transfer)： z-addr到z-addr的交易，发送方和接收方的地址和交易金额都被隐藏。
  * 匿名地址到公开地址交易(burn)： z-addr到t-addr的交易，z-addr的信息是隐藏的，t-addr的信息是公开的。

为支持匿名 TRC20 合约，TVM 中添加了四个新零知识指令（`verifyMintProof`, `verifyTransferProof`, `verifyBurnProof`  及  `pedersenHash`），可以为任意 TRC20 合约提供隐私保护。

## 注意
该版本为强制升级

## 新功能
 - 在 TVM 中添加 4 项新指令（`verifyMintProof`, `verifyTransferProof`, `verifyBurnProof` 和 `pedersenHash`）以支持基于零知识证明的TRC20 匿名交易（#3172）。
   - `verifyMintProof`: 用于验证 mint 函数的零知识证明。
   - `verifyTransferProof`: 用于验证 transfer 函数的零知识证明。
   - `verifyBurnProof`: 用于验证 burn 函数的零知识证明。
   - `pedersenHash`: 用于计算 Pedersen 哈希。
- 更新由 MPC 火炬计划生成的零知识证明方案的初始参数（#3210）。
- 添加 API 以支持匿名 TRC20 合约交易（#3172）。
  
   1.&nbsp;Create shielded contract parameters
  ```protobuf
  rpc CreateShieldedContractParameters (PrivateShieldedTRC20Parameters) returns (ShieldedTRC20Parameters) {}
  ```
  2.&nbsp;Create shielded contract parameters without ask
  ```protobuf
  rpc CreateShieldedContractParametersWithoutAsk (PrivateShieldedTRC20ParametersWithoutAsk) returns (ShieldedTRC20Parameters) {}
  ```
  3.&nbsp;Scan shielded TRC20 notes by ivk
  ```protobuf
  rpc ScanShieldedTRC20NotesByIvk (IvkDecryptTRC20Parameters) returns (DecryptNotesTRC20) {}
  ```
  4.&nbsp;Scan shielded TRC20 notes by ovk
  ```protobuf
  rpc ScanShieldedTRC20NotesByOvk (OvkDecryptTRC20Parameters) returns (DecryptNotesTRC20) {}
  ```
  5.&nbsp;Check if the shielded TRC20 note is spent
  ```protobuf
  rpc IsShieldedTRC20ContractNoteSpent (NfTRC20Parameters) returns (NullifierResult) {}
  ```
  6.&nbsp;Get the trigger input for the shielded TRC20 contract
  ```protobuf
    rpc GetTriggerInputForShieldedTRC20Contract (ShieldedTRC20TriggerContractParameters) returns (BytesMessage) {}
  ```
- 支持 `ovk` 扫描 burn 交易的输出（#3203）。
- 支持有 0 或 1 个匿名输出的 `burn` 交易（#3224）。
- 在事件日志触发器添加数据字段，可用于备注（#3200）。

此版本中实现了以下 TIP：
- [TIP-135](https://github.com/tronprotocol/tips/blob/master/tip-135.md): 匿名 TRC20 合约标准，保证 TRC20 代币匿名转账的隐私性。
- [TIP-137](https://github.com/tronprotocol/tips/blob/master/tip-137.md): 在波场虚拟机中实现三个零知识证明指令，以支持匿名 TRC-20合约（#3172）。

- [TIP-138](https://github.com/tronprotocol/tips/blob/master/tip-138.md): 在波场虚拟机中实现 Pedersen 哈希计算指令，以支持匿名TRC-20合约（#3172）。
 
## 更新
- 修复从 DB 获取交易信息时 `getTransactioninfoByBlkNum`异常，增加检查 getInstance 是否为空值（#3165）。