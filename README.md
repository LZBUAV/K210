# 中文
# 1.作者简介
* 项目参与人与仓库维护者：李展博，北京航空航天大学自动化科学与电气工程学院硕士研究生
* 项目负责人：李大伟，北京航空航天大学无人系统研究院研究员(副教授)
* 项目负责人：杨炯，北京航空航天大学无人系统研究院工程师
* 联系方式：lizhanbo@buaa.edu.cn
# 项目描述  
>在第一次尝试之前，您应该仔细阅读此README.md和[用户手册](https://github.com/LZBUAV/K210/tree/master/user's_manaul_en_zh/ "用户手册")。

该项目是Kendryte K210 AI芯片应用程序的集合，其中包括面部检测，颜色检测，目标检测和分类，QR码和Apriltag码检测以及与ArduPilot飞行软件的通信。 最后，我们可以将这些应用程序部署到无人机终端，使无人机更加智能。
本K210项目为Vision_MAV项目的配套项目，Vision_MAV项目旨在设计并实现一个依托深度学习和图像处理技术的基于视觉的微型无人机系统，能够实现在无GPS环境下的自主视觉导航、目标检测与追踪，该项目由北航无人系统研究院李大伟副教授课题组创立并进行研究，并将在项目没有保密需求后进行开源。本仓库的K210项目是Vision_MAV的一个配套项目，基于[嘉楠科技公司](https://canaan-creative.com/ "嘉楠科技公司")生产的边缘AI芯片[K210](https://canaan-creative.com/product/kendryteai "K210")，来实现目标检测与追踪，为Vision_MAV项目提供一个可选的视觉解决方案。该项目采用了一块[矽速科技公司](https://www.sipeed.com/ "矽速科技公司")生产的MAXI DOCK K210评估板，来验证K210芯片的AI计算能力。在本项目中，采用传统机器视觉方法实现了最大色块识别、二维码识别、Apriltag码识别、圆形识别，采用深度学习方法实现了人脸识别、人体识别、口罩识别等，并开发了K210和[Ardupilot](https://github.com/ArduPilot/ardupilot "Ardupilot")飞控固件之间的[MAVlink](https://github.com/ArduPilot/mavlink "MAVlink")通讯接口，来实时的将K210视觉模组解算出的目标位置信息发送给飞控来控制无人机运动。
# 项目文件结构  
用户克隆本项目后，会得到一个文件夹，里边有如下文件：
- IDE : K210的集成开发环境安装包
- images ： 相关图片，用户无需关心
- kflash_gui : K210的MaxiPy固件烧录工具
- MaxiPy ：K210的MicroPython固件
- model : 神经网络模型文件
- scripts : 各个功能对应的MicroPython脚本程序
- user's_manual_en_zh : 该项目的中英文详细用户手册
- README.md : 本项目说明文件

# 实现功能
该项目是Kendryte K210 AI芯片应用程序的集合，其中包括面部检测，颜色检测，目标检测和分类，QR码和Apriltag码检测以及与ArduPilot飞行软件的通信。 最后，我们可以将这些应用程序部署到无人机终端，使无人机更加智能。所实现的应用主要分为两类，第一个是机器视觉应用，该类应用基于openmv机器视觉库；第二类是深度学习应用，该类主要基于Tensorflow和yolov2。详细功能参见用户手册。

# English
# Project description  
>Before your first try, you should read this README.md and the User's manual carefully.

This repository is a collection of applications for the Kendryte K210 AI chip which include face detection, color detection, object detection and classification, QR code and Apriltag code detection ,and communication with the ArduPilot flight software. Finally, we can deploy these applications to the Uavs terminal and make drones more intelligent.
This K210 project is a supporting project of the Vision_MAV project. The Vision_MAV project aims to design and implement a vision-based micro drone system that relies on deep learning and image processing technology, which can realize autonomous visual navigation, target detection and Tracking, the project was founded and researched by the team of Associate Professor Li Dawei who works at the Institute of Unmanned System, Beihang University. And this project will be open source after the project has no confidentiality requirements. The K210 project is a supporting project of Vision_MAV, based on the edge AI chip [K210](https://canaan-creative.com/product/kendryteai "K210"), to achieve target detection and tracking, and to provide an optional vision solution for the Vision_MAV project. We used a MAXI DOCK K210 evaluation board produced by [Sipeed Technology Company](https://www.sipeed.com/ "矽速科技公司") to verify the AI ​​computing capabilities of the K210 chip. In this project, traditional machine vision methods are used to realize the largest color block recognition, QR code recognition, Apriltag code recognition, and circle recognition. Deep learning methods are used to realize face recognition, human body recognition, mask recognition, etc, and we also developed a [MAVlink](https://github.com/ArduPilot/mavlink "MAVlink") communication interface between K210 and [Ardupilot](https://github.com/ArduPilot/ardupilot "Ardupilot") flight control firmware, then The target position information calculated by the K210 vision module is sent to the flight controller in real time to control the movement of the drone.
# Project files structure  
This project is a collection of Kendryte K210 AI chip applications, which includes face detection, color detection, object detection and classification, QR code and Apriltag code detection, and the interface to communication with ArduPilot flight software. Finally, we can deploy these applications to drone to make drones more intelligent. These implemented applications are mainly divided into two categories, the first is machine vision applications, which are based on the openmv machine vision library; the second is deep learning applications, which are mainly based on Tensorflow and yolov2. See the user's manual for detailed functions. 
