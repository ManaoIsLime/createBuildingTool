from PySide6.QtCore import*
from PySide6.QtGui import*
from PySide6.QtWidgets import *

import maya.cmds as cmds
from . import fileManage
import importlib
importlib.reload(fileManage)

from .fileManage import*

class DragDropLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setStyleSheet('''color:#b19378;''')
        self.textChanged[str].connect(self.repic)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if isImageExsist(url.toLocalFile()):
                    event.acceptProposedAction()

    def setButton(self, button):
        self.button = button

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            file_url = event.mimeData().urls()[0]
            file_path = file_url.toLocalFile()
            if isImageExsist(file_path):
                self.setText(file_path)
                self.repic()

    def onChanged(self):
        if self.text() == '':
            self.setStyleSheet(
                '''
                color: #b19378;
                '''
            )
        else:
            self.setStyleSheet(
                '''
                color: Black;
                '''
            )
            
    def repic(self):
        path = self.text().replace('\"','')
        self.button.setIcon(QIcon(path))
        self.button.setIconSize(QSize(100,100))
        self.onChanged()


class DragDropButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.clicked.connect(self.pushPath)
        self.setStyleSheet(
        '''
            QLineEdit{
                border: 1px solid Black;
                min-height: 25px;
                max-height: 25px;
            }           
        '''
        )

    def setLineEdit(self, lineEdit):
        self.lineEdit = lineEdit

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if isImageExsist(url.toLocalFile()):
                    event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            file_url = event.mimeData().urls()[0]
            file_path = file_url.toLocalFile()
            self.setIcon(QIcon(file_path))
            self.setIconSize(QSize(100,100))
            self.lineEdit.setText(file_path)

    def pushPath(self):
        path = cmds.fileDialog(m=0)
        if isImageExsist(path):
            self.lineEdit.setText(path)
            self.setIcon(QIcon(path))
            self.setIconSize(QSize(100,100))


presetStyle= '''
            QWidget{
                color: White;
                background-color: Green;
            }
            QScrollArea{
                min-height: 125px;
                min-width: 287px;
                background-color: White;
                border: 1px solid Black;
            }
            QScrollBar:vertical {
                background: #3c2323;
                width:18px;
                margin: 18px 0 18px 0;
            }
            QScrollBar::handle:vertical {
                background: #b19378;
                border: 1px solid;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical {
                height: 18px;
                width: 18px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                height: 18px;
                width: 18px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: #3c2323;
            }
            '''

buttonStyle = (
            '''
            QPushButton{
                color: Black;
                font-size: 15px;
                border: 1px solid Black;
                min-height: 40px;
                max-width: 125px;
                border-radius: 5px;
                background-color: #b19378;
            }
            QPushButton:hover{
                color: White;
                background: #3c2323;
            }
            '''
        )