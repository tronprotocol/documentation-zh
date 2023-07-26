# 轻节点

Lite FullNode和普通的FullNode运行同样的代码，所不同的是Lite FullNode只基于状态数据快照进行启动，状态数据快照只包含所有的账户状态数据和最近的65536个区块的历史数据。状态数据快照空间占用较小，约为全节点数据的3%，所以，Lite Fullnode具有占用磁盘空间小，启动速度块的优点。但它默认不提供节点历史区块和交易数据查询，仅提供部分全节点的HTTP API 和GRPC API，其中不支持的API请参考[HTTP](https://github.com/tronprotocol/java-tron/blob/develop/framework/src/main/java/org/tron/core/services/filter/LiteFnQueryHttpFilter.java)，[GRPC](https://github.com/tronprotocol/java-tron/blob/develop/framework/src/main/java/org/tron/core/services/filter/LiteFnQueryGrpcInterceptor.java)，但这些API可以在配置文件中通过配置 `openHistoryQueryWhenLiteFN = true`来打开，但由于轻节点启动后，其保存的数据与全节点完全相同，所以该配置项打开后，节点就支持查询节点启动后同步过来的区块数据了，但仍然不支持查询节点启动前的区块数据。


因此，如果开发者只需要使用节点进行区块同步，处理和广播交易，或者仅需查询节点启动后同步过来的区块及交易，那么Lite Fullnoe将是更好的选择。

## 轻节点部署
轻节点的部署步骤及启动命令和全节点相同，请参考[部署说明](../../using_javatron/installing_javatron/)来部署轻节点，唯一不同的是数据库，您需要获取到轻节点数据库，可以直接从[公共备份数据](../../using_javatron/backup_restore/#lite-fullnode)中下载轻节点数据快照，并直接使用；也可以通过[轻节点数据剪裁工具](../../using_javatron/toolkit/#_6)将全节点的数据库转换成轻节点的数据库。


## 轻节点维护
由于轻节点启动后，会保存与全节点同样的数据，所以轻节点虽然在启动时数据量非常小，但是后期的数据膨胀速度与全节点相同，因此可能需要定期剪裁数据。裁剪轻节点数据也是使用[轻节点数据剪裁工具](../../using_javatron/toolkit/#_6)将轻节点数据切分成快照数据集，即得到裁剪后的轻节点数据。