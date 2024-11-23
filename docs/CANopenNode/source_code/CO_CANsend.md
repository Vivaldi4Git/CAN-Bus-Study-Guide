CO_CANsend 是CANopenNode中负责发送CAN消息的函数。

```c
CO_ReturnError_t CO_CANsend(
    CO_CANmodule_t* CANmodule, // CAN模块实例
    CO_CANtx_t* buffer // 发送消息
)
```
`CO_CANsend`由应用层直接调用，将消息发送出去。并提供自动重发的机制。

```mermaid
graph TD
    A[应用层调用CO_CANsend] --> B{首次发送}
    B -->|成功| C[发送完成]
    B -->|失败| D[设置 bufferFull = true]
    D --> E[增加 CANtxCount]
    
    F[CO_CANmodule_process 周期调用] --> G{检查CANtxCount > 0}
    G -->|是| H[查找 bufferFull = true 的消息]
    G -->|否| I[无需处理]
    H --> J[重新尝试发送]
    J -->|成功| K[清除 bufferFull 标志]
    J -->|失败| D
    K --> L[减少 CANtxCount]
```


