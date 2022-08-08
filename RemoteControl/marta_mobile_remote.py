import socket
import network
import esp
esp.osdebug(None)
import gc
gc.collect()
from machine import Pin, Signal

def get_gear_sts():
  if gear.value() == 1:
    return "AVANTI"
  else:
    return "RETRO"

def web_page():
    
    gear_state = get_gear_sts()  
    
    html ="""
<html>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<style>
html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
h1{color: #0F3376; padding: 3vh;}
p{font-size: 1.5rem;}
button{display: inline-block; background-color: #e72d3b; border: none; border-radius: 4px;
color: white; padding: 15px 60px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
</style>
<body>
<h1>MartaMobile</h1>
<h2>Cambio ("""+ gear_state + """)</h2>
<p><a href="/?gear=forward"><button class="button">Avanti</button></a></p>
<p><a href="/?gear=rear"><button class="button">Retro</button></a></p>
<h2>Acceleratore</h2>
<p><a href="/?gas=go"><button class="button">Marcia</button></a></p>
<p><a href="/?gas=stop"><button class="button">STOP</button></a></p>
</body>
</html>
"""
    return html  

Led = Pin(16, Pin.OUT)
led_sts = False
Led.off()

gear_pin = Pin(4, Pin.OUT)
gear = Signal(gear_pin, invert=True)

gas_pin = Pin(5, Pin.OUT)
gas = Signal(gas_pin, invert=True)

gear.off()
gas.off()

ssid = "MartaMobile"
password = "password"

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)
ap.ifconfig(('192.168.0.1', '255.255.255.0', '192.168.0.1', '8.8.8.8'))

while ap.active() == False:
  pass

print('Connection successful')
print(ap.ifconfig())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  #print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  #print('Content = %s' % str(request))
  
  # Get gear input
  if 'GET /?gear=forward' in request:
    gear.on()
  if 'GET /?gear=rear' in request:
    gear.off()
    
  # Get gas input
  if 'GET /?gas=go' in request:
    gas.on()
  if 'GET /?gas=stop' in request:
    gas.off()     
  response = web_page()
  conn.send(response)
  conn.close()