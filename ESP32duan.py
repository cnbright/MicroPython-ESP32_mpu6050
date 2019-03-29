#!/usr/bin/python3
import mpu6050
import network
from machine import Pin,I2C
import machine
import time
from wifi import do_connect

i2c = I2C(scl=Pin(33), sda=Pin(32))
accelerometer = mpu6050.accel(i2c)
ints = accelerometer.get_ints()
#初始化传感器
sum_val = 0
for i in range(400):
  acc_data = accelerometer.get_values()
  sum_val+=acc_data['AcX']/16384

error_x = sum_val/400

#平滑滤波器

class avg_fiter():
    def __init__(self, data_list):
        self.data_sum=sum(data_list)
        self.data_list=data_list

    def fit(self, data, len):
        #data是传入的数据,len是平滑的长度
        self.data_sum = self.data_sum - self.data_list[0] + data
        self.data_list.pop(0)
        self.data_list.append(data)
        data = self.data_sum/len
        return data

data_list=[0,0,0,0,0]
'''
for i in range(5):
  acc_data = accelerometer.get_values()
  data_list.append(acc_data['AcX']/16384)
 ''' 
avgfiter = avg_fiter(data_list)
ip_addr = do_connect(host='42',password='15863335982')

def conncb(task):
    print("[{}] Connected".format(task))

def disconncb(task):
    print("[{}] Disconnected".format(task))
    

def subscb(task):
    #print("[{}] Subscribed".format(task))
    pass

def pubcb(pub):
    print("[{}] Published: {}".format(pub[0], pub[1]))

def datacb(msg):
    #print("[{}] Data arrived from topic: {}, Message:\n".format(msg[0], msg[1]), msg[2])
    pass
    

TOPIC = b'acc_data'
mqtt = network.mqtt('acc_0', "mqtt://这里需要改为你的matt服务器地址", port=1883,
                      lwt_topic=TOPIC,autoreconnect=True,
                      cleansession=True,
                      connected_cb=conncb,
                      disconnected_cb=disconncb, subscribed_cb=subscb,
                      published_cb=pubcb, data_cb=datacb)
mqtt.start()
while not mqtt.subscribe(TOPIC):
  pass

def tcb(timer):
  acc_data = accelerometer.get_values()
  try:
    mqtt.publish(TOPIC, str(acc_data['AcX']/16384-error_x))
  except:
    print("MQTT HAND BROKEN!!!!!")
  
#t1 = machine.Timer(2)
#t1.init(period=50, mode=t1.PERIODIC, callback=tcb)
while True:
  #这个速度不能太快
  time.sleep_ms(1000)
  acc_data = accelerometer.get_values()
  try:
    #print(mqtt.status())
    temp = avgfiter.fit(acc_data['AcX']/16384-error_x,5)
    mqtt.publish(TOPIC, str(temp))

  except:
    print('===========END============')
    break
#mqtt.publish(TOPIC, 'Hi from Micropython')
#接收到消息时会进入中断，不用像umqtt那样写个循环
#mqtt.stop()

