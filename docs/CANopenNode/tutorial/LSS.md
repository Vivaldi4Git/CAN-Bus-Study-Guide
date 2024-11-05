
# 什么是LSS

LSS (Layer Setting Service) 是 CANopen 的一个重要服务，主要用于配置节点的基本参数。LSS 是扩展协议：
```
CANopen 协议
├── 核心协议 (CiA 301)
│   ├── NMT
│   ├── SDO
│   └── PDO
│   ├── Safety (CiA 304)
│   └── 其他...
```

# 为什么需�?LSS�?
想象一个场景：
```
新设备──接入网络──如何分配节点ID──如何设置正确的波特率
```

## 什么是波特率？

波特率 = 通信速度
例如：250 kbps = 每秒传输 250,000 位数
    越高 传输越快
    但距离受限


## 实际应用：新设备接入网络
1. 设备处于未配置状态
2. LSS 主机扫描网络
3. 发现新设备
4. 配置节点ID和波特率
5. 存储配置

# 使用LSS配置节点
官方给出的操作步骤如下：
```
cocomm "help lss"
cocomm "lss_switch_sel 0x00000000 0x00000001 0x00000002 0x00000003"
cocomm "lss_get_node"
cocomm "lss_set_node 10"
cocomm "lss_store"
cocomm "lss_switch_glob 0"
cocomm "4 reset comm"
```

但我在尝试操作 `lss_switch_sel` 时，即输入：
```
cocomm "lss_switch_sel 0x00000000 0x00000001 0x00000002 0x00000003"
```

提示错误：
```
[1] ERROR:103 #Time-out.
```

看起来像是设备没有响应。
查看这个demo设备的标识符，方式参看文档第二段：
>LSS uses the the OD Identity register (0x1018) as an unique value to select a node. Therefore the LSS address always consists of four 32 bit values. This also means that LSS relies on this register to actually be unique. (_vendorID_, _productCode_, _revisionNumber_ and _serialNumber_ must be configured and unique on each device.)

当然，因为刚启动了demo设备，我们知道他的id是：
```
cocomm "4 read 0x1018 1 u32"  # Vendor ID
cocomm "4 read 0x1018 2 u32"  # Product Code
cocomm "4 read 0x1018 3 u32"  # Revision Number
cocomm "4 read 0x1018 4 u32"  # Serial Number
```

返回如下：
```
cocomm "4 read 0x1018 1 u32"
[1] 0
cocomm "4 read 0x1018 2 u32"
[1] 1
cocomm "4 read 0x1018 3 u32"
[1] 0
cocomm "4 read 0x1018 4 u32"
[1] 3
```

显然应该设置为：0 1 0 3
```
cocomm "lss_switch_sel 0x00000000 0x00000001 0x00000000 0x00000
003"
```

重新设置后成功。
## fastscan

fastscan用于搜索网络?*未配置*的设备。
```
cocomm "_lss_fastscan"
```

在执行之前需要先转换到global模式。
```
cocomm "lss_switch_glob 1"
```

执行完后会显示：
```
[1] 0x00000000 0x00000000 0x00000000 0x00000000
```

这是一个未配置的节点。
设置新的节点ID，存储到EEPROM，应用新的节点ID。
```
cocomm "lss_set_node 4"
cocomm "lss_store"
cocomm "lss_switch_glob 0"
```

为了提高扫描速度，可以设置扫描步进时间：
```
cocomm "_lss_fastscan 25"
```
25的意思是扫描步进时间，单位是毫秒。请注意当延迟设置得太低时扫描会变得不可靠。
# Auto enumerate all nodes 自动枚举所有节点
通过LSS fastscan自动枚举所有未配置的节点。枚举从节点ID 2开始，节点ID自动存储到EEPROM。与_lss_fastscan类似，可以可选参数更改默认延迟时间。为了使此示例正常工作，请将demoDevice设置为上述未配置的节点ID。
```
cocomm "lss_allnodes"
```

请注意，只有未配置的节点（那些没有有效节点ID的节点）才会参与fastscan。
