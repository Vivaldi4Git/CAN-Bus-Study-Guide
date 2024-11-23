CANopenNode 是一个开源的 CANopen 协议栈。
# 克隆demo仓库

要开始学习如何使用CANopenNode，可以先克隆 demo 仓库：
```bash
git clone https://github.com/CANopenNode/CANopenDemo.git
cd CANopenDemo
git submodule update --init --recursive

```

# CANopen architecture

```mermaid
graph TD
    Start[程序启动] --> Init[CANopen 初始化]
    Init --> Threads[启动线程]
    
    Threads --> CAN[CAN接收线程]
    Threads --> Timer[定时器线程]
    Threads --> Main[主线程]
    
    subgraph CAN接收线程
        CAN --> |功能| CAN1[快速响应]
        CAN --> |功能| CAN2[识别CAN ID]
        CAN --> |功能| CAN3[处理消息并复制数据<br>到CANopen对象]
    end
    
    subgraph 定时器线程
        Timer --> |特点| Timer1[实时线程<br>1ms间隔]
        Timer --> |功能| Timer2[网络同步]
        Timer --> |功能| Timer3[复制输入数据<br>RPDOs/硬件 到 对象字典]
        Timer --> |功能| Timer4[调用应用程序<br>进行处理]
        Timer --> |功能| Timer5[从对象字典复制到输出<br>TPDOs/硬件]
    end
    
    subgraph 主线程
        Main --> |处理| Main1[耗时任务处理]
        Main1 --> Main2[SDO服务器]
        Main1 --> Main3[紧急事件]
        Main1 --> Main4[网络状态]
        Main1 --> Main5[心跳监控]
        Main1 --> Main6[LSS从站]
        
        Main --> |网关| GW[网关功能-可选]
        GW --> GW1[NMT主站]
        GW --> GW2[SDO客户端] 
        GW --> GW3[LSS主站]
        
        Main --> |应用| APP[周期性调用<br>应用程序代码]
    end
```

# tutorial

看到如此庞大的仓库可能会让人感到困惑，让我们从教程开始：
- [tutorial](tutorial/tutorial.md)
