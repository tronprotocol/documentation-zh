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
- `permission_name`：权限名称，最长 32 字节；
- `threshold`：权限域值，密钥权重总和 ≥ 该值时方可操作；
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
`active` 权限通过 `operations` 字段配置可执行哪些 `ContractType`，详见下方计算方法。

## 各权限类型说明
### `owner` 权限（账户主控）
- 拥有账户的全部控制权；
- 可修改任意权限结构（包括自己）；
- 创建账户时自动设置，默认阈值为 1，包含账户本身地址；
- 默认情况下，未指定 `permission_id` 的交易使用 `owner` 权限。

### `witness` 权限（出块权限）
- 仅超级代表，超级代表合伙人和超级代表候选人地址可用；
- 控制出块节点，不具备资金转出等操作权限；
- 可将出块权限授权给其他地址以提升账户安全性。

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
### 2. operations 值计算示例
`operations` 是表示可执行合约权限的 32 字节十六进制字符串（小端）。
以下 Java 示例生成将（ID=0-45）的合约权限加入：

```
Integer[] contractId = {0, 1, 2, ..., 45};
byte[] operations = new byte[32];
for (int id : contractId) {
  operations[id / 8] |= (1 << id % 8);
}
System.out.println(ByteArray.toHexString(operations));
```
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
