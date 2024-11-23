假设在Linux 系统中，我们首先进入tutorial目录:
```bash
cd tutorial
```
文件夹结构如下：
```
tutorial
    LSS.md
    PDO.md
    README.md
    SDO.md
```

README.md 中有一段简短的教程，并提供了其他教程的链接。主要帮助我们理解CAN的运行。
# 准备

LINUX系统

# 搭建环境

教程提供了几种工具，用于帮助查看CANopen网络上的数据。
## 1. 创建虚拟 CAN 网络
```bash
# 加载虚拟 CAN 模块
sudo modprobe vcan
# 创建一个叫 can0 的虚拟CAN 接口
sudo ip link add dev can0 type vcan
# 启动这个接口
sudo ip link set up can0
```

## 2. 启动监视工具
```bash
sudo apt install can-utils
candump -td can0
```
这个工具会显示从can0接口接收到的所有消息。
## 3. 启动主控设备
在另一个终端中，启动主控设备：
```bash
cd CANopenLinux
make
rm *.persist
./canopend can0 -i 1 -c "local-/tmp/CO_command_socket"
```
.persist 文件是CANopenNode用来存储持久化数据的文件，删除它就会恢复出厂设置。
```bash
./canopend    # 运行可执行文件
-i 1          # 设置节点 ID为1
-c "local-/tmp/CO_command_socket"   # 设置命令接口的路径
```

## 4. 启动从控设备
在另一个终端中，启动从控设备：
```bash
cd demo
make
rm *.persist
./demoLinuxDevice can0
```
demoDevice 的默认启动节点ID为4。可以通过 LSS 更改。
## 5. 运行cocomm

cocomm 是一个命令行工具，用于与 CANopen 网络上的设备进行交互。可以看做是一个CANopen系统外部的“遥控器”。
make cocomm
```bash
cd cocomm
make
```
in addition, 如果想全局使用，可以安装到/usr/local/bin目录下：
```bash
sudo make install
```
查看手册：
```bash
cocomm "help"
```

# 观察CAN 网络上的数据

candump 显示以下原始CAN消息：
```
(000.000000)  can0  701   [1]  00
(000.050352)  can0  081   [8]  00 50 01 2F 14 00 00 00
(856.752548)  can0  704   [1]  00
(000.000010)  can0  084   [8]  00 50 01 2F 74 00 00 00
```

消息格式：
```
(时间)     接口  ID    长度   数据
(000.000000) can0  701   [1]   00
```

简单来说：
两个设备都启动了。01和04。两个设备都报告了错误。81和84。错误是关于非易失性存储器的（这是正常的，因为我们删除了.persist 文件）。
# 尝试使用cocomm

## 心跳包
```
cocomm "4 read 0x1017 0 u16" 
```

命令要求CANopen Node-ID = 4 的设备读SDO 数据。参0x1017 在子索引 = 0 处访问，数据应显示为 16 位无符号整数。命令返回值为“”，表示心跳生产器已禁用。
可以增加一个参数对心跳包进行设置：

```
cocomm "4 write 0x1017 0 u16 1000"
```

这里设置心跳包的周期为1000ms。设置完成后可以看到有产生循环的CAN消息。7F 的意思是设备处于NMT预操作状态。
如果想要停止心跳包，可以设置周期为0：
```
cocomm "4 write 0x1017 0 u16 0"
```

## NMT

cocomm也提供了一些NMT命令，对节点状态进行操作：

```
cocomm "4 reset communication"
cocomm "4 start"
cocomm "0 reset node"
```

# Next steps
- [LSS](LSS.md)
- [SDO](SDO.md)
