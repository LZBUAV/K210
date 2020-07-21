# 找最大色块 - By: lzbqr - 周一 5月 18 2020
'''
色块对象是由 image.find_blobs 返回的。
image.find_blobs(thresholds, invert=False, roi, x_stride=2, y_stride=1, area_threshold=10, pixels_threshold=10, merge=False,margin=0, threshold_cb=None, merge_cb=None)
查找图像中指定的色块。返回 image.blog 对象列表；
【thresholds】 必须是元组列表。 [(lo, hi), (lo, hi), ..., (lo, hi)] 定义你想追踪的颜色范围。 对于灰度图像，每个元组需要包含两个值 - 最小灰度值和最大灰度值。 仅考虑落在这些阈值之间的像素区域。 对于 RGB565 图像，每个元组需要有六个值(l_lo，l_hi，a_lo，a_hi，b_lo，b_hi) - 分别是 LAB L，A 和 B通道的最小值和最大值。
【area_threshold】若色块的边界框区域小于此参数值，则会被过滤掉；
【pixels_threshold】若色块的像素数量小于此参数值，则会被过滤掉；
【merge】若为 True,则合并所有没有被过滤的色块；
【margin】调整合并色块的边缘。
对于 RGB565 图像，每个元组需要有六个值(l_lo，l_hi，a_lo，a_hi，b_lo，b_hi)
分别是 LAB中 L，A 和 B 通道的最小值和最大值。
L的取值范围为0-100，a/b 的取值范围为-128到127。
'''

import sensor
import image
import lcd
import time
lcd.init()
sensor.reset(freq=24000000, set_regs=True, dual_buff=True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)    #设置摄像头后置
sensor.run(1)

#红色阈值[0],绿色阈值[1],蓝色阈值[2]
rgb_thresholds =[
                (30, 100, 15, 127, 15, 127),
                (0, 80, -70, -10, -0, 30),
                (0, 30, 0, 64, -128, -20)]
while True:
    img=sensor.snapshot()
    blobs = img.find_blobs([rgb_thresholds[0]])
    a=[0,0,0,0,0,0,0,0]
    if blobs:
        for b in blobs:
            a[7]=b.area()
            if a[7]>a[6]:
                a[6]=a[7]
                a[0:4]=b.rect()
                a[4]=b.cx()
                a[5]=b.cy()
        img.draw_rectangle(a[0:4])
        img.draw_cross(a[4], a[5])
    lcd.rotation(2)
    lcd.display(img)
