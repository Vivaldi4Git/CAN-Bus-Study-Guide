# 报文格式

报文是要传递的信息，在CAN中，报文的格式是帧。

在 CAN 总线上传输的帧一共有四种类型 —— 数据帧、远程帧、错误帧、超载帧。
每一个帧都由多个称为“域”（Field）的信息区构成，而每一个域又包含一个或多个位。

## 数据帧

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

链接
[Controller Area Network (CAN Bus) - Message Frame Architecture - Copperhill (copperhilltech.com)](https://copperhilltech.com/blog/controller-area-network-can-bus-message-frame-architecture/)

发送数据帧的两种情况。

![](../attachments/Pasted%20image%2020241010163647.png)

![](../attachments/Pasted%20image%2020241010163712.png)