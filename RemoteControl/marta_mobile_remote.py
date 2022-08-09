import socket
import network
import esp
esp.osdebug(None)
import gc
gc.collect()
from machine import Pin, Signal

# Connection
# ---------------------
# Pin 12, 13 --> Powertrain
# Pin 4, 5   --> Electric Steering

def car_move (Dir):
    if (Dir == "FORWARD"):
        gear_a.on()
        gear_b.off()
    elif (Dir == "BACKWARD"):
        gear_a.off()
        gear_b.on()
    else:
        gear_a.off()
        gear_b.off()
        
def st_wheel_move (Dir):
    if (Dir == "RIGHT"):
        st_wheel_a.on()
        st_wheel_b.off()
    elif (Dir == "LEFT"):
        st_wheel_a.off()
        st_wheel_b.on()
    else:
        st_wheel_a.off()
        st_wheel_b.off()  

def web_page():
    
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
<p><a href="/?go=forward"><button class="button">Avanti</button></a></p>
<p><a href="/?go=stop"><button class="button">STOP</button></a></p>
<p><a href="/?go=rear"><button class="button">Retro</button></a></p>
<p><a href="/?go=right"><button class="button">Destra</button></a></p>
<p><a href="/?go=left"><button class="button">Sinistra</button></a></p>
</body>
</html>
"""
    return html

gear_pin_a = Pin(12, Pin.OUT)
gear_pin_b = Pin(13, Pin.OUT)
gear_a = Signal(gear_pin_a, invert=True)
gear_b = Signal(gear_pin_b, invert=True)
car_move("STOP")

st_wheel_pin_a = Pin(4, Pin.OUT)
st_wheel_pin_b = Pin(5, Pin.OUT)
st_wheel_a = Signal(st_wheel_pin_a, invert=True)
st_wheel_b = Signal(st_wheel_pin_b, invert=True)
st_wheel_move("STOP")

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
  
  # Get car direction input
  if 'GET /?go=forward' in request:
    car_move("FORWARD")
  if 'GET /?go=rear' in request:
    car_move("BACKWARD")
  if 'GET /?go=right' in request:
    st_wheel_move("RIGHT")
  if 'GET /?go=left' in request:
    st_wheel_move("LEFT")  
  if 'GET /?go=stop' in request:
    car_move("STOP")
    st_wheel_move("STOP")

  response = web_page()
  conn.send(response)
  conn.close()