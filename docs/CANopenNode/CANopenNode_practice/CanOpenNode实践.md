这个脚本(`canctl.sh`)提供了一个简单的命令行工具来管理CAN总线接口。它可以帮助用户快速完成以下操作:

- 启动/停止/重启 CAN接口
- 设置CAN总线波特率
- 监控CAN总线消息
- 查看CAN接口状态和错误统计
```sh
#!/bin/bash
# 文件名: canctl.sh

# 定义颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# CAN接口名称
CAN_IF="can0"
# 默认波特率 (1Mbps)
BITRATE=1000000

# 检查是否有root权限
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}请使用sudo运行此脚本${NC}"
    exit 1
fi

# 函数：显示CAN接口状态
show_status() {
    echo -e "${YELLOW}CAN接口状态：${NC}"
    ip -d link show $CAN_IF
    echo ""
    echo -e "${YELLOW}错误统计：${NC}"
    ip -d -s link show $CAN_IF
}

# 函数：启动CAN接口
start_can() {
    echo -e "${YELLOW}正在配置 $CAN_IF...${NC}"
    
    # 如果接口已启动，先关闭
    ip link set $CAN_IF down 2>/dev/null
    
    # 设置波特率并启动
    if ip link set $CAN_IF type can bitrate $BITRATE; then
        if ip link set $CAN_IF up; then
            echo -e "${GREEN}CAN接口已启动 (波特率: ${BITRATE}bps)${NC}"
            show_status
            return 0
        fi
    fi
    
    echo -e "${RED}CAN接口启动失败${NC}"
    return 1
}

# 函数：停止CAN接口
stop_can() {
    echo -e "${YELLOW}正在关闭 $CAN_IF...${NC}"
    if ip link set $CAN_IF down; then
        echo -e "${GREEN}CAN接口已关闭${NC}"
        return 0
    fi
    echo -e "${RED}CAN接口关闭失败${NC}"
    return 1
}

# 函数：重启CAN接口
restart_can() {
    stop_can
    sleep 1
    start_can
}

# 显示使用帮助
show_help() {
    echo "使用方法: $0 [选项]"
    echo "选项:"
    echo "  start   - 启动CAN接口"
    echo "  stop    - 关闭CAN接口"
    echo "  restart - 重启CAN接口"
    echo "  status  - 显示CAN接口状态"
    echo "  monitor - 启动CAN监控(candump)"
    echo "  -b rate - 设置波特率(kbps), 例如: -b 500 表示500kbps"
    echo "  -h      - 显示此帮助信息"
}

# 处理命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -b|--bitrate)
            BITRATE=$(($2*1000)) # 转换kbps到bps
            shift 2
            ;;
        start)
            start_can
            exit $?
            ;;
        stop)
            stop_can
            exit $?
            ;;
        restart)
            restart_can
            exit $?
            ;;
        status)
            show_status
            exit $?
            ;;
        monitor)
            if ! command -v candump &> /dev/null; then
                echo -e "${RED}请先安装can-utils${NC}"
                exit 1
            fi
            echo -e "${GREEN}启动CAN监控...${NC}"
            echo -e "${YELLOW}按 Ctrl+C 停止监控${NC}"
            candump $CAN_IF
            exit $?
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}未知选项: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# 如果没有参数，默认启动CAN
start_can

```
启动监控
```
root@hzncc:~# canctl monitor
```

在EYOUCANABLETOOL上打开设备,显示内容
```
  can0  77F   [1]  00
  can0  000   [2]  81 00
  can0  701   [0]  remote request
  can0  702   [0]  remote request
  can0  703   [0]  remote request
```
这表明 CANable 适配器已经正常工作，并在总线上发送/接收消息。
```
can0  77F  [1]  00        # 心跳消息
can0  000  [2]  81 00     # NMT消息
can0  701-70B [0] remote request  # 远程帧请求，用于查询节点状态
```

![](../../../attachments/Pasted%20image%2020241120161957.png)![](../../../attachments/Pasted%20image%2020241120162006.png)