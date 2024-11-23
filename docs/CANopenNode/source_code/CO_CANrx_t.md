`CO_CANrx_t` 是 CANopenNode 中用于描述接收 CAN 消息的数据结构。

```c
typedef struct {
    uint16_t ident; /**< 标准CAN标识符(位0..10) + RTR(位11) */
    uint16_t mask;  /**< 标准CAN标识符掩码,与ident具有相同的对齐方式 */
    void* object;   /**< 在CO_CANrxBufferInit()中初始化的CANopenNode对象 */
    void (*pCANrx_callback)(void* object,
                            void* message); /**< 指向CANrx_callback()的指针,在CO_CANrxBufferInit()中初始化 */
} CO_CANrx_t;
```
- 掩码用于过滤消息。
- `pCANrx_callback` 是回调函数，用于指定接收到消息后的处理方式， 会由`CO_CANrxMsg`函数调用。

# 为什么需要掩码
```c
// 场景1：精确接收
ident = 0x100;  // 只接收温度数据
mask  = 0x7FF;  // 完全匹配

// 场景2：接收一组相关数据
ident = 0x100;  // 基础ID
mask  = 0x7F0;  // 允许最后4位变化
// 可以接收：
// 0x100: 传感器1的温度
// 0x101: 传感器2的温度
// 0x102: 传感器3的温度
// ...
```
