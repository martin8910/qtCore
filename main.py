__author__ = "Martin Gunnarsson"
__email__ = "hello@deerstranger.com"

from external.Qt import QtWidgets, QtCompat, QtCore, QtGui, QtSvg
import os
windowAnim = True

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
    print type(value)
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

def connect_value_change(object, connection=None):
    '''Connect the changecommand for a object based on its type'''
    if type(object) == QtWidgets.QLineEdit:
        object.textChanged.connect(connection)
    elif type(object) == QtWidgets.QPushButton:
        object.clicked.connect(connection)
    elif "valueButton" in str(type(object)):  # ValueButton
        object.clicked.connect(connection)
    elif type(object) == QtWidgets.QLabel:
        print "Setting connection on a label is not supported for now"
    elif type(object) == QtWidgets.QSpinBox:
        object.valueChanged.connect(connection)
    elif type(object) == QtWidgets.QDoubleSpinBox:
        object.valueChanged.connect(connection)
    elif type(object) == QtWidgets.QComboBox:
        object.currentIndexChanged.connect(connection)
    elif type(object) == QtWidgets.QCheckBox:
        object.stateChanged.connect(connection)
    else:
        print "No supported type found for '{}'".format(type(object))

def load_svg(iconPath, size=(20,20)):
    svg_renderer = QtSvg.QSvgRenderer(iconPath)
    image = QtGui.QImage(size[0], size[1], QtGui.QImage.Format_ARGB32)
    image.fill(0x00000000)
    svg_renderer.render(QtGui.QPainter(image))
    pixmap = QtGui.QPixmap.fromImage(image)
    icon = QtGui.QIcon(pixmap)

    return icon

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
