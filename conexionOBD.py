import obd
import os

os.system("sudo rfcomm connect hci0 00:1D:A5:68:98:8B")

connection = obd.OBD() # auto connect

ports = obd.scan_serial()
print ports

#connection = obd.OBD('/dev/rfcomm0')

print connection.is_connected()

cmd = obd.commands.SPEED

while True:
        response =connection.query(cmd)
        print response.value
        print response.value.to("mph")
        print "NUEVO"