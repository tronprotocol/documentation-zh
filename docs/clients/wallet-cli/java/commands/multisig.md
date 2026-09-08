# 多重签名

配置账户权限、联合签名交易、查看签名权重，以及使用 TronLink 多签。底层的权限模型参见
[concepts/multisig](../concepts/multisig.md)。

REPL 中许多写操作命令只在**最后一个参数位**接受 `-m`。加上它，该操作就会走交互式多签流程，而不是普通的单签广播。并非所有命令都支持，请先查看该命令内置的用法说明再决定是否追加。

## 如何使用 wallet-cli 的多重签名功能 {#how-to-use-the-multi-signature-feature-of-wallet-cli}

多重签名允许其他用户访问该账户，以便更好地管理它。访问权限分为三类：

- **owner**：对账户所有者的访问权限。
- **active**：对账户其他功能的访问权限，以及授权某项特定功能的权限。如果用于见证人用途，不包含
  出块授权。
- **witness**：仅用于见证人；出块授权将被授予其他用户之一。

## UpdateAccountPermission

```console
> Updateaccountpermission TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ {"owner_permission":{"type":0,"permission_name":"owner","threshold":1,"keys":[{"address":"TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ","weight":1}]},"witness_permission":{"type":1,"permission_name":"witness","threshold":1,"keys":[{"address":"TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ","weight":1}]},"active_permissions":[{"type":2,"permission_name":"active12323","threshold":2,"operations":"7fff1fc0033e0000000000000000000000000000000000000000000000000000","keys":[{"address":"TNhXo1GbRNCuorvYu5JFWN3m2NYr9QQpVR","weight":1},{"address":"TKwhcDup8L2PH5r6hxp5CQvQzZqJLmKvZP","weight":1}]}]}
```

或者

```console
wallet> updateAccountPermission
=== UpdateAccountPermission Interactive Mode ===

Please enter the index(1-7) to operate:
1. owner_permission
2. witness_permission
3. active_permissions
4. Add new active_permission
5. Delete active_permission
6. Show preview and Confirm
7. Exit
>
```

账户 TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ 把 owner 访问权授予自己，把 active 访问权授予
TNhXo1GbRNCuorvYu5JFWN3m2NYr9QQpVR 和 TKwhcDup8L2PH5r6hxp5CQvQzZqJLmKvZP。active 访问需要这两个
账户都签名才能生效。

如果该账户不是见证人，就不需要设置 `witness_permission`，否则会报错。

## SendCoin（已签名交易） {#sendcoin-signed-transaction}

```console
> SendCoin TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW 10000000000000000
```

命令会显示以下提示：

`Please confirm and input your permission id, if input y/Y means default 0, other non-numeric characters will cancel transaction.`

该转账需要 active 权限授权，此处输入权限 ID `2`。

然后选择账户并输入本地密码，使用 TNhXo1GbRNCuorvYu5JFWN3m2NYr9QQpVR 对应的私钥签名。

再选择另一个账户并输入本地密码，使用 TKwhcDup8L2PH5r6hxp5CQvQzZqJLmKvZP 对应的私钥签名。

每个账户的权重为 1，权限阈值为 2。两个签名收集完成后，命令会显示：

`Send 10000000000000000 Sun to TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW  successful !!`

以上流程适用于在同一个 CLI 中使用多个账户完成多重签名。如果签名账户分布在不同的 CLI 实例中，
请传递交易的十六进制字符串，并使用 `addTransactionSign` 依次添加签名。收集完成后，需要手动广播
最终交易。

## GetTransactionSignWeight

根据交易获取权重信息。

```console
> getTransactionSignWeight
0a8c010a020318220860e195d3609c86614096eadec79d2d5a6e080112680a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412370a1541a7d8a35b260395c14aa456297662092ba3b76fc01215415a523b449890854c8fc460ab602df9f31fe4293f18808084fea6dee11128027094bcb8bd9d2d1241c18ca91f1533ecdd83041eb0005683c4a39a2310ec60456b1f0075b4517443cf4f601a69788f001d4bc03872e892a5e25c618e38e7b81b8b1e69d07823625c2b0112413d61eb0f8868990cfa138b19878e607af957c37b51961d8be16168d7796675384e24043d121d01569895fcc7deb37648c59f538a8909115e64da167ff659c26101
```

信息显示如下：

```json
{
    "result":{
        "code":"PERMISSION_ERROR",
        "message":"Signature count is 2 more than key counts of permission : 1"
    },
    "permission":{
        "operations":"7fff1fc0033e0100000000000000000000000000000000000000000000000000",
        "keys":[
            {
                "address":"TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
                "weight":1
            }
        ],
        "threshold":1,
        "id":2,
        "type":"Active",
        "permission_name":"active"
    },
    "transaction":{
        "result":{
            "result":true
        },
        "txid":"7da63b6a1f008d03ef86fa871b24a56a501a8bbf15effd7aca635de6c738df4b",
        "transaction":{
            "signature":[
                "c18ca91f1533ecdd83041eb0005683c4a39a2310ec60456b1f0075b4517443cf4f601a69788f001d4bc03872e892a5e25c618e38e7b81b8b1e69d07823625c2b01",
                "3d61eb0f8868990cfa138b19878e607af957c37b51961d8be16168d7796675384e24043d121d01569895fcc7deb37648c59f538a8909115e64da167ff659c26101"
            ],
            "txID":"7da63b6a1f008d03ef86fa871b24a56a501a8bbf15effd7aca635de6c738df4b",
            "raw_data":{
                "contract":[
                    {
                        "parameter":{
                            "value":{
                                "amount":10000000000000000,
                                "owner_address":"TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
                                "to_address":"TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW"
                            },
                            "type_url":"type.googleapis.com/protocol.TransferContract"
                        },
                        "type":"TransferContract",
                        "Permission_id":2
                    }
                ],
                "ref_block_bytes":"0318",
                "ref_block_hash":"60e195d3609c8661",
                "expiration":1554123306262,
                "timestamp":1554101706260
            },
            "raw_data_hex":"0a020318220860e195d3609c86614096eadec79d2d5a6e080112680a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412370a1541a7d8a35b260395c14aa456297662092ba3b76fc01215415a523b449890854c8fc460ab602df9f31fe4293f18808084fea6dee11128027094bcb8bd9d2d"
        }
    }
}
```

## GetTransactionApprovedList

根据交易获取签名信息。

```console
> getTransactionApprovedList
0a8c010a020318220860e195d3609c86614096eadec79d2d5a6e080112680a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412370a1541a7d8a35b260395c14aa456297662092ba3b76fc01215415a523b449890854c8fc460ab602df9f31fe4293f18808084fea6dee11128027094bcb8bd9d2d1241c18ca91f1533ecdd83041eb0005683c4a39a2310ec60456b1f0075b4517443cf4f601a69788f001d4bc03872e892a5e25c618e38e7b81b8b1e69d07823625c2b0112413d61eb0f8868990cfa138b19878e607af957c37b51961d8be16168d7796675384e24043d121d01569895fcc7deb37648c59f538a8909115e64da167ff659c26101
```

```json
{
    "result":{

    },
    "approved_list":[
        "TKwhcDup8L2PH5r6hxp5CQvQzZqJLmKvZP",
        "TNhXo1GbRNCuorvYu5JFWN3m2NYr9QQpVR"
    ],
    "transaction":{
        "result":{
            "result":true
        },
        "txid":"7da63b6a1f008d03ef86fa871b24a56a501a8bbf15effd7aca635de6c738df4b",
        "transaction":{
            "signature":[
                "c18ca91f1533ecdd83041eb0005683c4a39a2310ec60456b1f0075b4517443cf4f601a69788f001d4bc03872e892a5e25c618e38e7b81b8b1e69d07823625c2b01",
                "3d61eb0f8868990cfa138b19878e607af957c37b51961d8be16168d7796675384e24043d121d01569895fcc7deb37648c59f538a8909115e64da167ff659c26101"
            ],
            "txID":"7da63b6a1f008d03ef86fa871b24a56a501a8bbf15effd7aca635de6c738df4b",
            "raw_data":{
                "contract":[
                    {
                        "parameter":{
                            "value":{
                                "amount":10000000000000000,
                                "owner_address":"TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
                                "to_address":"TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW"
                            },
                            "type_url":"type.googleapis.com/protocol.TransferContract"
                        },
                        "type":"TransferContract",
                        "Permission_id":2
                    }
                ],
                "ref_block_bytes":"0318",
                "ref_block_hash":"60e195d3609c8661",
                "expiration":1554123306262,
                "timestamp":1554101706260
            },
            "raw_data_hex":"0a020318220860e195d3609c86614096eadec79d2d5a6e080112680a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412370a1541a7d8a35b260395c14aa456297662092ba3b76fc01215415a523b449890854c8fc460ab602df9f31fe4293f18808084fea6dee11128027094bcb8bd9d2d"
        }
    }
}
```

## TronlinkMultiSign

通过 TronLink 服务创建多签交易并查看多签交易列表。需要 `secretId` 和 `secretKey`——参见
[`config.conf`](../reference/config.md)。

```console
wallet> tronlinkmultisign

=== Multi-Sign Manager ===
1. Multi-sign transaction list
2. Create multi-sign transaction
0. Exit
Please enter to operate:
```

## 另请参见

- [concepts/multisig](../concepts/multisig.md)——权限 / 权重 / 阈值模型
- [wallet](wallet.md)——管理用于联合签名的 keystore
