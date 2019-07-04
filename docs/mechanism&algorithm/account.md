
## 账户模型介绍

Tron采用账户模型。账户的唯一标识为地址address，对账户操作需要验证私钥签名。每个账户拥有TRX、Token余额及智能合约、带宽、能量等各种资源。通过发送交易可以增减TRX或者Token余额，需要消耗带宽；可以发布并拥有智能合约，也可以调用他人发布的智能合约，需要消耗能量。可以申请成为超级代表并被投票，也可以对超级代表进行投票。等等。Tron所有的活动都围绕账户进行。

## 创建账号的方式  

首先用钱包或者浏览器生成私钥和地址，生成方法见3.3和3.4，公钥可以丢弃。  
由已有老账户调用转账TRX(CreateTransaction2)、转让Token(TransferAsset2)或者创建账户(CreateAccount2)合约，并广播到网络后将完成账户创建的流程。  

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

<h3> Step </h3>
1.&nbsp;取交易的rawdata，转成byte[]格式。  
2.&nbsp;对rawdata进行sha256运算。  
3.&nbsp;用交易每个合约中地址对应的私钥（现在一般就是一个合约，一个私钥），对sha256的结果进行签名。  
4.&nbsp;把签名结果添加到交易中。  
<h3> Algorithm </h3>
1.&nbsp;ECDSA算法，SECP256K。  
2.&nbsp;签名示例数据    
```text    
    priKey:::8e812436a0e3323166e1f0e8ba79e19e217b2c4a53c970d4cca0cfb1078979df         
    pubKey::04a5bb3b28466f578e6e93fbfd5f75cee1ae86033aa4bbea690e3312c087181eb366f9a1d1d6a437a9bf9fc65ec853b9fd60fa322be3997c47144eb20da658b3d1         
    hash:::159817a085f113d099d3d93c051410e9bfe043cc5c20e43aa9a083bf73660145         
    r:::38b7dac5ee932ac1bf2bc62c05b792cd93c3b4af61dc02dbb4b93dacb758123f         
    s:::08bf123eabe77480787d664ca280dc1f20d9205725320658c39c6c143fd5642d         
    v:::0  
```   
注意：签名结果应该是65字节。 r 32字节， s 32字节，v 1个字节。  
3.&nbsp;fullnode节点收到交易后会进行验签，由hash 和 r、s、v计算出一个地址，与合约中的地址进行比较，相同则为验签通过。  
<h3> Demo </h3>
```
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