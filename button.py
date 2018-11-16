__author__ = "Martin Gunnarsson"
__email__ = "hello@deerstranger.com"

from external.Qt import QtWidgets, QtCore, QtGui, QtSvg
import animation
import dialog
import icon as qt_icon

import os

import pymel.core as pm

relativePath = os.path.dirname(os.path.realpath(__file__)) + os.sep


class fadeButton(QtWidgets.QToolButton):
    """Create star-icon on card """

    def __init__(self, parent):
        super(fadeButton, self).__init__()
        # QToolButton.__init__(self, parent)

        self.width = 20
        self.height = 20
        self.opacity = 0.3
        self.endOpacity = 0.7
        self.inAnimDuration = 300
        self.outAnimDuration = 800

        # Create opacity effect
        self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacityEffect)
        self.setAutoFillBackground(True)
        self.setOpacity(self.opacity)
        self.activeButton = False

        # Set sizing policy on button
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)

        # Set cursor
        self.setCursor(QtCore.Qt.PointingHandCursor)

        # Set sizing of the button
        # self.setSize(self.width, self.height)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

        self.setStyleSheet('''QToolButton {color: rgb(250, 250, 250);background-color: rgb(0, 250, 0,0);border-style: None;border-width: 0px;}QToolButton:menu-indicator { image: none; }''')

    def setOpacity(self, opacity):
        self.opacityEffect.setOpacity(opacity)
        self.opacity = opacity

    def setSize(self, width, height):
        self.setIconSize(QtCore.QSize(width, height))

        self.width = width
        self.height = height

    def enterEvent(self, event):
        if self.activeButton is False:
            animation.fadeAnimation(start="current", end=self.endOpacity, duration=self.inAnimDuration,
                                 object=self.opacityEffect)
            # self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

    def leaveEvent(self, event):
        if self.activeButton is False:
            animation.fadeAnimation(start="current", end=self.opacity, duration=self.outAnimDuration,
                                 object=self.opacityEffect)
            # self.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)

class valueButton(QtWidgets.QToolButton):
    '''Create a button that can store values for us'''
    def __init__(self):
        super(valueButton, self).__init__()

        # Initialise value
        self.value = None
        self.multiple = False
        self.originalTitle = None


        # Create opacity effect
        self.opacity = 0.8
        self.endOpacity = 1
        self.inAnimDuration = 300
        self.outAnimDuration = 800
        self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacityEffect)
        self.setAutoFillBackground(True)

        # Set style

        self.inactiveStyleSheet = "QToolButton\n{\npadding: 5px;\nborder-radius: 5px;\nbackground-color: rgb(250,250,250,20);\ncolor: rgb(250,250,250,200);\nborder-style: solid;\nborder-color: rgb(250,250,250, 50);\nborder-width: 1px;\n\n\n}\n\nQToolButton:focus\n{\nbackground-color: rgb(250,250,250,20);\nborder-style: solid;\nborder-color: rgb(250,250,250);\nborder-width: 1px;\n}"
        self.activeStyleSheet = "QToolButton\n{\npadding: 5px;\nborder-radius: 5px;\nbackground-color: rgb(0, 153, 51);\ncolor: rgb(250,250,250,200);\nborder-style: solid;\nborder-color: rgb(250,250,250, 50);\nborder-width: 1px;\n\n\n}\n\nQToolButton:focus\n{\nbackground-color: rgb(0, 153, 51);\nborder-style: solid;\nborder-color: rgb(250,250,250, 240);\nborder-width: 1px;\n}"
        self.setStyleSheet(self.inactiveStyleSheet)
    def add_value(self):
        # Get current selection from the scene and add as values to this object
        selection = pm.ls(sl=True)
        if len(selection) >= 1:
            #self.value = [object.name() for object in selection]
            valueName = [object.name() for object in selection]
            valueName = ",".join(valueName)[:(int(self.width() * 0.15))]

            self.set_value(selection, valueName=valueName)
            self.opacity = 1
            self.setStyleSheet(self.activeStyleSheet)

        else:
            self.opacity = 0.6

            dialog.activatePopup(self, "You dont have any selection")
            self.setStyleSheet(self.inactiveStyleSheet)
            self.set_value(None, valueName=self.originalTitle)
    def reset_value(self):
        self.setStyleSheet("")
    def set_value(self, value, valueName="Assigned"):
        height = self.size().height()
        width = self.size().width()

        # Set value in button
        self.value = value
        # Set text of button

        # Calculate new size

        self.setText(valueName)



        # Measure text
        metrics = QtGui.QFontMetrics(self.font())
        newWidth = metrics.width(valueName) + 20



        # Set color of button
        #self.setStyleSheet("padding: 5px;border-radius: 5px;\nbackground-color: rgb(0,153,51);\ncolor: rgb(250,250,250,200);")

        # Aninmate size
        #animateWidgetSize(self, start=(30, height), end=((width * 2), height),duration=3000,attributelist=("minimumSize"))
        #propertyAnimation(start=[0,height], end=[width,width], duration=600, object=self, property="minimumSize")
        animation.propertyAnimation(start=[width,height], end=[newWidth,height], duration=600, object=self, property="maximumSize", mode="OutExpo")
        #propertyAnimation(start=[width, height], end=[newWidth, height], duration=600, object=self, property="minimumSize", mode="OutExpo")


    def set_text(self, input):
        self.setText(input)
        if self.originalTitle == None: self.originalTitle = input

        height = self.size().height()
        # Measure text
        metrics = QtGui.QFontMetrics(self.font())
        newWidth = metrics.width(input) + 20
        animation.propertyAnimation(start=[(newWidth - 20), height], end=[newWidth, height], duration=500, object=self, property="maximumSize", mode="OutExpo")

    def get_value(self):
        if self.value != None:
            if self.multiple == False:
                return self.value[0]
            else: return self.value

    def enterEvent(self, event):
        animation.fadeAnimation(start="current", end=self.endOpacity, duration=self.inAnimDuration,object=self.opacityEffect)
        # self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

    def leaveEvent(self, event):
        animation.fadeAnimation(start="current", end=self.opacity, duration=self.outAnimDuration,object=self.opacityEffect)
        # self.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)

class dropButton(QtWidgets.QPushButton):
    '''Create a button that can store values for us'''
    def __init__(self):
        super(dropButton, self).__init__()

        # Initialise value
        self.setAcceptDrops(True)
        self.value = None

    def add_value(self):
        print "Add a value to me"
        # Get current selection from the scene and add as values to this object
        selection = pm.ls(sl=True)
        if len(selection) >= 1:
            self.value = selection
            #self.value = [object.name() for object in selection]
            valueName = [object.name() for object in selection]

            # Set text of button
            self.setText(",".join(valueName)[:(int(self.width() * 0.15))])

            # Set color of button
            self.setStyleSheet('background-color: rgb(250,250,250,200')

    def get_value(self):
        if self.value != None:
            if self.multiple == False:
                return self.value[0]
            else: return self.value

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.accept()
            # Add highlight to window
            self.setStyleSheet('background-color: rgb(250,250,250,250')

    def dragLeaveEvent(self, e):
        # Reset highlight to window
        self.setStyleSheet('background-color: rgb(250,250,250,200')

    def dropEvent(self, event):
        # Reset highlight to window
        self.setStyleSheet('background-color: rgb(250,250,250,50')

        droppedCommand = event.mimeData().text()
        print droppedCommand
        print event.mimeData()

class pathButton(QtWidgets.QPushButton):
    '''Create a button that can store values for us'''
    def __init__(self):
        super(pathButton, self).__init__()

        # Initialise value
        self.value = None
        self.pathField = None
        self.mode = "Directory"
        self.filter = None
        #self.filter = "Maya file(*.mb)"

        icon = qt_icon.load_svg((relativePath + os.sep + "icons" + os.sep + "folderIcon.svg"))
        self.setIcon(icon)
        # Set color of button
        self.setStyleSheet('background-color: rgb(250,250,250,0')
        self.setFlat(True)


    def add_value(self):
        # Get current selection from the scene and add as values to this object
        selection = pm.ls(sl=True)
        if len(selection) >= 1:
            self.value = selection
            valueName = [object.name() for object in selection]

            # Set text of button
            self.setText(",".join(valueName)[:(int(self.width() * 0.15))])



    def get_value(self):
        if self.value != None:
            if self.multiple == False:
                return self.value[0]
            else: return self.value

    def add_path(self):
        file = dialog.picker_dialog(mode=self.mode, filter=self.filter)
        print file
        print len(file)
        if self.pathField != None:
            self.pathField.setText(file[0])