背景：nmt.c:2375: debug: NMT: slave 1 finished booting with error status A

case 'A': return "The CANopen device is not listed in object 1F81.";

修改从站配置

```[1F81]
ParameterName=NMT slave assignment    # 对象名称：NMT从站分配
ObjectType=0x08                       # 对象类型：0x08表示ARRAY数组类型
DataType=0x0007                       # 数据类型：0x0007表示UNSIGNED32（32位无符号整数）
AccessType=rw                         # 访问类型：rw表示可读写
CompactSubObj=127                     # 子索引数量：最多支持127个从站

[1F81Value]
NrOfEntries=1
127=0x00000005

```
```
[1F81Value]
NrOfEntries=1                        # 实际使用的条目数
1=0x00000007                         # 节点ID=1的配置值
```

配置值 0x00000007 的含义：
bit 0 (0x01)：1 - 在网络列表中
bit 1 (0x02)：1 - 需要启动
bit 2 (0x04)：1 - 支持设备监控
总计：0x01 + 0x02 + 0x04 = 0x07

0x00000003 = 0b11：表示该节点在网络列表中且需要启动
原来的 0x00000005 = 0b101：表示该节点在网络列表中且支持设备监控