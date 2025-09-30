# HTTP API 接口
本章节介绍节点的HTTP API及其用法。

!!! 注意
    尽管 TRON 通过将 HTTP API 的 Content-Type 设置为 application/json 避免了 XSS 攻击，但仍有一些 API 没有输入验证。为了更好地保护用户数据安全，我们建议您在使用 API 的任何数据之前，先对其进行正确编码（尤其是当参数'visible'为true时）。  
    
    以下是一种典型的 XSS 防护方法：对来自 API 的所有数据在 HTML 中进行编码。使用诸如 `encodeURIComponent()` 或 `escape()` 等方法对数据进行编码，这可以将特殊字符转换为其 HTML 实体，防止浏览器将其解释为 HTML 代码。
    
    请务必为来自 API 的所有数据实施 XSS 防护，以确保用户数据的安全。我们了解您可能需要有关 XSS 防护的更多信息。建议您参考以下资源：[OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)。


TRON 节点的 HTTP API 支持两种地址格式，开发者可以通过 `visible` 参数来统一控制请求和响应中的地址格式。

`visible` 参数的设置决定了地址格式的规则：

* `"visible": false (默认值)`：参数和返回值中的地址必须为 HexString 格式。如果省略此参数，则按默认值处理。
* `"visible": true`：参数和返回值中的地址必须为 Base58Check 格式。

**设置方式**：

1. 对于 GET 请求或无参数的查询接口
将` visible=true` 作为 URL 查询参数追加到链接末尾。
```
http://127.0.0.1:8090/wallet/listexchanges?visible=true
```

2. 对于 POST 请求
将 ` "visible": true ` 添加到 JSON 请求体中。
```
curl -X POST http://127.0.0.1:8090/wallet/createtransaction -d
'{
    "owner_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
    "to_address": "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW",
    "amount": 1000000,
    "visible": true
}'
```



## Fullnode HTTP API
Fullnode HTTP API分类如下:

- [链上账户](#account)
- [转账和交易](#txn)
- [账户资源](#resources)
- [查询链上数据](#network)
- [智能合约](#contract)
- [TRC-10通证](#trc10)
- [投票和 SR](#sr)
- [TIP](#tip)
- [去中心化交易所](#dex)
- [Pending Pool](#pending-pool)


<a id="account"></a>
### 链上账户
下面是链上账户相关 API：

- [wallet/validateaddress](#walletvalidateaddress)
- [wallet/createaccount](#walletcreateaccount)
- [wallet/getaccount](#walletgetaccount)
- [wallet/updateaccount](#walletupdateaccount)
- [wallet/accountpermissionupdate](#walletaccountpermissionupdate)
- [wallet/getaccountbalance](#walletgetaccountbalance)
- [wallet/setaccountid](#walletsetaccountid)
- [wallet/getaccountbyid](#walletgetaccountbyid)

#### wallet/validateaddress
作用：验证一个 TRON 地址是否有效。此接口非常适用于在应用前端或后端发送交易前，预先检查用户输入的地址是否合法。
```
curl -X POST  http://127.0.0.1:8090/wallet/validateaddress -d '{"address": "4189139CB1387AF85E3D24E212A008AC974967E561"}'
```
参数：`address`：可以是 Base58Checksum、hexString、base64 格式

返回值：地址正确或者错误，示例：
```
#正确示例
{
    "result": true,
    "message": "Hex string format"
}

#错误示例
{
    "result": false,
    "message": "Invalid address"
}
```


#### wallet/createaccount
作用：创建账号，一个已经激活的账号创建一个新账号。如果创建者账号有足够的通过质押 TRX 获得的带宽，那么创建账户只会消耗带宽，否则，会烧掉 0.1 个 TRX 来支付带宽费用，同时需要额外支付 1 TRX 的创建费用。
```
curl -X POST  http://127.0.0.1:8090/wallet/createaccount -d '{"owner_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292", "account_address": "41e552f6487585c2b58bc2c9bb4492bc1f17132cd0"}'
```
参数：

- `owner_address` 是创建者的地址，必须是一个已在链上激活的账户。
- `account_address` 是待激活的新账户地址。此地址必须预先在链下生成好。
- `Permission_id` 可选参数，在使用账户管理权限签名时使用。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：未签名的创建账号的 Transaction

#### wallet/getaccount
作用：查询并返回一个指定 TRON 账户的完整链上信息(包括余额、资源、权限、资产在内的所有账户详情)。
```
curl -X POST  http://127.0.0.1:8090/wallet/getaccount -d '{"address": "41E552F6487585C2B58BC2C9BB4492BC1F17132CD0"}'
```
参数：

* `address` 需要查询的账户地址。
* `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为HexString。

返回值：Account 对象

#### wallet/updateaccount

作用：更新或设置一个指定 TRON 账户的链上名称 (`account_name`)。
```
curl -X POST  http://127.0.0.1:8090/wallet/updateaccount -d '{"account_name": "0x7570646174654e616d6531353330383933343635353139" ,"owner_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292"}'
```
参数：

- `account_name` 是账号名称，默认为 HexString格式
- `owner_address` 是要修改名称的账号地址，默认为 HexString 格式
- `Permission_id` 可选参数, 在使用账户管理权限签名时使用。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：未签名的修改名称 Transaction


#### wallet/accountpermissionupdate
作用：修改一个账户的权限结构。
```
curl -X POST  http://127.0.0.1:8090/wallet/accountpermissionupdate -d
'{
    "owner_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
    "owner": {
        "type": 0,
        "permission_name": "owner",
        "threshold": 1,
        "keys": [{
            "address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
            "weight": 1
        }]
    },
    "witness": {
        "type": 1,
        "permission_name": "witness",
        "threshold": 1,
        "keys": [{
            "address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
            "weight": 1
        }]
    },
    "actives": [{
        "type": 2,
        "permission_name": "active",
        "threshold": 2,
        "operations": "7fff1fc0033e0000000000000000000000000000000000000000000000000000",
        "keys": [{
            "address": "TNhXo1GbRNCuorvYu5JFWN3m2NYr9QQpVR",
            "weight": 1
        }, {
            "address": "TKwhcDup8L2PH5r6hxp5CQvQzZqJLmKvZP",
            "weight": 1
        }]
    }],
    "visible": true}'
```
参数：

- `owner_address`：创建合约的账户地址，默认为 HexString 格式
- `owner`：账户 owner 权限的分配信息
- `witness`：出块权限的分配信息，如果不是超级代表（Super Representative，简称 SR），不需要设置
- `actives`：其他功能权限的分配信息
- `visible`：设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：未签名的 transaction

#### wallet/getaccountbalance
作用：查询一个 TRON 账户在**过去某个特定区块高度**的 TRX 余额。

目前官方以下节点支持查询：

* 13.228.119.63
* 18.139.193.235
* 18.141.79.38
* 18.139.248.26

本地节点需要在配置文件中开启 `storage.balance.history.lookup= true`。
```
curl -X POST  http://127.0.0.1:8090/wallet/getaccountbalance -d
'{
    "account_identifier": {
        "address": "TLLM21wteSPs4hKjbxgmH1L6poyMjeTbHm"
    },
    "block_identifier": {
        "hash": "0000000000010c4a732d1e215e87466271e425c86945783c3d3f122bfa5affd9",
        "number": 68682
    },
    "visible": true
}'
```

参数： 

* `account_identifier.address`: 要查询的账户地址。
* `block_identifier.hash`: 目标区块的哈希值。
* `block_identifier.number`: 目标区块的高度（块号）。
* `visible`：设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值示例：
```
{
    "balance": 64086449348265042,
    "block_identifier": {
        "hash": "0000000000010c4a732d1e215e87466271e425c86945783c3d3f122bfa5affd9",
        "number": 68682
    }
}
```

#### wallet/setaccountid
作用：为指定的TRON账户设置或更新一个自定义的**账户ID (`account_id`)**。
```
curl -X POST  http://127.0.0.1:8090/wallet/setaccountid -d '{
"owner_address":"41a7d8a35b260395c14aa456297662092ba3b76fc0","account_id":"6161616162626262"}'
```
参数：

- `owner_address`：是交易对创建者的地址，默认为 HexString 格式
- `account_id` accountid，默认为 HexString 格式
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：设置 `AccountID` 的 transaction

#### wallet/getaccountbyid
作用：通过accountId查询一个账号的信息
```
curl -X POST  http://127.0.0.1:8090/wallet/getaccountbyid -d
'{"account_id":"6161616162626262"}'
```
参数：`account_id`：默认为 HexString 格式

返回值：Account 对象

<a id="txn"></a>
### 转账和交易

下面是转账和交易相关 API：

- [wallet/createtransaction](#walletcreatetransaction)
- [wallet/broadcasttransaction](#walletbroadcasttransaction)
- [wallet/broadcasthex](#walletbroadcasthex)
- [wallet/getsignweight](#walletgetsignweight)
- [wallet/getapprovedlist](#walletgetapprovedlist)


#### wallet/createtransaction
作用： 创建一笔 TRX 转账的 Transaction，如果转账的 to 地址不存在，则在区块链上创建该账号
```
curl -X POST  http://127.0.0.1:8090/wallet/createtransaction -d '{"to_address": "41e9d79cc47518930bc322d9bf7cddd260a0260a8d", "owner_address": "41D1E7A6BC354106CB410E65FF8B181C600FF14292", "amount": 1000 }'
```
参数：

- `to_address` 是接收方地址。
- `owner_address` 是转出方地址（发送者）。
- `amount` 是转账金额，单位为 sun (1 TRX = 1,000,000 sun)。
- `Permission_id` 可选，在使用账户管理权限签名时使用。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：未签名的TRX转账交易


#### wallet/broadcasttransaction
作用：将一个已经完成签名的交易广播到 TRON 网络。
```
curl -X POST  http://127.0.0.1:8090/wallet/broadcasttransaction -d '{"signature":["97c825b41c77de2a8bd65b3df55cd4c0df59c307c0187e42321dcc1cc455ddba583dd9502e17cfec5945b34cad0511985a6165999092a6dec84c2bdd97e649fc01"],"txID":"454f156bf1256587ff6ccdbc56e64ad0c51e4f8efea5490dcbc720ee606bc7b8","raw_data":{"contract":[{"parameter":{"value":{"amount":1000,"owner_address":"41e552f6487585c2b58bc2c9bb4492bc1f17132cd0","to_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292"},"type_url":"type.googleapis.com/protocol.TransferContract"},"type":"TransferContract"}],"ref_block_bytes":"267e","ref_block_hash":"9a447d222e8de9f2","expiration":1530893064000,"timestamp":1530893006233}}'
```
参数：一个完整的已签名交易对象 (Signed Transaction)。它是在调用创建类接口（如 `wallet/createtransaction`）返回的未签名交易的基础上，添加了 signature 字段构成的。

返回值：

* 返回一个包含广播结果的 JSON 对象。
* 一个成功的响应通常包含 `"result": true`，表示您连接的这个节点已成功接收您的交易并开始向全网广播。

**重要提示**：`"result": true` 不代表交易已被区块链确认。它仅表示“已成功广播”。您需要通过` wallet/gettransactioninfobyid ｜wallet/gettransactionbyid` 接口使用 `txID` 来查询交易的最终状态（是否成功上链）。

#### wallet/broadcasthex
作用：将一个已经完成签名并序列化为十六进制字符串 (Hex)的交易进行广播。
```
curl -X POST  http://127.0.0.1:8090/wallet/broadcasthex -d '{"transaction":"0A8A010A0202DB2208C89D4811359A28004098A4E0A6B52D5A730802126F0A32747970652E676F6F676C65617069732E636F6D2F70726F746F636F6C2E5472616E736665724173736574436F6E747261637412390A07313030303030311215415A523B449890854C8FC460AB602DF9F31FE4293F1A15416B0580DA195542DDABE288FEC436C7D5AF769D24206412418BF3F2E492ED443607910EA9EF0A7EF79728DAAAAC0EE2BA6CB87DA38366DF9AC4ADE54B2912C1DEB0EE6666B86A07A6C7DF68F1F9DA171EEE6A370B3CA9CBBB00"}'
```
参数：`transaction`：一个包含了所有交易信息（包括签名）并已被序列化为 hex 的完整交易。

返回值：

* 返回一个包含广播结果的JSON对象。
* 一个成功的响应通常包含 `"result": true`，表示您连接的这个节点已成功接收您的交易并开始向全网广播。

**重要提示**：`"result": true` 不代表交易已被区块链确认。它仅表示“已成功广播”。您需要通过 ` wallet/gettransactioninfobyid ｜wallet/gettransactionbyid ` 接口使用 `txID` 来查询交易的最终状态（是否成功上链）。


#### wallet/getsignweight
作用：检查一个使用账户管理权限 (Account management Permission) 的交易的当前签名状态。

当交易发起账户设置了账户管理权限后，该交易可能需要多个私钥签名才能被广播。此接口用于在集齐所有必需的签名之前，随时检查当前已收集到的签名权重是否达到了该权限设定的阈值。因此，它是处理此类交易时一个关键的预广播检查工具。

```
curl -X POST  http://127.0.0.1:8090/wallet/getsignweight -d '{
    "signature": [
        "e0bd4a60f1b3c89d4da3894d400e7e32385f6dd690aee17fdac4e016cdb294c5128b66f62f3947a7182c015547496eba95510c113bda2a361d811b829343c36501",
        "596ead6439d0f381e67f30b1ed6b3687f2bd53ce5140cdb126cfe4183235804741eeaf79b4e91f251fd7042380a9485d4d29d67f112d5387bc7457b355cd3c4200"
    ],
    "txID": "0ae84a8439f5aa8fd2c458879a4031a7452aebed8e6e99ffbccd26842d4323c4",
    "raw_data": {
        "contract": [{
            "parameter": {
                "value": {
                    "amount": 1000000,
                    "owner_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
                    "to_address": "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW"
                },
                "type_url": "type.googleapis.com/protocol.TransferContract"
            },
            "type": "TransferContract"
        }],
        "ref_block_bytes": "163d",
        "ref_block_hash": "77ef4ace148b05ba",
        "expiration": 1555664823000,
        "timestamp": 1555664763418
    },
    "raw_data_hex": "0a02163d220877ef4ace148b05ba40d8c5e5a6a32d5a69080112630a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412320a1541a7d8a35b260395c14aa456297662092ba3b76fc01215415a523b449890854c8fc460ab602df9f31fe4293f18c0843d2802709af4e1a6a32d",
    "visible": true}'
```
参数：一个完整的、包含了**一个或多个签名**的交易对象。

返回值：返回一个 JSON 对象，已签名权重是否达到阈值（即是否满足验签标准），签名地址列表，permission 的详细信息，已签名的权重及交易信息。

#### wallet/getapprovedlist
作用：在账户管理权限流程中，用于查询并返回一个交易的已签名地址列表。

此接口与 `wallet/getsignweight` 功能相似，但其主要目的是快速获取已提供有效签名的参与方列表，以跟踪签名收集进度。

```
curl -X POST  http://127.0.0.1:8090/wallet/getapprovedlist -d '{
    "signature": [
        "e0bd4a60f1b3c89d4da3894d400e7e32385f6dd690aee17fdac4e016cdb294c5128b66f62f3947a7182c015547496eba95510c113bda2a361d811b829343c36501",
        "596ead6439d0f381e67f30b1ed6b3687f2bd53ce5140cdb126cfe4183235804741eeaf79b4e91f251fd7042380a9485d4d29d67f112d5387bc7457b355cd3c4200"
    ],
    "txID": "0ae84a8439f5aa8fd2c458879a4031a7452aebed8e6e99ffbccd26842d4323c4",
    "raw_data": {
        "contract": [{
            "parameter": {
                "value": {
                    "amount": 1000000,
                    "owner_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
                    "to_address": "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW"
                },
                "type_url": "type.googleapis.com/protocol.TransferContract"
            },
            "type": "TransferContract"
        }],
        "ref_block_bytes": "163d",
        "ref_block_hash": "77ef4ace148b05ba",
        "expiration": 1555664823000,
        "timestamp": 1555664763418
    },
    "raw_data_hex": "0a02163d220877ef4ace148b05ba40d8c5e5a6a32d5a69080112630a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412320a1541a7d8a35b260395c14aa456297662092ba3b76fc01215415a523b449890854c8fc460ab602df9f31fe4293f18c0843d2802709af4e1a6a32d",
    "visible": true}'
```
参数：一个完整的、包含了一个或多个签名的交易对象。

返回值：返回一个 JSON 对象，其中包含了已批准的地址列表和交易的整体签名状态。

<a id="resources"></a>
### 帐户资源
下面是链上资源相关 API：

- [wallet/getaccountresource](#walletgetaccountresource)
- [wallet/getaccountnet](#walletgetaccountnet)
- [wallet/unfreezebalance](#walletunfreezebalance)
- [wallet/getdelegatedresource](#walletgetdelegatedresource)
- [wallet/getdelegatedresourceaccountindex](#walletgetdelegatedresourceaccountindex)
- [wallet/freezebalancev2](#walletfreezebalancev2)
- [wallet/unfreezebalancev2](#walletunfreezebalancev2)
- [wallet/cancelallunfreezev2](#walletcancelallunfreezev2)
- [wallet/delegateresource](#walletdelegateresource)
- [wallet/undelegateresource](#walletundelegateresource)
- [wallet/withdrawexpireunfreeze](#walletwithdrawexpireunfreeze)
- [wallet/getavailableunfreezecount](#walletgetavailableunfreezecount)
- [wallet/getcanwithdrawunfreezeamount](#walletgetcanwithdrawunfreezeamount)
- [wallet/getcandelegatedmaxsize](#walletgetcandelegatedmaxsize)
- [wallet/getdelegatedresourcev2](#walletgetdelegatedresourcev2)
- [wallet/getdelegatedresourceaccountindexv2](#walletgetdelegatedresourceaccountindexv2)


#### wallet/getaccountresource
作用：查询一个指定 TRON 账户的**资源信息**，包括其带宽、能量、投票权以及相关的质押等信息。
```
curl -X POST  http://127.0.0.1:8090/wallet/getaccountresource -d {"address" : "419844f7600e018fd0d710e2145351d607b3316ce9"}
```
参数：

- `address`：查询账户的地址，默认为 HexString 格式。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个包含账户所有资源相关信息的 JSON 对象。


#### wallet/getaccountnet
作用：查询一个指定 TRON 账户的**带宽资源**详情。
```
curl -X POST  http://127.0.0.1:8090/wallet/getaccountnet -d '{"address": "4112E621D5577311998708F4D7B9F71F86DAE138B5"}'
```
参数：

- `address`  查询账户的地址，默认为 HexString 格式。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个包含账户所有带宽相关信息的 JSON 对象。

#### wallet/freezebalance
作用：该接口是 TRON Stake 1.0 阶段的产物，已被正式废弃。所有新的质押操作请使用`freezebalancev2`。


#### wallet/unfreezebalance
作用：解质押 Stake1.0 阶段质押并已经结束质押期的 TRX，会同时失去这部分 TRX 带来的带宽和投票权
```
curl -X POST http://127.0.0.1:8090/wallet/unfreezebalance -d '{
"owner_address":"41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
"resource": "BANDWIDTH",
"receiver_address":"414332f387585c2b58bc2c9bb4492bc1f17342cd1"
}'
```
参数：

- `owner_address`是解质押 TRX 账号的地址，默认为 HexString 格式
- `resource`可以是 `BANDWIDTH` 或者 `ENERGY`
- `receiverAddress`表示受委托账户的地址，默认为 HexString 格式
- 可选参数`Permission_id`，在使用账户管理权限签名时使用。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个未签名的解质押交易对象 (Unsigned Transaction)。


#### wallet/getdelegatedresource
作用：Stake 1.0 中查询指定账户（代理方）为另一个特定账户（接收方）所代理的资源（能量或带宽）详情。
```
curl -X POST  http://127.0.0.1:8090/wallet/getdelegatedresource -d '
{
"fromAddress": "419844f7600e018fd0d710e2145351d607b3316ce9",
"toAddress": "41c6600433381c731f22fc2b9f864b14fe518b322f"
}'
```
参数：

- `fromAddress`：是要查询的账户地址，默认为 HexString 格式
- `toAddress`：代理对象的账户地址，默认为 HexString 格式
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：账户的资源代理的列表，列表的元素为 `DelegatedResource`

#### wallet/getdelegatedresourceaccountindex
作用：Stake1.0 中查询一个指定账户的代理以及被代理资源关系列表。
```
curl -X POST  http://127.0.0.1:8090/wallet/getdelegatedresourceaccountindex -d '
{
"value": "419844f7600e018fd0d710e2145351d607b3316ce9",
}'
```
参数：

- `value`：是要查询的账户地址，默认为 HexString 格式。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：账户的资源代理概况，结构为 `DelegatedResourceAccountIndex`。

#### wallet/freezebalancev2
作用：**Stake 2.0** 质押 TRX。通过此操作，质押者不仅能获取指定的网络资源（能量或带宽），还将**同时获得**与质押 TRX 数量等同的**投票权 (TRON Power, TP)**，比例为 1 TRX : 1 TP。
```
curl -X POST http://127.0.0.1:8090/wallet/freezebalancev2 -d
'{
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
    "frozen_balance": 10000,
    "resource": "BANDWIDTH"
}'
```

参数： 

- `owner_address`: 质押 TRX 账号的地址, HEX 格式或 Base58Check 格式
- `frozen_balance`: 质押 TRX 的数量, 单位为 sun
- `resource`: 质押 TRX 获取资源的类型, 可以是 `BANDWIDTH` 或者 `ENERGY`
- `permission_id`: 可选参数，在使用账户管理权限签名时使用。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个未签名的质押交易对象 (Unsigned Transaction)。

#### wallet/unfreezebalancev2

作用： 解质押通过 Stake2.0 机制质押的 TRX, 释放所相应数量的带宽和能量，同时回收相应数量的投票权 (TP)。
```
curl -X POST http://127.0.0.1:8090/wallet/unfreezebalancev2 -d
'{
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
    "unfreeze_balance": 1000000,
    "resource": "BANDWIDTH"
}'
```

参数：

- `owner_address`: 解质押 TRX 账号的地址, HEX 格式或 Base58Check 格式
- `resource`: 资源类型, `BANDWIDTH` 或者 `ENERGY`
- `unfreeze_balance`: 解质押的TRX数量，单位为 sun
- `permission_id`: 可选参数，在使用账户管理权限签名时使用。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个未签名的解质押交易对象 (Unsigned Transaction)。

#### wallet/cancelallunfreezev2

作用：立即取消账户所有正在进行中（未满 14 天）的解质押请求。此操作具有以下双重效果：

- 重新质押：所有被取消的、未到期的解质押本金将立即被重新质押，资源类型与之前保持一致。
- 提取到期 TRX：如果账户中存在其他已完成 14 天锁定期的解质押资金，本次操作会将其自动提取到账户余额中。

```
curl -X POST http://127.0.0.1:8090/wallet/cancelallunfreezev2 -d
'{
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1"
}'
```

参数：

- `owner_address`: 账户地址, HEX 格式或 Base58Check 格式。
- `permission_id`: 可选参数，在使用账户管理权限签名时使用。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：一个未签名的取消解质押交易对象 (Unsigned Transaction)。


#### wallet/delegateresource

作用： 将您通过质押TRX获得的**能量**或**带宽**资源代理给其他TRON账户, 但是投票权（TP）无法被代理

```
curl -X POST http://127.0.0.1:8090/wallet/delegateresource -d
'{
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
    "receiver_address": "41d1e7a6bc354106cb410e65ff8b181c600ff14292",
    "balance": 1000000,
    "resource": "BANDWIDTH",
    "lock": false
}'
```

参数：

- `owner_address`: 交易发起者账号的地址, HEX 格式或 Base58Check 格式。
- `receiver_address`: 资源的接收账户地址, HEX 格式或 Base58Check 格式。
- `balance`: 代理balance数量的 TRX 所对应的资源给目标地址, 单位为sun。
- `resource`: 代理的资源类型, `BANDWIDTH` 或者 `ENERGY`。
- `lock`: true 表示为该资源代理操作设置三天的锁定期，即资源代理给目标地址后的三天内不可以取消对其的资源代理，如果锁定期内，再次代理资源给同一目标地址，则锁定期将重新设置为3天。false 表示本次资源代理没有锁定期，可随时取消对目标地址的资源代理。
- `lock_period`: 锁定周期，以区块时间（3s）为单位，表示锁定多少个区块的时间，当 lock 为 `true` 时，该字段有效。如果代理锁定期为 1 天，则 `lock_period` 为：28800。
- `permission_id`: 可选参数，在使用账户管理权限签名时使用。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个未签名的资源代理交易对象 (Unsigned Transaction)。

#### wallet/undelegateresource

作用： 取消（收回）此前为其他账户代理的能量或带宽资源。

**重要提示**：如果一笔资源代理设置了时间锁 (`lock: true`) 并且尚未到期，调用此接口来取消该笔代理将会失败。您必须等待锁定期结束后才能执行此操作。

```
curl -X POST http://127.0.0.1:8090/wallet/undelegateresource -d
'{
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
    "receiver_address": "41d1e7a6bc354106cb410e65ff8b181c600ff14292",
    "balance": 1000000,
    "resource": "BANDWIDTH"
}'
```

参数：

- `owner_address`: 交易发起者账号的地址, HEX 格式或 Base58Check 格式。
- `receiver_address`: 资源的接收账户地址, 也就是取消为该地址的资源代理。 HEX 格式或 Base58Check 格式。
- `balance`: 取消代理 balance 数量的 TRX 所对应的资源, 单位为 sun。
- `resource`: 取消代理的资源类型, `BANDWIDTH` 或者 `ENERGY`。
- `permission_id`: 可选参数，在使用账户管理权限签名时使用。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个未签名的取消资源代理交易对象 (Unsigned Transaction)。

#### wallet/withdrawexpireunfreeze

作用：提取所有**已过锁定期**的解质押 TRX。
```
curl -X POST http://127.0.0.1:8090/wallet/withdrawexpireunfreeze -d
'{
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
}'
```

参数：

- `owner_address`: 交易发起者账号的地址, HEX 格式或 Base58Check 格式。
- `permission_id`: 可选参数，在使用账户管理权限签名时使用。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个未签名的提取到期解质押资金的交易对象 (Unsigned Transaction)。

#### wallet/getavailableunfreezecount

作用：查询一个指定账户当前还可发起**解质押操作的剩余次数**。由于TRON网络规定每个账户最多只能同时保有 **32 笔**处于 14 天锁定期内的解质押操作，此接口可用于在调用 `unfreezebalancev2` 之前，预先检查是否还有可用的“解质押额度”。

```
curl -X POST http://127.0.0.1:8090/wallet/getavailableunfreezecount -d
'{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "visible": true
}
'
```

参数：

- `owner_address`: 需要查询的账户地址。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个包含剩余次数的 JSON 对象。

#### wallet/getcanwithdrawunfreezeamount

作用：查询在某时间点可以提取的解质押本金数量。
```
curl -X POST http://127.0.0.1:8090/wallet/getcanwithdrawunfreezeamount -d
'{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "timestamp": 1667977444000,
  "visible": true
}
'
```

参数：

- `owner_address`: 交易发起者账号的地址。
- `timestamp`: 查询在该时间戳时，可提取的本金数量，单位为毫秒。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个包含可提取金额的 JSON 对象。


#### wallet/getcandelegatedmaxsize

作用：查询目标地址中指定类型资源的可代理数量，单位为 sun
```
curl -X POST http://127.0.0.1:8090/wallet/getcandelegatedmaxsize -d
'{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "type": 0,
  "visible": true
}
'
```

参数：

- `owner_address`: 需要查询的账户地址。
- `type`: 资源类型，0 为带宽，1 为能量。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个包含可代理份额最大值的 JSON 对象。

#### wallet/getdelegatedresourcev2

作用：查询在 Stake 2.0 机制下，指定账户（代理方）为另一个特定账户（接收方）所代理的资源详情。
```
curl -X POST http://127.0.0.1:8090/wallet/getdelegatedresourcev2 -d
'{
  "fromAddress": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "toAddress": "TPswDDCAWhJAZGdHPidFg5nEf8TkNToDX1",
  "visible": true
}
'
```

参数：

- `fromAddress`: 代理账户地址。
- `toAddress`: 资源的接收账户地址。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个 delegatedResource 数组，包含了两者在Stake 2.0下的所有资源代理记录。

#### wallet/getdelegatedresourceaccountindexv2
作用：查询在 Stake2.0 阶段，某地址的资源委托索引。返回两个列表，一个是该帐户将资源委托给的地址列表 (`toAddress`)，另一个是将资源委托给该帐户的地址列表 (`fromAddress`)
```
curl -X POST http://127.0.0.1:8090/wallet/getdelegatedresourceaccountindexv2 -d
'{
  "value": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "visible": true
}
'
```

参数：

- `value`: 账户地址。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个包含双向代理关系列表的 JSON 对象。包含两个列表，一个是该帐户将资源委托给的地址列表 (toAddress)，另一个是将资源委托给该帐户的地址列表 (fromAddress)

<a id="network"></a>
### 查询链上数据
下面是查询链上数据相关 API：

- [wallet/getnowblock](#walletgetnowblock)
- [wallet/getblock](#walletgetblock)
- [wallet/getblockbynum](#walletgetblockbynum)
- [wallet/getblockbyid](#walletgetblockbyid)
- [wallet/getblockbylatestnum](#walletgetblockbylatestnum)
- [wallet/getblockbylimitnext](#walletgetblockbylimitnext)
- [wallet/getblockbalance](#walletgetblockbalance)
- [wallet/gettransactionbyid](#walletgettransactionbyid)
- [wallet/gettransactioninfobyid](#walletgettransactioninfobyid)
- [wallet/gettransactioncountbyblocknum](#walletgettransactioncountbyblocknum)
- [wallet/gettransactioninfobyblocknum](#walletgettransactioninfobyblocknum)
- [wallet/listnodes](#walletlistnodes)
- [wallet/getnodeinfo](#walletgetnodeinfo)
- [wallet/getchainparameters](#walletgetchainparameters)
- [wallet/getenergyprices](#walletgetenergyprices)
- [wallet/getbandwidthprices](#walletgetbandwidthprices)
- [wallet/getmemofee](#walletgetmemofee)
- [wallet/getburntrx](#walletgetburntrx)

#### wallet/getnowblock
作用：查询最新块。
```
curl -X POST  http://127.0.0.1:8090/wallet/getnowblock
```
参数说明：无

返回值：最新的区块对象 (Block object)。

#### wallet/getblock
作用：根据区块高度或区块哈希查询区块信息。
```
curl -X POST  http://127.0.0.1:8090/wallet/getblock -d '{"detail":false}'
```
参数:

- `id_or_num`: 区块高度或者区块哈希，不设置表示查询最新区块
- `detail`: 默认为 false，表示只查询区块头信息，true 表示查询整个区块

返回值：区块对象 (Block object) 或仅包含区块头信息的对象。

#### wallet/getblockbynum
作用：通过指定的区块高度查询完整的区块信息。
```
curl -X POST  http://127.0.0.1:8090/wallet/getblockbynum -d '{"num": 1}'
```
参数：`num`：区块高度 (整型)。

返回值：指定高度的区块对象 (Block object)。

#### wallet/getblockbyid
作用：通过指定的区块ID（哈希）查询完整的区块信息。
```
curl -X POST  http://127.0.0.1:8090/wallet/getblockbyid -d '{"value": "0000000000038809c59ee8409a3b6c051e369ef1096603c7ee723c16e2376c73"}'
```
参数：`value`：区块的ID (hash)。

返回值：指定ID的区块对象 (Block object)。

#### wallet/getblockbylatestnum
作用：查询从最新区块开始，倒序的N个区块。
```
curl -X POST  http://127.0.0.1:8090/wallet/getblockbylatestnum -d '{"num": 5}'
```
参数：`num`：需要查询的区块数量。

返回值：一个包含多个区块对象的数组 (Block[])。

#### wallet/getblockbylimitnext
作用：分页查询指定高度范围内的区块列表。
```
curl -X POST  http://127.0.0.1:8090/wallet/getblockbylimitnext -d '{"startNum": 1, "endNum": 2}'
```
参数：

- `startNum`：起始块高度，包含此块
- `endNum`：截止块高度，不包含此此块

返回值：一个包含多个区块对象的数组 (Block[])。


#### wallet/getblockbalance
作用：获取一个指定区块中，所有交易引起的 TRX 余额变化详情。
```
curl -X POST  http://127.0.0.1:8090/wallet/getblockbalance -d
'{
    "hash": "000000000000dc2a3731e28a75b49ac1379bcc425afc95f6ab3916689fbb0189",
    "number": 56362,
    "visible": true
}'
```
参数:

 - `hash`: 区块的哈希值。
 - `number`: 区块的高度。与区块哈希必须精确匹配。

返回值：一个包含了该区块所有余额变动追踪信息的对象,示例如下：
```
{
    "block_identifier": {
        "hash": "000000000000dc2a3731e28a75b49ac1379bcc425afc95f6ab3916689fbb0189",
        "number": 56362
    },
    "timestamp": 1530060672000,
    "transaction_balance_trace": [
        {
            "transaction_identifier": "e6cabb1833cd1f795eed39d8dd7689eaa70e5bb217611766c74c7aa9feea80df",
            "operation": [
                {
                    "operation_identifier": 0,
                    "address": "TPttBLmFuykRi83y9HxDoEWxTQw6CCcQ4p",
                    "amount": -100000
                },
                {
                    "operation_identifier": 1,
                    "address": "TLsV52sRDL79HXGGm9yzwKibb6BeruhUzy",
                    "amount": 100000
                },
                {
                    "operation_identifier": 2,
                    "address": "TPttBLmFuykRi83y9HxDoEWxTQw6CCcQ4p",
                    "amount": -10000000
                },
                {
                    "operation_identifier": 3,
                    "address": "TMrysg7DbwR1M8xqhpaPdVCHCuWFhw7uk1",
                    "amount": 10000000
                }
            ],
            "type": "TransferContract",
            "status": "SUCCESS"
        }
    ]
}
```

#### wallet/gettransactionbyid
作用：通过交易 ID（哈希）查询一个已上链交易的完整信息。
```
curl -X POST  http://127.0.0.1:8090/wallet/gettransactionbyid -d '{"value": "d5ec749ecc2a615399d8a6c864ea4c74ff9f523c2be0e341ac9be5d47d7c2d62"}'
```
参数：`value`：交易 ID (hash)。

返回值：完整的交易对象 (Transaction object)。如果交易不存在，返回空对象。

#### wallet/gettransactioninfobyid
作用：根据交易 ID（哈希）查询交易的摘要信息，如费用、所在区块等。
```
curl -X POST  http://127.0.0.1:8090/wallet/gettransactioninfobyid -d '{"value" : "309b6fa3d01353e46f57dd8a8f27611f98e392b50d035cef213f2c55225a8bd2"}'
```
参数：`value`：交易 ID (hash)。

返回值：交易的摘要信息对象 (TransactionInfo object)，包含交易费用、所在区块高度、区块时间戳、合约执行结果等。

#### wallet/gettransactioncountbyblocknum
作用：查询指定区块高度上包含的交易总数。
```
curl -X POST  http://127.0.0.1:8090/wallet/gettransactioncountbyblocknum -d '{"num" : 100}'
```
参数：`num`：区块高度。

返回值：一个包含交易数量的对象，如 {"count": 50}。

#### wallet/gettransactioninfobyblocknum
作用：获取指定区块高度上所有交易的摘要信息列表。
```
curl -X POST  http://127.0.0.1:8090/wallet/gettransactioninfobyblocknum -d '{"num" : 100}'
```
参数：`num`：区块高度。

返回值：一个包含多个交易摘要信息对象的列表。

#### wallet/listnodes
作用：查询当前节点通过节点发现功能探测到的其他节点。
```
curl -X POST  http://127.0.0.1:8090/wallet/listnodes
```
参数：无

返回值：一个包含多个节点信息的数组，每个节点包含IP地址和端口。


#### wallet/getnodeinfo
作用：查看当前节点自身的运行状态和信息。
```
curl  http://127.0.0.1:8090/wallet/getnodeinfo
```
返回值：一个包含节点版本、网络状况、区块同步状态等信息的对象。

#### wallet/getchainparameters
作用：查询当前TRON网络的所有动态参数。
```
curl -X POST  http://127.0.0.1:8090/wallet/getchainparameters
```
返回值：一个包含所有链上参数及其当前值的列表。

#### wallet/getenergyprices
作用：查询历史上能量单价的变化记录。
```
curl -X POST  http://127.0.0.1:8090/wallet/getenergyprices
```
返回值：所有历史能量单价信息。每次单价变动以逗号分隔，冒号前为毫秒时间戳，冒号后为以 sun 为单位的能量单价。

#### wallet/getbandwidthprices
作用：查询历史上带宽单价的变化记录。
```
curl -X POST  http://127.0.0.1:8090/wallet/getbandwidthprices
```
返回值：所有历史带宽单价信息。每次单价变动以逗号分隔，冒号前为毫秒时间戳，冒号后为以 sun 为单位的带宽单价。

#### wallet/getmemofee
作用：查询历史上备注价格变化记录。
```
curl -X POST  http://127.0.0.1:8090/wallet/getmemofee
```
返回值：所有历史备注价格信息。每次价格变动以逗号分隔，冒号前为毫秒时间戳，冒号后为以 sun 为单位的备注价格。



#### wallet/getburntrx
作用：查询 TRON 网络创世以来累计燃烧的 TRX 总量。
```
curl -X POST  http://127.0.0.1:8090/wallet/getburntrx
```
返回值：燃烧的 TRX 数量，以 sun 为单位。


<a id="contract"></a>
### 智能合约
下面是智能合约相关API：

- [wallet/getcontract](#walletgetcontract)
- [wallet/getcontractinfo](#walletgetcontractinfo)
- [wallet/deploycontract](#walletdeploycontract)
- [wallet/triggersmartcontract](#wallettriggersmartcontract)
- [wallet/triggerconstantcontract](#wallettriggerconstantcontract)
- [wallet/updatesetting](#walletupdatesetting)
- [wallet/updateenergylimit](#walletupdateenergylimit)
- [wallet/clearabi](#walletclearabi)
- [wallet/estimateenergy](#walletestimateenergy)

#### wallet/getcontract
作用：通过合约地址获取合约的静态信息，如 ABI 和字节码。
```
curl -X POST  http://127.0.0.1:8090/wallet/getcontract -d '{"value":"4189139CB1387AF85E3D24E212A008AC974967E561"}'
```
参数：

- `value`：合约地址，默认为 HexString 格式。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：智能合约对象 (SmartContract)，包含ABI、部署字节码、名称等。

#### wallet/getcontractinfo
作用：通过合约地址获取合约的运行时信息。
```
curl -X POST  http://127.0.0.1:8090/wallet/getcontractinfo -d '{"value":"4189139CB1387AF85E3D24E212A008AC974967E561"}'
```
参数：

- `value`：合约地址，默认为 HexString 格式。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：查询链上的合约信息。与 `wallet/getcontract` 接口不同的是，该接口不仅返回 bytecode 还会返回合约的 runtime bytecode。runtime bytecode 相比 bytecode，不包含构造函数以及构造函数的参数信息。

#### wallet/deploycontract
作用：创建一笔部署智能合约的交易。
```
curl -X POST  http://127.0.0.1:8090/wallet/deploycontract -d '{"abi":"[{\"constant\":false,\"inputs\":[{\"name\":\"key\",\"type\":\"uint256\"},{\"name\":\"value\",\"type\":\"uint256\"}],\"name\":\"set\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"key\",\"type\":\"uint256\"}],\"name\":\"get\",\"outputs\":[{\"name\":\"value\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"}]","bytecode":"608060405234801561001057600080fd5b5060de8061001f6000396000f30060806040526004361060485763ffffffff7c01000000000000000000000000000000000000000000000000000000006000350416631ab06ee58114604d5780639507d39a146067575b600080fd5b348015605857600080fd5b506065600435602435608e565b005b348015607257600080fd5b50607c60043560a0565b60408051918252519081900360200190f35b60009182526020829052604090912055565b600090815260208190526040902054905600a165627a7a72305820fdfe832221d60dd582b4526afa20518b98c2e1cb0054653053a844cf265b25040029","parameter":"","call_value":100,"name":"SomeContract","consume_user_resource_percent":30,"fee_limit":10,"origin_energy_limit": 10,"owner_address":"41D1E7A6BC354106CB410E65FF8B181C600FF14292"}'
```
参数：

- `abi`：abi。
- `bytecode`：bytecode，需要是 HexString 格式。
- `parameter`：构造函数的参数列表，需要按照 ABI encoder 编码后转话为 HexString 格式。如果构造函数没有参数，该参数可以不用设置。
- `consume_user_resource_percent`：指定的使用该合约用户的资源占比，是[0, 100]之间的整数。如果是 0，则表示用户不会消耗资源。如果开发者资源消耗完了，才会完全使用用户的资源。
- `fee_limit`：最大消耗的 sun（1TRX = 1,000,000 sun）。
- `call_value`：本次调用往合约转账的 sun（1TRX = 1,000,000 sun）。
- `owner_address`：发起 deploycontract 的账户地址，默认为 HexString 格式。
- `name`：合约名。
- `origin_energy_limit`: 创建者设置的，在一次合约执行或创建过程中创建者自己消耗的最大的 energy，是大于 0 的整数。
- `call_token_value`:本次调用往合约中转账 TRC-10 币的数量，如果不设置 token_id，这项设置为 0 或者不设置。
- `token_id`:本次调用往合约中转账 TRC-10 币的 id，如果没有，不需要设置。
- `Permission_id`可选参数，多重签名时使用，设置交易多重签名时使用的 permissionId。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个包含了未签名部署交易的对象。

#### wallet/triggersmartcontract
作用：创建一笔调用智能合约函数的交易
```
curl -X POST  http://127.0.0.1:8090/wallet/triggersmartcontract -d '{"contract_address":"4189139CB1387AF85E3D24E212A008AC974967E561","function_selector":"set(uint256,uint256)","parameter":"00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002","fee_limit":10,"call_value":100,"owner_address":"41D1E7A6BC354106CB410E65FF8B181C600FF14292"}'
```
参数：

- `contract_address`：调用者的地址，默认为 HexString 格式。
- `function_selector`：函数签名，不能有空格。
- `parameter`：调用参数 [1,2] 的虚拟机格式，使用 remix 提供的 js 工具，将合约调用者调用的参数数组 [1,2] 转化为虚拟机所需要的参数格式
- `data`：与智能合约进行交互的数据，包括所调用的合约函数和参数。可以选择通过该字段，也可以选择通过 function_selector 和 parameter 进行合约交互，当 data 与 function_selector 同时存在时，使用 function_selector 进行合约交互。
- `fee_limit`：最大消耗的 sun（1TRX = 1,000,000 sun）。
- `call_value`：本次调用往合约转账的 sun（1TRX = 1,000,000 sun）。
- `owner_address`：发起 triggercontract 的账户地址，默认为 HexString 格式。
- `call_token_value`:本次调用往合约中转账 TRC-10 币的数量，如果不设置 token_id，这项设置为 0 或者不设置。
- `token_id`:本次调用往合约中转账 TRC-10 币的 id，如果没有，不需要设置。
- `Permission_id`可选参数，多重签名时使用，设置交易多重签名时使用的 permissionId。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个包含了未签名部署交易的对象。


#### wallet/triggerconstantcontract
作用：在本地节点模拟执行合约，用于数据查询、交易预执行或预估能量消耗，此操作不上链，不消耗资源。
```
curl -X POST  http://127.0.0.1:8090/wallet/triggerconstantcontract -d '{"contract_address":"4189139CB1387AF85E3D24E212A008AC974967E561","function_selector":"set(uint256,uint256)","parameter":"00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002","call_value":100,"owner_address":"41D1E7A6BC354106CB410E65FF8B181C600FF14292"}'
```
参数：

- `contract_address`：调用者的地址，默认为 HexString 格式。
- `function_selector`：函数签名，不能有空格。
- `parameter`：调用参数 [1,2] 的虚拟机格式，使用 remix 提供的 js 工具，将合约调用者调用的参数数组 [1,2] 转化为虚拟机所需要的参数格式
- `data`：合约字节码或者与智能合约进行交互的数据，包括所调用的合约函数和参数。可以选择通过该字段，也可以选择通过 function_selector 和 parameter 进行合约交互，当 data 与 function_selector 同时存在时，优先使用 function_selector。
- `owner_address`：发起 triggercontract 的账户地址，默认为 HexString 格式。
- `call_value`：本次调用往合约转账的 sun（1TRX = 1,000,000 sun）。
- `call_token_value`:本次调用往合约中转账 TRC-10 币的数量，如果不设置 token_id，这项设置为 0 或者不设置。
- `token_id`:本次调用往合约中转账 TRC-10 币的 id，如果没有，不需要设置。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：合约函数的返回值，经过 ABI 编码后的结果。


#### wallet/updatesetting
作用：更新已部署合约的 consume_user_resource_percent（调用者能量承担比例）。
```
curl -X POST  http://127.0.0.1:8090/wallet/updatesetting -d '{"owner_address": "419844f7600e018fd0d710e2145351d607b3316ce9", "contract_address": "41c6600433381c731f22fc2b9f864b14fe518b322f", "consume_user_resource_percent": 7}'
```
参数：

- `owner_address`：合约的所有者地址，默认为 HexString 格式。
- `contract_address`：要修改的合约的地址，默认为 HexString 格式。
- `consume_user_resource_percent`：指定的使用该合约用户的资源占比。
- `Permission_id`可选参数，多重签名时使用，设置交易多重签名时使用的 permissionId。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个包含了未签名更新交易的对象。

#### wallet/updateenergylimit
作用：更新已部署合约的 origin_energy_limit（开发者愿意为单次调用提供的能量上限）。
```
curl -X POST  http://127.0.0.1:8090/wallet/updateenergylimit -d '{"owner_address": "419844f7600e018fd0d710e2145351d607b3316ce9", "contract_address": "41c6600433381c731f22fc2b9f864b14fe518b322f", "origin_energy_limit": 7}'
```
参数：

- `owner_address`：合约的所有者地址，默认为 HexString 格式。
- `contract_address`：要修改的合约的地址，默认为  HexString 格式。
- `origin_energy_limit`：创建者设置的，在一次合约执行或创建过程中创建者自己消耗的最大的 energy。
- `Permission_id`可选参数，多重签名时使用，设置交易多重签名时使用的 permissionId。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个包含了未签名更新交易的对象。

#### wallet/clearabi
作用：创建一笔清除智能合约 ABI 的交易。
```
curl -X POST  http://127.0.0.1:8090/wallet/clearabi -d '{
"owner_address":"41a7d8a35b260395c14aa456297662092ba3b76fc0",
"contract_address":"417bcb781f4743afaacf9f9528f3ea903b3782339f"}'
```
参数：

- `owner_address`：创建合约的账户地址，默认为 HexString 格式
- `contract_address`：合约地址,默认为 HexString
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个未签名的交易对象

#### wallet/estimateenergy
作用：预估一次智能合约调用所需的能量。
```
curl -X POST  http://127.0.0.1:8090/wallet/estimateenergy -d '{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "contract_address": "TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs",
  "function_selector": "transfer(address,uint256)",
  "parameter": "00000000000000000000004115208EF33A926919ED270E2FA61367B2DA3753DA0000000000000000000000000000000000000000000000000000000000000032",
  "visible": true
}'
```

参数：

- `contract_address`，默认为 HexString 格式
- `function_selector`，函数签名，不能有空格
- `parameter`：调用参数 [1,2] 的虚拟机格式，使用 remix 提供的 js 工具，将合约调用者调用的参数数组 [1,2] 转化为虚拟机所需要的参数格式
- `data`：合约字节码或者与智能合约进行交互的数据，包括所调用的合约函数和参数。可以选择通过该字段，也可以选择通过 function_selector 和 parameter 进行合约交互，当 data 与 function_selector 同时存在时，优先使用 function_selector
- `fee_limit`：最大消耗的 sun（1TRX = 1,000,000 sun）
- `owner_address`：发起 triggercontract 的账户地址，默认为 HexString 格式
- `call_value`：本次调用往合约转账的 sun（1TRX = 1,000,000 sun）
- `call_token_value`:本次调用往合约中转账 TRC-10 币的数量，如果不设置 token_id，这项设置为 0 或者不设置
- `token_id`:本次调用往合约中转账 TRC-10 币的 id，如果没有，不需要设置
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个包含预估能量值的对象。


<a id="trc10"></a>
### TRC-10 通证
下面是 TRC-10 代币相关 API：

- [wallet/getassetissuebyaccount](#walletgetassetissuebyaccount)
- [wallet/getassetissuebyname](#walletgetassetissuebyname)
- [wallet/getassetissuelistbyname](#walletgetassetissuelistbyname)
- [wallet/getassetissuebyid](#walletgetassetissuebyid)
- [wallet/getassetissuelist](#walletgetassetissuelist)
- [wallet/getpaginatedassetissuelist](#walletgetpaginatedassetissuelist)
- [wallet/transferasset](#wallettransferasset)
- [wallet/participateassetissue](#walletparticipateassetissue)
- [wallet/createassetissue](#walletcreateassetissue)
- [wallet/unfreezeasset](#walletunfreezeasset)
- [wallet/updateasset](#walletupdateasset)


#### wallet/getassetissuebyaccount
作用：查询指定账户所发行的所有 TRC-10 代币。
```
curl -X POST  http://127.0.0.1:8090/wallet/getassetissuebyaccount -d '{"address": "41F9395ED64A6E1D4ED37CD17C75A1D247223CAF2D"}'
```

参数：

- `address`：发行者账户地址，默认为 HexString 格式。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：该接口返回一个包含了该地址发行的 TRC-10 代币列表的对象。

#### wallet/getassetissuebyname
作用：根据名称查询 TRC-10 代币。
```
curl -X POST  http://127.0.0.1:8090/wallet/getassetissuebyname -d '{"value": "44756354616E"}'
```
参数：`value`：代币名称，默认为 HexString 格式。

返回值：TRC-10 代币对象。


注意：Odyssey-v3.2开始，推荐使用 getassetissuebyid 或者 getassetissuelistbyname 替换此接口，因为从 3.2 开始将允许通证名称相同。如果存在相同的通证名称，此接口将会报错。

#### wallet/getassetissuelistbyname
作用：根据名称查询所有匹配的 TRC-10 代币列表。
```
curl -X POST  http://127.0.0.1:8090/wallet/getassetissuelistbyname -d '{"value": "44756354616E"}'
```
参数：`value`：代币名称，默认为 HexString 格式。

返回值：一个包含所有同名 TRC-10 代币对象的数组。

#### wallet/getassetissuebyid
作用：根据 ID 查询 TRC-10 代币
```
curl -X POST  http://127.0.0.1:8090/wallet/getassetissuebyid -d '{"value": "1000001"}'
```
参数：`value`：TRC-10 代币的 ID。

返回值：指定的 TRC-10 代币对象。


#### wallet/getassetissuelist
作用：查询全网所有的 TRC-10 代币列表。
```
curl -X POST  http://127.0.0.1:8090/wallet/getassetissuelist
```
参数：无

返回值：一个包含全网所有 TRC-10 代币对象的数组。

#### wallet/getpaginatedassetissuelist
作用：分页查询全网的 TRC-10 代币列表。
```
curl -X POST  http://127.0.0.1:8090/wallet/getpaginatedassetissuelist -d '{"offset": 0, "limit": 10}'
```
参数：

 - `offset`：分页查询的起始索引。
 - `limit`：本次查询期望返回的代币数量。

返回值：一个包含了分页结果的 TRC-10 代币对象的数组。

#### wallet/transferasset
作用：创建一笔 TRC-10 代币转账交易。
```
curl -X POST  http://127.0.0.1:8090/wallet/transferasset -d '{"owner_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292", "to_address": "41e552f6487585c2b58bc2c9bb4492bc1f17132cd0", "asset_name": "0x6173736574497373756531353330383934333132313538", "amount": 100}'
```
参数：

- `owner_address`是转出方地址。，默认为 HexString 格式。
- `to_address`是接收方地址，默认为 HexString 格式。
- `asset_name`是 TRC-10 代币 ID，默认为 HexString 格式。
- `amount`是 token 转账数量。
- `Permission_id`可选参数，多重签名时使用，设置交易多重签名时使用的 permissionId。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：一个未签名的 TRC-10 转账交易对象。


#### wallet/participateassetissue
作用：创建一笔参与 TRC-10 代币众筹的交易。

```
curl -X POST http://127.0.0.1:8090/wallet/participateassetissue -d '{
"to_address": "41e552f6487585c2b58bc2c9bb4492bc1f17132cd0",
"owner_address":"41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
"amount":100,
"asset_name":"3230313271756265696a696e67"
}'
```
参数：

- `to_address`是代币发行方地址，默认为 HexString 格式。
- `owner_address`是参与者地址（购买方），默认为HexString 格式
- `amount`是参与 token 的数量。
- `asset_name`是要参与的代币 ID，默认为 HexString 格式。
- `Permission_id`可选参数，多重签名时使用，设置交易多重签名时使用的 permissionId。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：一个未签名的参与众筹交易对象。

> 注意
> 当前的 `asset_name` 为 token 名称。当委员会通过 `AllowSameTokenName` 提议后 `asset_name` 改为 token ID 的 String 类型。


#### wallet/createassetissue
作用：创建一笔发行 TRC-10 代币的交易（成本为 1024 TRX）。
```
curl -X POST  http://127.0.0.1:8090/wallet/createassetissue -d '{
"owner_address":"41e552f6487585c2b58bc2c9bb4492bc1f17132cd0",
"name":"0x6173736574497373756531353330383934333132313538",
"abbr": "0x6162627231353330383934333132313538",
"total_supply" :4321,
"trx_num":1,
"num":1,
"start_time" : 1530894315158,
"end_time":1533894312158,
"description":"007570646174654e616d6531353330363038383733343633",
"url":"007570646174654e616d6531353330363038383733343633",
"free_asset_net_limit":10000,
"public_free_asset_net_limit":10000,
"frozen_supply":{"frozen_amount":1, "frozen_days":2}
}'
```
参数：

- `owner_address`发行人地址，默认为 HexString 格式。
- `name`是 token 名称，默认为 HexString 格式。
- `abbr`是 token 简称，默认为 HexString 格式。
- `total_supply`是发行总量。
- `trx_num`和`num`是 token 和 TRX 的最小单位兑换比。
- `start_time`和`end_time`是 token 发行起止时间。
- `description`是 token 说明，默认为 HexString 格式。
- `url` 是 token 发行方的官网，默认为 HexString 格式。
- `free_asset_net_limit`是 token 的总的免费带宽。
- `public_free_asset_net_limit` 是每个 token 拥护者能使用本 token 的免费带宽。
- `frozen_supply`是 token 发行者可以在发行的时候指定质押的 token。
- `Permission_id`可选参数，多重签名时使用，设置交易多重签名时使用的 permissionId。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：一个未签名的发行 TRC-10 代币交易对象。

#### wallet/unfreezeasset
作用：解质押已经结束质押期的 token
```
curl -X POST http://127.0.0.1:8090/wallet/unfreezeasset -d '{
"owner_address":"41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
}'
```
参数：

- `owner_address`是解质押 token 账号的地址，默认为 HexString 格式。
- `Permission_id`可选参数，多重签名时使用，设置交易多重签名时使用的 permissionId。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：一个未签名的解质押代币交易对象。

#### wallet/updateasset
作用：更新已发行的 TRC-10 代币的信息。
```
curl -X POST http://127.0.0.1:8090/wallet/updateasset -d '{
"owner_address":"41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
"description": ""，
"url": "",
"new_limit" : 1000000,
"new_public_limit" : 100
}'
```
参数：

- `owner_address` 是 token 发行人的地址，默认为 HexString 格式。
- `description` 是 token 的描述，默认为 HexString 格式。
- `url` 是 token 发行人的官网地址，默认为 HexString 格式。
- `new_limit` 是 token 每个持有人能够使用的免费带宽。
- `new_public_limit` 是该 token 全部的免费带宽。
- `Permission_id` 可选参数，多重签名时使用，设置交易多重签名时使用的 permissionId。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：一个未签名的更新代币信息交易对象。

<a id="sr"></a>
### 投票和超级代表
下面是投票和超级代表（SR）相关的 API：

- [wallet/createwitness](#walletcreatewitness)
- [wallet/updatewitness](#walletupdatewitness)
- [wallet/listwitnesses](#walletlistwitnesses)
- [wallet/withdrawbalance](#walletwithdrawbalance)
- [wallet/votewitnessaccount](#walletvotewitnessaccount)
- [wallet/getBrokerage](#walletgetbrokerage)
- [wallet/updateBrokerage](#walletupdatebrokerage)
- [wallet/getReward](#walletgetreward)
- [wallet/getnextmaintenancetime](#walletgetnextmaintenancetime)

#### wallet/createwitness
作用：创建一笔申请成为 SR 的交易。
```
curl -X POST  http://127.0.0.1:8090/wallet/createwitness -d '{"owner_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292", "url": "007570646174654e616d6531353330363038383733343633"}'
```
参数：

- `owner_address`是申请成为超级代表的账号地址，默认为 HexString 格式。
- `url`是官网地址，默认为 HexString 格式。
- 可选参数`Permission_id`，多重签名时使用，设置交易多重签名时使用的 permissionId。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：一个未签名的申请 SR 交易对象。


#### wallet/updatewitness
作用：更新超级代表网站 URL。
```
curl -X POST  http://127.0.0.1:8090/wallet/updatewitness -d '{
"owner_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292",
"update_url": "007570646174654e616d6531353330363038383733343633"
}'
```
参数：

- `owner_address`是创建人地址，默认为 HexString 格式。
- `update_url`是更新的官网的 url，默认为 HexString 格式。
- 可选参数`Permission_id`，多重签名时使用，设置交易多重签名时使用的 permissionId。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：一个未签名的更新 URL 交易对象。


#### wallet/listwitnesses
作用：查询当前的所有 SR 列表。
```
curl -X POST  http://127.0.0.1:8090/wallet/listwitnesses
```
参数：无

返回值：返回所有 SR 信息列表。

#### wallet/withdrawbalance
作用：超级代表或者用户提取奖励到 balance，每 24 个小时可以提现一次。

```
curl -X POST http://127.0.0.1:8090/wallet/withdrawbalance -d '{
"owner_address":"41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
}'
```
参数：

- `owner_address`是提现账号的地址，默认为 HexString 格式。
- `Permission_id`可选参数，多重签名时使用，设置交易多重签名时使用的 permissionId。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：一个未签名的提取奖励交易对象。


#### wallet/votewitnessaccount
作用：对 SR 进行投票
```
curl -X POST  http://127.0.0.1:8090/wallet/votewitnessaccount -d '{
"owner_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292",
"votes": [{"vote_address": "41e552f6487585c2b58bc2c9bb4492bc1f17132cd0", "vote_count": 5}]
}'
```
参数：

- `owner_address`是投票人地址，默认为 HexString 格式。
- `votes.vote_address`是被投票的超级代表的地址，默认为 HexString 格式。
- `vote_count`是投票数量。
- 可选参数`Permission_id`，多重签名时使用，设置交易多重签名时使用的 permissionId。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：一个未签名的投票交易对象。

#### wallet/getBrokerage
作用：查询指定超级代表（或合伙人）设置的佣金比例。
```
curl -X GET  http://127.0.0.1:8090/wallet/getBrokerage -d '{
"address":"41E552F6487585C2B58BC2C9BB4492BC1F17132CD0"}'
```
参数：
 - `address`是被投票的超级代表的地址，默认为 HexString 格式
 - `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：超级代表的当前 brokerage 比例。

#### wallet/updateBrokerage
作用：更新超级代表当前的Brokerage比例
```
curl -X POST  http://47.252.81.126:8090/wallet/updateBrokerage  -d '{
"owner_address":"41E552F6487585C2B58BC2C9BB4492BC1F17132CD0",
"brokerage":30}'
```
参数：

- `owner_address`是被投票的超级代表的地址，默认为 HexString 格式。
- `brokerage`是超级代表想要更新为的 brokerage 比例。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：一个未签名的更新佣金交易对象。

#### wallet/getReward
作用：查询一个投票者账户中当前未领取的投票奖励总额。
```
curl -X GET
http://127.0.0.1:8090/wallet/getReward -d '{
"address":"41E552F6487585C2B58BC2C9BB4492BC1F17132CD0"}'
```
参数：
 - `address`是投票人地址，默认为 HexString 格式
 - `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。
返回值：一个包含未领取奖励金额（单位 sun）的对象。

#### wallet/getnextmaintenancetime
作用：获取下次统计投票的时间
```
curl -X POST  http://127.0.0.1:8090/wallet/getnextmaintenancetime
```
参数：无

返回值：下次统计投票时间的毫秒数。

<a id="tip"></a>
### 提案
下面是提案相关API：


- [wallet/proposalcreate](#walletproposalcreate)
- [wallet/getproposalbyid](#walletgetproposalbyid)
- [wallet/listproposals](#walletlistproposals)
- [wallet/proposalapprove](#walletproposalapprove)
- [wallet/proposaldelete](#walletproposaldelete)
- [wallet/getpaginatedproposallist](#walletgetpaginatedproposallist)


#### wallet/proposalcreate
作用：创建一笔用于修改网络动态参数的提案交易。
```
curl -X POST  http://127.0.0.1:8090/wallet/proposalcreate -d {"owner_address" : "419844F7600E018FD0D710E2145351D607B3316CE9","parameters":[{"key": 0,"value": 100000},{"key": 1,"value": 2}] }
```
参数：

- `owner_address`：创建人地址。
- `parameters`：提案参数。
- 可选参数`Permission_id`，多重签名时使用，设置交易多重签名时使用的 permissionId。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：一个未签名的创建提案交易对象。

#### wallet/getproposalbyid
作用：根据ID查询提案的详细信息。
```
curl -X POST  http://127.0.0.1:8090/wallet/getproposalbyid -d {"id":1}
```
参数：
- `id`：提案 id

返回值：指定的提案详细信息。

#### wallet/listproposals
作用：查询当前网络上所有提案的列表。
```
curl -X POST  http://127.0.0.1:8090/wallet/listproposals
```
参数：无

返回值：一个包含所有提案对象的数组。

#### wallet/proposalapprove
作用：提案批准
```
curl -X POST  http://127.0.0.1:8090/wallet/proposalapprove -d {"owner_address" : "419844F7600E018FD0D710E2145351D607B3316CE9", "proposal_id":1, "is_add_approval":true}
```
参数：

- `owner_address`：批准人地址，默认为 HexString 格式。
- `proposal_id`：提案 id。
- `is_add_approval`：是否批准。
- 可选参数`Permission_id`，多重签名时使用，设置交易多重签名时使用的 permissionId。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：一个未签名的批准提案交易对象。

#### wallet/proposaldelete
作用：删除提案。
```
curl -X POST  http://127.0.0.1:8090/wallet/proposaldelete -d {"owner_address" : "419844F7600E018FD0D710E2145351D607B3316CE9", "proposal_id":1}
```
参数：

- `owner_address`：删除人的地址，只有提案所有人允许删除提案，默认为 HexString 格式。
- `proposal_id`：提案 id。
- 可选参数`Permission_id`，多重签名时使用，设置交易多重签名时使用的 permissionId。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：一个未签名的删除提案交易对象。

#### wallet/getpaginatedproposallist
作用：分页查询提案列表。
```
curl -X POST  http://127.0.0.1:8090/wallet/getpaginatedproposallist -d '{"offset": 0, "limit": 10}'
```
参数：
 -` offset`：分页查询的起始索引。
 - `limit`：本次查询期望返回的提案数量。

返回值：一个包含了分页结果的提案对象的数组。

<a id="dex"></a>
### 去中心化交易所
下面是去中心化交易所相关API：

- [wallet/exchangecreate](#walletexchangecreate)
- [wallet/exchangeinject](#walletexchangeinject)
- [wallet/exchangewithdraw](#walletexchangewithdraw)
- [wallet/exchangetransaction](#walletexchangetransaction)
- [wallet/getexchangebyid](#walletgetexchangebyid)
- [wallet/listexchanges](#walletlistexchanges)
- [wallet/getpaginatedexchangelist](#walletgetpaginatedexchangelist)
- [wallet/marketsellasset](#walletmarketsellasset)
- [wallet/marketcancelorder](#walletmarketcancelorder)
- [wallet/getmarketorderbyaccount](#walletgetmarketorderbyaccount)
- [wallet/getmarketpairlist](#walletgetmarketpairlist)
- [wallet/getmarketorderlistbypair](#walletgetmarketorderlistbypair)
- [wallet/getmarketpricebypair](#walletgetmarketpricebypair)
- [wallet/getmarketorderbyid](#walletgetmarketorderbyid)


#### wallet/exchangecreate
作用：创建交易对
```
curl -X POST  http://127.0.0.1:8090/wallet/exchangecreate -d {"owner_address":"419844f7600e018fd0d710e2145351d607b3316ce9", 、
"first_token_id":token_a, "first_token_balance":100, "second_token_id":token_b,"second_token_balance":200}
```
参数：

- `first_token_id`  ：第 1 种 token 的 id，默认为 HexString 格式
- `first_token_balance`：第 1 种 token 的 balance
- `second_token_id` ： 第 2 种 token 的 id，默认为 HexString 格式
- `second_token_balance`：第 2 种 token 的 balance
- 可选参数`Permission_id`，多重签名时使用，设置交易多重签名时使用的 permissionId

返回值：一个未签名的创建交易对交易对象。

#### wallet/exchangeinject
作用：给交易对注资，注资后可以防止交易对价格波动太大
```
curl -X POST  http://127.0.0.1:8090/wallet/exchangeinject -d {"owner_address":"419844f7600e018fd0d710e2145351d607b3316ce9", "exchange_id":1, "token_id":"74726f6e6e616d65", "quant":100}
```
参数：

- `owner_address`：交易对创建者的地址，默认为 HexString 格式。
- `exchange_id`：交易对 id。
- `token_id`： token 的 id，一般情况是 token 的 name，默认为 HexString 格式。
- `quant`：注资 token 的数量。
- 可选参数`Permission_id`，多重签名时使用，设置交易多重签名时使用的 permissionId。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：一个未签名的注资交易对象。

#### wallet/exchangewithdraw
作用：对交易对撤资。
```
curl -X POST  http://127.0.0.1:8090/wallet/exchangewithdraw -d {"owner_address":"419844f7600e018fd0d710e2145351d607b3316ce9", "exchange_id":1, "token_id":"74726f6e6e616d65", "quant":100}
```
参数：

- `owner_address`：是交易对创建者的地址，默认为 HexString 格式。
- `exchange_id`：交易对 id。
- `token_id`： token的 id，一般情况是 token 的 name，需要是 HexString 格式。
- `quant`：撤资 token 的数量。
- 可选参数`Permission_id`，多重签名时使用，设置交易多重签名时使用的 permissionId。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：一个未签名的撤资交易对象。

#### wallet/exchangetransaction
作用：参与交易对交易。
```
curl -X POST  http://127.0.0.1:8090/wallet/exchangetransaction -d {"owner_address":"419844f7600e018fd0d710e2145351d607b3316ce9", "exchange_id":1, "token_id":"74726f6e6e616d65", "quant":100,"expected":10}
```
参数：

- `owner_address`：是交易对创建者的地址，默认为 HexString 格式。
- `exchange_id`：交易对 id。
- `token_id`： 卖出的 token 的 id，一般情况是 token 的 name，默认为 HexString 格式。
- `quant`：卖出 token 的数量。
- `expected`：期望买入 token 的数量。
- 可选参数`Permission_id`，多重签名时使用，设置交易多重签名时使用的 permissionId。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：一个未签名的兑换交易对象。

#### wallet/getexchangebyid
作用：根据 id 查询交易对
```
curl -X POST  http://127.0.0.1:8090/wallet/getexchangebyid -d {"id":1}
```
参数：
- `id`：交易对 id

返回值：返回指定的交易对对象。

#### wallet/listexchanges
作用：查询所有交易对
```
curl -X POST  http://127.0.0.1:8090/wallet/listexchanges
```
参数：无

返回值：一个包含所有交易对对象的数组。

#### wallet/getpaginatedexchangelist
作用：分页查询交易对列表
```
curl -X POST  http://127.0.0.1:8090/wallet/getpaginatedexchangelist -d '{"offset": 0, "limit":10}'
```
参数：
 - `offset`：分页查询的起始索引。
 - `limit`：本次查询期望返回的交易对数量。

返回值：一个包含了分页结果的交易对对象的数组。

#### wallet/marketsellasset
作用：创建订单
```
curl -X POST  http://127.0.0.1:8090/wallet/marketsellasset -d
'{
    "owner_address": "4184894b42f66dce8cb84aec2ed11604c991351ac8",
    "sell_token_id": "5f",
    "sell_token_quantity": 100,
    "buy_token_id": "31303030303031",
    "buy_token_quantity": 200
}'
```
参数：

- `owner_address`：订单发起者地址，默认为 HexString 格式。
- `sell_token_id`：卖出 asset 的 id，默认为 HexString 格式。
- `sell_token_quantity`：卖出 asset 的数量。
- `buy_token_id`：买入 asset 的 id，默认为 HexString 格式。
- `buy_token_quantity`：最少买入的 asset 的数量。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：一个未签名的挂单交易对象。


#### wallet/marketcancelorder
作用：取消订单
```
curl -X POST  http://127.0.0.1:8090/wallet/marketcancelorder -d
'{
    "owner_address": "4184894b42f66dce8cb84aec2ed11604c991351ac8",
    "order_id": "0a7af584a53b612bcff1d0fc86feab05f69bc4528f26a4433bb344d453bd6eeb"
}'
```
参数：

- `owner_address`：订单发起者地址，默认为 HexString 格式。
- `order_id`：取消订单的 id。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。

返回值：一个未签名的取消订单交易对象。

#### wallet/getmarketorderbyaccount
作用：查询账户拥有的订单
```
curl -X POST  http://127.0.0.1:8090/wallet/getmarketorderbyaccount -d
'{
    "value": "4184894b42f66dce8cb84aec2ed11604c991351ac8"
}'
```
参数：

- `value`：地址，默认为 HexString 格式。
- `visible` 设置地址格式，`true` 为 Base58Check，`false` 或省略则为 HexString。


返回值：一个包含了该账户所有订单对象的数组。

#### wallet/getmarketpairlist
作用：查询存在的所有交易对
```
curl -X get  http://127.0.0.1:8090/wallet/getmarketpairlist
```
参数：
无

返回值：一个包含了所有交易对信息的数组。

#### wallet/getmarketorderlistbypair
作用：查询某交易对的所有订单
```
curl -X POST  http://127.0.0.1:8090/wallet/getmarketorderlistbypair -d
'{
    "sell_token_id": "5f" ,
    "buy_token_id": "31303030303031"
}'
```
参数：

- `sell_token_id`：卖出 asset 的 id，默认为 HexString 格式
- `buy_token_id`：买入 asset 的 id，默认为 HexString 格式

返回值：一个包含了该交易对所有订单对象的数组。

#### wallet/getmarketpricebypair
作用：查询某交易对的所有价格
```
curl -X POST  http://127.0.0.1:8090/wallet/getmarketpricebypair -d
'{
    "sell_token_id": "5f"
    "buy_token_id": "31303030303031"
}'
```
参数：

- `sell_token_id`：卖出 asset 的 id，默认为 HexString 格式
- `buy_token_id`：买入 asset 的 id，默认为 HexString 格式

返回值：一个包含了该交易对所有价格点对象的数组。

#### wallet/getmarketorderbyid
作用：查询订单
```
curl -X POST  http://127.0.0.1:8090/wallet/getmarketorderbyid -d
'{
   "value": "orderid"
}'
```
参数：
- `value`：order id，默认为 HexString 格式

返回值：指定的订单对象。

<a id="pending-pool"></a>
### Pending Pool
下面是Pending Pool相关API：

- [wallet/gettransactionfrompending](#walletgettransactionfrompending)
- [wallet/gettransactionlistfrompending](#walletgettransactionlistfrompending)
- [wallet/getpendingsize](#walletgetpendingsize)

#### wallet/gettransactionfrompending
作用：查询pending pool中的交易信息
```
curl -X POST  http://127.0.0.1:8090/wallet/gettransactionfrompending -d
'{
  "value": "txId"
}'
```
参数：
- `value`: 交易id，默认为hexString格式

返回值：完整的交易对象。如果交易不在等待池中，返回空对象。

#### wallet/gettransactionlistfrompending
作用：获取当前交易等待池中所有交易的ID列表。
```
curl -X get  http://127.0.0.1:8090/wallet/gettransactionlistfrompending
```
参数：无

返回值：一个包含了所有等待中交易ID的数组。

#### wallet/getpendingsize
作用：查询当前交易等待池中的交易数量。
```
curl -X get  http://127.0.0.1:8090/wallet/getpendingsize
```
参数：无

返回值：一个包含等待池大小的对象。

## FullNode Solidity HTTP API


### 账户资源

#### walletsolidity/getaccount
作用：查询并返回一个指定TRON账户的完整链上信息(包括余额、资源、权限、资产在内的所有账户详情)。
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getaccount -d '{"address": "41E552F6487585C2B58BC2C9BB4492BC1F17132CD0"}'
```
参数：
* `address` 需要查询的账户地址。
* `visible` 设置地址格式，`true`为Base58Check，`false`或省略则为HexString。

返回值：Account对象

#### walletsolidity/getdelegatedresource
作用：Stake1.0中查询指定账户（代理方）为另一个特定账户（接收方）所代理的资源（能量或带宽）详情。
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getdelegatedresource -d '
{
"fromAddress": "419844f7600e018fd0d710e2145351d607b3316ce9",
"toAddress": "41c6600433381c731f22fc2b9f864b14fe518b322f"
}'
```
参数：
- `fromAddress`：是要查询的账户地址，默认为hexString格式
- `toAddress`：代理对象的账户地址，默认为hexString格式
- `visible` 设置地址格式，`true`为Base58Check，`false`或省略则为HexString。

返回值：
- 账户的资源代理的列表，列表的元素为DelegatedResource

#### walletsolidity/getdelegatedresourceaccountindex
作用：Stake1.0中查询一个指定账户代理及被代理资源关系列表。
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getdelegatedresourceaccountindex -d '
{
"value": "419844f7600e018fd0d710e2145351d607b3316ce9",
}'
```
参数：
- `value`：是要查询的账户地址，默认为hexString格式。
- `visible` 设置地址格式，`true`为Base58Check，`false`或省略则为HexString。

返回值：
- 账户的资源代理概况，结构为DelegatedResourceAccountIndex。

#### walletsolidity/getaccountbyid
作用：通过accountId查询一个账号的信息。
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getaccountbyid -d '{"account_id":"6161616162626262"}'
```
参数：account_id 默认为hexString格式

返回值：Account对象

#### walletsolidity/getavailableunfreezecount

作用：查询一个指定账户当前还可发起**解质押操作的剩余次数**。由于TRON网络规定每个账户最多只能同时保有**32笔**处于14天锁定期内的解质押操作，此接口可用于在调用 `unfreezebalancev2` 之前，预先检查是否还有可用的“解质押额度”。
```
curl -X POST http://127.0.0.1:8090/walletsolidity/getavailableunfreezecount -d
'{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "visible": true
}
'
```

参数：
- `owner_address`: 需要查询的账户地址。
- `visible` 设置地址格式，`true`为Base58Check，`false`或省略则为HexString。

返回值：
- 该接口返回一个包含剩余次数的JSON对象。

#### walletsolidity/getcanwithdrawunfreezeamount

作用：查询在某时间点可以提取的解质押本金数量。
```
curl -X POST http://127.0.0.1:8090/walletsolidity/getcanwithdrawunfreezeamount -d
'{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "timestamp": 1667977444000,
  "visible": true
}
'
```

参数：
- `owner_address`: 交易发起者账号的地址。
- `timestamp`: 查询在该时间戳时，可提取的本金数量，单位为毫秒。
- `visible` 设置地址格式，`true`为Base58Check，`false`或省略则为HexString。

返回值：
- 该接口返回一个包含可提取金额的JSON对象。


#### walletsolidity/getcandelegatedmaxsize

作用：查询目标地址中指定类型资源的可代理数量，单位为sun
```
curl -X POST http://127.0.0.1:8090/walletsolidity/getcandelegatedmaxsize -d
'{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "type": 0,
  "visible": true
}
'
```

参数：
- `owner_address`: 需要查询的账户地址。
- `type`: 资源类型，0为带宽，1为能量。
- `visible` 设置地址格式，`true`为Base58Check，`false`或省略则为HexString。

返回值：
- 该接口返回一个包含可代理份额最大值的JSON对象。

#### walletsolidity/getdelegatedresourcev2

作用：查询在 Stake 2.0 机制下，指定账户（代理方）为另一个特定账户（接收方）所代理的资源详情。
```
curl -X POST http://127.0.0.1:8090/walletsolidity/getdelegatedresourcev2 -d
'{
  "fromAddress": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "toAddress": "TPswDDCAWhJAZGdHPidFg5nEf8TkNToDX1",
  "visible": true
}
'
```

参数：
- `fromAddress`: 代理账户地址。
- `toAddress`: 资源的接收账户地址。
- `visible` 设置地址格式，`true`为Base58Check，`false`或省略则为HexString。

返回值：
- 该接口返回一个 delegatedResource 数组，包含了两者在Stake 2.0下的所有资源代理记录。

#### walletsolidity/getdelegatedresourceaccountindexv2
作用：查询在Stake2.0阶段，某地址的资源委托索引。返回两个列表，一个是该帐户将资源委托给的地址列表(toAddress)，另一个是将资源委托给该帐户的地址列表(fromAddress)
```
curl -X POST http://127.0.0.1:8090/walletsolidity/getdelegatedresourceaccountindexv2 -d
'{
  "value": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "visible": true
}
'
```

参数：
- `value`: 账户地址。
- `visible` 设置地址格式，`true`为Base58Check，`false`或省略则为HexString。

返回值：
- 该接口返回一个包含双向代理关系列表的JSON对象。包含两个列表，一个是该帐户将资源委托给的地址列表(toAddress)，另一个是将资源委托给该帐户的地址列表(fromAddress)

### 投票和SR

#### walletsolidity/listwitnesses
作用：查询当前的所有 SR 列表。
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/listwitnesses
```
参数：无

返回值：返回所有 SR 信息列表。

### TRC10 通证

#### walletsolidity/getassetissuelist
作用：查询所有Token列表
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getassetissuelist
```
参数：无

返回值：返回所有 Token 列表。

#### walletsolidity/getpaginatedassetissuelist
作用：分页查询全网的TRC-10 Token 列表。
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getpaginatedassetissuelist -d '{"offset": 0, "limit":10}'
```
参数：
 - `offset`：分页查询的起始索引。
 - `limit`：本次查询期望返回的TRC-10 Token 数量。

返回值：一个包含了分页结果的TRC-10 Token 对象的数组。

#### walletsolidity/getassetissuebyname
作用：根据名称查询TRC-10 Token。
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getassetissuebyname -d '{"value": "44756354616E"}'
```
参数：
 - `value`：TRC-10 Token 名称，默认为HexString格式。
返回值：TRC-10 Token 对象。

注意：Odyssey-v3.2开始，推荐使用getassetissuebyid或者getassetissuelistbyname替换此接口，因为从3.2开始将允许 TRC-10 Token 名称相同。如果存在相同的 TRC-10 Token 名称，此接口将会报错。

#### walletsolidity/getassetissuelistbyname
作用：根据名称查询所有匹配的 TRC-10 Token 列表。
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getassetissuelistbyname -d '{"value": "44756354616E"}'
```
参数：
 - `value`：TRC-10 Token 名称，默认为HexString格式。

返回值：一个包含所有同名 TRC-10 Token 对象的数组。

#### walletsolidity/getassetissuebyid
作用：根据ID查询 TRC-10 Token
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getassetissuebyid -d '{"value": "1000001"}'
```
参数：
- `value`：TRC-10 Token 的 ID。

返回值：指定的 TRC-10 Token 对象。


### 区块

#### walletsolidity/getnowblock
作用：查询最新块。
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getnowblock
```
参数：无

返回值：solidityNode 上的最新的区块对象。

#### walletsolidity/getblockbynum
作用：通过指定的区块高度查询完整的区块信息。
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getblockbynum -d '{"num" : 100}'
```
参数：
- num：区块高度 (整型)。

返回值：指定高度的区块对象 (Block object)。

#### walletsolidity/getblockbyid
作用：通过指定的区块ID（哈希）查询完整的区块信息。
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getblockbyid-d '{"value":
"0000000000038809c59ee8409a3b6c051e369ef1096603c7ee723c16e2376c73"}'
```
参数：
- value：区块的ID (hash)。

返回值：指定ID的区块对象 (Block object)。

#### walletsolidity/getblockbylimitnext
作用：分页查询指定高度范围内的区块列表。
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getblockbylimitnext -d '{"startNum": 1, "endNum": 2}'
```
参数：

- `startNum`：起始块高度，包含此块
- `endNum`：截止块高度，不包含此此块

返回值：一个包含多个区块对象的数组 (Block[])。

#### walletsolidity/getblockbylatestnum
作用：查询solidityNode从最新区块开始，倒序的N个区块。
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getblockbylatestnum -d '{"num": 5}'
```
参数：
- num：需要查询的区块数量。

返回值：一个包含多个区块对象的数组 (Block[])。

#### wallet/getnodeinfo
作用：查看当前节点自身的运行状态和信息。
```
curl -X GET http://127.0.0.1:8091/wallet/getnodeinfo
```
参数：无

返回值：一个包含节点版本、网络状况、区块同步状态等信息的对象。


### 交易

#### walletsolidity/gettransactionbyid
作用：通过交易ID（哈希）查询一个已上链交易的完整信息。
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/gettransactionbyid -d '{"value" : "309b6fa3d01353e46f57dd8a8f27611f98e392b50d035cef213f2c55225a8bd2"}'
```
参数：
- value：交易ID (hash)。

返回值：完整的交易对象 (Transaction object)。如果交易不存在或未确认，返回空对象。

#### walletsolidity/gettransactioncountbyblocknum
作用：查询指定区块高度上包含的交易总数。
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/gettransactioncountbyblocknum -d '{"num" : 100}'
```
参数：
- num：区块高度。

返回值：一个包含交易数量的对象，如 {"count": 50}。

#### walletsolidity/gettransactioninfobyid
作用：根据交易ID（哈希）查询交易的摘要信息，如费用、所在区块等。
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/gettransactioninfobyid -d '{"value" : "309b6fa3d01353e46f57dd8a8f27611f98e392b50d035cef213f2c55225a8bd2"}'
```
参数：
- value：交易ID (hash)。

返回值：交易的摘要信息对象 (TransactionInfo object)，包含交易费用、所在区块高度、区块时间戳、合约执行结果等。

#### walletsolidity/gettransactioninfobyblocknum
作用：获取指定区块高度上所有交易的摘要信息列表。
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/gettransactioninfobyblocknum -d '{"num" : 100}'
```
参数：
- num：区块高度。

返回值：一个包含多个交易摘要信息对象的列表。


### 去中心化交易所

#### walletsolidity/getexchangebyid
作用：根据id查询交易对
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getexchangebyid -d {"id":1}
```
参数：
- `id`：交易对id

返回值：返回指定的交易对对象。

#### walletsolidity/listexchanges
作用：查询所有交易对
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/listexchanges
```
参数：无

返回值：一个包含所有交易对对象的数组。


