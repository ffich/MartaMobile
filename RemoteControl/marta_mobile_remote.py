import socket
import network
import esp
esp.osdebug(None)
import gc
gc.collect()
from machine import Pin, Signal
import time

W_DELAY_S = 0.2
C_DELAY_S = 0.1

def car_move (Dir):
    if (Dir == "FORWARD"):
        gear_b.off()        
        time.sleep(C_DELAY_S)        
        gear_a.on()
    elif (Dir == "BACKWARD"):
        gear_a.off()
        time.sleep(C_DELAY_S)            
        gear_b.on()
    else:
        gear_a.off()
        gear_b.off()
        
def st_wheel_move (Dir):
    if (Dir == "RIGHT"):
        st_wheel_a.on()
        st_wheel_b.off()
        time.sleep(W_DELAY_S)
        st_wheel_a.off()
        st_wheel_b.off()        
    elif (Dir == "LEFT"):
        st_wheel_a.off()
        st_wheel_b.on()
        time.sleep(W_DELAY_S)
        st_wheel_a.off()
        st_wheel_b.off()        
    else:
        st_wheel_a.off()
        st_wheel_b.off()

        
def web_page():
    
    html ="""
<html>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<style>
#outer
{
    text-align: center;
}
.inner
{
    display: inline-block;
}
</style>
<body>
<div id="outer"><h1>MartaMobile</h1></div>
<div id="outer"><a href="/?go=forward"><div class="outer"><button style="height: 50px; width: 120px; font-size: 1.5rem;">Avanti</button></div></div>
<p></p>
<div id="outer">
    <a href="/?go=right"><div class="inner"><button style="height: 50px; width: 120px; font-size: 1.5rem;">Destra</button></div>
    <a href="/?go=stop"><div class="inner"><button style="height: 50px; width: 120px; font-size: 1.5rem;">STOP</button></div>
    <a href="/?go=left"><div class="inner"><button style="height: 50px; width: 120px; font-size: 1.5rem;">Sinstra</button></div>
 </div>
<p></p>
<div id="outer"><a href="/?go=backward"><div class="outer"><button style="height: 50px; width: 120px; font-size: 1.5rem;">Indietro</button></div></div>
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
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  print('Content = %s' % str(request))
  
  # Get car direction input
  if 'GET /?go=forward' in request:
    car_move("FORWARD")
    st_wheel_move("STOP")
  if 'GET /?go=backward' in request:
    car_move("BACKWARD")
    st_wheel_move("STOP")
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