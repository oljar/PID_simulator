from pyModbusTCP.client import ModbusClient

setpoint = 20
setpoint = setpoint * 256
Kp = 100
Kp = Kp * 256
Ti = 1
Ti = Ti * 256
Td = 8
Td = Td * 256
dt_heat = 1
dt_cool = -0.1

dtime = 1


c = ModbusClient(host='192.168.0.8', port=56789, unit_id=1, auto_open=True) ###########
c.write_single_register(8, setpoint)
c.write_single_register(0,Kp)
c.write_single_register(2,Ti)
c.write_single_register(4,Td)


window_size = 5000

