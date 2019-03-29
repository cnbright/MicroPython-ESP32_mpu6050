# -*-coding:utf-8-*-
#coding=utf-8
import threading
from time import sleep
import random
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import seaborn as sns


gesture_i = [0] * 2200
# 创建画布
fig = plt.figure(figsize=(15, 10))
ax1 = fig.add_subplot(1, 1, 1)
ax1.set_facecolor('none')#设置该子图背景透明，其他子图同理
# 绘制初始图形
x = np.arange(0, 2200, 1)  # x轴
#ax1.set_ylim(-1, 1)#设置y轴范围为-1到1
line1, = ax1.plot(x, gesture_i,color='coral')


#初始化函数
def init():
    gesture_i
    line1.set_ydata(gesture_i)
    ax1.set_xlabel("I")
    return line1 

#更新图像的函数
def animate(i):
    global gesture_i
    line1.set_ydata(gesture_i)
    return line1


def draw_view():
    ani = animation.FuncAnimation(fig=fig,
                                  func=animate,
                                  frames=100,
                                  init_func=init,
                                  interval=100,
                                  blit=False)
    plt.show()


#接收数据线程
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    '''处理message回调'''
    global gesture_i
    #print('topic: {}'.format(msg.topic))
    #print('message: {}'.format(str(msg.payload)))
    new_val = float(str(msg.payload)[2:-1])
    gesture_i.pop(0)
    gesture_i.append(new_val)



def Rec_Data():
    client = mqtt.Client()
    client.on_message = on_message
    HOST_IP = '这里需要改为你的matt服务器地址' # Server的IP地址
    HOST_PORT = 1883 # mosquitto 默认打开端口
    TOPIC_ID = 'acc_data'# TOPIC的ID
    client.connect(HOST_IP, HOST_PORT, 60)
    client.subscribe(TOPIC_ID)
    client.loop_forever()


t1 = threading.Thread(target=Rec_Data)

if __name__ == '__main__':
    t1.setDaemon(True)
    t1.start()

    #t.join()
    draw_view()
    print("接收结束")