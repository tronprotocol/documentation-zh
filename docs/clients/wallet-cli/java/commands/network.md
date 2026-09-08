# 网络命令

在已配置的 TRON 网络之间切换并查看当前网络。三个内置网络是 `MAIN`、`NILE` 和 `SHASTA`；你也可以
指向自定义端点。网络在本地如何配置，参见[配置参考](../reference/config.md)。

## SwitchNetwork

随时切换网络。`switchnetwork local` 切换到你本地 `config.conf` 中配置的网络。

交互式选择：

```console
wallet> switchnetwork
Please select network：
1. MAIN
2. NILE
3. SHASTA
Enter numbers to select a network (1-3):1
Now, current network is : MAIN
SwitchNetwork  successful !!!
```

按名称直接选择：

```console
wallet> switchnetwork main
Now, current network is : MAIN
SwitchNetwork  successful !!!
```

自定义端点（`switchnetwork <fullnode> <soliditynode>`，用 `empty` 省略其中之一）：

```console
wallet> switchnetwork empty localhost:50052
Now, current network is : CUSTOM
SwitchNetwork  successful !!!
```

## CurrentNetwork

查看当前网络。

```console
wallet> currentnetwork
current network: NILE
```

对于自定义网络，会显示节点端点：

```console
wallet> currentnetwork
current network: CUSTOM
fullNode: EMPTY, solidityNode: localhost:50052
```

## 另请参见

- [reference/config](../reference/config.md)——节点端点配置
