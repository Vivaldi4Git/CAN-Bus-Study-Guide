```c
/**
 * @defgroup CO_SDOclient SDO客户端
 * CANopen服务数据对象 - 客户端协议
 *
 * @ingroup CO_CANopen_301
 * @{
 * SDO客户端能够访问远程节点的对象字典变量。通常在CANopen网络中
 * 只有一个SDO客户端，它可以配置其他CANopen节点。也可以在设备之间
 * 建立单独的SDO客户端-服务器通信通道。
 *
 * SDO客户端在CANopenNode中通过CO_gateway_ascii.c使用默认的SDO CAN标识符。
 * 它在非阻塞函数中有相当高级的用法。
 *
 * 如果启用，SDO客户端会在CANopen.c文件中通过CO_SDOclient_init()函数初始化。
 */
```