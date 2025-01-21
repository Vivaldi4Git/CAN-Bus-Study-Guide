# CANopen PDO发送队列满问题解决方案

## 问题描述

在使用Lely-core库进行CANopen PDO通信时，出现以下错误：
warning: CAN transmit queue full; dropping frame: Resource temporarily unavailable

## 原因分析

- PDO消息发送过快
- 事件循环没有足够时间处理pending的消息
- 导致发送队列积压，最终队列满

这个是lely处理机制的问题，即使txqueue调到400000仍然无法处理，不可能是大小问题。
## 解决方案

### 1. 在发送循环中加入事件处理

```c++

void runPositionProfile(int32_t step_size, std::chrono::seconds duration) {

    auto start_time = std::chrono::steady_clock::now();

    int32_t current_pos = getDriver(1)->getCurrentPosition();

    while (std::chrono::steady_clock::now() - start_time < duration) {

        current_pos += step_size;

        sendPosByPdo(current_pos);

        // 关键：给事件循环处理时间

        io_context_->getLoop().run_one();

    }

}
```