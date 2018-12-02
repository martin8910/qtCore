__author__ = "Martin Gunnarsson (hello@deerstranger.com)"


from .external.Qt import QtWidgets, QtCompat, QtCore, QtGui, QtSvg
import os

from mayaCore import window
windowAnim = True

import pymel.core as pm
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQDockWidget


relativePath = os.path.dirname(os.path.realpath(__file__)) + os.sep

def qtUiLoader(uifile, widget=None):
    ui = QtCompat.loadUi(uifile)  # Qt.py mapped function
    if not widget:
        return ui
    else:
        for member in dir(ui):
            if not member.startswith('__') and \
                            member is not 'staticMetaObject':
                setattr(widget, member, getattr(ui, member))
        return ui

class generic_ui_window(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    def __init__(self, interfacePath, parent=None):
        super(generic_ui_window, self).__init__(parent)
        self.interfacePath = interfacePath
        self.ui = qtUiLoader(self.interfacePath)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.ui)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.repaint()

        #Set unice objectname
        self.setObjectName(str(self.objectName))

        # Install filter
        self.installEventFilter(self)

    def showEvent(self, event):
        self.show()

    def closeEvent(self, event):
        event.accept()
        #fadeWindowAnimation(start=1, end=0, duration=400, object=self,finishAction=self.deleteLater)
        #slideWindowAnimation(start=0, end=300, duration=500, object=self)


class dropButton(QtWidgets.QPushButton):
    '''Create a button that can store values for us'''
    def __init__(self):
        super(dropButton, self).__init__()

        # Initialise value
        self.setAcceptDrops(True)
        self.value = None

    def add_value(self):
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

    def add_value(self):
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

    def add_path(self):
        file = picker_dialog(mode="ExistingFile", filter="Maya file(*.mb)")
        if self.pathField != None:
            self.pathField.setText(file[0])

def get_value(object):
    '''Get the current value from a input field, numeric slider etc'''
    # Get type
    if type(object) == QtWidgets.QLineEdit:  #QLineEdit
        value = object.text()
    elif "valueButton" in str(type(object)):  #ValueButton
        value = object.get_value()
    elif "vectorInput" in str(type(object)):  #ValueButton
        value = object.get_values()
    elif type(object) == QtWidgets.QLabel:  #Label
        value = None
    elif type(object) == QtWidgets.QSpinBox:  #QSpineBox
        value = object.value()
    elif type(object) == QtWidgets.QDoubleSpinBox:  #QDoubleSpinBox
        value = object.value()
    elif type(object) == QtWidgets.QCheckBox:  #QCheckBox
        value = object.isChecked()
    elif type(object) == QtWidgets.QComboBox:  #QComboBox
        value = object.currentText()


    else:
        print "No supported type found for '{}'".format(type(object))
        value = None

    return value

def set_value(object, value):
    '''Get the current value from a input field, numeric slider etc'''
    # Get type
    if type(object) == QtWidgets.QLineEdit:
        object.setText(value)
    elif type(object) == QtWidgets.QPushButton:
        object.set_value(value)
    elif type(object) == QtWidgets.QLabel:
        object.setText(value)
    elif type(object) == QtWidgets.QSpinBox:
        object.setValue()
    elif type(object) == QtWidgets.QDoubleSpinBox:
        object.setValue()
    elif type(object) == QtWidgets.QComboBox:
        object.setCurrentText(value)
    elif type(object) == QtWidgets.QCheckBox:
        object.isChecked(value)
    else:
        print "No supported type found for '{}'".format(type(object))
        value = None

    return value



def clearLayout(layout):
    '''Clear input layout of its content'''
    if layout != None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clearLayout(child.layout())


def autoFieldWidth(inputObject, offset=0, minimum=0):
    '''Takes any object that have a "text" attribute and sets its width according to its content'''
    text = inputObject.text()
    metrics = QtGui.QFontMetrics(inputObject.font())
    width = metrics.width(text) + offset
    #Set field
    if width <= minimum: width = minimum

    inputObject.setMaximumWidth(width)
    inputObject.setMinimumWidth(width)

def selectItemByIndex(listWidget, index):
    '''Select the index of a QListWidget'''
    firstItem = listWidget.item(index)
    listWidget.setCurrentItem(firstItem)


def select_item_by_text(listWidget, text):
    '''Select the index of a QListWidget'''
    if type(listWidget) == QtWidgets.QListWidget:
        items = [listWidget.item(i).text() for i in range(listWidget.count())]
        index = items.index(text)  # Get text's index
        if index != -1:
            listWidget.setCurrentRow(index)
        else:
            print "Index probably not found:"
            print "Input text", text
            print "Index found", index
    elif type(listWidget) ==  QtWidgets.QListWidget:
        index = listWidget.findText(str(text))
        listWidget.setCurrentIndex(index)
    else:
        print "No supported type provided for 'qtCore.select_item_by_text'"
        print "TYPE:", type(listWidget)



def centerWidgetOnScreen(widget):
    '''Center a given widget on the active screen'''
    frameGm = widget.frameGeometry()
    screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
    centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
    frameGm.moveCenter(centerPoint)
    widget.move(frameGm.topLeft())

def animateWidgetSize(element, start=(300, 100), end=(300, 150),expanding=False, attributelist=("minimumSize", "maximumSize"), duration=False):
    '''Animate an objects height'''

    # Set automatic duration if not set
    if duration == False:
        duration = min(abs(start[1] - end[1]) * 5, 500)

    #for attribute in ["minimumSize", "maximumSize"]:
    for attribute in attributelist:
        if attribute == "minimumSize":
            element.setMinimumHeight(end[1])
            element.setMinimumWidth(end[0])
        elif attribute == "maximumSize":
            element.setMaximumHeight(0)
            element.setMaximumWidth(0)
            # pass

        # Create animation property and set start and end point
        animation = QtCore.QPropertyAnimation(element, attribute, element)

        # Set start and end values
        animation.setStartValue(QtCore.QSize(start[0], start[1]))
        animation.setEndValue(QtCore.QSize(end[0], end[1]))

        # Create easing style
        style = QtCore.QEasingCurve()
        if start[1] <= end[1]:
            style.setType(QtCore.QEasingCurve.OutBounce)
            #style.setType(QtCore.QEasingCurve.OutExpo)
            style.setAmplitude(0.2)

        else:
            style.setType(QtCore.QEasingCurve.InOutQuart)
        animation.setEasingCurve(style)

        if expanding == True:
            [animation.finished.connect(x) for x in [lambda: element.setMaximumHeight(1699999), lambda: element.setMinimumHeight(0)]]
            [animation.finished.connect(x) for x in [lambda: element.setMaximumWidth(1699999), lambda: element.setMinimumWidth(0)]]

        animation.setDuration(duration)

        # Start animation and delete when finished
        animation.start(QtCore.QPropertyAnimation.DeleteWhenStopped)

###################################################################################################
# Animation
###################################################################################################


def fadeAnimation(start=0, end=1, duration=300, object=None, finishAction=None):
    if windowAnim is True:
        style = QtCore.QEasingCurve()
        style.setType(QtCore.QEasingCurve.OutQuint)

        if start is "current": start = object.opacity()
        if end is "current": end = object.opacity()

        # Animate window opasity
        opasicyAnimation = QtCore.QPropertyAnimation(object, "opacity", object)
        opasicyAnimation.setEasingCurve(style)
        opasicyAnimation.setDuration(duration)
        opasicyAnimation.setStartValue(start)
        opasicyAnimation.setEndValue(end)
        opasicyAnimation.start()
        if finishAction != None:
            opasicyAnimation.finished.connect(finishAction)
    else:
        object.setOpacity(end)

def fadeWindowAnimation(start=0, end=1, duration=300, object=None, finishAction=None):
    if windowAnim is True:
        style = QtCore.QEasingCurve()
        style.setType(QtCore.QEasingCurve.OutQuint)

        # Animate window opasity
        opasicyAnimation = QtCore.QPropertyAnimation(object, "windowOpacity", object)
        opasicyAnimation.setEasingCurve(style)
        opasicyAnimation.setDuration(duration)
        opasicyAnimation.setStartValue(start)
        opasicyAnimation.setEndValue(end)
        opasicyAnimation.start()
        if finishAction != None:
            opasicyAnimation.finished.connect(finishAction)
    else:
        object.setWindowOpacity(end)
        if finishAction != None:
            object.close()

def resizeWindowAnimation(start=(0, 0), end=(0, 0), duration=300, object=None, finishAction=None,attribute="maximumHeight"):
    if windowAnim is True:
        style = QtCore.QEasingCurve()
        style.setType(QtCore.QEasingCurve.OutQuint)

        if start[0] == "current": start[0] = object.size().height()
        if start[1] == "current": start[1] = object.size().width()

        # Animate window opasity
        positionAnimation = QtCore.QPropertyAnimation(object, attribute, object)
        positionAnimation.setEasingCurve(style)
        positionAnimation.setDuration(duration)
        positionAnimation.setStartValue(QtCore.QSize(start[0], start[1]))
        positionAnimation.setEndValue(QtCore.QSize(end[0], end[1]))
        positionAnimation.start()

        if finishAction != None:
            positionAnimation.finished.connect(finishAction)
    else:
        object.resize(end[0], end[1])
        if finishAction != None:
            object.close()
    pass

def slideWindowAnimation(start=-100, end=0, duration=300, object=None, animationStyle=None,finishAction=None):
    if windowAnim is True:
        # Get current position
        pos = object.pos()

        # Create animation and properties
        slideAnimation = QtCore.QPropertyAnimation(object, 'pos', object)
        slideAnimation.setDuration(duration)
        style = QtCore.QEasingCurve()
        # Change curve if the value is end or beginning
        if start >= end:
            style.setType(QtCore.QEasingCurve.OutExpo)
        else:
            style.setType(QtCore.QEasingCurve.InOutExpo)
        if animationStyle != None:  style.setType(animationStyle)

        # Connect finish animation
        if finishAction != None: slideAnimation.finished.connect(finishAction)

        slideAnimation.setEasingCurve(style)
        slideAnimation.setStartValue(QtCore.QPoint(pos.x(), pos.y() + start))
        slideAnimation.setEndValue(QtCore.QPoint(pos.x(), pos.y() + end))
        slideAnimation.start()




def slideWindowBothAnimation(start=(-100, 0), end=(0, 0), duration=300, object=None, animationStyle=None,finishAction=None):
    if windowAnim is True:
        # Get current position
        pos = object.pos()

        # Create animation and properties
        slideAnimation = QtCore.QPropertyAnimation(object, 'pos', object)
        slideAnimation.setDuration(duration)
        style = QtCore.QEasingCurve()
        # Change curve if the value is end or beginning

        if start[0] >= end[0]:
            style.setType(QtCore.QEasingCurve.OutExpo)
        else:
            style.setType(QtCore.QEasingCurve.InOutExpo)
        if animationStyle != None:  style.setType(animationStyle)

        # Connect finish animation
        if finishAction != None: slideAnimation.finished.connect(finishAction)

        slideAnimation.setEasingCurve(style)
        slideAnimation.setStartValue(QtCore.QPoint(pos.x() + start[1], pos.y() + start[0]))
        slideAnimation.setEndValue(QtCore.QPoint(pos.x() + end[1], pos.y() + end[0]))
        slideAnimation.start()



###################################################################################################
# Dialogs
###################################################################################################

def yesCancelDialog(title="Remove action", message="Are you sure you wanna remove this action?"):
    # Create dialog
    saveCurrentDialog = QtWidgets.QMessageBox()
    saveCurrentDialog.setText(title)
    saveCurrentDialog.setInformativeText(message)
    saveCurrentDialog.addButton(QtWidgets.QMessageBox.No)
    saveCurrentDialog.addButton(QtWidgets.QMessageBox.Yes)

    # Execute dialog
    reply = saveCurrentDialog.exec_()
    if reply == QtWidgets.QMessageBox.Yes:
        reply = "Yes"
    if reply == QtWidgets.QMessageBox.No:
        reply = "Cancel"
    return reply

def saveDialog(title="Unsaved Action", message="Do you want to save your changes?", object=False):
    # Create dialog
    saveCurrentDialog = QtWidgets.QMessageBox()
    saveCurrentDialog.setText(title)
    saveCurrentDialog.setInformativeText(message)
    saveCurrentDialog.setStandardButtons(
        QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
    saveCurrentDialog.setDefaultButton(QtWidgets.QMessageBox.Save)
    # Execute dialog
    reply = saveCurrentDialog.exec_()
    if reply == QtWidgets.QMessageBox.Save:
        return "save"
    if reply == QtWidgets.QMessageBox.Discard:
        return "discard"
    if reply == QtWidgets.QMessageBox.Cancel:
        return "cancel"



def activatePopup(button, text, header="Info", icon="infoIcon", actionText=None, action=None):
    window = button.parent().window()
    '''Create a popup object from the current sender'''
    global popup
    popup = info_popup(widget=window)
    popup.setText(text)
    if actionText != None:
        popup.set_action_text(actionText)
        popup.set_action(action)



    popup.setHeader(header)
    popup.setIcon(icon)
    popup.show()

class info_popup(QtWidgets.QWidget):
    def __init__(self, parent = None, widget=None):
        super(info_popup, self).__init__()
        self.ui = qtUiLoader("{}popupCardSimple.ui".format(relativePath + os.sep + "ui" + os.sep))
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.ui)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)


        #Hide action on default
        self.ui.actionButton.hide()
        self.executeAction = None


        # Tag this widget as a popup
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(True)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.ui.actionButton.clicked.connect(self.execute_action)

        # calculate the botoom right point from the parents rectangle
        #point = widget.srect().bottomRight()
        #print point

        # Set image
        iconFile = load_svg((relativePath + os.sep + "icons" + os.sep + "plugIcon.svg"),size=(15,15))
        self.ui.icon.setIcon(iconFile)

        # map that point as a global position
        global_point = QtGui.QCursor.pos()

        self.adjustSize()

        #Position based on the cursor
        self.move(global_point - QtCore.QPoint((self.width() * 3), 0))
        self.ui.closeButton.clicked.connect(self.hide)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)


    def hide(self):
        fadeWindowAnimation(start=1, end=0, duration=400, object=self, finishAction=self.deleteLater)
        slideWindowBothAnimation(start=(0, 0), end=(30, 0), duration=150, object=self)
        #self.deleteLater()

    def set_action_text(self, input):
        self.ui.actionButton.setText(input)
        self.ui.actionButton.show()

    def set_action(self, action=None):
        if action != None:
            self.executeAction = action
            self.ui.actionButton.show()

    def execute_action(self):
        print self.executeAction
        if self.executeAction != None:
            exec(self.executeAction)

        # Close popup
        self.hide()


    def setText(self, text):
        self.ui.infoLabel.setText(text)

        # Calculate size
        # Measure text
        #metrics = QtGui.QFontMetrics(self.ui.infoLabel.font())
        #newWidth = metrics.width(text)

        # Set small size to the fill out with what it needs
        self.resize(20, 20)  # width, height

        global_point = QtGui.QCursor.pos()
        #self.adjustSize()
        self.move(global_point - QtCore.QPoint((self.width()) - 10, self.height() - 10))
        slideWindowBothAnimation(start=(30, 0), end=(0, 0), duration=400, object=self)
        self.ui.infoLabel.adjustSize()

    def setHeader(self, text):
        self.ui.header.setText(text)

    def setIcon(self, text):
        # Set image
        iconFile = load_svg((relativePath + os.sep + "icons" + os.sep + text + ".svg"),size=(15,15))
        self.ui.icon.setIcon(iconFile)

    def closeEvent(self, event):
        event.accept()
        fadeWindowAnimation(start=1, end=0, duration=400, object=self, finishAction=self.deleteLater)



class vectorInput(QtWidgets.QWidget):
    def __init__(self, parent = None, widget=None):
        super(vectorInput, self).__init__()
        self.ui = qtUiLoader("{}vectorWidget.ui".format(relativePath + os.sep + "ui" + os.sep))
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.ui)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Adjust size
        self.adjustSize()

    def get_values(self):
        value01 = self.ui.value01.value()
        value02 = self.ui.value02.value()
        value03 = self.ui.value03.value()

        return (value01, value02, value03)

    def set_values(self, value01, value02, value03):
        self.ui.value01.setValue(value01)
        self.ui.value02.setValue(value02)
        self.ui.value03.setValue(value03)

class QHLine(QtWidgets.QFrame):
    '''Class to make a horizontal line break'''
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
    def set_style(self, input):
        if input == "Plain":
            self.setFrameShadow(QtWidgets.QFrame.Sunken)
        elif input == "Sunken":
            self.setFrameShadow(QtWidgets.QFrame.Sunken)
        else:
            print "Style '{}' is not supported".format(input)



###################################################################################################
# Handle QTreeWidget/QTreeWidgetItems
###################################################################################################
def get_children_from_treeWidgetItem(treeWidgetItem):
    '''Return all items from a qTreeWidgetItem'''
    items = [treeWidgetItem.child(number) for number in xrange(treeWidgetItem.childCount())]

    return items

def remove_children_from_treeWidgetItem(treeWidgetItem):
    '''Remove all the children from a QTreeWidgetItem'''

    for item in reversed(range(treeWidgetItem.childCount())):
        treeWidgetItem.removeChild(treeWidgetItem.child(item))


def traverse_tree(treeWidgetItem):
    '''Traverse a tree for all ites treeWidgetItems'''
    fullList = []
    for number in range(treeWidgetItem.childCount()):
        # Get item
        item = treeWidgetItem.child(number)

        # Add to list
        fullList.append(item)

        if item.childCount() != 0:
            # If children exists
            results = traverse_tree(item)

            for item in results:
                fullList.append(item)

    return fullList