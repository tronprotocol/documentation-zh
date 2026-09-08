# GasFree 转账

wallet-cli 支持集成 GasFree 服务，用于发起免 Gas 的 TRC20 转账。

更多细节参见 [GasFree 文档](https://gasfree.io/specification)和
[TronLink 的 GasFree 用户指南](https://support.tronlink.org/hc/en-us/articles/38903684778393-GasFree-User-Guide)。

**前置条件。** 需要从 GasFree 获取用于鉴权的 **API Key** 和 **API Secret**，并在
[`config.conf`](../reference/config.md) 中完成配置。申请方式参见官方
[申请表](https://docs.google.com/forms/d/e/1FAIpQLSc5EB1X8JN7LA4SAVAG99VziXEY6Kv6JxmlBry9rUBlwI-GaQ/viewform)。

## GasFreeInfo

查询 GasFree 信息——获取基本信息，包括与当前钱包地址关联的 GasFree 地址。GasFree 地址会在首次转账
时自动激活，这可能产生一笔激活费用。

查询当前钱包地址：

```console
wallet> gasfreeinfo
{
	"gasFreeAddress":"TCtSt8fCkZcVdrGpaVHUr6P8EmdjysswMF",
	"active":true,
	"tokenBalance":998696000,
	"activateFee":0,
	"transferFee":2000,
	"maxTransferValue":998694000
}
gasFreeInfo:  successful !!
```

查询指定地址：

```console
wallet> gasfreeinfo TRvVXgqddDGYRMx3FWf2tpVxXQQXDZxJQe
{
	"gasFreeAddress":"TCtSt8fCkZcVdrGpaVHUr6P8EmdjysswMF",
	"active":true,
	"tokenBalance":998696000,
	"activateFee":0,
	"transferFee":2000,
	"maxTransferValue":998694000
}
gasFreeInfo:  successful !!
```

## GasFreeTransfer

提交一笔免 Gas 的 token 转账请求。

```console
wallet> gasfreetransfer TEkj3ndMVEmFLYaFrATMwMjBRZ1EAZkucT 100000

GasFreeTransfer result:
{
	"code":200,
	"data":{
		"amount":100000,
		"providerAddress":"TKtWbdzEq5ss9vTS9kwRhBp5mXmBfBns3E",
		"apiKey":"",
		"accountAddress":"TUUSMd58eC3fKx3fn7whxJyr1FR56tgaP8",
		"signature":"",
		"targetAddress":"TEkj3ndMVEmFLYaFrATMwMjBRZ1EAZkucT",
		"maxFee":2000000,
		"version":1,
		"nonce":8,
		"tokenAddress":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf",
		"createdAt":1747909635678,
		"expiredAt":1747909695000,
		"estimatedTransferFee":2000,
		"id":"6c3ff67e-0bf4-4c09-91ca-0c7c254b01a0",
		"state":"WAITING",
		"estimatedActivateFee":0,
		"gasFreeAddress":"TNER12mMVWruqopsW9FQtKxCGfZcEtb3ER",
		"updatedAt":1747909635678
	}
}
GasFreeTransfer  successful !!!
```

## GasFreeTrace

跟踪转账状态——使用从 `GasFreeTransfer` 获得的 `id`（trace ID）查看 GasFree 转账的进度。

```console
wallet> gasfreetrace 6c3ff67e-0bf4-4c09-91ca-0c7c254b01a0
GasFreeTrace result:
{
	"code":200,
	"data":{
		"amount":100000,
		"providerAddress":"TKtWbdzEq5ss9vTS9kwRhBp5mXmBfBns3E",
		"txnTotalCost":102000,
		"accountAddress":"TUUSMd58eC3fKx3fn7whxJyr1FR56tgaP8",
		"txnActivateFee":0,
		"estimatedTotalCost":102000,
		"targetAddress":"TEkj3ndMVEmFLYaFrATMwMjBRZ1EAZkucT",
		"txnBlockTimestamp":1747909638000,
		"txnTotalFee":2000,
		"nonce":8,
		"estimatedTotalFee":2000,
		"tokenAddress":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf",
		"txnHash":"858f9a00776163b1f8a34467b9c5727657f8971a9f4e9d492f0a247fac0384f9",
		"txnBlockNum":57175988,
		"createdAt":1747909635678,
		"expiredAt":1747909695000,
		"estimatedTransferFee":2000,
		"txnState":"ON_CHAIN",
		"id":"6c3ff67e-0bf4-4c09-91ca-0c7c254b01a0",
		"state":"CONFIRMING",
		"estimatedActivateFee":0,
		"gasFreeAddress":"TNER12mMVWruqopsW9FQtKxCGfZcEtb3ER",
		"txnTransferFee":2000,
		"txnAmount":100000
	}
}
GasFreeTrace:  successful!!
```

## 另请参见

- [reference/config](../reference/config.md)——GasFree API key / secret 的设置
- [usdt](usdt.md)——常规（非免 Gas）TRC20 转账
