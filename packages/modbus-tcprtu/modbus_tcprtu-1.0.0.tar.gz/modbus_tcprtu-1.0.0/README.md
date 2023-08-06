# modbus_tcprtu

A ModbusRTU Over TCP/IP library, depends on modbus_tk. It's often use with 485-to-TCP converter.

```python

# must install modbus_tk
import modbus_tk.defines as cst
from modbus_tcprtu import TcpRtuMaster

# create a master
master = TcpRtuMaster(host='127.0.0.1', port=9001)
master.set_timeout(2)
for i in range(10):
    # read data from modbus
    # just use as modbus_tk.Master
    print(i, master.execute(1, cst.READ_HOLDING_REGISTERS, 0, i + 1))

```