`CO_CANtx_t` 是 CANopenNode 中用于描述待发送 CAN 消息的数据结构。

```c
typedef struct {
    uint32_t ident;             /**< CAN 消息的 ID */
    uint8_t DLC;                /**< CAN 消息的 数据长度 */
    uint8_t data[8];            /**< CAN 消息的数据 */
    volatile bool_t bufferFull; /**< 如果前一个消息还在缓冲区，则为 true */
    volatile bool_t syncFlag;   /**< 同步 PDO 消息有此标志，它防止它们在同步窗口之外发送 */
} CO_CANtx_t;
```

通过`CO_CANtxBufferInit`函数初始化发送缓冲区

```c
// 初始化发送缓冲区
CO_CANtx_t* txBuff = CO_CANtxBufferInit(
    CANmodule,  // CAN模块
    index,      // 缓冲区索引
    0x100,      // 发送ID
    0,          // 不是远程帧
    8,          // 数据长度
    0           // 不是同步消息
);
```

使用`CO_CANsend`发送消息， 当然在之前要准备好数据。

```c
// 准备发送数据
if (txBuff != NULL) {
    txBuff->data[0] = 0x11;
    txBuff->data[1] = 0x22;
    // ...填充数据
    
    // 发送消息
    CO_CANsend(CANmodule, txBuff);
}
```
