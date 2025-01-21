eds/dcf

字典内容解释
MandatoryObjects（强制对象）：
必须存在于设备中的对象
通常包含：
0x1000：设备类型
0x1001：错误寄存器
0x1018：身份对象
OptionalObjects（可选对象）：
CANopen 标准定义的可选对象
包括：
0x1400-0x1403：RPDO 通信参数
0x1600-0x1603：RPDO 映射参数
0x1800-0x1803：TPDO 通信参数
0x1A00-0x1A03：TPDO 映射参数
其他通信和设备参数
ManufacturerObjects（制造商特定对象）：
制造商自定义的对象（0x2000-0x5FFF）
在我们的例子中：
0x2200：主站用于 PDO 的应用对象
0x2201：第二个 PDO 的应用对象