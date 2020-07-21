# cycle_detect - By: lzb - 周一 6月 15 2020
#双次检测 无二值化
'''
使用说明：
1.在第24行 sensor.set_vflip(1)，修改摄像头安装方式，1/0表示正面或反面
2.使用液晶屏时，在第27行，lcd.rotation(0)，修改液晶屏选装角度，0-3每增加1图像旋转90度。
3.第33行，修改LCD_ON来使用或不适应液晶屏。0不使用，1使用。
4.第35行，修改Vedio_ON来进行录像开关，1开启录像，0关闭录像
'''

import sensor,image,lcd,time,video,os
import KPU as kpu
from machine import UART,Timer
from fpioa_manager import fm
import struct

#摄像头初始化
sensor.reset(freq=24000000, set_regs=True, dual_buff=True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)

#修改摄像头安装方式：1/0表示正面或反面
sensor.set_vflip(1)
sensor.run(1)
#此处可修改输入图像大小，经验证160*120大小时，最流畅。
#sensor.set_windowing((224, 224))
lcd.init() #LCD初始化
lcd.rotation(2)

clock = time.clock()

#调试开关，打开方便调试，关掉略微增加帧率
#lcd显示开关，1使用显示，0不使用LCD
LCD_ON = 1
#录像开关，1开启录像，0关闭录像
Vedio_ON = 1

#注册与飞控通讯的串口
fm.register(6, fm.fpioa.UART1_RX, force=True)
fm.register(7, fm.fpioa.UART1_TX, force=True)

##########################################编写有关Mavlink协议有关的代码#################################

# 设置MAVlink的几个字节的信息
MAV_system_id = 1
MAV_component_id = 1
packet_sequence = 0
MAV_OPTICAL_FLOW_message_id = 76
MAV_OPTICAL_FLOW_extra_crc = 152

#初始化串口
uart = UART(UART.UART1, 115200, read_buf_len=4096)

# 编写计算校验位的函数
def checksum(data, extra):
    output = 0xFFFF
    for i in range(len(data)):
        tmp = data[i] ^ (output & 0xFF)
        tmp = (tmp ^ (tmp << 4)) & 0xFF
        output = ((output >> 8) ^ (tmp << 8) ^ (tmp << 3) ^ (tmp >> 4)) & 0xFFFF
    tmp = extra ^ (output & 0xFF)
    tmp = (tmp ^ (tmp << 4)) & 0xFF
    output = ((output >> 8) ^ (tmp << 8) ^ (tmp << 3) ^ (tmp >> 4)) & 0xFFFF
    return output

# Mavlink协议打包
def send_optical_flow_packet(x, y,flag):
    global packet_sequence
    temp = struct.pack("<fffffffHBBB",x,y,flag,4,5,100,0,31010,0,0,0)#

    #print(len(temp))
    temp = struct.pack("<bbbbb33s",
                       33,
                       packet_sequence & 0xFF,
                       MAV_system_id,
                       MAV_component_id,
                       MAV_OPTICAL_FLOW_message_id,
                       temp)

    #print(len(temp))
    temp = struct.pack("<b38sh",
                       0xFE,
                       temp,
                       checksum(temp, MAV_OPTICAL_FLOW_extra_crc))

    #print(len(temp))

    print (struct.unpack("<bbbbbbfffffffHBBBh",temp))

    print([hex(x) for x in temp])

    packet_sequence += 1

    uart.write(temp)
    return temp


#创建视频录制对象,录制帧率25帧
if(Vedio_ON):
    vedio_flag=0
    dir_name=os.listdir()
    print(dir_name)
    for i_name in dir_name:
        if i_name == 'vedio':
            vedio_flag=1
    if vedio_flag==0:
        os.mkdir('vedio')
    dir_name=os.listdir()
    print(dir_name)
    i_frame=0
    j_video=1
    v_rec= video.open("/sd/vedio/capture1.avi", record=1, interval=200000, quality=50)

while(True):
    clock.tick()
    img = sensor.snapshot()
    img=img.mean(1)
    img=img.mean(1)
    img=img.mean(1)
    res  = img.find_circles(threshold = 3500, x_margin = 20, y_margin = 10, r_margin = 10,r_min = 2, r_max = 100, r_step = 2)
    res1 = img.find_circles(threshold = 3500, x_margin = 20, y_margin = 10, r_margin = 10,r_min = 2, r_max = 100, r_step = 2)
    fps =clock.fps()
    c_x=[]
    c_y=[]
    c_r=[]
    c_x1=[]
    c_y1=[]
    c_r1=[]
    if(LCD_ON):
        #显示帧率
        img.draw_string(2,2, ("%2.1ffps" %(fps)), color=(230,0,0), scale=2)
        #画坐标轴
        img.draw_arrow(int(img.width()/80),int(img.height()/2),int(img.width()-int(img.width()/80)),int(img.height()/2),150,5)
        img.draw_arrow(int(img.width()/2),int(img.height()-int(img.height()/80)),int(img.width()/2),int(img.height()/80),150,5)
        if res and res1:
            for i in res:
                c_x.append(i.x())
                c_y.append(i.y())
                c_r.append(i.r())

            for i in res1:
                c_x1.append(i.x())
                c_y1.append(i.y())
                c_r1.append(i.r())

            c_r_max=max(c_r)
            c_r_index=c_r.index(c_r_max)
            c_x_max=c_x[c_r_index]
            c_y_max=c_y[c_r_index]

            c_r_max1=max(c_r)
            c_r_index1=c_r.index(c_r_max1)
            c_x_max1=c_x[c_r_index1]
            c_y_max1=c_y[c_r_index1]

            if(abs(c_r_max1-c_r_max)<2) and (abs(c_x_max1-c_x_max)<2) and (abs(c_y_max1-c_y_max)<2):
                #框住目标
                img.draw_circle(int((c_x_max+c_x_max1)/2),int((c_y_max+c_y_max1)/2),int((c_r_max+c_r_max1)/2),color = (0, 255, 0),thickness = 2, fill = False)
                #计算码中心坐标，并画出中心点
                x=int((c_x_max+c_x_max1)/2)
                y=int((c_y_max+c_y_max1)/2)
                img.draw_cross(x,y,200,10,5)
                #显示中心点坐标
                img.draw_string(x+2,y+2, ("(%2.1f,%2.1f)" %((x-(img.width()/2)),((img.height()/2)-y))), color=(230,0,0), scale=2, mono_space=0)
                #给飞控发送mavlink帧
                send_optical_flow_packet((x-(img.width()/2)),((img.height()/2)-y),1)
        else:
            send_optical_flow_packet(0,0,0)
        lcd.display(img)
    else :
        print(fps)
        if res:
            for i in res:
                c_x.append(i.x())
                c_y.append(i.y())
                c_r.append(i.r())
            c_r_max=max(c_r)
            c_r_index=c_r.index(c_r_max)
            c_x_max=c_x[c_r_index]
            c_y_max=c_y[c_r_index]
            #计算码中心坐标
            x=int(c_x_max)
            y=int(c_y_max)
            #给飞控发送mavlink帧
            send_optical_flow_packet((x-(img.width()/2)),((img.height()/2)-y),1)
        else:
            send_optical_flow_packet(0,0,0)
    if(Vedio_ON):
        tim = time.ticks_ms()
        img_len = v_rec.record(img)
        print("record",j_video,i_frame,time.ticks_ms() - tim)
        i_frame += 1
        if i_frame == int(fps*3):
            print("finish:",j_video)
            j_video+=1
            v_rec.record_finish()
            i_frame=0
            v_rec = video.open("/sd/vedio/capture"+str(j_video)+".avi", record=1, interval=int(1000000/fps), quality=50)
    del c_x[:]
    del c_y[:]
    del c_r[:]
    del c_x1[:]
    del c_y1[:]
    del c_r1[:]
