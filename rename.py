from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QCheckBox, QSizePolicy
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

# 標準モジュール
import sys
import os
import re


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 初期値
        self.dirname = os.path.dirname(os.path.abspath(__file__))
        self.font = QtGui.QFont('Arial', 10)
        self.files = None
        self.new_file_flag = False
        self.old_file_flag = False
        self.run_count = 0
        self.undo_able_flag = False
        self.top_flag = True
        self.bottom_flag = False
        self.serialNumber_flag = False
        self.all_change_flag = False
        self.delete_flag = False
        self.change_name = None
        self.counter = None
        self.p = 0
        self.setGeometry(100, 100, 900, 480)


        # レイアウト
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.Hbox = QtWidgets.QHBoxLayout()
        self.grid.addLayout(self.Hbox, 1, 0)

        # widgetsの配置
        self.createWidgets()

        # checkAction
        self.topCheckbox.stateChanged.connect(self.topCheckBoxChangedAction)
        self.bottomCheckbox.stateChanged.connect(self.bottomCheckBoxChangedAction)
        self.serialNumberCheckbox.stateChanged.connect(self.serialNumberCheckBoxChangedAction)
        self.allChangeCheckbox.stateChanged.connect(self.allChangeCheckBoxChangedAction)
        self.deleteCheckbox.stateChanged.connect(self.deleteCheckBoxChangedAction)

    def selectFiles(self):
        self.run_count = 0
        self.undo_able_flag = False
        # renameしたいファイルを選択
        self.files = QtWidgets.QFileDialog.getOpenFileNames(self, 'select files')[0]
        self.counter = len(self.files)

        # ファイル情報リスト
        self.file_list = [FileInfo() for i in range(self.counter)]
        
        # ラベル情報リスト
        self.label_list = [LabelInfo() for i in range(self.counter)]
        
        # if counter > 10:
        #     for i in range(10):
        #         base_name = os.path.basename(self.files[i])
        #         self.label_list[i].label.setText(base_name)
        #         self.grid.addWidget(self.label_list[i].label)
        #         if i == 9:
        #             self.grid.addWidget(QLabel(':'))
        # else:

        self.table.setRowCount(self.counter)
        for i in range(self.counter):
            self.base_name = os.path.basename(self.files[i])
            # self.label_list[i].label.setText(base_name)
            # self.grid.addWidget(self.label_list[i].label)

            # old file nameを保持
            self.file_list[i].old_file_name = self.files[i]
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(self.base_name)))
        
        self.old_file_flag = True

    def review(self):
        if self.counter:
            if self.addText.text() != '':
                for i in range(self.counter):
                    self.base_name = os.path.basename(self.files[i])
                    self.dir_name = os.path.dirname(self.files[i])
                    # top_flagがTrueの場合
                    if self.top_flag:
                        self.change_name = os.path.join(self.dir_name, self.addText.text() + self.base_name)
                        self.display_name = self.addText.text() + self.base_name
                        # serialNumber_flagがTrueの場合
                        if self.serialNumber_flag:
                            self.change_name = os.path.join(self.dir_name, self.addText.text() + str(i + 1) + self.base_name)
                            self.display_name = self.addText.text() + str(i + 1) + self.base_name
                        # all_change_flagがTrueの場合
                        if self.all_change_flag:
                            base_name, ext = os.path.splitext(self.base_name)
                            self.change_name = os.path.join(self.dir_name, str(i + 1) + '_' + self.addText.text() + ext)
                            self.display_name = str(i + 1) + '_' + self.addText.text() + ext
                        

                    # bottom_flagがTrueの場合
                    if self.bottom_flag:
                        base_name, ext = os.path.splitext(self.base_name)
                        self.change_name = os.path.join(self.dir_name, base_name + self.addText.text()) + ext
                        self.display_name = base_name + self.addText.text() + ext
                        # serialNumber_flagがTrueの場合
                        if self.serialNumber_flag:
                            self.change_name = os.path.join(self.dir_name, base_name + self.addText.text() + str(i + 1))
                            self.display_name = base_name + self.addText.text() + str(i + 1) + ext
                        # all_change_flagがTrueの場合
                        if self.all_change_flag:
                            base_name, ext = os.path.splitext(self.base_name)
                            self.change_name = os.path.join(self.dir_name, self.addText.text() + str(i + 1) + '_' + ext)
                            self.display_name = self.addText.text() + '_' + str(i + 1) +  ext

                    # delete_flagがTrueの場合
                    if self.delete_flag:
                        base_name, ext = os.path.splitext(self.base_name)
                        self.change_name = os.path.join(self.dir_name, re.sub(self.addText.text(), '', base_name) + ext)
                        self.display_name = re.sub(self.addText.text(), '', base_name) + ext


                    # new file nameを保持
                    self.file_list[i].new_file_name = self.change_name
                    self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.display_name)))

                self.new_file_flag = True
            
            else:
                for i in range(self.counter):
                    self.base_name = os.path.basename(self.files[i])
                    self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.base_name)))
                self.new_file_flag = False

    def run(self):
        if self.new_file_flag and self.old_file_flag:
            for i in range(self.counter):
                try:
                    os.rename(self.file_list[i].old_file_name, self.file_list[i].new_file_name)
                except Exception as ex:
                    print('error')

            self.undo_able_flag = True
            self.run_count += 1
            print(self.run_count)

    def undo(self):
        if self.undo_able_flag:
            if self.change_name:
                for i in range(self.counter):
                    os.rename(self.file_list[i].new_file_name, self.file_list[i].old_file_name)
                self.undo_able_flag = False
                self.run_count = 1

    # top_check
    def topCheckBoxChangedAction(self, state):
        if (QtCore.Qt.Checked == state):
            self.top_flag = True
            self.bottom_flag = False
            self.bottomCheckbox.setChecked(False)
        else:
            self.top_flag = False
            self.bottom_flag = True
            self.bottomCheckbox.setChecked(True)

    # bottom_check
    def bottomCheckBoxChangedAction(self, state):
        if (QtCore.Qt.Checked == state):
            self.top_flag = False
            self.bottom_flag = True
            self.topCheckbox.setChecked(False)
        else:
            self.top_flag = True
            self.bottom_flag = False
            self.topCheckbox.setChecked(True)

    # serial_check
    def serialNumberCheckBoxChangedAction(self, state):
        if (QtCore.Qt.Checked == state):
            self.serialNumber_flag = True
        else:
            self.serialNumber_flag = False

    # all_change_check
    def allChangeCheckBoxChangedAction(self, state):
        if (QtCore.Qt.Checked == state):
            self.all_change_flag = True

        else:
            self.all_change_flag = False

    # delete_check
    def deleteCheckBoxChangedAction(self, state):
        if (QtCore.Qt.Checked == state):
            self.delete_flag = True

        else:
            self.delete_flag = False


    def createWidgets(self):
        self.getFile_button = QPushButton('file select')
        self.getFile_button.setFont(self.font)
        self.Hbox.addWidget(self.getFile_button)
        self.getFile_button.clicked.connect(self.selectFiles)

        self.addText = QLineEdit(self)
        self.Hbox.addWidget(self.addText)

        self.topCheckbox = QCheckBox("前")
        self.Hbox.addWidget(self.topCheckbox)
        self.topCheckbox.setChecked(True)
        self.bottomCheckbox = QCheckBox("後")
        self.Hbox.addWidget(self.bottomCheckbox)
        self.serialNumberCheckbox = QCheckBox("連番")
        self.Hbox.addWidget(self.serialNumberCheckbox)
        self.allChangeCheckbox = QCheckBox("all_change")
        self.Hbox.addWidget(self.allChangeCheckbox)
        self.deleteCheckbox = QCheckBox("delete")
        self.Hbox.addWidget(self.deleteCheckbox)

        self.review_button = QPushButton('review')
        self.review_button.setFont(self.font)
        self.Hbox.addWidget(self.review_button)
        self.review_button.clicked.connect(self.review)

        self.run_button = QPushButton('run')
        self.run_button.setFont(self.font)
        self.Hbox.addWidget(self.run_button)
        self.run_button.clicked.connect(self.run)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['before rename', 'after rename'])
        self.table.setRowCount(10)
        self.grid.addWidget(self.table)
        self.table.horizontalHeader().setDefaultSectionSize(400)

        self.undo_button = QPushButton('undo')
        self.undo_button.setFont(self.font)
        self.Hbox.addWidget(self.undo_button)
        self.undo_button.clicked.connect(self.undo)
       

class FileInfo():
    '''
    FileInfoクラス
    '''
    def __init__(self):
        # old file name
        self.old_file_name = None
        # new file name
        self.new_file_name = None


class LabelInfo():
    '''
    LabelInfoクラス
    '''
    def __init__(self):
        # ラベル
        self.label = QLabel()
        # フォント
        self.label.setFont(QtGui.QFont('Arial', 10))

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

main()
