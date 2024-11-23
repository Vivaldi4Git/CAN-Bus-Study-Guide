```
cat /dev/ttyPS1  # 能看到原始数据
^C23811223344AaBB
```

此时串口是空闲的，可以直接读取原始数据
```BASH
sudo ip link set slcan1 up
candump slcan1  # 能看到解析后的 CAN 数据
  slcan1  123   [4]  DE AD BE EF
```

- SLCAN 驱动接管了串口

- 将串口数据解析为标准 CAN 消息
- 再次尝试读取串口：
```
cat /dev/ttyPS1
cat: /dev/ttyPS1: Input/output error
```
出错是正常的，因为串口已被 SLCAN 驱动接管
一旦 SLCAN 启动，就必须通过 CAN 工具（如 candump）来查看数据，而不是直接读串口

重启slcan1
```bash
sudo ip link set slcan1 down
ps aux | grep slcan
kill -9 pid
slcand -o -c -f -s8 ttyPS1 slcan1
sudo ip link set slcan1 up

candump slcan1
```