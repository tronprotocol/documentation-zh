# 账户权限管理

TRON 网络支持账户权限的细粒度控制，通过配置权限（owner、witness、active），可实现账户的联合控制、安全委托以及功能权限分离。以下文档详细介绍账户权限模型、合约结构、配置方式、以及常用接口调用。



## 功能概览

账户权限管理允许：

- 给账户设置多个权限层级；
- 每个权限对应一组地址及权重；
- 通过阈值机制实现权限控制；
- 灵活配置哪些地址可以执行哪些合约类型。

详细规范参见 [TIP-16: Account Permission Management](https://github.com/tronprotocol/tips/blob/master/tip-16.md)。



## 权限层级概念

TRON 中支持三类权限类型：

| 权限类型   | 说明                                 |
|------------|--------------------------------------|
| owner      | 账户最高权限，控制所有权及权限结构   |
| witness    | 超级代表权限，仅用于出块             |
| active     | 自定义权限，可指定功能权限组合       |



## 权限结构定义

### 1. 账户结构：`Account`

```
message Account {
  ...
  Permission owner_permission = 31;
  Permission witness_permission = 32;
  repeated Permission active_permission = 33;
}
```

说明：

- `owner_permission`：`owner` 权限（仅一个）；
- `witness_permission`：超级代表权限（仅一个）；
- `active_permission`：`active` 权限列表，最多支持 8 个。

### 2. 权限配置：`Permission`
```
message Permission {
  enum PermissionType {
    Owner = 0;
    Witness = 1;
    Active = 2;
  }
  PermissionType type = 1;
  int32 id = 2;
  string permission_name = 3;
  int64 threshold = 4;
  int32 parent_id = 5;
  bytes operations = 6;
  repeated Key keys = 7;
}

```

说明：

- `type`：权限类型（owner/witness/active）；
- `id`：权限 ID，系统自动分配；
    - `owner` = 0，`witness` = 1，`active` 从 2 起递增；
- `permission_name`：权限名称，最长 32 个字符；
- `threshold`：权限阈值，密钥权重总和 ≥ 该值时方可操作；
- `operations`：仅 `active` 权限使用，表示可执行的合约类型；
- `keys`：具备此权限的地址与权重（最多 5 个）。

### 3. 权限密钥结构：`Key`
```
message Key {
  bytes address = 1;
  int64 weight = 2;
}
```

- `address`：具备权限的地址；
- `weight`：该地址在该权限下的权重。

### 4. 权限更新交易：`AccountPermissionUpdateContract`
```
message AccountPermissionUpdateContract {
  bytes owner_address = 1;
  Permission owner = 2;
  Permission witness = 3;
  repeated Permission actives = 4;
}
```

- 此合约用于 **一次性更新账户的所有权限结构**；
- 即便只修改其中一种权限，也需完整设置其余字段。

### 5. 合约类型枚举：`ContractType`
```
enum ContractType {
  AccountCreateContract = 0;
  ...
  AccountPermissionUpdateContract = 46;
}
```
`active` 权限通过 `operations` 字段配置可执行哪些 `ContractType`。 `operations` 字段值的计算请参考[operations 值计算示例](#operations-value-calculation-example)。

`ContractType` 的详细信息如下(包括消息名、执行器、状态以及触发的业务)：

| # | ContractType | Proto Message(消息名) | Actuator(执行器) | 状态 | 触发的业务 |
|---|---|---|---|---|---|
| 0 | AccountCreateContract | AccountContract.AccountCreateContract | CreateAccountActuator | ✅ 启用 | 创建一个链上账户 |
| 1 | TransferContract | BalanceContract.TransferContract | TransferActuator | ✅ 启用 | TRX 转账 |
| 2 | TransferAssetContract | AssetIssueContractOuterClass.TransferAssetContract | TransferAssetActuator | ✅ 启用 | TRC10 代币转账 |
| 3 | VoteAssetContract |  |  | 🚫 禁用(未实现Actuator)  |  |
| 4 | VoteWitnessContract | WitnessContract.VoteWitnessContract | VoteWitnessActuator | ✅ 启用 | 用账户的 TronPower 为 SR 投票,刷新投票记录(下次 maintenance 生效) |
| 5 | WitnessCreateContract | WitnessContract.WitnessCreateContract | WitnessCreateActuator | ✅ 启用 | 申请成为超级代表候选人，写入 witness store |
| 6 | AssetIssueContract | AssetIssueContractOuterClass.AssetIssueContract | AssetIssueActuator | ✅ 启用 | 发行 TRC10 代币,按 ICO 规则冻结募集期余额 |
| 8 | WitnessUpdateContract | WitnessContract.WitnessUpdateContract | WitnessUpdateActuator | ✅ 启用 | 更新 SR 的官网 URL |
| 9 | ParticipateAssetIssueContract | AssetIssueContractOuterClass.ParticipateAssetIssueContract | ParticipateAssetIssueActuator | ✅ 启用 | 在 ICO 期间用 TRX 认购 TRC10 代币 |
| 10 | AccountUpdateContract | AccountContract.AccountUpdateContract | UpdateAccountActuator | ✅ 启用 | 修改账户名(受 AllowUpdateAccountName 约束) |
| 11 | FreezeBalanceContract | BalanceContract.FreezeBalanceContract | FreezeBalanceActuator | 🚫 禁用(`supportUnfreezeDelay` 启用后链拒绝) | Stake 1.0:冻结 TRX 换取 Bandwidth/Energy,并可委托给他人 |
| 12 | UnfreezeBalanceContract | BalanceContract.UnfreezeBalanceContract | UnfreezeBalanceActuator | ✅ 启用 | Stake 1.0:到期后解冻 TRX,释放对应资源、清除得票 |
| 13 | WithdrawBalanceContract | BalanceContract.WithdrawBalanceContract | WithdrawBalanceActuator | ✅ 启用 | 领取 SR 出块 / 投票奖励到余额 |
| 14 | UnfreezeAssetContract | AssetIssueContractOuterClass.UnfreezeAssetContract | UnfreezeAssetActuator | ✅ 启用 | 发行人解冻 ICO 时冻结的 TRC10 代币份额 |
| 15 | UpdateAssetContract | AssetIssueContractOuterClass.UpdateAssetContract | UpdateAssetActuator | ✅ 启用 | 更新 TRC10 代币的 description / url / 免费带宽配额 |
| 16 | ProposalCreateContract | ProposalContract.ProposalCreateContract | ProposalCreateActuator | ✅ 启用 | SR 发起链上参数提案,写入 ProposalStore 等待投票 |
| 17 | ProposalApproveContract | ProposalContract.ProposalApproveContract | ProposalApproveActuator | ✅ 启用 | SR 对提案投赞成/取消票 |
| 18 | ProposalDeleteContract | ProposalContract.ProposalDeleteContract | ProposalDeleteActuator | ✅ 启用 | 提案发起人撤回自己创建的提案 |
| 19 | SetAccountIdContract | AccountContract.SetAccountIdContract | SetAccountIdActuator | ✅ 启用 | 为账户设置唯一 account_id(仅可设置一次) |
| 20 | CustomContract  |  |  | 🚫 禁用(未实现Actuator)  |  |
| 30 | CreateSmartContract | SmartContractOuterClass.CreateSmartContract | VMActuator | ✅ 启用 | 部署智能合约 |
| 31 | TriggerSmartContract | SmartContractOuterClass.TriggerSmartContract | VMActuator | ✅ 启用 | 调用智能合约 |
| 32 | GetContract |  |  | 🚫 禁用(未实现Actuator)  |  |
| 33 | UpdateSettingContract | SmartContractOuterClass.UpdateSettingContract | UpdateSettingContractActuator | ✅ 启用 | 合约所有者修改合约的 consume_user_resource_percent(用户承担能量比例) |
| 41 | ExchangeCreateContract | ExchangeContract.ExchangeCreateContract | ExchangeCreateActuator | ✅ 启用 | 创建 Bancor 交易对, 为两种资产初始注入流动性 |
| 42 | ExchangeInjectContract | ExchangeContract.ExchangeInjectContract | ExchangeInjectActuator | ✅ 启用 | 向已有交易对继续注入流动性, 按 Bancor 算法扣减双方资产 |
| 43 | ExchangeWithdrawContract | ExchangeContract.ExchangeWithdrawContract | ExchangeWithdrawActuator | ✅ 启用 | 交易对创建人按比例赎回交易对中双方资产 |
| 44 | ExchangeTransactionContract | ExchangeContract.ExchangeTransactionContract | ExchangeTransactionActuator | 🚫 禁用 | 通过 Bancor 交易对进行资产兑换 |
| 45 | UpdateEnergyLimitContract | SmartContractOuterClass.UpdateEnergyLimitContract | UpdateEnergyLimitContractActuator | ✅ 启用 | 合约所有者更新合约的 origin_energy_limit(合约所有者愿意为每一笔合约调用交易承担的能量消耗上限) |
| 46 | AccountPermissionUpdateContract | AccountContract.AccountPermissionUpdateContract | AccountPermissionUpdateActuator | ✅ 启用 | 更新账户权限:owner/witness/active |
| 48 | ClearABIContract | SmartContractOuterClass.ClearABIContract | ClearABIContractActuator | ✅ 启用 | 合约所有者清空合约 ABI |
| 49 | UpdateBrokerageContract | StorageContract.UpdateBrokerageContract | UpdateBrokerageActuator | ✅ 启用 | SR 调整对投票者的佣金比例(0-100%) |
| 51 | ShieldedTransferContract | ShieldContract.ShieldedTransferContract | ShieldedTransferActuator | 🚫 禁用(`getAllowShieldedTransaction` 未开启) | ZK-SNARK 匿名转账(透明 in + 匿名 spend/receive + 透明 out) |
| 52 | MarketSellAssetContract | MarketContract.MarketSellAssetContract | MarketSellAssetActuator | 🚫 禁用(`getAllowMarketTransaction` 未开启) | 内置订单簿挂限价卖单(sell / buy 两种资产 + 价格) |
| 53 | MarketCancelOrderContract | MarketContract.MarketCancelOrderContract | MarketCancelOrderActuator | 🚫 禁用(`getAllowMarketTransaction` 未开启) | 撤销自己挂出的未成交订单,退回剩余资产 |
| 54 | FreezeBalanceV2Contract | BalanceContract.FreezeBalanceV2Contract | FreezeBalanceV2Actuator | ✅ 启用 | Stake 2.0:冻结 TRX 得到 Bandwidth/Energy, 资源与 TronPower 分离 |
| 55 | UnfreezeBalanceV2Contract | BalanceContract.UnfreezeBalanceV2Contract | UnfreezeBalanceV2Actuator | ✅ 启用 | Stake 2.0:发起解质押,进入解冻等待期 |
| 56 | WithdrawExpireUnfreezeContract | BalanceContract.WithdrawExpireUnfreezeContract | WithdrawExpireUnfreezeActuator | ✅ 启用 | 提取已过等待期的解冻 TRX 到账户余额 |
| 57 | DelegateResourceContract | BalanceContract.DelegateResourceContract | DelegateResourceActuator | ✅ 启用 | Stake 2.0:把自己已质押的 Bandwidth/Energy 委托给其他地址(可设锁定期) |
| 58 | UnDelegateResourceContract | BalanceContract.UnDelegateResourceContract | UnDelegateResourceActuator | ✅ 启用 | Stake 2.0:从他人处回收先前委托的资源 |
| 59 | CancelAllUnfreezeV2Contract | BalanceContract.CancelAllUnfreezeV2Contract | CancelAllUnfreezeV2Actuator | ✅ 启用 | 一次性取消账户所有处于等待期的 V2 解冻,剩余份额重新质押 | 

## 各权限类型说明
### `owner` 权限（账户主控）
- 拥有账户的全部控制权；
- 可修改任意权限结构（包括自己）；
- 创建账户时自动设置，默认阈值为 1，包含账户本身地址；
- 默认情况下，未指定 `Permission_id` 的交易使用 `owner` 权限。

### `witness` 权限（出块权限）
- 仅超级代表，超级代表合伙人和超级代表候选人地址可用；
- 控制出块节点，不具备资金转出等操作权限；
- 可将出块权限授权给其他地址以提升账户安全性；
- 必须且只能包含一个 key。

#### 超级代表节点配置示例：
```
# config.conf
//localWitnessAccountAddress = TMK5c1jd...m6FXFXEz  # TRON 地址
localwitness = [
  xxx  # TMK5c1jd...m6FXFXEz 地址的私钥
]
```
若修改了 `witness` 权限，则：
```
localWitnessAccountAddress = TSMC4YzU...PBebBk2E
localwitness = [
  yyy  # TSMC4YzU...PBebBk2E 地址的私钥
]
```
>**注意**：`localwitness` 中只允许配置一个私钥。

### Active 权限（功能权限组合）
- 可组合合约权限，划分子权限给不同角色；
- 最多支持 8 个 `active` 权限配置；
- 权限 ID 从 2 开始递增；
- 默认创建账户时生成一个 `active` 权限，默认阈值为 1，仅包含自身地址。

## 操作费用
| 操作             | 收费标准       |
| -------------- | ---------- |
| 修改账户权限         | 100 TRX    |
| 交易（2 个及以上签名） | 额外收取 1 TRX |

以上费用可通过提案调整。

## 接口与操作示例
### 1. 修改权限操作流程
1. 使用 `getaccount` 查询当前账户权限结构；
2. 构造新的权限配置；
3. 调用 `AccountPermissionUpdateContract`；
4. 签名并广播交易。

**注意**: 当一个区块内有账户权限变更交易时，后续不会再打包该账户的其他交易，以保证账户权限变更交易从下一个区块才实际生效。

#### 示例请求：
```
POST http://{{host}}:{{port}}/wallet/accountpermissionupdate

{
  "owner_address": "41ffa946...",
  "owner": {
    "type": 0,
    "id": 0,
    "permission_name": "owner",
    "threshold": 2,
    "keys": [...]
  },
  "witness": {
    "type": 1,
    "id": 1,
    "permission_name": "witness",
    "threshold": 1,
    "keys": [...]
  },
  "actives": [
    {
      "type": 2,
      "id": 2,
      "permission_name": "active0",
      "threshold": 3,
      "operations": "7fff1fc0037e...",
      "keys": [...]
    }
  ]
}
```
### 2. operations 值计算示例 { #operations-value-calculation-example }
`operations` 是表示可执行合约权限的 32 字节十六进制字符串（小端）。
以下 Java 示例生成 ID 为 0-45 的合约权限：

```
Integer[] contractId = {0, 1, 2, ..., 45};
byte[] operations = new byte[32];
for (int id : contractId) {
  operations[id / 8] |= (1 << id % 8);
}
System.out.println(ByteArray.toHexString(operations));
```

>**注意**：上例中的 `contractId` 仅用于演示位运算写法。`ContractType` 的 ID 并不连续（7、21-29、34-40 等为空缺 ID），实际只能对链上 `AVAILABLE_CONTRACT_TYPE` 位图中已包含的合约类型置位，否则交易会被校验拒绝。`AVAILABLE_CONTRACT_TYPE` 大致对应上表的 # 列，但不含 ShieldedTransferContract(51)。

### 3. 交易执行流程
1. 创建交易；
2. 设置 `Permission_id`（默认为 0，即 `owner` 权限）；
3. A 用户签名，转发给 B；
4. B 用户签名，转发给 C；
5. ...
6. 最后一个用户签名后广播；
7. 节点验证签名权重总和是否 ≥ `threshold`，若是则接受交易。
>示例代码参考：[wallet-cli 用例](https://github.com/tronprotocol/wallet-cli/blob/develop/src/main/java/org/tron/common/utils/TransactionUtils.java)

## 辅助接口
### 查询已签名地址
```
POST /wallet/getapprovedlist

rpc GetTransactionApprovedList(Transaction) returns (TransactionApprovedList) {}
```
### 查询签名权重
```
POST /wallet/getsignweight

rpc GetTransactionSignWeight(Transaction) returns (TransactionSignWeight) {}
```
## 参考资料
- [TIP-16 权限管理提案](https://github.com/tronprotocol/tips/blob/master/tip-16.md)
- [Tron.proto 合约类型定义](https://github.com/tronprotocol/java-tron/blob/master/protocol/src/main/protos/core/Tron.proto)
