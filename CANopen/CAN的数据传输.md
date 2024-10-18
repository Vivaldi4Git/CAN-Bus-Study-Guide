# 报文格式

- 报文: 要传递的实际信息
- 帧: 报文在CAN网络中的传输形式

在 CAN 总线上传输的帧一共有四种类型 —— 数据帧、远程帧、错误帧、超载帧。
每一个帧都由多个称为“域”（Field）的信息区构成，而每一个域又包含一个或多个位。

数据帧 和 远程帧 都非常 类似。基本上，远程帧 是没有 Data Field 的数据帧。
## 数据和远程帧

CAN标准数据帧的结构如下:
1. SOF (Start of Frame) - 帧起始
2. 仲裁段 (Arbitration Field)
    - 标识符 (Identifier): 11位
    - RTR (Remote Transmission Request) 位: 在数据帧中为0
3. 控制段 (Control Field)
4. 数据段 (Data Field): 0-8字节
5. CRC段 (CRC Field): 用于校验
6. ACK段 (ACK Field)
7. EOF (End of Frame) - 帧结束

![](../attachments/Pasted%20image%2020241010162238.png "**CAN Data Frame Architecture**")

下面是更详细的结构

![](../attachments/Pasted%20image%2020241010162659.png)

深入研究 CRC 段左侧

![](../attachments/Pasted%20image%2020241010163647.png)

我们可以看到图片展示了CAN帧的基本结构，从左到右依次是：
- Bus Idle（总线空闲状态）
- SOF（Start of Frame，帧起始）
- 11 Bit Identifier（11位标识符）
- RTR（Remote Transmission Request，远程传输请求）位
- 后续的Control Field（控制字段）, Data Field（数据字段）等

其中RTR位为0时，代表这是一个数据帧，而非远程帧。

CAN网络中的节点会根据RTR位来识别帧的类型：数据帧或远程帧。
根据CAN协议的仲裁机制，在总线竞争时，数据帧通常比远程帧具有更高的优先级。
这是因为数据帧的RTR位为显性（0），而远程帧的RTR位为隐性（1）。

## 参考资料

如需了解更多关于CAN总线消息帧架构的详细信息，可以参考以下链接：

[Controller Area Network (CAN Bus) - Message Frame Architecture - Copperhill Technologies](https://copperhilltech.com/blog/controller-area-network-can-bus-message-frame-architecture/)

# 相关文章
- [CAN的物理机制](CAN的物理机制.md)
- [CANopen](CANopen.md)