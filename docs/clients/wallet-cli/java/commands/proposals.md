# 提案

链上治理提案。除查看类操作外，所有与提案相关的操作都必须由委员会成员执行。

## CreateProposal

发起提案。

```console
> createProposal [OwnerAddress] id0 value0 ... idN valueN
```

- `OwnerAddress`（可选）——发起交易的账户地址。默认：登录账户的地址。
- `id0`——参数的序号。TRON 网络的每个参数都有一个序号。请参考
  `http://tronscan.org/#/sr/committee`。
- `Value0`——修改后的值。

参数值会原样提交给链上——CLI 不做任何单位换算，因此以 SUN 计价的参数必须按 SUN 传入。示例中把 4 号提案（token 发行费用）设为原始值 `1000`，也就是 1000 SUN：

```console
> createProposal 4 1000
> listproposals  # 查看已发起的提案
{
    "proposals": [
        {
            "proposal_id": 1,
            "proposer_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
            "parameters": [
                {
                    "key": 4,
                    "value": 1000
                }
            ],
            "expiration_time": 1567498800000,
            "create_time": 1567498308000
        }
    ]
}
```

示例中创建的提案 ID 为 1。

## ApproveProposal

批准提案，或撤销此前对提案的批准。

```console
> approveProposal [OwnerAddress] id is_or_not_add_approval
```

- `OwnerAddress`（可选）——发起交易的账户地址。默认：登录账户的地址。
- `id`——已发起提案的 ID。示例：1。
- `is_or_not_add_approval`——`true` 表示批准；`false` 表示撤销已有批准。

示例：

```console
> ApproveProposal 1 true  # 批准该提案
> ApproveProposal 1 false  # 撤销对该提案的批准
```

## DeleteProposal

删除已有提案。只有发起该提案的超级代表账户才能执行此操作。

```console
> deleteProposal [OwnerAddress] proposalId
```

`proposalId`——已发起提案的 ID。示例：1。

示例：

```console
> DeleteProposal 1
```

## 获取提案信息 {#obtain-proposal-information}

- `ListProposals`——获取已发起提案的列表。
- `ListProposalsPaginated`——以分页模式获取已发起的提案。
- `GetProposal`——根据提案 ID 获取提案信息。

## 另请参见

- [exchange](exchange.md)——内置的 Bancor 交易所
- [dex](dex.md)——TRON-DEX 订单市场
- [multisig](multisig.md)——委员会 / 多签操作
