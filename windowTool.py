from PySide6.QtCore import*
from PySide6.QtGui import*
from PySide6.QtWidgets import *
from shiboken6 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui

import importlib
from . import buttonAndLineEdit
from . import proc

importlib.reload(buttonAndLineEdit)
importlib.reload(proc)

from .proc import *
from .buttonAndLineEdit import *

class CreateBuildingTool(QDialog):
    def __init__(self, parent):
        super(CreateBuildingTool, self).__init__(parent)
        self.resize(310, 425)
        self.setWindowTitle('Create Building Tool')
        self.setStyleSheet(
            '''
            QDialog{
                background-color: #e9d9cb;
                max-width: 310;
                min-width: 310;
            }
            QWidget{
                color: Black;
                font-size: 15px;
            }
            QLineEdit{
                min-Height: 30px;
                border: 2px solid Black;
                border-radius: 8px;
                background-color: White;
                font-size: 15px;
                color: #b19378;
                alignment: center;
            }
            '''
        )
        
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setSpacing(0)

        self.tab=QTabWidget()
        self.tab.setFixedHeight(40)
        self.tab.setContentsMargins(0,100,0,0)
        self.tab.setStyleSheet(
            '''
            QTabBar::tab {
                color: Black;
                background: #b19378;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                min-width: 75px;
                padding: 10px;
                
            }
            QTabBar::tab:selected {
                background: #e9d9cb;
            }
            QTabWidget::pane{
                background: #3c2323;
            }
            QWidget{
                padding: 10px;
                border: 0px;
            }
        ''')

        self.buildingLabel = QLabel('Building')
        self.shapeLabel = QLabel('Shape')
        self.presetLabel = QLabel('Preset')
        self.customLabel = QLabel('Custom')

        self.mainLabel = [self.buildingLabel, self.shapeLabel, self.presetLabel, self.customLabel]
        for each in self.mainLabel:
            each.setStyleSheet(
                '''
                    font-size: 20px;
                '''
            )

        #////////input/////////
        self.inputWidget = QWidget()
        self.inputLayout = QHBoxLayout()
        #self.inputLayout.setAlignment(Qt.AlignCenter)
        self.inputLayout.setSpacing(15)
        self.inputLayout.setContentsMargins(0,0,0,0)
        self.inputWidget.setLayout(self.inputLayout)

        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.setPlaceholderText('building')
        self.nameLineEdit.textChanged[str].connect(self.onChanged)

        self.inputLayout.addWidget(QLabel('Object name:'))
        self.inputLayout.addWidget(self.nameLineEdit)



        ##############################
        ###########        ###########
        ########    Shape     ########
        ###########        ###########
        ##############################
        self.widthLabel = QLabel('Width')
        self.lengthLabel = QLabel('Length')
        self.heightLabel = QLabel('Height')
        
        self.widthLineEdit = QLineEdit()
        self.lengthLineEdit = QLineEdit()
        self.heightLineEdit = QLineEdit()

        self.shapeLayout = QGridLayout()
        self.shapeWidget = QWidget()
        self.shapeLayout.setHorizontalSpacing(5)
        self.shapeWidget.setLayout(self.shapeLayout)
        self.shapeLayout.setContentsMargins(0,0,0,0)

        self.shapeLayoutList = [self.widthLabel, self.widthLineEdit, self.lengthLabel, self.lengthLineEdit, self.heightLabel, self.heightLineEdit]
        c=0
        for each in self.shapeLayoutList:
            self.shapeLayout.addWidget(each,0,c)
            if str(type(each)).split('.')[-1]=='QLineEdit\'>' :
                c+=1
                each.textChanged[str].connect(self.onChanged)
                each.setPlaceholderText('1')
                each.setAlignment(Qt.AlignCenter)   
                if c!=8:
                    self.shapeLayout.addWidget(QLabel(),0,c)
            c+=1
        del c
    
        self.shapeWidget.setStyleSheet(
            '''
                QWidget{
                    max-width: 285px;
                }
                QLineEdit{
                    max-width: 30;
                }
            '''
        )
        
        self.shapeLayout.setAlignment(Qt.AlignRight)



        ##############################
        ###########        ###########
        ########    Preset    ########
        ###########        ###########
        ##############################

        #Box
        self.presetList = ['Office','School','Dorm','TownHouse','B1','B2','B3','B4','B5','B6','B6','B6','B6']
        self.presetList = readSave()['allText']
        self.presetBox = QScrollArea()
        self.presetBox.setStyleSheet(presetStyle)

        #InsideBox
        self.materialWidget = QWidget()
        self.materialLayout = QVBoxLayout()
        self.materialLayout.setAlignment(Qt.AlignHCenter)
        self.materialWidget.setLayout(self.materialLayout)
        self.materialLayout.setSpacing(1)
        self.materialLayout.setContentsMargins(0,0,0,0)
        self.materialWidget.setStyleSheet(
            '''
            QWidget{
                min-height: 25;
                min-width: 272;
                background-color: Black;
            }
            
            QPushButton{
                color: Black;
                min-height: 35;
                max-height: 35;
                min-width: 260;
                background: White;
            }
            QPushButton:hover{
                color: Gray;
                background-color: White;
            }
            QPushButton:pressed{
                color: White;
                border: none;
                background: #3c2323;
            }
            QPushButton:checked{
                color: Gray;
                border: none;
                background: #3c2323;
            }
            QPushButton::hover:checked{
                color: White;
                background: #3c2323;
            }
            ''')
        

        #listButton
        self.buttonList = []
        for x in self.presetList:
            self.__dict__['preset'+x] = QPushButton(x)
            self.__dict__['preset'+x].setCheckable(True)
            self.materialLayout.addWidget(self.__dict__['preset'+x])
            self.buttonList.append(self.__dict__['preset'+x])

        self.presetBox.setWidget(self.materialWidget)


        ##############################
        ###########        ###########
        ########    CUSTOM    ########
        ###########        ###########
        ##############################
        #Box
        self.customBox = QWidget()
        self.customLayout = QVBoxLayout()
        self.customBox.setLayout(self.customLayout)
        self.customLayout.setContentsMargins(0,0,0,0)
        #insideBox
        self.photoWidget = QWidget()
        self.photoWidget.setStyleSheet(
            '''
            QWidget{
                background-color: White;
                border: 2px solid Black;
                border-radius: 5px;
            }
            QLineEdit{
                border: 1px solid Black;
                min-height: 25px;
                max-height: 250px;
            }
            ''')
        self.photoLayout = QGridLayout()
        self.photoLayout.setVerticalSpacing(10)
        self.photoLayout.setContentsMargins(20,20,20,20)
        #self.photoLayout.setHorizontalSpacing(20)
        self.photoWidget.setLayout(self.photoLayout)
        self.photoList=['front', 'side', 'back', 'top']
        c=1
        #each Polariod
        for x in self.photoList:
            widget= QWidget()
            widget.setStyleSheet(
                '''
                QWidget{
                    background-color: White;
                    min-height: 150;
                    border-radius: 0px;
                }
                QPushButton{
                    background-color: #e9d9cb;
                    max-width: 100;
                    max-height: 100;
                    min-width: 100;
                    min-height: 100;
                }
                QPushButton::hover{
                    background-color:Black;
                }
                QLabel{
                    max-width: 95;
                    max-height: 15;
                    min-width: 95;
                    min-height: 15;
                    border: 0px;
                }
                '''
            )

            layout = QVBoxLayout()
            layout.setContentsMargins(0,0,0,0)
            layout.setAlignment(Qt.AlignCenter)
            widget.setLayout(layout)

            label = QLabel(x)

            self.__dict__[x+'Pic']= DragDropButton()
            button=self.__dict__[x+'Pic']
            

            self.__dict__[x+'LineEdit'] = DragDropLineEdit()
            lineEdit= self.__dict__[x+'LineEdit']
            lineEdit.setPlaceholderText('path: ')
            lineEdit.setAcceptDrops(True)
            
            button.setLineEdit(lineEdit)
            lineEdit.setButton(button)
            
            label.setAlignment(Qt.AlignCenter)

            layout.addWidget(button)
            layout.addWidget(label)
            if c<=2:
                self.photoLayout.addWidget(widget,0,c)
                self.photoLayout.addWidget(lineEdit,1,c)
            else:
                self.photoLayout.addWidget(widget,2,c-2)
                self.photoLayout.addWidget(lineEdit,3,c-2)
            c+=1

        self.customLayout.addWidget(self.photoWidget)
        
        ##############################
        ###########        ###########
        #########    page    #########
        ###########        ###########
        ##############################
        self.tab.addTab(QWidget(),'Preset')
        self.tab.addTab(QWidget(),'Custom')
        
        self.pageWidget=QWidget()
        self.pageLayout=QVBoxLayout()
        self.pageLayout.setSpacing(5)
        self.pageWidget.setLayout(self.pageLayout)

        
        self.saveButton = QPushButton('save')
        self.saveButton.setIcon(QIcon(f'{current_dir}/icons/save.png'))
        self.saveButton.setIconSize(QSize(32,32))
        self.saveButton.setStyleSheet((buttonStyle))
        self.saveButton.setFixedWidth(200)
        self.saveButton.pressed.connect(self.saveToJson)

        self.addIndex0()
        self.tab.currentChanged.connect(self.changeTab)

        self.setMaximumHeight(450)
        #self.setMaximumHeight((292+25+(36*len(self.presetList))))


        ##############################
        ###########        ###########
        ########    Button    ########
        ###########        ###########
        ##############################

        self.okButton = QPushButton('Apply')
        self.okButton.setIcon(QIcon(f'{current_dir}/icons/hammer.png'))
        self.okButton.setIconSize(QSize(30,30))
        self.okButton.clicked.connect(self.createObj)

        self.cancleButton = QPushButton('Close')
        self.cancleButton.clicked.connect(self.closeSlot)
        self.cancleButton.setIcon(QIcon(f'{current_dir}/icons/close.png'))
        self.cancleButton.setIconSize(QSize(30,30))

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setContentsMargins(0,0,0,30)
        self.buttonWidget = QWidget()
        self.buttonWidget.setLayout(self.buttonLayout)
        self.buttonWidget.setStyleSheet(buttonStyle)

        self.buttonLayout.addWidget(self.okButton)
        self.buttonLayout.addWidget(self.cancleButton)
        



        ##############################
        ###########        ###########
        #########    Main    #########
        ###########        ###########
        ##############################
        

        self.mainLayout.addWidget(self.tab)
        self.mainLayout.addWidget(self.pageWidget)
        self.mainLayout.addWidget(self.buttonWidget)


    def onChanged(self):
        for x in (self.nameLineEdit, self.widthLineEdit, self.heightLineEdit, self.lengthLineEdit):
            if x.text() == '':
                x.setStyleSheet(
                    '''
                    QLineEdit{
                        color: #b19378;
                    }
                    '''
                )
            else:
                x.setStyleSheet(
                    '''
                    QLineEdit{
                        color: Black;
                    }
                    '''
                )

    def clearLayout(self,layout):
        for x in reversed(range(layout.count())):
            layout.itemAt(x).widget().setParent(None)

    def addIndex0(self):
        self.presetList = readSave()['allText']
        self.pageLayout.addWidget(self.buildingLabel)
        self.pageLayout.addWidget(self.inputWidget)
        self.pageLayout.addWidget(self.shapeLabel)
        self.pageLayout.addWidget(self.shapeWidget)
        self.pageLayout.addWidget(self.presetLabel)
        self.pageLayout.addWidget(self.presetBox)
        self.setFixedSize(310,450)
        #self.setMaximumHeight((292+25+(36*len(self.presetList))))

    def addIndex1(self):
        self.pageLayout.addWidget(self.buildingLabel)
        self.pageLayout.addWidget(self.inputWidget)
        self.pageLayout.addWidget(self.shapeLabel)
        self.pageLayout.addWidget(self.shapeWidget)
        self.pageLayout.addWidget(self.customLabel)
        self.pageLayout.addWidget(self.customBox)
        self.pageLayout.addWidget(self.saveButton, alignment=Qt.AlignHCenter)
        self.setFixedSize(310,730+40)
        self.setMaximumHeight(730+40)

    def changeTab(self, index):
        layout = self.pageLayout
        try:
            self.clearLayout(layout)
        except:
            pass

        if index == 0:
            self.addIndex0()

        elif index == 1:
            self.addIndex1()
        self.changeButtonWidth()

    def createObj(self):
        objName = self.nameLineEdit.text()
        width = self.widthLineEdit.text()
        length = self.lengthLineEdit.text()
        height = self.heightLineEdit.text()


        if self.tab.currentIndex() == 0:
            
            
            build(objName,width,length,height)
            
            sels = cmds.ls(sl=True, l=True)
            allObj = cmds.listRelatives(sels, allDescendents=True, fullPath=True)
            print(len(self.presetCheck()))
            print(self.presetCheck())
            if len(self.presetCheck()) == 1:
                name = self.presetCheck()[0]
                for side in ['top','side','front','back']:
                    textureBySide(name, side ,allObj, globals()[name+side+'Text'])
            else:
                name=random.choice(self.presetCheck())
                for side in ['top','side','front','back']:
                    textureBySide(name, side ,allObj, globals()[name+side+'Text'])

        if self.tab.currentIndex() == 1:
            build(objName,width,length,height)

            sels = cmds.ls(sl=True, l=True)
            allObj = cmds.listRelatives(sels, allDescendents=True, fullPath=True)

            if self.frontPic.icon().availableSizes() == [] and self.sidePic.icon().availableSizes() == [] and self.backPic.icon().availableSizes() == [] and self.topPic.icon().availableSizes() == []:
                randomShadding()
            
            for side in ['side','front','back','top']:
                path =self.__dict__[side+'LineEdit'].text()
                if self.__dict__[f'{side}Pic'].icon().availableSizes() == []:
                    pass
                else:
                    textureBySide(objName, side ,allObj, path)

        lamImportt = [s for s in cmds.ls(materials=True) if 'lambert' in s][-1]
        cmds.delete(lamImportt)
        self.changeButtonWidth()
        

    def saveToJson(self):
        for side in ['side','front','back','top']:
            name = self.nameLineEdit.text()
            if name == '':
                cmds.confirmDialog(
                    title='Confirmation',
                    message='Please enter name',
                    button=['OK']
                )
                return
            path = self.__dict__[side+'LineEdit'].text()
            if checkFile(path):
                saveText(name, side, path)
        cmds.confirmDialog(
            title='Confirmation',
            message='Saved!',
            button=['OK']
        )
        self.__dict__['preset'+name] = QPushButton(name)
        self.__dict__['preset'+name].setCheckable(True)
        self.materialLayout.addWidget(self.__dict__['preset'+name])
        self.buttonList.append(self.__dict__['preset'+name])
        self.updateButton()
    
    def showEvent(self, event: QEvent):
        super().showEvent(event)
        self.changeButtonWidth()

    def changeButtonWidth(self):
        for x in self.presetList:
            if len(self.presetList) < 4:
                self.__dict__['preset'+x].setFixedWidth(290)
                self.materialWidget.setFixedWidth(290)
            else:
                self.__dict__['preset'+x].setFixedWidth(272)

    def presetCheck(self):
        checked = []
        for x in self.presetList:
            if self.__dict__['preset'+x].isChecked():
                checked.append(x)
        return checked

    def updateButton(self):
        self.clearLayout(self.materialLayout)
        for button in self.buttonList:
            self.materialLayout.addWidget(button)
        self.materialLayout.setSpacing(2)

    def closeSlot(self):
        ui.close()

def run():
    global ui
    mayaWindow = omui.MQtUtil.mainWindow()
    ptr = wrapInstance(int(mayaWindow),QWidget)

    try:
        ui.close()
    except:
        pass
    
    ui = CreateBuildingTool(parent=ptr)
    ui.show()