# coding:utf-8

from PyQt5 import QtGui, QtCore, QtWidgets, QtSql
import sys
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery


class MainUi(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUi()

    # 初始化UI界面
    def initUi(self):
        # 设置窗口标题
        self.setWindowTitle("ID Card Database")
        # 设置窗口大小
        self.resize(600, 400)

        # 创建一个窗口部件
        self.widget = QtWidgets.QWidget()
        # 创建一个网格布局
        self.grid_layout = QtWidgets.QGridLayout()
        # 设置窗口部件的布局为网格布局
        self.widget.setLayout(self.grid_layout)

        # 创建一个按钮组
        self.group_box = QtWidgets.QGroupBox()
        self.group_box_layout = QtWidgets.QVBoxLayout()
        self.group_box.setLayout(self.group_box_layout)
        # 创建一个表格部件
        self.table_widget = QtWidgets.QTableView()
        # 将上述两个部件添加到网格布局中
        self.grid_layout.addWidget(self.group_box, 0, 0)
        self.grid_layout.addWidget(self.table_widget, 0, 1)

        # 创建按钮组的按钮
        self.b_connect_db = QtWidgets.QPushButton("连接数据库")
        self.b_connect_db.clicked.connect(self.connect_db)

        self.b_view_data = QtWidgets.QPushButton("浏览数据")
        self.b_view_data.clicked.connect(self.view_data)
        self.b_view_data.setDisabled(True)

        self.b_add_row = QtWidgets.QPushButton("添加一行")
        self.b_add_row.clicked.connect(self.add_row_data)
        self.b_add_row.setDisabled(True)

        self.b_delete_row = QtWidgets.QPushButton("删除一行")
        self.b_delete_row.clicked.connect(self.del_row_data)
        self.b_delete_row.setDisabled(True)

        self.b_close = QtWidgets.QPushButton("退出")
        self.b_close.clicked.connect(self.close)

        # 添加按钮到按钮组中
        self.group_box_layout.addWidget(self.b_connect_db)
        self.group_box_layout.addWidget(self.b_view_data)
        self.group_box_layout.addWidget(self.b_add_row)
        self.group_box_layout.addWidget(self.b_delete_row)
        self.group_box_layout.addWidget(self.b_close)

        # 设置UI界面的核心部件
        self.setCentralWidget(self.widget)

    def connect_db(self):
        con = QSqlDatabase.addDatabase('QSQLITE')
        con.setDatabaseName('idcard.db')
        if con.open():
            QtWidgets.QMessageBox.information(self, "已连接上", "数据库连接成功")
            self.b_view_data.setDisabled(False)
            self.b_add_row.setDisabled(False)
            self.b_delete_row.setDisabled(False)

    def view_data(self):
        self.model = QtSql.QSqlTableModel()
        self.table_widget.setModel(self.model)
        self.model.setTable('idcard_info')
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        # 设置表格头
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, '姓名')
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, '性别')
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, '民族')
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, '身份证号')
        self.model.setHeaderData(4, QtCore.Qt.Horizontal, '地址')

    def add_row_data(self):
        if self.model:
            self.model.insertRows(self.model.rowCount(), 1)
        else:
            QtWidgets.QMessageBox.warning(self, "错误", "数据追加失败")

    def del_row_data(self):
        if self.model:
            self.model.removeRow(self.table_widget.currentIndex().row())
        else:
            QtWidgets.QMessageBox.warning(self, "错误", "数据删除失败")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainUi()
    w.show()
    sys.exit(app.exec_())
