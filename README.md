

# MicroPython——ESP32驱动mpu6050
    MicroPython固件使用的是Lobo的micropython固件而非官网固件，
    此程序仅对加速度X轴数据进行了平滑滤波和上传，
  
[mpu6050采集] -- IIC --> (ESP32) -->[平滑滤波] --mqtt--> (PC) --> [matplotlib动态展示]



## 引脚

|ESP32|MPU6050|
|---|---|
|P32|SCL|
|P33|SDA|

INT和AD0不使用
## 注意
mqtt服务器是在阿里云上自己搭建的，所以ip地址被隐去了，需要自己设定

mqtt上传每200ms一次以内时间大概几分钟后会断线，即便设置了自动重连也连接不上
后续可以多次采集，一次上传
