# wallet-cli x402 update-catalog

把 x402 目录下载到本地缓存。

## 用法

```
wallet-cli x402 update-catalog [options]
```

## 说明

下载整个目录（包含每个服务方的详细信息），保存到 `~/.cache/wallet-cli/x402/catalog.json`（文件权限 0600，目录 0700）。此后 [`x402 provider-list`](provider-list.md)、[`provider-show`](provider-show.md) 和 [`endpoint-list`](endpoint-list.md) 都从该文件作答，不再访问目录服务。

这些命令自己从不刷新该文件，因此想要最新的服务方与价格时，请重新执行 `update-catalog`。

只有全部下载成功时才会替换缓存；更新失败（例如 `timeout`）会保留原有缓存。目录版本若是本版本无法读取的，则以 `catalog_schema_unsupported` 失败。不需要钱包，也不需要密码。

## 选项

没有本命令特有的选项；仅[全局选项](../index.md#global-options-every-command)。

## 示例

```bash
wallet-cli x402 update-catalog
```

```console
✅ Provider catalog updated
  Providers     5
  Cache         /home/you/.cache/wallet-cli/x402/catalog.json
  Generated at  2026-07-30T08:04:57Z
```

```bash
wallet-cli x402 update-catalog -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"x402.update-catalog","data":{"updated":true,"cache":"/home/you/.cache/wallet-cli/x402/catalog.json","providers":5,"generatedAt":"2026-07-30T08:04:57Z"},"meta":{"durationMs":2873,"warnings":[]}}
```

`Providers` 是目录中列出的服务方数量，`Generated at`（JSON 中的 `generatedAt`）是目录本身最后一次发布的时间。

## 输出

| 字段 | 类型 | 含义 |
|---|---|---|
| `updated` | boolean | 缓存是否被替换 |
| `cache` | string | 缓存文件的绝对路径 |
| `providers` | number | 下载到的目录中的服务方数量 |
| `generatedAt` | string | 目录的生成时间 |

如果存在目录相关的警告，会放在 `meta.warnings` 中。

## 退出码

`0` 成功 · `1` 执行失败（`provider_error`——某次下载失败，或缓存文件无法写入；`catalog_schema_unsupported`；`response_too_large`；`timeout`） · `2` 用法错误。

## 另请参见

[`x402 provider-list`](provider-list.md) · [`x402 endpoint-list`](endpoint-list.md)
