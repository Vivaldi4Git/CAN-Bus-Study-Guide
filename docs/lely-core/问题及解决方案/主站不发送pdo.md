candump上能看到sync及从站的PDO，但是主站不发送PDO。
检查配置，没有问题。
怀疑是error booting的问题，但是是从站的error booting,且从站已经进入了
观察打印，
NMT: entering reset application state
NMT: entering reset communication state
NMT: running as master
../../../src/co/lss.c:785: debug: creating LSS
NMT: entering pre-operational state
...
发现主站没有operational state。

出现这种情况是将DCF改为使用dcfgen之后出现的。
即便在yaml中指定了start, 似乎仍没有生效。
观察到字典1F81
[1F81]
ParameterName=NMT slave assignment
ObjectType=0x08
DataType=0x0007
AccessType=rw
CompactSubObj=127

[1F81Value]
NrOfEntries=2
2=0x0000030D
3=0x0000030D

而原来手动修改的里面是：

[1F81]
ParameterName=NMT slave assignment
ObjectType=0x08
DataType=0x0007
AccessType=rw
CompactSubObj=127

[1F81Value]
NrOfEntries=2
2=0x00000007
3=0x00000007

修改value为0x00000007后，主站可以进入operational state，并正常发送PDO。

