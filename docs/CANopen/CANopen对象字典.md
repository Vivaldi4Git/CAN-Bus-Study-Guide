# 什么是对象字典?
对象字典是CANopen设备中所有可访问数据的结构化目录。它定义了设备的所有特性和功能。

对象字典是一本详细的设备说明书，列出了设备的所有功能、参数和使用方法。

# 对象字典的结构
打开对象字典这本书，我们可以看到他的目录是这样的:
![](attachments/Pasted%20image%2020241011160622.png)

通讯对象子协议区和制造商特定子协议区是用户需要关注的区域

## 通讯对象子协议区

我们"翻到"通讯对象子协议区，可以看到他的目录是这样的:
![](attachments/Pasted%20image%2020241011161447.png)

特别需要注意的是，索引范围 0x1000 到 0x1029 （图中绿色底纹部分）被定义为**通用通讯对象**。这些对象对于CANopen设备来说是**必不可少**的——如果一个设备缺少这些必要的对象，它将无法正常加入CANopen网络。

NMT启动时会读取设备信息，这些设备信息被定义在通用通讯对象中，所以必须要有实现。

### 通用通讯对象

"点开"通用通讯对象，我们可以看到他的构成:
![](attachments/Pasted%20image%2020241011163910.png)
![](attachments/Pasted%20image%2020241011163943.png)

如果说对象字典是一本详细的设备说明书，那么通用通讯对象可以比作这本说明书的"标准前言"或"快速入门指南"。通用通讯对象可以被视为CANopen设备的"最小构成"、"基本信息"，或者说通用通讯对象就像是CANopen设备的"最小可行产品"（MVP）。它们提供了设备加入网络、被识别、进行基本通信所必需的全部信息，是设备功能的核心和基础。

## 制造商特定子协议
对象字典索引 2000h to 5FFFh为制造商特定子协议，通常是存放所应用子协议的应用数据。

可以将制造商特定子协议视为CANopen的"官方mod管理器"。在许多单机游戏中，mod管理器可以安装mod，来扩展游戏功能。而制造商特定子协议可以安装"制造商特定对象"，来扩展CANopen设备的功能。

相应的通用通讯对象子协议区可以视为"游戏本体"，通用通讯对象则可以视为"游戏的基本玩法"。

## 标准化设备子协议

标准化设备子协议其实就是一种"官方mod"，由CANopen标准组织（CiA）官方开发和维护的子协议。目前已有十几种为不同类型的设备定义的子协议，例如 DS401、DS402、DS406 等，其索引值范围为 0x6000到0x9FFF。

## EDS文件：对象字典的文件格式

EDS文件是对象字典的文件格式，全称是"Electronic Device Specification"。下图为为 XGate-COP10 的 EDS 文件导入到 USBCAN-E-P 主站卡管理软件CANManager for CANopen 中。配置从站框中可以观察到 XGate-COP10 的对象字典内容，1008h的索引是这个设备的名称XGate-COP10，1009h是硬件版本，100Ah是软件版本，1018h的索引为标示对象，其下有若干个子索引，其中1008.01h 的子索引为厂商代码0x2B6，这是广州致远电子股份有限公司在 CiA 协会申请的厂商代码，任何一个生产 CANopen 的厂家虽然不强制加入 CiA 协会，但必须申请唯一的厂商代码。
![](attachments/Pasted%20image%2020241012093421.png)

下面是致远电子的XGate-COP10的EDS文件内容:
```eds
[FileInfo]
FileName=XGate-COP10.eds
FileVersion=1
FileRevision=100
EDSVersion=100
Description=EDS for XGate-COP10
CreationTime=10:22AM
CreationDate=06-20-2009
CreatedBy=
ModificationTime=10:22AM
ModificationDate=06-20-2009
ModifiedBy=xiangjl, GUANGZHOU ZHIYUAN electronic co.,ltd
[DeviceInfo]
VendorName=GUANGZHOU ZHIYUAN electronic co.,ltd
VendorNumber=694
ProductName=CANopen Comm_moudle
ProductNumber=0
RevisionNumber=100
OrderCode=XGate-COP10
Baudrate_10=1
Baudrate_20=1
Baudrate_50=1
Baudrate_125=1
Baudrate_250=1
Baudrate_500=1
Baudrate_800=1
Baudrate_1000=1
SimpleBootUpMaster=0
SimpleBootUpSlave=1
Granularity=8
DynamicChannelsSupported=0
GroupMessaging=0
NrOfRXPDO=12
NrOfTXPDO=12
LSS_Supported=1
[DummyUsage]
Dummy0001=0
Dummy0002=0
Dummy0003=0
Dummy0004=0
Dummy0005=1
```

# 参考资料
- [CANopen轻松入门（周立功）](CANopen轻松入门（周立功）.pdf)