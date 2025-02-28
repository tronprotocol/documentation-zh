# 账户权限管理

## 背景

[账户权限管理](https://github.com/tronprotocol/tips/blob/master/tip-16.md)功能允许权限分级，每个权限可以对应多个私钥。这使得实现账户的多人联合控制成为可能。

## 概念说明

该方案共包含三种权限级别，owner、witness以及active权限，其中owner权限具有执行所有合约的权限，witness权限用于超级代表出块，active是自定义权限(可以组合权限集合)，以下将详细说明。

### 结构说明

#### Account

```protobuf
message Account {
  ...
  Permission owner_permission = 31;
  Permission witness_permission = 32;
  repeated Permission active_permission = 33;
}
```

在账户结构中有三个权限属性，分别是 owner_permission、witness_permission 和 active_permission，其中 active_permission 是个列表，可以指定最多8个。

#### ContractType

```protobuf
message Transaction {
  message Contract {
    enum ContractType {
      AccountCreateContract = 0;
      ...
      AccountPermissionUpdateContract = 46;
    }
  }
}
```
ContractType(合约类型)的定义可以在[这里](https://github.com/tronprotocol/java-tron/blob/master/protocol/src/main/protos/core/Tron.proto)查看。
AccountPermissionUpdateContract类型的交易，用于更新账户权限。

#### AccountPermissionUpdateContract

```protobuf
message AccountPermissionUpdateContract {
  bytes owner_address = 1;
  Permission owner = 2;
  Permission witness = 3;
  repeated Permission actives = 4;
}
```

* `owner_address`：待修改权限的账户的地址
* `owner`：修改后的 owner 权限
* `witness`：修改后的 witness 权限(仅限witness使用)
* `actives`：修改后的 actives 权限

注意：该接口是覆盖原账户权限，因此，如果只想修改owner权限，witness及actives的也需要设置。

#### Permission

```protobuf
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

- `PermissionType`: 权限类型，目前仅支持三种权限
- `id`: 值由系统自动设置，Owner id=0, Witness id=1, Active id 从2开始递增分配。在执行合约时，通过该id来指定使用哪个权限，如使用owner权限，即将id设置为0
- `permission_name`: 权限名称，由用户设定，长度限制为32字节
- `threshold`: 阈值，只有当参与签名的权重之和超过域值才允许做相应的操作
- `parent_id`：目前只能为0
- `operations`：active权限使用，一个十六进制编码序列（小端字节序），32字节（256位），每一位代表一个ContractType的权限。第n位表示ID为n的ContractType的权限，其值为1表示拥有执行该ContractType的权限，其值为0则表示没有该权限。
    为了方便用户阅读，我们从二进制大端字节序开始说明如何计算operations的值。位数从0开始计数，从左到右对应ContractType的ID。将一个大端字节序的二进制序列转换为小端字节序的十六进制序列，即为operations的值。以下是一个示例，展示如何计算允许执行TransferContract（ID=1）和VoteWitnessContract（ID=4）的active权限的operations值。ContractType与其ID的映射关系可参见上述ContractType的定义链接。

    | Operations Allowed  | Binary Code(big-endian) | Binary Code(little-endian) | Hex Code(little-endian) |
    | ------------- | ------------- | ------------- | ------------- |
    | TransferContract(1) & VoteWitnessContract(4)  | 01001000 00000000 00000000 ...  | 00010010 00000000 00000000 ... | 12 00 00 ... |

- `keys`：共同拥有该权限的地址及权重，最多允许5个key

#### Key

```protobuf
message Key {
  bytes address = 1;
  int64 weight = 2;
}
```

* `address`：拥有该权限的地址
* `weight`：该地址对该权限拥有的权重

#### Transaction

```protobuf
message Transaction {
  ...
  int32 Permission_id = 5;
}
```

在交易中增加 `Permission_id`字段，与`Permission.id`相对应，用于指定使用哪个权限。默认为0，即owner权限。
不允许为1，因为witness权限仅用于出块，不用于对交易进行签名。

### Owner权限

OwnerPermission是账户的最高权限，用于控制用户的所有权、调整权限结构，Owner权限也可以执行所有合约。

Owner权限具有以下特性：

1. 拥有OwnerPermission的地址可以修改OwnerPermission。
2. 当OwnerPermission为空时，默认采用该账户的地址具有owner权限。
3. 账户新建时，自动将该账户的地址填充到OwnerPermission中，并默认域值为1，keys中仅包含该账户地址且权重为1。
4. 当执行合约时未指定permissionId时， 默认采用OwnerPermission。

### Witness权限

超级代表可使用该权限，管理出块节点。非超级代表账户无该权限。

使用场景示例：一个超级代表在云服务器上部署出块程序，为了账户安全，此时可以将出块权限赋予另一个地址。由于该地址仅具有出块权限，无TRX转出权限，即使该服务器上私钥被泄密，也不会出现TRX丢失。

出块节点的配置：当以witness身份部署一个节点时，需要将witness账户的私钥填入配置文件的`localwitness`项中，而`localWitnessAccountAddress`无需配置，直接注释，如下所示：
```
# config.conf
//localWitnessAccountAddress =
localwitness = [
  xxx // private key of the witness account
]
```

- 如果未修改witness权限，无需更改配置文件。
- 如果修改了witness权限，配置文件需做如下两项修改
    - `localwitness`需要更改为被授权witness权限的账户的私钥
    -  必须明确设置`localWitnessAccountAddress`为witness账户的地址

    以下是witness账户[TCbxHgibJutCjVZUprvexKZZ4Rc6sJ4Xrk](https://nile.tronscan.org/#/address/TCbxHgibJutCjVZUprvexKZZ4Rc6sJ4Xrk)将其witness权限授权给账户TSwCH45gi2HvtqDYX3Ff39yHeu5moEqQDJ的配置示例：
    ```
    #config.conf
    localWitnessAccountAddress = TCbxHgibJutCjVZUprvexKZZ4Rc6sJ4Xrk
    localwitness = [
      yyy // private key of TSwCH45gi2HvtqDYX3Ff39yHeu5moEqQDJ
    ]
    ```
    注意：当修改witness权限时，只能向`localwitness`添加一个私钥。
    

### Active权限

Active权限，用于提供一个权限的组合，比如提供一个只能执行创建账户、转账功能的权限。

Active权限有以下特性：

1. 拥有OwnerPermission的地址可以修改Active权限
2. 拥有执行AccountPermissionUpdateContract权限的地址也能够修改Active权限
3. 最多支持8个组合。
4. permission的id从2开始自动递增。
5. 账户新建时，自动创建一个Active权限，并将该账户的地址填充到其中，默认域值为1，keys中仅包含该账户地址且权重为1。

### 费用

1. 使用更新账户权限时，即 AccountPermissionUpdate 合约，收取100TRX。
2. 交易中包括两个及两个以上签名时，除交易费用外，另收取1TRX。
3. 可通过提议，修改以上费用。

## API

### 修改权限

`AccountPermissionUpdateContract`，修改权限步骤如下：

1. 使用接口`getaccount`查询账户，并获取原权限
2. 修改permission
3. 创建合约，签名
4. 发送交易

### http-demo

```json
http://{{host}}:{{port}}/wallet/accountpermissionupdate


{
  "owner_address": "41ffa9466d5bf6bb6b7e4ab6ef2b1cb9f1f41f9700",
  "owner": {
    "type": 0,
    "id": 0,
    "permission_name": "owner",
    "threshold": 2,
    "keys": [{
        "address": "41F08012B4881C320EB40B80F1228731898824E09D",
        "weight": 1
      },
      {
        "address": "41DF309FEF25B311E7895562BD9E11AAB2A58816D2",
        "weight": 1
      },
      {
        "address": "41BB7322198D273E39B940A5A4C955CB7199A0CDEE",
        "weight": 1
      }
    ]
  },
  "witness": {
      "type": 1,
      "id": 1,
      "permission_name": "witness",
      "threshold": 1,
      "keys": [{
          "address": "41F08012B4881C320EB40B80F1228731898824E09D",
          "weight": 1
        }
      ]
    },
  "actives": [{
    "type": 2,
    "id": 2,
    "permission_name": "active0",
    "threshold": 3,
    "operations": "7fff1fc0037e0000000000000000000000000000000000000000000000000000",
    "keys": [{
        "address": "41F08012B4881C320EB40B80F1228731898824E09D",
        "weight": 1
      },
      {
        "address": "41DF309FEF25B311E7895562BD9E11AAB2A58816D2",
        "weight": 1
      },
      {
        "address": "41BB7322198D273E39B940A5A4C955CB7199A0CDEE",
        "weight": 1
      }
    ]
  }]
}


```

### active权限中operations的计算示例

``` java
public static void main(String[] args) {

  //指定需要支持的合约id(查看proto中Transaction.ContractType定义)，这里包含除AccountPermissionUpdateContract（id=46）以外的所有合约
  Integer[] contractId = {0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 30, 31,
      32, 33, 41, 42, 43, 44, 45};
  List<Integer> list = new ArrayList<>(Arrays.asList(contractId));
  byte[] operations = new byte[32];
  list.forEach(e -> {
    operations[e / 8] |= (1 << e % 8);
  });

  //7fff1fc0033e0000000000000000000000000000000000000000000000000000
  System.out.println(ByteArray.toHexString(operations));
}
```

### 执行合约

1. 创建交易，与非多重签名交易的构建过程相同
2. 指定Permission_id，默认为0，表示owner-permission, [demo](https://github.com/tronprotocol/wallet-cli/commit/ff9122f2236f1ce19cbb9ba9f0494c8923a3d10c#diff-a63fa7484f62fe1d8fb27276c991a4e3R211)
3. 用户A签名，将签名后交易通过其他方式发送给B。
4. 用户B签名，将签名后交易通过其他方式发送给C。

…

n. 最后一个完成签名的用户，将交易广播到节点。

n+1. 节点验证所有签名的权重之和，如果大于等于域值则接受交易，否则拒绝交易


### 其他相关接口


#### 查询已签名地址

```text
curl -X POST  http://127.0.0.1:8090/wallet/getapprovedlist -d '{"transaction"}'

rpc GetTransactionApprovedList(Transaction) returns (TransactionApprovedList) { }
```

#### 查询交易签名权重

```shell
curl -X POST  http://127.0.0.1:8090/wallet/getsignweight -d '{"transaction"}'

rpc GetTransactionSignWeight (Transaction) returns (TransactionSignWeight) {}
```
