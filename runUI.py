import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QGraphicsPixmapItem, \
    QGraphicsScene, QMessageBox
from PyQt5 import QtSql
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtGui import QImage, QPixmap
from window import Ui_MainWindow
import cv2
import json
import sqlite3
import shutil
import threading
from random import randrange
from getDistance import getDiatance

image_file = None  # 身份证图片文件
video_file = None  # 视频文件
server_address = ""  # 服务器地址
server_port = ""  # 服务器端口号
fake_return_value = 0  # 多线程伪返回值


class MWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MWindow, self).__init__()
        self.setupUi(self)

    def open_file(self):
        global image_file
        image_file, _ = QFileDialog.getOpenFileName(None, '打开文件', './', '图片文件(*.jpg *.jpeg *.png *.bmp)')
        if image_file:
            """
            image = cv2.imread(image_file)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width = image.shape[:2]
            size = (int(width*0.25), int(height*0.25))
            shrink = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
            x = image.shape[1]
            y = image.shape[0]
            frame = QImage(image, x, y, QImage.Format_RGB888)
            pix = QPixmap.fromImage(frame)
            item = QGraphicsPixmapItem(pix)
            """
            scene = QGraphicsScene()
            scene.addPixmap(QPixmap(image_file))
            self.Picture.setScene(scene)
            self.FileNameText.setText(image_file)
        else:
            QMessageBox.warning(self, "错误", "请先打开文件")

    def is_ipv4(self, ip: str) -> bool:
        return True if [1] * 4 == [x.isdigit() and 0 <= int(x) <= 255 for x in ip.split(".")] else False

    def is_port(self, port: int) -> bool:
        return True if 0 < port < 65535 else False

    def test_connection(self):
        global server_address, server_port
        server_address = self.AddressText.text()
        server_port = self.PortText.text()
        if not self.is_ipv4(server_address):
            QMessageBox.warning(self, "错误", "请输入正确的IP地址")
            return
        result = os.system(u"ping " + server_address + " -c 4")
        if result == 0:
            self.StatusLabel.setText("连接成功")
        else:
            self.StatushrinksLabel.setText("连接失败")

    def start_recognition(self):
        global server_address, server_port, image_file
        server_address = self.AddressText.text()
        server_port = self.PortText.text()
        if not self.is_ipv4(server_address) or not self.is_port(int(server_port)):
            QMessageBox.warning(self, "错误", "请填写正确的IP地址及端口号")
            return
        url = "http://" + server_address + ":" + server_port
        command = "curl --request POST --url " + url
        command += " --header 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'"
        command += " --form 'pic=@" + image_file + "'"
        result = os.popen(command).read()
        dict_data = json.loads(result)
        name = dict_data["name"]
        sex = dict_data["sex"]
        nation = dict_data["nation"]
        address = dict_data["address"]
        idnum = dict_data["idnum"]
        self.NameText.setText(name)
        self.SexText.setText(sex)
        self.NationText.setText(nation)
        self.NumberText.setText(idnum)
        self.OuchiText.setText(address)  # おうちテキスト
        # 写入数据库
        try:
            conn = sqlite3.connect("idcard.db")
            cur = conn.cursor()
            sql = "INSERT INTO idcard_info (name, sex, nation, number, ouchi) "
            sql += "VALUES ('%s', '%s', '%s', '%s', '%s')" % (name, sex, nation, idnum, address)
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            # 把身份证和头像写入idcard_db和head_db文件夹
            shutil.copyfile("./saved/1.jpg", "./idcard_db/%s.jpg" % idnum)
            shutil.copyfile("./head/1.jpg", "./head_db/%s.jpg" % idnum)
        except sqlite3.IntegrityError:
            pass

    def process(self):
        # /usr/local/bin/python3.7改成python安装路径
        p = os.popen(u"/usr/local/bin/python3.7 process.py " + self.NumberText.text())
        if p.read() == "Error":
            QMessageBox.warning(self, "错误", "请先进行识别")

    def history(self):
        global image_file
        # /usr/local/bin/python3.7改成python安装路径
        command = "/usr/local/bin/python3.7 sql.py"
        os.popen(command)

    def video(self):
        global video_file
        video_file, _ = QFileDialog.getOpenFileName(None, '打开文件', './', '视频文件(*.mp4)')
        p = os.popen(u"/usr/local/bin/python3.7 video.py " + video_file)
        files = []
        for filename in os.listdir("./video_capture"):
            files.append(filename)
        random_index = randrange(0, len(files))
        chosen_file = files[random_index]
        # chosen_file = "4.jpg"
        min_dist = 10000000
        min_file = None
        for filename in os.listdir("./head_db"):
            distance = getDiatance("./video_capture/" + chosen_file, "./head_db/" + filename)
            # print(str(chosen_file) + "\t" + str(distance))
            if distance < min_dist:
                min_dist = distance
                min_file = "./head_db/" + filename
        # 若最小距离还比0.9大，那么直接显示没有匹配
        if min_dist > 0.9:
            QMessageBox.information(self, "检测完成", "无匹配人脸")
            return
        else:
            # 查询数据库
            idnum = min_file[10:].split(".")[0]
            conn = sqlite3.connect("idcard.db")
            cur = conn.cursor()
            sql = "SELECT * FROM idcard_info "
            sql += "WHERE number='" + idnum + "'"
            print(idnum)
            cur.execute(sql)
            result = cur.fetchall()[0]
            conn.commit()
            self.NameText.setText(result[0])
            self.SexText.setText(result[1])
            self.NationText.setText(result[2])
            self.NumberText.setText(result[3])
            self.OuchiText.setText(result[4])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MWindow()
    w.ChooseFileBtn.clicked.connect(w.open_file)
    w.TestBtn.clicked.connect(w.test_connection)
    w.RecognizeBtn.clicked.connect(w.start_recognition)
    w.ProcessBtn.clicked.connect(w.process)
    w.HistoryBtn.clicked.connect(w.history)
    w.VideoBtn.clicked.connect(w.video)
    w.show()
    sys.exit(app.exec_())
