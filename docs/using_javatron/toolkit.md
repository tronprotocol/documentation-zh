# Toolkit：Java-tron 节点维护工具集

TRON Toolkit 是一个集成了多种 `java-tron` 周边工具的实用程序，旨在简化节点维护和管理任务。未来，我们将持续为其添加更多功能，以提升开发者的使用体验。目前，Toolkit 提供了以下核心功能：

* [数据存储分区](#database-partitioning-tool) - 解决链上数据增长带来的存储压力
* [轻节点数据裁剪](#lite-fullnode-data-pruning) - 轻节点数据定期裁剪
* [数据拷贝](#fast-data-copy-tool) - 实现数据库快速拷贝
* [数据转换](#data-conversion-tool) - 支持 LevelDB 到 RocksDB 的数据库格式转换
* [LevelDB 启动优化](#leveldb-startup-optimization-tool) - 加快数据库类型为 LevelDB 的节点启动速度
* [Merkle Root 计算](#merkle-root-computation-tool) - 计算小型数据库的 Merkle Root，用于数据校验
* [Keystore 管理](#keystore-management) - 生成、导入、列出和更新账户 keystore 文件

本文将详细介绍如何获取和使用 TRON Toolkit。

**注意**：由于在 arm64 架构上只支持 RocksDB，所以像 `db convert` 和 `db archive` 这样处理 LevelDB 的工具只能在 x86_64 架构上使用。

## Toolkit 的获取

您可以通过编译 `java-tron` 源代码或直接从已发布的版本中获取 `Toolkit.jar` 文件。推荐从 [GitHub Releases](https://github.com/tronprotocol/java-tron/releases) 下载最新版本。

### 从源代码编译

1. **克隆 `java-tron` 源代码仓库**：

   ```bash
   git clone https://github.com/tronprotocol/java-tron.git
   git checkout -t origin/master
   ```

2. **编译项目**：

   ```bash
   cd java-tron
   ./gradlew clean build -x test
   ```

编译成功后，`Toolkit.jar` 文件将生成在 `java-tron/build/libs/` 目录下。

## 命令行输出与退出行为 { #command-line-output-and-exit-behavior }

Toolkit 的输出和退出码因命令而异。目前，Toolkit **不提供**全局 JSON 输出选项，也没有所有命令共用的统一错误 envelope。

* 使用具体命令调用 Toolkit 时，进程会以该命令返回的整数作为退出码。无效的命令行语法由 Picocli 处理，退出码为 `2`。
* 不带参数调用 Toolkit 时，会打印顶层用法并以退出码 `0` 结束。
* 下文介绍的 `keystore` 命令执行成功时返回 `0`，发生执行错误时通常返回 `1`。当目录不存在或没有 keystore 时，`keystore list` 也返回 `0`。
* `--json` 是逐命令选项，仅由 `keystore new`、`keystore import`、`keystore list` 和 `keystore update` 支持。它控制写入 stdout 的成功结果；即使指定了 `--json`，错误和警告仍以纯文本写入 stderr。
* `db` 命令不支持 JSON 输出，并保留各自的退出码行为。除非某条命令的文档明确说明，否则自动化程序不能假定 Toolkit 全局遵循 `0`/`1`/`2` 契约。

用于 shell 自动化时，应先检查退出码，再解析 stdout；不要尝试把 stderr 当作 JSON 解析。

## Keystore 管理 { #keystore-management }

`keystore` 命令组用于管理 Web3 Secret Storage 格式的账户 keystore 文件，替代已弃用的交互式 `FullNode.jar --keystore-factory` 工作流。

```bash
java -jar build/libs/Toolkit.jar keystore --help
```

默认 keystore 目录为当前工作目录下的 `Wallet`。可使用 `--keystore-dir <path>` 选择其他目录。

### 生成 Keystore { #generate-a-keystore }

`keystore new` 会生成随机密钥对，并写入加密的 keystore 文件：

```bash
# 交互式输入密码
java -jar build/libs/Toolkit.jar keystore new

# 非交互式输入密码并返回 JSON 结果
java -jar build/libs/Toolkit.jar keystore new \
  --keystore-dir /data/keystores \
  --password-file /secure/path/password.txt \
  --json
```

成功时的 JSON 输出包含生成的地址和文件名：

```json
{"address":"T...","file":"UTC--...json"}
```

### 导入私钥 { #import-a-private-key }

`keystore import` 用于导入以 64 个十六进制字符表示的 32 字节私钥，也接受 `0x` 或 `0X` 前缀。

```bash
# 交互式输入私钥和密码
java -jar build/libs/Toolkit.jar keystore import

# 非交互式导入
java -jar build/libs/Toolkit.jar keystore import \
  --keystore-dir /data/keystores \
  --key-file /secure/path/private-key.txt \
  --password-file /secure/path/password.txt \
  --json
```

成功时的 JSON 输出与 `keystore new` 相同，包含 `address` 和 `file` 字段。

默认情况下，如果目标目录中已经存在由该私钥派生地址对应的 keystore，命令会拒绝导入。仅当确实需要为同一地址创建额外的 keystore 时才使用 `--force`。

### 列出 Keystore { #list-keystores }

`keystore list` 会列出目录中结构有效的 `.json` keystore 文件：

```bash
java -jar build/libs/Toolkit.jar keystore list --keystore-dir /data/keystores
java -jar build/libs/Toolkit.jar keystore list --keystore-dir /data/keystores --json
```

成功时的 JSON 输出使用 `keystores` 数组封装结果：

```json
{
  "keystores": [
    {"address":"T...","file":"UTC--...json"}
  ]
}
```

如果目录不存在或其中没有有效的 keystore，JSON 模式会返回 `{"keystores":[]}`，退出码为 `0`。无法读取或格式错误的 `.json` 文件会被跳过，并可能在 stderr 输出警告。

`keystore list` 不会解密每个文件。显示的地址来自 keystore JSON 中声明的地址，本命令不会对其进行密码学验证。仅信任来自受控来源的 keystore。

### 更新 Keystore 密码 { #update-a-keystore-password }

`keystore update` 会按地址查找 keystore，使用当前密码解密，然后通过临时文件以新密码重写。Toolkit 会先尝试原子替换；如果文件系统不支持，则回退到普通替换：

```bash
# 交互式输入密码
java -jar build/libs/Toolkit.jar keystore update T... \
  --keystore-dir /data/keystores

# 非交互式更新密码
java -jar build/libs/Toolkit.jar keystore update T... \
  --keystore-dir /data/keystores \
  --password-file /secure/path/passwords.txt \
  --json
```

对于 `update`，密码文件必须恰好包含两行：第一行为当前密码，第二行为新密码。

成功时的 JSON 输出包含验证后的地址、文件名和更新状态：

```json
{"address":"T...","file":"UTC--...json","status":"updated"}
```

如果没有匹配的 keystore，或有多个有效 keystore 声明了所请求的地址，命令会失败，不会在重复项中任意选择。

### Keystore 选项与安全 { #keystore-options-and-security }

| 选项 | 命令 | 行为 |
|---|---|---|
| `--keystore-dir <path>` | 全部 | keystore 目录，默认为 `Wallet`。 |
| `--json` | 全部 | 将成功结果以 JSON 写入 stdout；错误仍以文本写入 stderr。 |
| `--password-file <file>` | `new`、`import`、`update` | 避免交互式密码提示。`new` 和 `import` 要求一行；`update` 要求恰好两行。 |
| `--key-file <file>` | `import` | 从文件而非终端读取私钥。 |
| `--force` | `import` | 允许为已有 keystore 的地址再创建一个 keystore。 |
| `--sm2` | `new`、`import`、`update` | 使用 SM2 而非默认的 ECDSA。对于 `update`，必须与现有 keystore 使用的算法一致。 |

密码和私钥输入文件必须是大小不超过 1,024 字节的普通文件；符号链接会被拒绝。`keystore new` 和 `keystore import` 设置的密码，以及 `keystore update` 提供的新密码，必须至少包含六个字符。为兼容旧 keystore，`keystore update` 不对当前密码应用这一最小长度限制。在 POSIX 系统上，Toolkit 会以仅所有者可访问的 `0600` 权限创建或重写 keystore 文件。

!!! warning "保护临时密钥文件"
    `--password-file` 和 `--key-file` 支持非交互式执行，但这些文件以明文保存敏感信息。请将它们存放在仓库之外，使用 `chmod 600` 将权限限制为当前用户，切勿提交到版本控制，并在不再需要时删除。

## 数据存储分区工具 { #database-partitioning-tool }

随着 TRON 链上数据的持续增长（目前主网全节点数据已达 2TB，每日增长约 1.2GB），节点的数据存储压力日益增大。为了解决单个磁盘容量不足的问题，TRON Toolkit 引入了**数据库存储分区工具**。该工具允许您根据配置将部分数据库迁移到其他存储盘，从而在磁盘空间不足时，无需更换原有磁盘，只需增加新的存储设备即可。

### 命令与参数

使用 `db mv` 命令来执行数据迁移操作：

```bash
# full command
java -jar build/libs/Toolkit.jar db mv [-h] [-c=<config>] [-d=<database>]
# examples
java -jar build/libs/Toolkit.jar db mv -c framework/src/main/resources/config.conf -d /data/tron/output-directory
```

**可选参数**：

*   `-c | --config <string>`：指定 FullNode 配置文件路径。默认值为 `config.conf`。
*   `-d | --database-directory <string>`：指定 FullNode 数据库目录。默认值为 `output-directory`。
*   `-h | --help <boolean>`：显示帮助信息。默认值为 `false`。

### 使用步骤

请按照以下步骤使用数据库存储分区工具：

1. [停止 FullNode 服务](#stop-the-fullnode-service)
2. [配置数据库存储迁移](#configure-database-storage-migration)
3. [执行数据库迁移](#execute-the-database-migration)
4. [重新启动 FullNode 服务](#restart-the-fullnode-service)


#### 1. 停止 FullNode 服务 { #stop-the-fullnode-service }

在执行数据库迁移之前，**必须**停止当前运行的 FullNode 服务。您可以使用以下命令查找 FullNode 进程 ID（PID）并终止进程：

```bash
kill -15 $(ps -ef | grep FullNode.jar | grep -v grep | awk '{print $2}')
```


#### 2. 配置数据库存储迁移 { #configure-database-storage-migration }

数据库迁移的配置通过 `java-tron` 节点配置文件中的 `storage.properties` 字段进行。您可以在 [java-tron 仓库](https://github.com/tronprotocol/java-tron/blob/master/framework/src/main/resources/config.conf) 中找到示例配置。

以下示例展示了如何将 `block` 和 `trans` 数据库迁移到 `/data1/tron` 目录：

```properties
storage {
 ......
  properties = [
    {
     name = "block",
     path = "/data1/tron",
    },
    {
     name = "trans",
     path = "/data1/tron",
   }
  ]
 ......
}
```

*   `name`：指定要迁移的数据库名称。
*   `path`：指定数据库迁移的目标目录。

工具会将 `name` 指定的数据库迁移到 `path` 指定的目录，并在原目录下创建一个软链接指向新目录。FullNode 启动后将通过此软链接找到数据。

#### 3. 执行数据库迁移 { #execute-the-database-migration }

配置完成后，执行以下命令进行数据库迁移。命令执行时会显示当前迁移进度：

```bash
java -jar build/libs/Toolkit.jar db mv -c framework/src/main/resources/config.conf -d /data/tron/output-directory
```

#### 4. 重新启动 FullNode 服务 { #restart-the-fullnode-service }

数据库迁移完成后，重新启动 `java-tron` 节点。

[**FullNode 启动命令示例**](installing_javatron.md#starting-a-fullnode-on-the-tron-main-network)

[**超级代表（SR）FullNode 启动命令示例**](installing_javatron.md#starting-a-block-production-node)

## 轻节点数据裁剪工具 { #lite-fullnode-data-pruning }

TRON Toolkit 提供了**数据裁剪工具**，主要用于生成和管理轻节点数据。

全节点的完整数据可被分成两部分：快照数据集（Snapshot dataset）或历史数据集（History dataset）。

*   **快照数据集**：用于启动轻节点，不包含裁剪时的最新区块高度之前的历史数据。
*   **历史数据集**：用于历史数据查询。

快照数据集只包含全网最新状态数据和最近的 65536 个区块的历史数据。其占用空间远小于全节点数据，而轻节点只基于快照数据集来启动，所以，Lite Fullnode 具有占用磁盘空间小，启动速度快的优点。

而数据裁剪工具能够根据当前最新区块高度将FullNode的完整数据切分为**快照数据集**（Snapshot dataset）或**历史数据集**（History dataset）；同时数据裁剪工具还支持将历史数据集与快照数据集进行合并，以满足不同的使用场景：


* **将全节点数据切分成轻节点数据**：通过将全节点数据切分为快照数据集，即可得到用于启动轻节点的数据。
* **定期裁剪轻节点数据**：轻节点启动后数据量会随时间增长，因此可能需要定期裁剪。使用数据裁剪工具将轻节点数据切分为新的快照数据集，即可实现裁剪。
* **将轻节点数据转回全节点数据**：如果需要轻节点支持历史数据查询，可以将其转换为全节点。除了直接下载全节点数据库快照外，您也可以先将全节点数据切分为历史数据集，然后将其与轻节点的快照数据集合并，从而得到一个完整的全节点数据。

> **重要提示**：在使用本工具进行任何操作之前，**必须**停止当前运行的节点。

### 命令与参数

使用 `db lite` 命令来执行数据裁剪操作：

```bash
# full command
  java -jar build/libs/Toolkit.jar db lite [-h] -ds=<datasetPath> -fn=<fnDataPath> [-o=<operate>] [-t=<type>]
# examples
  #split and get a snapshot dataset
  java -jar build/libs/Toolkit.jar db lite -o split -t snapshot --fn-data-path output-directory/database --dataset-path /tmp
  #split and get a history dataset
  java -jar build/libs/Toolkit.jar db lite -o split -t history --fn-data-path output-directory/database --dataset-path /tmp
  #merge history dataset and snapshot dataset
  java -jar build/libs/Toolkit.jar db lite -o merge --fn-data-path /tmp/snapshot --dataset-path /tmp/history
```

**可选参数**：

*   `-o | --operate <split | merge>`：指定操作类型，`split`（拆分）或 `merge`（合并）。默认值为 `split`。
*   `-t | --type <snapshot | history>`：仅与 `-o split` 配合使用。`snapshot` 表示切分为快照数据集，`history` 表示切分为历史数据集。
*   `-fn | --fn-data-path <string>`：
    *   当操作类型为 `split` 时，指定待裁剪数据的目录。
    *   当操作类型为 `merge` 时，指定轻节点的数据库目录或快照数据集的目录。
*   `-ds | --dataset-path <string>`：
    *   当操作类型为 `split` 时，指定切分完成的快照数据集或历史数据集的输出目录。
    *   当操作类型为 `merge` 时，指定历史数据集目录。


### 使用示例

节点数据库通常默认保存在 `output-directory/database` 目录下。以下示例将以该默认目录进行说明。

#### 切分快照数据集

此功能可将全节点数据转换为轻节点数据，也可用于定期裁剪轻节点数据。步骤如下：

首先，停止节点，然后执行以下命令：


```bash
# 简单起见，将快照数据集存放在`/tmp`目录下
java -jar build/libs/Toolkit.jar db lite -o split -t snapshot --fn-data-path output-directory/database --dataset-path /tmp
```

* `--fn-data-path`： 待裁剪数据目录，即节点数据目录
* `--dataset-path`： 存放输出的快照数据集的目录

命令执行完毕后，将在 `/tmp` 目录下生成一个名为 `snapshot` 的目录。此目录中的数据即为轻节点数据。将该目录中的数据拷贝到节点数据库目录中（例如，将 `snapshot` 目录重命名为 `database` 并拷贝到 Lite FullNode 的运行目录 `output-directory` 下），然后启动轻节点即可。

#### 切分历史数据集

切分历史数据集的命令如下：

```bash
# 简单起见，将历史数据集存放在 `/tmp` 目录下
java -jar build/libs/Toolkit.jar db lite -o split -t history --fn-data-path output-directory/database --dataset-path /tmp
```

*   `--fn-data-path`：全节点数据目录
*   `--dataset-path`：存放输出的历史数据集的目录

命令执行完毕后，将在 `/tmp` 目录下生成一个名为 `history` 的目录，其中包含切分好的历史数据集。

#### 合并历史数据集和快照数据集

历史数据集和快照数据集中都包含一个 `info.properties` 文件，用于记录数据拆分时的区块高度。
> **请注意**：在合并两个数据集时，历史数据集的区块高度必须大于或等于快照数据集的区块高度。通过 `merge` 操作合并后，轻节点将成为一个真正的全节点。

合并历史数据集和快照数据集的命令如下：

```shell
# 简单起见，假设快照数据集存放在 `/tmp/snapshot`，历史数据集存放在 `/tmp/history`
java -jar build/libs/Toolkit.jar db lite -o merge --fn-data-path /tmp/snapshot --dataset-path /tmp/history
```

*   `--fn-data-path`：快照数据集目录。
*   `--dataset-path`：历史数据集目录。

命令执行完毕后，合并后的数据将覆盖 `--fn-data-path` 指定的快照数据集所在目录。将合并完成的数据拷贝到节点数据库目录下，轻节点即可转换为全节点。

## 数据拷贝工具 { #fast-data-copy-tool }

节点数据库通常较大，传统的数据拷贝操作耗时较长。TRON Toolkit 提供了**数据库快速拷贝功能**，通过创建硬链接的方式，在同一磁盘中实现 LevelDB 或 RocksDB 数据库的高效拷贝。

### 命令与参数

使用 `db cp` 命令来执行数据拷贝操作：

```shell
# full command
  java -jar build/libs/Toolkit.jar db cp [-h] <src> <dest>
# examples
  java -jar build/libs/Toolkit.jar db cp  output-directory/database /tmp/databse
```

**可选参数**：

*   `<src>`：指定源数据库目录。默认值为 `output-directory/database`。
*   `<dest>`：指定拷贝的目标目录。默认值为 `output-directory-cp/database`。
*   `-h | --help <boolean>`：显示帮助信息。默认值为 `false`。

> **重要提示**：在使用本工具进行任何操作之前，**必须**停止当前运行的节点。

## 数据转换工具 { #data-conversion-tool }

TRON Toolkit 支持数据库数据转换功能，可以将 LevelDB 格式的数据转换为 RocksDB 格式。

### 命令与参数

使用 `db convert` 命令来执行数据转换操作：


```bash
# full command
  java -jar build/libs/Toolkit.jar db convert [-h] <src> <dest>
# examples
  java -jar build/libs/Toolkit.jar db convert  output-directory/database /tmp/database
```

**可选参数**：

*   `<src>`：指定 LevelDB 数据目录。默认值为 `output-directory/database`。
*   `<dest>`：指定输出的 RocksDB 数据目录。默认值为 `output-directory-dst/database`。
*   `-h | --help <boolean>`：显示帮助信息。默认值为 `false`。

> **重要提示**：在使用本工具进行任何操作之前，必须停止当前运行的节点。

## LevelDB 启动优化工具 { #leveldb-startup-optimization-tool }

随着 LevelDB 数据库的持续运行，其 `manifest` 文件会不断增长。过大的 `manifest` 文件不仅会影响节点启动速度，还可能导致内存持续增长并引发服务异常中止。为了解决这些问题，TRON Toolkit 提供了 **LevelDB 启动优化工具**。该工具可以优化 `manifest` 文件大小和 LevelDB 的启动过程，从而减少内存占用并提升节点启动速度。

### 命令与参数

使用 `db archive` 命令来执行 LevelDB 启动优化操作：


```bash
# full command
   java -jar build/libs/Toolkit.jar db archive [-h] [-b=<maxBatchSize>] [-d=<databaseDirectory>] [-m=<maxManifestSize>]
# examples
   #1. use default settings
   java -jar build/libs/Toolkit.jar db archive 
   #2. specify the database directory as /tmp/db/database
   java -jar build/libs/Toolkit.jar db archive -d /tmp/db/database 
   #3. specify the batch size to 64000 when optimizing manifest
   java -jar build/libs/Toolkit.jar db archive -b 64000
   #4. specify optimization only when Manifest exceeds 128M
   java -jar build/libs/Toolkit.jar db archive -m 128 
```

**可选参数**：

*   `-b | --batch-size <integer>`：指定 `manifest` 批处理大小。默认值为 `80000`。
*   `-d | --database-directory <string>`：指定 LevelDB 数据库目录。默认值为 `output-directory/database`。
*   `-m | --manifest-size <integer>`：`manifest` 文件的最小大小（单位：MB）。当 `manifest` 文件大小低于此值时，不进行处理；高于此值时才进行批处理。默认值为 `0`。
*   `-h | --help <boolean>`：显示帮助信息。默认值为 `false`。

> **重要提示**：在使用本工具进行任何操作之前，**必须**停止当前运行的节点。

## Merkle Root 计算工具 { #merkle-root-computation-tool }

TRON Toolkit 提供了 **Merkle Root 计算工具**，可以计算指定数据库的 Merkle Root，用于跨节点的数据校验和一致性比对。

> **重要提示**：本工具仅适用于小型数据库。在大型数据库上运行可能会触发 `GC overhead limit exceeded` 异常。

### 命令与参数

使用 `db root` 命令来计算 Merkle Root：

```bash
# full command
   java -jar build/libs/Toolkit.jar db root [-h] [--db=<dbs>]... [<db>]
# examples
   #计算默认数据库目录下 account 和 witness 两个数据库的 Merkle Root
   java -jar build/libs/Toolkit.jar db root --db account --db witness
   #指定数据库目录
   java -jar build/libs/Toolkit.jar db root --db account /tmp/db/database
```

**可选参数**：

*   `<db>`：指定数据库目录。默认值为 `output-directory/database`。
*   `--db <string>`：指定需要计算 Merkle Root 的数据库名称。该选项可以重复使用，以同时计算多个数据库。
*   `-h | --help <boolean>`：显示帮助信息。默认值为 `false`。
