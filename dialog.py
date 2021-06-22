from __future__ import print_function
# -*- coding: utf-8 -*-

__author__ = "Martin Gunnarsson"
__email__ = "hello@deerstranger.com"

from .external.Qt import QtWidgets, QtCore, QtGui, QtSvg
from . import icon as qt_icon
from . import animation, main
import os

relativePath = os.path.dirname(os.path.realpath(__file__)) + os.sep


###################################################################################################
# Dialogs
###################################################################################################

def progress_window(max=100, title="Operation in progress.", windowTitle="Please stand by"):
    progress_window = QtWidgets.QProgressDialog(title, "Cancel", 0, max)

    # Set window title
    progress_window.setWindowTitle(windowTitle)

    # Show window
    progress_window.show()
    QtWidgets.QApplication.processEvents()

    return progress_window


def inputDialog(instance, header="This is the header", text="Default Text here", input=""):
    output, ok = QtWidgets.QInputDialog.getText(instance, header, text,text=input)

    if ok:
        return output
    else:
        return None


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

def picker_dialog(mode="AnyFile", filter=None, message="Open file/folder"):
    '''Open a filePickerDialog and return the path to the object'''

    # Example on filter
    #"A - TEMPLATE(*.aTemplate)"

    # Create dialog
    dialog = QtWidgets.QFileDialog()


    # Set filter if asked for
    if filter != None:
        dialog.setNameFilter(filter)


    # Set mode
    if mode == "AnyFile":
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
    elif mode == "SaveFile":
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
    elif mode == "ExistingFile":
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
    elif mode == "Directory":
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
    elif mode == "ExistingFiles":
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
    elif mode == "DirectoryOnly":
        dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)


    if "Directory" in mode:
        output = dialog.getExistingDirectory(None, message, filter=filter)
    elif mode == "SaveFile":
        output = dialog.getSaveFileName(None, message, filter=filter)[0]
    elif mode == "ExistingFiles":
        output = dialog.getSaveFileNames(None, message, filter=filter)
    else:
        output = dialog.getOpenFileName(None, message, filter=filter)

    return output


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
        self.ui = main.qtUiLoader("{}popupCardSimple.ui".format(relativePath + os.sep + "ui" + os.sep))
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

        # Set image
        iconFile = qt_icon.load_svg((relativePath + os.sep + "icons" + os.sep + "plugIcon.svg"),size=(15,15))
        self.ui.icon.setIcon(iconFile)

        # map that point as a global position
        global_point = QtGui.QCursor.pos()

        self.adjustSize()

        #Position based on the cursor
        self.move(global_point - QtCore.QPoint((self.width() * 3), 0))
        self.ui.closeButton.clicked.connect(self.hide)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        try:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)
        except:
            pass


    def hide(self):
        animation.fadeWindowAnimation(start=1, end=0, duration=400, object=self, finishAction=self.deleteLater)
        animation.slideWindowBothAnimation(start=(0, 0), end=(30, 0), duration=150, object=self)
        #self.deleteLater()

    def set_action_text(self, input):
        self.ui.actionButton.setText(input)
        self.ui.actionButton.show()

    def set_action(self, action=None):
        if action != None:
            self.executeAction = action
            self.ui.actionButton.show()

    def execute_action(self):
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
        animation.slideWindowBothAnimation(start=(30, 0), end=(0, 0), duration=400, object=self)
        self.ui.infoLabel.adjustSize()

    def setHeader(self, text):
        self.ui.header.setText(text)

    def setIcon(self, text):
        # Set image
        iconFile = qt_icon.load_svg((relativePath + os.sep + "icons" + os.sep + text + ".svg"),size=(15,15))
        self.ui.icon.setIcon(iconFile)

    def closeEvent(self, event):
        event.accept()
        animation.fadeWindowAnimation(start=1, end=0, duration=400, object=self, finishAction=self.deleteLater)


