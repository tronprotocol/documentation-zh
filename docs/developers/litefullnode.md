# 轻节点

Lite FullNode和普通的FullNode运行同样的代码，所不同的是Lite FullNode只基于状态数据快照进行启动，状态数据快照只包含所有的账户状态数据和最近的256个区块的历史数据。而且在节点运行过程中，只存储和状态数据快照相关的数据，而不保存区块和交易的历史数据。因此Lite Fullnode具有占用磁盘空间小，启动速度块的优点，但它不提供历史区块和交易数据查询，仅提供部分全节点的HTTP API 和GRPC API，其中不支持的API请参考[HTTP](https://github.com/tronprotocol/java-tron/blob/develop/framework/src/main/java/org/tron/core/services/filter/LiteFnQueryHttpFilter.java)，[GRPC](https://github.com/tronprotocol/java-tron/blob/develop/framework/src/main/java/org/tron/core/services/filter/LiteFnQueryGrpcInterceptor.java)，这些API可以通过在配置文件中配置 `openHistoryQueryWhenLiteFN = true`来强制打开，但不推荐这样做。


因此，如果开发者只需要使用节点进行区块同步，处理和广播交易，那么Lite Fullnoe将是更好的选择。

轻节点的部署步骤和全节点相同，不同的是需要获取到轻节点数据库，您可以直接从公共备份数据中下载轻节点数据快照，并直接使用；也可以通过轻节点工具将全节点的数据库转换成轻节点的数据库。下面将详细介绍轻节点工具的使用。

# 轻节点工具

Lite FullNode工具用于将全节点（FullNode）的数据切分成快照数据集（Snapshot dataset）和历史数据集（History dataset）两部分。

* `Snapshot dataset`: 用于快速启动Lite FullNode节点的必要数据集。
* `History dataset`: 用于历史数据查询的归档数据集。

使用本工具进行任何操作之前，需要首先停止当前运行的FullNode节点。 本工具提供了根据当前`最新区块高度`(latest_block_number)将完整数据切分成两个数据集的功能。通过快照数据集启动的轻节点不支持查询此区块高度之前的历史数据。本工具还提供了将历史数据集同快照数据集合并的功能。

更多的设计思想，请参考: [TIP-128](https://github.com/tronprotocol/tips/issues/128)。

## Lite Fullnode工具的获取
可以通过编译java-tron源代码来获取 LiteFullNodeTool.jar，步骤如下：

1. 获取java-tron源码
    ```
    $ git clone https://github.com/tronprotocol/java-tron.git
    $ git checkout -t origin/master
    ```
2. 编译
    ```    
    $ cd java-tron
    $ ./gradlew clean build -x test
    ```

    编译完成之后，`LiteFullNodeTool.jar`会生成在 `java-tron/build/libs/` 目录下。


## Lite Fullnode工具的使用
### 选项

此工具提供了快照数据集和历史数据集独立的拆分功能和合并功能。

- `--operation | -o`: [ split | merge ]  此选项用于指定使用拆分功能还是合并功能。
- `--type | -t`: [ snapshot | history ]  此选项只能同`-o split`配合使用。 `snapshot` 指示切分为快照数据集，`history`指示切分为历史数据集。 
- `--fn-data-path`: FullNode数据库的目录。
- `--dataset-path`: 切分完成的数据集输出目录。 当操作类型是 `split`时, `dataset-path` 用于指示切分完成的快照数据集输出目录或者历史数据集输出目录；当操作类型是 `merge`时， `dataset-path`指示历史数据集的输出目录。

### 例子

通过默认的配置文件启动全节点时，将在当前启动目录下生成一个`output-directory`目录，在`output-directory` 目录的`database`子目录就是将要被切分的数据库。 

* **切分快照数据集**

    首先, 停止FullNode并执行命令:

    ```shell
    # 简单起见，将快照数据集存放在`/tmp`目录下
    java -jar LiteFullNodeTool.jar -o split -t snapshot --fn-data-path output-directory/database --dataset-path /tmp
    ```

    命令执行完毕之后，将在`/tmp`目录下生成`snapshot`目录, 将此目录的名字修改为`database`，并拷贝到Lite FullNode的运行目录output-directory之下。 

* **切分历史数据集**

    如果需要查询历史数据，历史数据集必须被生成并合并到微节点数据库中。

    ```shell
    # 简单起见，将历史数据集存放在`/tmp`目录下
    java -jar LiteFullNodeTool.jar -o split -t history --fn-data-path output-directory/database --dataset-path /tmp
    ```

    命令执行完毕之后，将在`/tmp`目录下生成`history`目录，将此目录拷贝到Lite FullNode运行目录output-directory之下，注意需要确保有足够的硬盘空间来存储历史数据集。

* **合并历史数据集和快照数据集**

    历史数据集和快照数据集中都保存了一个info.properties文件，用于记录数据拆分时的区块高度。需要注意的是，两个数据集进行合并时，历史数据集的区块高度必须大于等于快照数据集的区块高度。通过merge操作将历史数据集同快照数据集进行合并之后，微节点将成为一个真正的全节点。

    ```shell
    # 简单起见，假设历史数据集存放在了`/tmp`目录下
    java -jar LiteFullNodeTool.jar -o merge --fn-data-path output-directory/database --dataset-path /tmp/history
    ```

