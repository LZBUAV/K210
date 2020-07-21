# Apriltag_v3 - By: lzb - 周四 5月 28 2020
#第三版AprilTag识别程序，添加了ID显示，优化了坐标计算逻辑
'''
使用说明：
1.在第26行 sensor.set_windowing((224, 160))，中修改输入图片大小，宽高都应该为8的倍数
2.在第28行 sensor.set_vflip(1)，修改摄像头安装方式，1/0表示正面或反面
3.使用液晶屏时，在第116行，lcd.rotation(0)，修改液晶屏选装角度，0-3每增加1图像旋转90度。
4.第37行，修改LCD_off来使用或不适应液晶屏。0不使用，1使用。
'''

import sensor
import image
import lcd
import time
from machine import UART,Timer
from fpioa_manager import fm
import struct

clock = time.clock()
lcd.init()
sensor.reset(freq=24000000, set_regs=True, dual_buff=True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)

#此处可修改输入图像大小，经验证160*120大小时，最流畅。
sensor.set_windowing((224, 160))
#修改摄像头安装方式：1/0表示正面或反面
sensor.set_vflip(1)
sensor.run(1)

#注册与飞控通讯的串口
fm.register(6, fm.fpioa.UART1_RX, force=True)
fm.register(7, fm.fpioa.UART1_TX, force=True)


####lcd调试开关，打开方便调试，关掉略微增加帧率
LCD_off = 0

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

while True:
    clock.tick()
    img = sensor.snapshot()
    img=img.mean(1)
    img=img.mean(1)
    img=img.mean(1)
    res = img.find_apriltags(families=image.TAG16H5)
    fps =clock.fps()
    if(LCD_off):
        print(fps)
        if len(res) > 0:
          for i in res:
              #计算码中心坐标，并画出中心点
              x=int(i.x()+i.w()/2)
              y=int(i.y()+i.h()/2)
              #给飞控发送mavlink帧
              send_optical_flow_packet((x-(img.width()/2)),((img.height()/2)-y),1)
        else:
          send_optical_flow_packet(0,0,0)
    else :
        #显示帧率
        img.draw_string(2,2, ("%2.1ffps" %(fps)), color=(0,128,0), scale=2)
        #画坐标轴
        img.draw_arrow(int(img.width()/80),int(img.height()/2),int(img.width()-int(img.width()/80)),int(img.height()/2),150,5)
        img.draw_arrow(int(img.width()/2),int(img.height()-int(img.height()/80)),int(img.width()/2),int(img.height()/80),150,5)
        if len(res) > 0:
          for i in res:
              #输出码信息
              img.draw_string(int(img.width()/2),2, ("ID:%d"%(i.id())), color=(0,128,0), scale=2)
              #框住码
              img.draw_rectangle(i.rect(), color = (0, 255, 0),
                                  thickness = 2, fill = False)
              #计算码中心坐标，并画出中心点
              x=int(i.x()+i.w()/2)
              y=int(i.y()+i.h()/2)
              img.draw_cross(x,y,200,10,5)
              #显示中心点坐标
              img.draw_string(x+2,y+2, ("(%2.1f,%2.1f)" %((x-(img.width()/2)),((img.height()/2)-y))), color=(230,0,0), scale=2, mono_space=0)
              #给飞控发送mavlink帧
              send_optical_flow_packet((x-(img.width()/2)),((img.height()/2)-y),1)
        else:
          send_optical_flow_packet(0,0,0)
        lcd.rotation(0)
        lcd.display(img)
