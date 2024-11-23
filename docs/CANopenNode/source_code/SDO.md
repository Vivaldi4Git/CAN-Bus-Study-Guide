# CANopen SDO通信详解

## SDO通信概述

SDO(Service Data Object)是CANopen中用于配置和参数访问的通信机制。它采用客户端-服务端模式,通过对象字典(OD)进行数据交换。

### 基本通信流程
```mermaid
flowchart LR
    subgraph SDO通信
        Client[SDO客户端] -->|1.请求读写OD COB-ID: 0x600+NodeID| Server[SDO服务端]
        Server -->|2.响应数据 COB-ID: 0x580+NodeID| Client
        Server <-->|3.访问| OD[对象字典Object Dictionary]
    end
```
在`tutorial`中执行过`cocomm "read 4 0x1234 ...."`的命令。
实际上他执行的就是上述过程。

读取时由SDO 客户端发起请求。
```mermaid
sequenceDiagram
    participant App as 应用程序
    participant Client as SDO Client
    participant Server as SDO Server
    participant OD as 对象字典

    App->>Client: 1. CO_SDOclient_setup(nodeId)
    Note over App,Client: 设置要访问的节点ID
    
    App->>Client: 2. CO_SDOclientUploadInitiate(index, subIndex)
    Note over App,Client: 指定要读取的对象字典条目
    
    App->>Server: 3. CO_SDOclientUpload发送上传请求
    Note over App,Server: CAN报文：读取指定index和subIndex
    
    Server->>OD: 4. OD_find() & OD_getSub()
    Note over Server,OD: 在服务器端查找并读取对象字典
    
    Server-->>Client: 5. 返回数据
    Note over Server,Client: 通过CAN报文返回数据
    
    Client->>App: 6. CO_SDOclientUploadBufRead()
    Note over Client,App: 应用程序读取接收到的数据                     
```



## SDO通信实现细节

### 通信架构
```mermaid
flowchart TB
    subgraph CAN总线
        direction LR
        B1[发送缓冲区] --- B2[接收缓冲区]
    end

    subgraph SDO服务端
        direction TB
        S1[CO_SDOserver_init] -->|1.初始化| S2[服务端对象]
        S2 -->|3.处理请求| S3[CO_SDOserver_process]
        
        subgraph 中断服务程序
            ISR1[CAN_ISR] -->|调用回调| S4[CO_SDO_receive]
        end
        
        S4 -->|中断接收| S3
        MainLoop1((主循环)) -.->|周期调用| S3
    end

    subgraph SDO客户端
        direction TB
        C1[CO_SDOclient_init] -->|1.初始化| C2[客户端对象]
        C2 -->|2.发起请求| C3[CO_SDOclient_upload/download]
        
        subgraph 中断服务程序2
            ISR2[CAN_ISR] -->|调用回调| C4[CO_SDOclient_process]
        end
        
        C4 -->|4.处理响应| C3
        MainLoop2((主循环)) -.->|周期调用| C4
    end

    %% 请求流
    C3 -.-> B1
    B1 -.-> ISR1
    
    %% 响应流
    S3 -.-> B2
    B2 -.-> ISR2

    linkStyle 8,9 stroke:red
    linkStyle 10,11 stroke:blue

    classDef loop fill:#f9f,stroke:#333,stroke-width:2px
    class MainLoop1,MainLoop2 loop
    classDef isr fill:#faa,stroke:#333,stroke-width:2px
    class ISR1,ISR2 isr
```

### SDO服务端初始化
SDO服务端通过`CO_SDOserver_init`函数完成初始化,主要包括基本参数配置和CAN通信通道的建立。

```mermaid
      flowchart TB
    subgraph CO_SDOserver_init
        direction TB
        Init[CO_SDOserver_init] -->|1.初始化基本参数| Basic[设置超时等基本参数]
        Init -->|2.调用| InitCAN[CO_SDOserver_init_canRxTx]
    end

    subgraph CO_SDOserver_init_canRxTx
        direction TB
        InitCAN -->|1.验证COB-ID| ValidCheck{验证有效位}
        ValidCheck -->|有效| Config1[配置CAN接收]
        ValidCheck -->|无效| Invalid[设置无效标志]
        Config1 -->|CO_CANrxBufferInit| RxInit[初始化接收缓冲区]
        RxInit -->|注册回调| CB[CO_SDO_receive]
        Config1 --> Config2[配置CAN发送]
        Config2 -->|CO_CANtxBufferInit| TxInit[初始化发送缓冲区]
    end

    %% COB-ID说明
    COB1[Client->Server COB-ID<br>默认: 0x600+NodeID]
    COB2[Server->Client COB-ID<br>默认: 0x580+NodeID]
    COB1 -.->|输入| ValidCheck
    COB2 -.->|输入| ValidCheck
```

### SDO请求处理
`CO_SDOserver_process`其实就是一个分发器

```mermaid
stateDiagram-v2
    [*] --> IDLE
    
    state IDLE {
        description: "等待新请求状态"
        [*] --> Listening
        note right of Listening
            isOKstate = false
            - 可以接收新请求
            - 监听CAN总线
        end note
    }
    
    state "活跃状态 (isOKstate = true)" as ACTIVE {
        state "传输初始化" as INIT {
            DOWNLOAD_INITIATE_REQ
            UPLOAD_INITIATE_REQ
        }
        
        state "数据传输" as TRANSFER {
            state "分段传输" as SEGMENT
            state "块传输" as BLOCK
        }
    }
    
    IDLE --> ACTIVE: 收到请求
    ACTIVE --> IDLE: 传输完成
    ACTIVE --> ABORT: 错误
    ABORT --> IDLE: 错误处理完成
```

#### SDO状态说明
IDLE状态(Inactive, Disconnected, Listening and Enabled)包含以下含义:

- **Inactive**: 不活跃状态,等待新请求
- **Disconnected**: 未建立连接
- **Listening**: 持续监听总线
- **Enabled**: 服务已启用并准备就绪

## CAN层

那`CO_CANsend`和`CO_CANread`在什么地方？他们俩是CAN层收发的接口
```mermaid
flowchart TD
    subgraph 应用层协议
        SDO[SDO通信] --> |配置数据| CAN
        PDO[PDO通信] --> |实时数据| CAN
    end
    
    subgraph 底层通信
        CAN[CAN驱动层] --> |硬件接口| H[CAN硬件]
    end
```

### 数据流向
```mermaid
flowchart TD
    subgraph SDO层
        A[SDO缓冲区] -->|数据处理| B[对象字典访问/数据组装]
    end
    
    subgraph CAN层
        C1[发送缓冲区] -->|硬件发送| D1[CAN总线]
        D2[CAN总线] -->|硬件接收| C2[接收缓冲区]
    end

    B -->|处理后的数据| C1
    C2 -->|待处理数据| A
```