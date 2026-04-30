# /wallet/accountpermissionupdate

修改账户的 owner / witness / active 权限（多签配置）。

- 源码：`framework/src/main/java/org/tron/core/services/http/AccountPermissionUpdateServlet.java`
- Method：`POST`
- Contract：`protocol.AccountPermissionUpdateContract`（`account_contract.proto:44`）

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `owner_address` | string | 是 | 账户地址 |
| `owner` | Permission | 是 | owner 权限（type=Owner，id=0；不能为空） |
| `witness` | Permission | 否 | 见证人权限（type=Witness，id=1）；只有 SR 账户填 |
| `actives` | repeated Permission | 是 | active 权限列表（type=Active，id 从 2 开始） |
| `permission_id` | int32 | 否 | 当前签名所用权限 ID |
| `visible` | bool | 否 | 地址格式 |

`Permission` 字段（`Tron.proto:262`）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `type` | enum | `Owner` / `Witness` / `Active` |
| `id` | int32 | Owner=0，Witness=1，Active>=2 |
| `permission_name` | string | 权限名 |
| `threshold` | int64 | 触发阈值（所有 key.weight 之和达到该值才生效） |
| `operations` | bytes | active 权限可执行的合约类型位图（hex，32 字节） |
| `keys` | repeated Key | 签名 key（`{address, weight}`） |

示例（最小 owner 权限 + 1 个 active）：

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/accountpermissionupdate \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "owner": {
    "type": 0, "id": 0, "permission_name": "owner",
    "threshold": 1,
    "keys": [{ "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9", "weight": 1 }]
  },
  "actives": [{
    "type": 2, "id": 2, "permission_name": "active",
    "threshold": 1,
    "operations": "7fff1fc0033e0100000000000000000000000000000000000000000000000000",
    "keys": [{ "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9", "weight": 1 }]
  }]
}
'
```

## 响应

返回未签名 `protocol.Transaction`。

响应示例（`txID`、`ref_block_*`、`expiration`、`timestamp`、`raw_data_hex` 因构造时机而异）：

```json
{
  "visible": false,
  "txID": "beb8e742fc1f345a9eed45456e54cb3eba4ec286845b57a89bc8638e2e6a8dad",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "owner": {
              "permission_name": "owner",
              "threshold": 1,
              "keys": [
                { "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9", "weight": 1 }
              ]
            },
            "actives": [
              {
                "type": "Active",
                "id": 2,
                "permission_name": "active",
                "threshold": 1,
                "operations": "7fff1fc0033e0100000000000000000000000000000000000000000000000000",
                "keys": [
                  { "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9", "weight": 1 }
                ]
              }
            ]
          },
          "type_url": "type.googleapis.com/protocol.AccountPermissionUpdateContract"
        },
        "type": "AccountPermissionUpdateContract"
      }
    ],
    "ref_block_bytes": "270b",
    "ref_block_hash": "d95e28e9c4c8af73",
    "expiration": 1777445901000,
    "timestamp": 1777445841729
  },
  "raw_data_hex": "0a02270b2208d95e28e9c4c8af7340c8a5a0c0dd335ad001082e12cb010a3c747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e4163636f756e745065726d697373696f6e557064617465436f6e7472616374128a010a1541dd791d6b49e190062d650e6a23c575510d35f2f912241a056f776e657220013a190a1541dd791d6b49e190062d650e6a23c575510d35f2f91001224b080210021a06616374697665200132207fff1fc0033e01000000000000000000000000000000000000000000000000003a190a1541dd791d6b49e190062d650e6a23c575510d35f2f9100170c1d69cc0dd33"
}
```

> 注：响应中 `owner.type` 和 `owner.id` 为协议 enum/默认值，序列化时被省略，等价于 `Owner`/`0`。

⚠️ 一旦生效，旧 owner 权限失效；务必先模拟验证。

### 异常响应

| 触发条件 | 响应 |
|---|---|
| 请求体超过 `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| 请求体不是合法 JSON / 字段类型不符 | `{"Error": "class com.alibaba.fastjson.JSONException : <解析器信息>"}` 或 `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <解码器信息>"}` |
| `AllowMultiSign` 提案未开启 | `{"Error": "class org.tron.core.exception.ContractValidateException : multi sign is not allowed, need to be opened by the committee"}` |
| `owner_address` 不是 21 字节合法地址 | `{"Error": "class org.tron.core.exception.ContractValidateException : invalidate ownerAddress"}` |
| `owner_address` 在链上不存在 | `{"Error": "class org.tron.core.exception.ContractValidateException : ownerAddress account does not exist"}` |
| 缺失 `owner` 权限 | `{"Error": "class org.tron.core.exception.ContractValidateException : owner permission is missed"}` |
| SR 账户缺失 `witness` 权限 | `{"Error": "class org.tron.core.exception.ContractValidateException : witness permission is missed"}` |
| 非 SR 账户却设置了 `witness` 权限 | `{"Error": "class org.tron.core.exception.ContractValidateException : account isn't witness can't set witness permission"}` |
| 缺失 `actives` 权限 | `{"Error": "class org.tron.core.exception.ContractValidateException : active permission is missed"}` |
| `actives` 数量超过 8 | `{"Error": "class org.tron.core.exception.ContractValidateException : active permission is too many"}` |
| `owner.type != Owner` | `{"Error": "class org.tron.core.exception.ContractValidateException : owner permission type is error"}` |
| `witness.type != Witness` | `{"Error": "class org.tron.core.exception.ContractValidateException : witness permission type is error"}` |
| `actives[i].type != Active` | `{"Error": "class org.tron.core.exception.ContractValidateException : active permission type is error"}` |
| `Permission.keys` 数量超过 5 | `{"Error": "class org.tron.core.exception.ContractValidateException : number of keys in permission should not be greater than 5"}` |
| `Permission.keys` 为空 | `{"Error": "class org.tron.core.exception.ContractValidateException : key's count should be greater than 0"}` |
| `witness` 权限的 keys 不为 1 | `{"Error": "class org.tron.core.exception.ContractValidateException : Witness permission's key count should be 1"}` |
| `Permission.threshold <= 0` | `{"Error": "class org.tron.core.exception.ContractValidateException : permission's threshold should be greater than 0"}` |
| `Permission.permission_name` 长度超过 32 字节 | `{"Error": "class org.tron.core.exception.ContractValidateException : permission's name is too long"}` |
| `Permission.parent_id != 0` | `{"Error": "class org.tron.core.exception.ContractValidateException : permission's parent should be owner"}` |
| `keys` 中存在重复地址 | `{"Error": "class org.tron.core.exception.ContractValidateException : address should be distinct in permission <Owner\|Witness\|Active>"}` |
| `keys[i].address` 不是 21 字节合法地址 | `{"Error": "class org.tron.core.exception.ContractValidateException : key is not a validate address"}` |
| `keys[i].weight <= 0` | `{"Error": "class org.tron.core.exception.ContractValidateException : key's weight should be greater than 0"}` |
| `Permission.threshold` 大于 `keys.weight` 之和 | `{"Error": "class org.tron.core.exception.ContractValidateException : sum of all key's weight should not be less than threshold in permission <Owner\|Witness\|Active>"}` |
| `active.operations` 长度不为 32 字节 | `{"Error": "class org.tron.core.exception.ContractValidateException : operations size must 32"}` |
| `active.operations` 中包含未注册的合约类型位 | `{"Error": "class org.tron.core.exception.ContractValidateException : <i> isn't a validate ContractType"}` |
| 其他异常 | `{"Error": "<exceptionClass> : <message>"}` |
