# 账户模型

## 账户模型介绍

TRON采用账户模型，账户的唯一标识为地址（address），对账户操作需要私钥签名。每个账户可以拥有TRX、TRC10 Token、带宽、能量等各种资源。通过发送交易可以增减TRX或者TRC10 Token余额,可以发布并拥有智能合约，也可以调用自己或者他人发布的智能合约。可以申请成为超级代表并被投票，也可以对超级代表进行投票等等。TRON所有的活动都围绕账户进行。

## 创建波场账号的方式

1. 首先用钱包或者浏览器生成私钥和地址，然后由已有老账户往目标地址发送TRX或者TRC10 Token，并广播到网络后将完成账户创建的流程。

2. 通过调用[wallet/createaccount](../api/http.md/#walletcreateaccount)系统合约，完成创建账户。

如果账户有足够的通过质押TRX获得的带宽，那么创建账户只会消耗带宽，否则，创建账户会烧掉0.1个TRX。

### 未激活状态
注意：由上述第一种方式创建的私钥和地址，比如TranLink钱包创建的账户，对于波场来说属于未激活的状态，也就是在java-tron逻辑中没有创建这个地址对应的账户对象。
如果此时往该地址发送智能合约交易，交易会成功，但是从新创建的账户查询交易记录会返回空，从调用方可以正常查询记录。当然新创建的地址发起交易也会失败，因为没有对应的账户对象，对应的带宽和能量也是为0。
激活一个已经创建的地址就通过往改地址发送TRX或TRC10系统专属合约token。

## 生成密钥对算法

Tron的签名算法为ECDSA，选用曲线为SECP256K1。其私钥为一个随机数，公钥为椭圆曲线上一个点。生成过程为，首先生成一个随机数d作为私钥，再计算P = d * G作为公钥；其中G为椭圆曲线的基点。

## 地址格式说明

用公钥P作为输入，计算SHA3得到结果H, 这里公钥长度为64字节，SHA3选用Keccak256。
取H的最后20字节，在前面填充一个字节0x41得到address。
对address进行basecheck计算得到最终地址，所有地址的第一个字符为T。
其中basecheck的计算过程为：首先对address计算sha256得到h1，再对h1计算sha256得到h2，取其前4字节作为check填充到address之后得到address||check，对其进行base58编码得到最终结果。
我们用的字符映射表为：
ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

## 签名说明

### 步骤

1. 取交易的rawdata，转成byte[]格式。
2. 对rawdata进行sha256运算。
3. 用交易发起账户的私钥，对sha256的结果进行签名。
4. 把签名结果添加到交易中。

### 算法

1. ECDSA算法，SECP256K。
2. 签名示例数据

```shell
    priKey:::8e812436a0e3323166e1f0e8ba79e19e217b2c4a53c970d4cca0cfb1078979df       
    pubKey::04a5bb3b28466f578e6e93fbfd5f75cee1ae86033aa4bbea690e3312c087181eb366f9a1d1d6a437a9bf9fc65ec853b9fd60fa322be3997c47144eb20da658b3d1       
    hash:::159817a085f113d099d3d93c051410e9bfe043cc5c20e43aa9a083bf73660145       
    r:::38b7dac5ee932ac1bf2bc62c05b792cd93c3b4af61dc02dbb4b93dacb758123f       
    s:::08bf123eabe77480787d664ca280dc1f20d9205725320658c39c6c143fd5642d       
    v:::0
```

注意：签名结果应该是65字节。 r 32字节， s 32字节，v 1个字节。

3. fullnode节点收到交易后会进行验签，由hash 和 r、s、v计算出一个地址，与交易rawData中的发起交易地址进行比较，相同则为验签通过。

### 示例

```java
public static Transaction sign(Transaction transaction, ECKey myKey) {
    Transaction.Builder transactionBuilderSigned = transaction.toBuilder();
    byte[] hash = sha256(transaction.getRawData().toByteArray());
    List<Contract> listContract = transaction.getRawData().getContractList();

    for (int i = 0; i < listContract.size(); i++) {
      ECDSASignature signature = myKey.sign(hash);
      ByteString bsSign = ByteString.copyFrom(signature.toByteArray());

      //Each contract may be signed with a different private key in the future.
      transactionBuilderSigned.addSignature(bsSign);
    }
  }
```
