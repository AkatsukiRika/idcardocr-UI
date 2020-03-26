# 第二代身份证信息识别
本项目基于 Raymondhhh90 的 [idcardocr](https://github.com/Raymondhhh90/idcardocr)

使用 PyQt5 设计了一套用户界面并添加了视频抓取及数据库功能。

本系统由于在实现过程中使用了Unix命令，因此需要在Unix或类Unix系统上运行，推荐使用Linux或macOS。

使用前，请检查是否安装好python3（版本最好为3.7）和以下软件包（括号内为推荐版本）：PyQt5（5.13.1）、imageio（2.4.1）、imutils（0.5.3）、numpy（1.17.2）、opencv-contrib-python（3.4.2.16）、pytesseract（0.3.0）。

推荐使用PyCharm以项目方式打开本文件夹，方便使用。

在确保能正常使用前，还需更改几个配置路径，具体如下：

1. 将runUI.py中第110行的/usr/local/bin/python3.7改成本机python3的安装路径（如有多个，请改成已经安装好相关软件包的）。

2. 对runUI.py中的第116行进行同样的更改。

3. 将video.py中的第11行中的test_video.mp4改为要进行处理的视频路径（可使用相对路径或绝对路径）。

4. 将video.py中的第14行和第15行中的路径替换为本机OpenCV安装文件夹下haarcascade_frontalface_alt2.xml的位置。

运行方式：

1. 运行服务器：右键运行idcard_recognize.py

2. 运行客户端（服务器必须已经启动）：右键运行runUI.py

3. 运行视频抓取程序：右键运行video.py