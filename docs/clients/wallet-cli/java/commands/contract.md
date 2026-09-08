# 智能合约

部署、触发和查看智能合约。

## DeployContract

```console
> DeployContract [ownerAddress] contractName ABI byteCode constructor params isHex fee_limit consume_user_resource_percent origin_energy_limit value token_value token_id(e.g: TRXTOKEN, use # if don't provided) <library:address,...> <lib_compiler_version(e.g:v5)>
```

- `OwnerAddress`——发起交易的账户地址，可选，默认为登录账户的地址。
- `contractName`——智能合约的名称。
- `ABI`——编译生成的 ABI 代码。
- `byteCode`——编译生成的字节码。
- `constructor`、`params`、`isHex`——定义字节码的格式，决定从参数解析 `byteCode` 的方式。
- `fee_limit`——该交易允许消耗的最多 TRX。
- `consume_user_resource_percent`——用户资源消耗百分比，取值范围 [0, 100]。
- `origin_energy_limit`——触发一次合约所消耗的开发者能量上限。
- `value`——转入合约账户的 TRX 数量。
- `token_value`——TRC10 的数量。
- `token_id`——TRC10 id。

示例：

```console
> deployContract normalcontract544 [{"constant":false,"inputs":[{"name":"i","type":"uint256"}],"name": "findArgsByIndexTest","outputs":[{"name":"z","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"}] 608060405234801561001057600080fd5b50610134806100206000396000f3006080604052600436106100405763ffffffff7c0100000000000000000000000000000000000000000000000000000000600035041663329000b58114610045575b600080fd5b34801561005157600080fd5b5061005d60043561006f565b60408051918252519081900360200190f35b604080516003808252608082019092526000916060919060208201838038833901905050905060018160008151811015156100a657fe5b602090810290910101528051600290829060019081106100c257fe5b602090810290910101528051600390829060029081106100de57fe5b6020908102909101015280518190849081106100f657fe5b906020019060200201519150509190505600a165627a7a72305820b24fc247fdaf3644b3c4c94fcee380aa610ed83415061ff9e65d7fa94a5a50a00029 # # false 1000000000 75 50000 0 0 #
```

用 `getTransactionInfoById` 命令获取合约执行结果：

```console
> getTransactionInfoById 4978dc64ff746ca208e51780cce93237ee444f598b24d5e9ce0da885fb3a3eb9
{
    "id": "8c1f57a5e53b15bb0a0a0a0d4740eda9c31fbdb6a63bc429ec2113a92e8ff361",
    "fee": 6170500,
    "blockNumber": 1867,
    "blockTimeStamp": 1567499757000,
    "contractResult": [
        "6080604052600436106100405763ffffffff7c0100000000000000000000000000000000000000000000000000000000600035041663329000b58114610045575b600080fd5b34801561005157600080fd5b5061005d60043561006f565b60408051918252519081900360200190f35b604080516003808252608082019092526000916060919060208201838038833901905050905060018160008151811015156100a657fe5b602090810290910101528051600290829060019081106100c257fe5b602090810290910101528051600390829060029081106100de57fe5b6020908102909101015280518190849081106100f657fe5b906020019060200201519150509190505600a165627a7a72305820b24fc247fdaf3644b3c4c94fcee380aa610ed83415061ff9e65d7fa94a5a50a00029"
    ],
    "contract_address": "TJMKWmC6mwF1QVax8Sy2AcgT6MqaXmHEds",
    "receipt": {
        "energy_fee": 6170500,
        "energy_usage_total": 61705,
        "net_usage": 704,
        "result": "SUCCESS"
    }
}
```

## DeployConstantContract

以**常量（只读）调用**的方式运行一次合约部署——该部署在节点上本地执行，**不会广播**到链上，因此
可以用来事先检查部署的结果和能量开销。

```console
> DeployConstantContract ownerAddress(use # if you own) byteCode constructor params isHex [value token_value token_id]
```

接受 5 个参数；若提供末尾的 `value token_value token_id` 一组，则为 8 个。

- `ownerAddress`——发起交易的账户地址；如果是你自己的登录账户，使用 `#`。
- `byteCode`——编译生成的字节码。
- `constructor`、`params`、`isHex`——构造函数签名及其实参值；`isHex` 决定它们的解析方式。如果
  `constructor` 或 `params` 中任意一个为 `#`，则不向字节码追加任何参数。
- `value`——转入合约账户的 TRX 数量。
- `token_value`——TRC10 的数量。
- `token_id`——TRC10 id；未提供时使用 `#`。

## TriggerContract

```console
> TriggerContract [ownerAddress] contractAddress method args isHex fee_limit value token_value token_id
```

- `ownerAddress`——必填。传入 base58 地址，或传 `#` 表示使用当前登录账户。
- `contractAddress`——智能合约地址。
- `method`——函数名及参数；参见示例。
- `args`——参数值；如果想调用 `receive`，请传 `#`。
- `isHex`——参数 `method` 和 `args` 的格式；是否为十六进制字符串。
- `value`——可选的调用金额，单位为 SUN；一旦传入，`token_value` 和 `token_id` 也必须一并传入。
- `token_value`——TRC10 的数量。
- `token_id`——TRC10 id；如果没有，使用 `#`。

本命令只接受两种形式：不带 value / token 字段的 5 个参数，或带全部三个可选字段的 8 个参数。它不接受 `fee_limit`。

示例：

```console
> triggerContract TGdtALTPZ1FWQcc5MW7aK3o1ASaookkJxG findArgsByIndexTest(uint256) 0 false 1000000000 0 0 #
# 用 getTransactionInfoById 命令获取合约执行结果
> getTransactionInfoById 7d9c4e765ea53cf6749d8a89ac07d577141b93f83adc4015f0b266d8f5c2dec4
{
    "id": "de289f255aa2cdda95fbd430caf8fde3f9c989c544c4917cf1285a088115d0e8",
    "fee": 8500,
    "blockNumber": 2076,
    "blockTimeStamp": 1567500396000,
    "contractResult": [
        ""
    ],
    "contract_address": "TJMKWmC6mwF1QVax8Sy2AcgT6MqaXmHEds",
    "receipt": {
        "energy_fee": 8500,
        "energy_usage_total": 85,
        "net_usage": 314,
        "result": "REVERT"
    },
    "result": "FAILED",
    "resMessage": "REVERT opcode executed"
}
```

## TriggerConstantContract

```console
> TriggerConstantContract ownerAddress contractAddress method args isHex [value token_value token_id]
```

- `OwnerAddress`——发起交易的账户地址，可选，默认为登录账户的地址。
- `contractAddress`——智能合约地址。
- `method`——函数名及参数；参见示例。
- `args`——参数值；如果想调用 `receive`，请传 `#`。
- `isHex`——参数 `method` 和 `args` 的格式；是否为十六进制字符串。
- `fee_limit`——允许消耗的最多 TRX。
- `token_value`——TRC10 的数量。
- `token_id`——TRC10 id；如果没有，使用 `#`。

示例：

```console
> TriggerConstantContract TSNEe5Tf4rnc9zPMNXfaTF5fZfHDDH8oyW TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs balanceOf(address) 000000000000000000000000a614f803b6fd780986a42c78ec9c7f77e6ded13c true
```

## ClearContractABI

```console
> ClearContractABI [ownerAddress] contractAddress
```

- `OwnerAddress`——发起交易的账户地址，可选，默认为登录账户的地址。
- `contractAddress`——合约地址。

示例：

```console
> ClearContractABI TSNEe5Tf4rnc9zPMNXfaTF5fZfHDDH8oyW TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs
```

## GetContract

获取智能合约的详情。

```console
> GetContract contractAddress
```

`contractAddress`——智能合约地址。

示例：

```console
> GetContract TGdtALTPZ1FWQcc5MW7aK3o1ASaookkJxG
{
    "origin_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
    "contract_address": "TJMKWmC6mwF1QVax8Sy2AcgT6MqaXmHEds",
    "abi": {
        "entrys": [
            {
                "name": "findArgsByIndexTest",
                "inputs": [
                    {
                        "name": "i",
                        "type": "uint256"
                    }
                ],
                "outputs": [
                    {
                        "name": "z",
                        "type": "uint256"
                    }
                ],
                "type": "Function",
                "stateMutability": "Nonpayable"
            }
        ]
    },
    "bytecode": "608060405234801561001057600080fd5b50610134806100206000396000f3006080604052600436106100405763ffffffff7c0100000000000000000000000000000000000000000000000000000000600035041663329000b58114610045575b600080fd5b34801561005157600080fd5b5061005d60043561006f565b60408051918252519081900360200190f35b604080516003808252608082019092526000916060919060208201838038833901905050905060018160008151811015156100a657fe5b602090810290910101528051600290829060019081106100c257fe5b602090810290910101528051600390829060029081106100de57fe5b6020908102909101015280518190849081106100f657fe5b906020019060200201519150509190505600a165627a7a72305820b24fc247fdaf3644b3c4c94fcee380aa610ed83415061ff9e65d7fa94a5a50a00029",
    "consume_user_resource_percent": 75,
    "name": "normalcontract544",
    "origin_energy_limit": 50000,
    "code_hash": "23423cece3b4866263c15357b358e5ac261c218693b862bcdb90fa792d5714e6"
}
```

## GetContractInfo

获取智能合约的信息。

```console
> GetContractInfo contractAddress
```

`contractAddress`——智能合约地址。

示例：

```console
> GetContractInfo TGdtALTPZ1FWQcc5MW7aK3o1ASaookkJxG
```

## UpdateEnergyLimit / UpdateSetting {#updateenergylimit--updatesetting}

更新智能合约参数。

```console
> UpdateEnergyLimit [ownerAddress] contract_address energy_limit  # 更新参数 energy_limit
> UpdateSetting [ownerAddress] contract_address consume_user_resource_percent  # 更新参数 consume_user_resource_percent
```

## Create2

预测部署合约后生成的合约地址。`address` 是执行 create2 指令的合约地址，`code` 是待部署合约的
字节码，`salt` 是一个随机的盐值。

```console
> Create2 address code salt
```

示例：

```console
> Create2 TEDapYSVvAZ3aYH7w8N9tMEEFKaNKUD5Bp 5f805460ff1916600190811790915560649055606319600255 2132
```

## EstimateEnergy

估算智能合约交易成功执行所需的能量（已确认状态）。

```console
> EstimateEnergy owner_address(use # if you own) contract_address method args isHex [value token_value token_id(e.g: TRXTOKEN, use # if don't provided)]
```

示例：

```console
> EstimateEnergy TSNEe5Tf4rnc9zPMNXfaTF5fZfHDDH8oyW TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs balanceOf(address) 000000000000000000000000a614f803b6fd780986a42c78ec9c7f77e6ded13c true
```

## 另请参见

- [usdt](usdt.md)——通过合约调用进行 TRC20 转账
- [concepts/resources](../concepts/resources.md)——能量消耗
