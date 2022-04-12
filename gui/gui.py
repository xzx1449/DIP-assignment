import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,QGraphicsScene,QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from gui.mainui import Ui_MainWindow
import cv2
import random
from PyQt5 import QtWidgets
from gui.config import fun
import copy

class DIPGUI(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.imageList = []
        self.imageShape = None
        self.setting_signals = pyqtSignal(dict)

        self.exampleButton.clicked.connect(self.showExample)
        self.para000.setValue(2.13)
        self.openButton.clicked.connect(self.openfile)
        self.saveButton.clicked.connect(self.savefile)
        self.cmpButton.pressed.connect(self.showcmp)
        self.cmpButton.released.connect(self.closecmp)
        self.revokeButton.clicked.connect(self.revoke)
        self.updateButton.clicked.connect(self.applyChange)
        self.cmpOrigin.setChecked(True)
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.graphicsView.show()
        self.cmpLast.setCheckable(False)

    def updateFigure(self,n):
        self.scene.clear()
        if len(self.imageList)>0:
            y,x = self.imageList[n].shape[:-1]
            frame = QImage(self.imageList[n], x, y, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(frame)
            if x<600 or y<600:
                pixmap = pixmap.scaled(720,540)
            self.scene.addPixmap(pixmap)
            
    def showcmp(self):
        if len(self.imageList)>1:
            self.cmpLast.setCheckable(True)
        else:
            self.cmpLast.setChecked(False)
            self.cmpLast.setCheckable(False)
        if self.cmpLast.isChecked():
            self.updateFigure(-2)
        else:
            self.updateFigure(0)
    
    def closecmp(self):
        self.updateFigure(-1)

    def openfile(self):
        self.imageList = []
        print("load file")
        fname, _ = QFileDialog.getOpenFileName(self, '选择图片','./', 'Image files(*.jpg *.gif *.png)')
        if fname:
            img = cv2.imread(fname)
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            self.imageShape = img.shape
            self.imageList.append(img)
            self.updateFigure(0)

    def savefile(self):
        if len(self.imageList)>0:
            file_path =  QFileDialog.getSaveFileName(self,"save file","./" ,"Image files(*.jpg *.gif *.png);;all files(*.*)") 
            cv2.imwrite(file_path[0]+'.jpg',self.imageList[-1])
            QMessageBox.information(self, "Info", '保存成功')
        else:
            QMessageBox.information(self, "Info", '请先打开图片')

    def revoke(self):
        if len(self.imageList)>1:
            self.imageList.pop()
            self.updateFigure(-1)
        elif len(self.imageList)==1:
            QMessageBox.information(self, "Info", '已经是原图了')
        else:
            QMessageBox.information(self, "Info", '请先打开图片')

    def applyChange(self):
        if len(self.imageList)>0:
            self.progressBar.setValue(60+random.randint(1,39))
            c = self.choiceButtonGroup.checkedButton()
            if c is None:
                QMessageBox.information(self, "Info", '请选择一项操作')
                return
            c.setChecked(False)
            cname = c.objectName()
            para_list = []
            for i in range(5):
                p = self.findChild(QtWidgets.QDoubleSpinBox,'para'+cname[6:]+str(i+1))
                if p is not None:
                    para_list.append(p.value())
                else:
                    p = self.findChild(QtWidgets.QSlider,'para'+cname[6:]+str(i+1))
                if p is not None:
                    para_list.append(p.value())
            img = copy.copy(self.imageList[-1])
            result = fun[int(cname[6])][int(cname[7])](img,para_list)
            self.imageList.append(result)
            self.updateFigure(-1)
            self.progressBar.setValue(100)
        else:
            QMessageBox.information(self, "Info", '请先打开图片')

    def showExample(self):
        if len(self.imageList)>0:
            a = self.findChild(QtWidgets.QDoubleSpinBox,'para000')
            b = self.findChild(QtWidgets.QDoubleSpinBox,'para111')
            img = copy.copy(self.imageList[-1])
            r = fun[-1][0](img,[a.value()])
            self.imageList.append(r)
            self.updateFigure(-1)
        # QMessageBox.information(self, "Info", '返回值：'+str(r))
        else:
            QMessageBox.information(self, "Info", '请先打开图片')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())