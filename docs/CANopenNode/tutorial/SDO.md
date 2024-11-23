
现在我们已经建立了基础(LSS)，让我们继续学习SDO。

SDO是CANopen协议中用于节点之间数据交换的协议。它可以传输以下数据类型：

1. Record 基本数值类型操作
   - i64 (64位整数)
   - u64 (64位无符号整数) 
   - r32/r64 (32/64位浮点数)

2. Strings
   - vs (visible string，可见字符串)
   - os (octet string，八位字节串)
   - hex (十六进制显示)

3. Domain
   - 大块数据传输

接下来我们与 demoDevice 通信，所以设置默认节点ID????
```bash
cocomm "set node 4"
```

# Demo record

从地址0x2120读取一个4-bit的integer数据:
```bash
cocomm "r 0x2120 1 i64"
[1] -1234567890123456789
```
也可以读取无符号64-bit的integer数据，让我们拆解一下命令：
```bash
cocomm "r 0x2120 2 u64"
        │ │      │ │
        │ │      │ └── 数据类型(u64=无符号64位)
        │ │      └──── 子索引(偏移量)
        │ └─────────── 主索引
        └───────────── 命令(r=read的简写)
```
r是read的简写。
尝试一下命令：
```bash
cocomm "r 0x2120 1 x64" "r 0x2120 2 x64" "r 0x2120 3 x64"
```
输出
```bash
[1] 0xEEDDEF0B82167EEB
[2] 0x1234567890ABCDEF
[3] 1F 85 45 41
```
发现索引??的位置上返回的格式迥异于前两个，这是因为索引3存储的是32位浮点数(r32)，而不??4位整数。可以用r32格式进行读取??
复习一下前缀的全??
```bash
i   = Integer (有符号整数)
└── i8   = 8-bit Integer
└── i16  = 16-bit Integer
└── i32  = 32-bit Integer
└── i64  = 64-bit Integer

u   = Unsigned Integer (无符号整数)
└── u8   = 8-bit Unsigned Integer
└── u16  = 16-bit Unsigned Integer
└── u32  = 32-bit Unsigned Integer
└── u64  = 64-bit Unsigned Integer
```

```bash
x   = heXadecimal (十六进制)
└── x8   = 8-bit Hexadecimal
└── x16  = 16-bit Hexadecimal
└── x32  = 32-bit Hexadecimal
└── x64  = 64-bit Hexadecimal

r   = Real number (实数/浮点数)
└── r32  = 32-bit Real/Float
└── r64  = 64-bit Real/Double

vs  = Visible String (可见字符串)
os  = Octet String (八位字节串)
hex = HEXadecimal bytes (十六进制字节)
d   = Domain (域/大块数据)
```

# demo string

字符串的数据处理会和数值类型有所不同，因为字符串需要考虑编码格式。
尝试读取0x2121地址上的数据：
```bash
cocomm "r 0x2121 1 vs" "r 0x2121 2 vs" "r 0x2121 3 hex"
[1] "str"
[2] "Example string with 1000 bytes capacity. It may contain UTF-8 characters, like '??, tabs '	', newlines, etc."
[3] C8 3D BB 00 00 00 00 00 00 00
```

索引1的位置上只能写入3字节，尝试用不同的方式写入，并读取值：

```bash
cocomm "w 0x2121 1 vs 12"      "r 0x2121 1 vs" \
        "w 0x2121 1 vs 1234"    "r 0x2121 1 vs" \
        "w 0x2121 1 vs \"1 2\"" "r 0x2121 1 vs"
[1] OK
[2] "12"
[3] ERROR:0x06070012 #Data type does not match, length of service parameter too high.
[4] "12"
[5] OK
[6] "1 2"
```

可以看到第三个命令返回了错误，因为写入的字符串长度超过了索引1的容量。索引2被设置为可以写入1000字节，尝试写入：

```bash
cocomm "w 0x2121 2 vs \"Writing newLines is not possible as visible string, but exotic \"..\" characters work.\"" "r 0x2121 2 vs"
[1] OK
[2] "Writing newLines is not possible as visible string, but exotic \"..\" characters work."
```
"octet string" 的方式读取索引2上的数据，返回值为base64格式:
```bash
cocomm "r 0x2121 2 os"
[1] V3JpdGluZyBuZXdMaW5lcyBpcyBub3QgcG9zc2libGUgYXMgdmlzaWJsZSBzdHJpbmcsIGJ1dCBleG90aWMgIsOfIiBjaGFyYWN0ZXJzIHdvcmtzLg==
```
可以进行解码:
```bash
cocomm "r 0x2121 2 os" | base64 -d
[1]
Writing newLines is not possible as visible string, but exotic "?" characters works.
```

也可以用hexdump查看:
```bash
cocomm "r 0x2121 2 os" | base64 -d | hexdump -C
00000000  57 72 69 74 69 6e 67 20  6e 65 77 4c 69 6e 65 73  |Writing newLines|
00000010  20 69 73 20 6e 6f 74 20  70 6f 73 73 69 62 6c 65  | is not possible|
00000020  20 61 73 20 76 69 73 69  62 6c 65 20 73 74 72 69  | as visible stri|
00000030  6e 67 2c 20 62 75 74 20  65 78 6f 74 69 63 20 22  |ng, but exotic "|
00000040  c3 9f 22 20 63 68 61 72  61 63 74 65 72 73 20 77  |.." characters w|
00000050  6f 72 6b 73 2e   
```
hexdump 其实就是查看16进制的dump工具。dump就是倾倒，就像将一个装满乱七八糟的包里的东西倒出来，-C 表示 Canonical 格式输出。就像对这些乱七八糟的东西进行整理。
```bash
数据转换过程：
原始数据 ──► Base64编码 ──► Base64解码 ──► 十六进制显示
          os           -d            -C
```

os是一个定长的字符串。
通过管道解码base64数据:
```bash
cocomm "r 0x2121 2 os" | base64 -d
[1]
Writing newLines is not possible as visible string, but exotic "?" characters works.

cocomm "r 0x2121 2 os" | base64 -d | hexdump -C
[1]...
```

管道就是一种Linux命令执行方式，像流水线一样:
```bash
命令1 | 命令2 | 命令3
│      │      │
└──►数据──►数据──►结果
```

将数据编码为base64并通过管道发送给cocomm:
```bash
echo -ne "We can encode anything to base64\n\nand transfer data as octet string or domain." | base64 -w0 | cocomm -i "w 0x2121 2 os"
[1] OK
```

这样仍然可以工作，但通过base64会更安全:
```bash
cocomm "r 0x2121 2 vs"
[1] "We can encode anything to base64

and transfer data as octet string or domain."
```

以不同数据类型读取和显示octet string:
```bash
cocomm "r 0x2121 3 hex" "r 0x2121 3 os" "r 0x2121 3 vs" "r 0x2121 3 d" "r 0x2121 3"
[1] C8 3D BB 00 00 00 00 00 00 00
[2] yD27AAAAAAAAAA==
[3] "????
[4] yD27AAAAAAAAAA==
[5] C8 3D BB 00 00 00 00 00 00 00
```

与可接受小于缓冲区大小的字符串不同，octet string具有固定长度:
```bash
cocomm "w 0x2121 3 hex 01 02 03"
[1] ERROR:0x06070013 #Data type does not match, length of service parameter too short.
```

我们的参数长度为10字节:
```bash
cocomm "w 0x2121 3 hex 01 2 30 456789 0A b0 0 ff"
[1] OK
```

# demo domain

domain数据类型用于传输大块数据??如有必要，它会自动重新传输损坏的数据??
## block

打开块传输：

```bash
cocomm "set sdo_block 1"
[1] OK
```
尝试读取
```bash
cocomm "r 0x2122 0 d" | base64 -d | pv > file_read
[1] 
...success
10.0KiB 0:00:00 [47.1KiB/s] [<=>    
```

同样可以使用hexdump查看
```bash
hexdump -C file_read
```

pv "Pipe Viewer", 可以详细的显示传输的进度??
现在创建一个大小为原文10倍的文件并上传到演示设备:
```bash
for n in {1..10}; do cat file_read >> file_write; done
pv file_write | base64 -w0 | cocomm -i "w 0x2122 0 d"
```

读取大小 = 上次写入的大小
且数据必须是循环序列
```bash
0, 1, 2, ..., 255, 0, 1, ...

例如1024字节数据应该是：
    0, 1, 2, ..., 255,    # 56字节
    0, 1, 2, ..., 255,    # 56字节
    0, 1, 2, ..., 255,    # 56字节
    0, 1, 2, ..., 255     # 56字节
```
## segment

切换到分段模式：
```bash
cocomm "set sdo_block 0"
```

再执行:
```bash
pv file_write | base64 -w0 | cocomm -i "w 0x2122 0 d"
```

我们可以看到速率是不同的。
