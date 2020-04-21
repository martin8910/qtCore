__author__ = "Martin Gunnarsson"
__email__ = "hello@deerstranger.com"

from external.Qt import QtWidgets, QtCompat, QtCore, QtGui, QtSvg
import animation
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

def get_value(object, static=False):
    '''Get the current value from a input field, numeric slider etc'''
    # Get type
    if type(object) == QtWidgets.QLineEdit:  #QLineEdit
        value = object.text()
    elif type(object) == QtWidgets.QTextEdit:  #QTextEdit
        value = object.toPlainText()
    elif "valueButton" in str(type(object)):  #ValueButton
        value = object.get_value(static=static)
        # Return the first instance if multiple is false
        if object.multiple is False:
            try: value = value[0]
            except: value = value
            #if type(value) is not None:
            #    value = value[0]
            #else:
            #    value = value
    elif "vectorInput" in str(type(object)):  #ValueButton
        value = object.get_values()
    elif "colorInput" in str(type(object)):  #ValueButton
        value = object.get_values()
    elif "pymel_holder" in str(type(object)):  #Pymel holder
        value = object.get_value()
    elif "dict_holder" in str(type(object)):  #Dictionary Holder
        value = object.get_values()
    elif "combobox_multiple" in str(type(object)):  #ValueButton
        value = object.get_value()
    elif "attribute_holder" in str(type(object)):  #Combobox Multiple
        value = object.get_value()
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
        print "GET VALUE: No supported type found for '{}'".format(type(object))
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
        object.setValue(value)
    elif type(object) == QtWidgets.QTextEdit:
        object.setText(value)
    elif type(object) == QtWidgets.QDoubleSpinBox:
        object.setValue(value)
    elif type(object) == QtWidgets.QComboBox:
        object.setCurrentText(value)
    elif type(object) == QtWidgets.QCheckBox:
        object.setChecked(value)
    elif "valueButton" in str(type(object)):  #ValueButton
        if value is not None:
            object.set_value(value)
    elif "vectorInput" in str(type(object)):  #ValueButton
        object.set_values(value)
    elif "colorInput" in str(type(object)):  #ValueButton
        object.set_values(value)
    elif "pymel_holder" in str(type(object)):  #ValueButton
        object.set_value(value)
    elif "dict_holder" in str(type(object)):  #ValueButton
        object.set_values(value)
    elif "combobox_multiple" in str(type(object)):  #ValueButton
        object.set_value(value)
    elif "attribute_holder" in str(type(object)):  #ValueButton
        object.set_value(object=value["object"], attributes=value["attributes"])
    else:
        print "SET VALUE: No supported type found for '{}'".format(type(object))
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
    elif "colorInput" in str(type(object)) or "vectorInput" in str(type(object)):
        object.ui.value01.valueChanged.connect(connection)
        object.ui.value02.valueChanged.connect(connection)
        object.ui.value03.valueChanged.connect(connection)
    elif "pymel_holder" in str(type(object)):  # Pymel holder item
        object.select_button.clicked.connect(connection)
    elif "attribute_holder" in str(type(object)):  # Pymel holder item
        object.select_button.clicked.connect(connection)
    elif "dict_holder" in str(type(object)):  # Dictionary Sheet
        type_list = [x.type for x in object.rows]
        for index in range(object.tableWidget.rowCount()):
            for row, header_type in enumerate(type_list):
                widget = object.tableWidget.cellWidget(index, row)
                connect_value_change(widget, connection=connection)
    elif "combobox_multiple" in str(type(object)):  # ValueButton
        object.expand_button.clicked.connect(connection)
        object.holder.textEdited.connect(connection)
        for c in object.checkboxes:
            c.clicked.connect(connection)
    elif type(object) == QtWidgets.QLabel:
        print "Setting connection on a label is not supported for now"
    elif type(object) == QtWidgets.QSpinBox:
        object.valueChanged.connect(connection)
    elif type(object) == QtWidgets.QTextEdit:
        object.textChanged.connect(connection)
    elif type(object) == QtWidgets.QDoubleSpinBox:
        object.valueChanged.connect(connection)
    elif type(object) == QtWidgets.QComboBox:
        object.currentIndexChanged.connect(connection)
    elif type(object) == QtWidgets.QCheckBox:
        object.stateChanged.connect(connection)
    else:
        print "CONNECT: No supported type found for '{}'".format(type(object))



def object_from_type(object):
    '''Return an object that accepts its input type'''
    # Get type
    #print "TYPE:", type(object)
    #print "VALUE:", object
    if type(object) == str or type(object) == unicode:
        widget = QtWidgets.QLineEdit()
        widget.setText(object)
    elif type(object) == None:
        widget = QtWidgets.QLineEdit()
    elif type(object) == bool:
        widget = QtWidgets.QCheckBox()
        if object is True:
            widget.setChecked(True)
    elif type(object) == list:
        widget = QtWidgets.QLineEdit()
    elif type(object) == list:
        widget = QtWidgets.QLineEdit()
    elif type(object) == None:
        widget = QtWidgets.QPushButton("None")
    elif type(object) == dict:
        widget = QtWidgets.QPushButton("Dictionary")
    #object = QtWidgets.QLineEdit()
    #object = QtWidgets.QPushButton()
    #object = QtWidgets.QLabel()
    #object = QtWidgets.QSpinBox()
    #object = QtWidgets.QTextEdit()
    #object = QtWidgets.QDoubleSpinBox()
    #object = QtWidgets.QComboBox()
    #bject = QtWidgets.QCheckBox()
    #"valueButton"
    #"vectorInput"
    #"colorInput"
    #"pymel_holder"
    #"dict_holder"
    #"combobox_multiple"
    #else:
    #    print "SET VALUE: No supported type found for '{}'".format(type(object))
    #    value = None
    #print

    # '''Connect the changecommand for a object based on its type'''
    # if type(object) == QtWidgets.QLineEdit:
    #     object.textChanged.connect(connection)
    # elif type(object) == QtWidgets.QPushButton:
    #     object.clicked.connect(connection)
    # elif type(object) == QtWidgets.QLabel:
    #     print "Setting connection on a label is not supported for now"
    # elif type(object) == QtWidgets.QSpinBox:
    # elif type(object) == QtWidgets.QTextEdit:
    # elif type(object) == QtWidgets.QDoubleSpinBox:
    # elif type(object) == QtWidgets.QComboBox:
    # elif type(object) == QtWidgets.QCheckBox:
    # else:
    #     print "CONNECT: No supported type found for '{}'".format(type(object))

    return widget

# def load_svg(iconPath, size=(20,20)):
#     svg_renderer = QtSvg.QSvgRenderer(iconPath)
#     image = QtGui.QImage(size[0], size[1], QtGui.QImage.Format_ARGB32)
#     image.fill(0x00000000)
#     svg_renderer.render(QtGui.QPainter(image))
#     pixmap = QtGui.QPixmap.fromImage(image)
#     icon = QtGui.QIcon(pixmap)
#
#     return icon


def get_index_in_layout(item):
    '''Return a position index of an item in a widgetss children'''
    index = [num for num, object in enumerate(item.parent().children()) if object == item]
    if len(index) != 0:
        return index[0]
    else:
        print "ERROR: Item not found in layout"
        return -1


def clearLayout(layout):
    '''Clear input layout of its content'''
    if layout != None:
        try:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    clearLayout(child.layout())
        except: pass
def autoFieldWidth(inputObject, offset=0, minimum=0, animate=False):
    '''Takes any object that have a "text" attribute and sets its width according to its content'''
    current_width = inputObject.width()
    current_height = inputObject.height()

    text = inputObject.text()
    metrics = QtGui.QFontMetrics(inputObject.font())
    width = metrics.width(text) + offset

    #Set field
    if width <= minimum: width = minimum

    if animate:
        animation = QtCore.QPropertyAnimation(inputObject, "minimumWidth", inputObject)

        # Set start and end values
        animation.setStartValue(current_width)
        animation.setEndValue(width + offset)

        # Create easing style
        style = QtCore.QEasingCurve()
        style.setType(QtCore.QEasingCurve.InOutQuart)
        animation.setEasingCurve(style)

        animation.setDuration(500)
        animation.start(QtCore.QPropertyAnimation.DeleteWhenStopped)
        #animation.animateWidgetSize(inputObject, start=(current_width, current_height), end=(width, current_height), duration=600, attributelist=("maximumSize", "minimumSize"),expanding=False)
    else:
        inputObject.setMaximumWidth(width)
        inputObject.setMinimumWidth(width)

def selectItemByIndex(listWidget, index):
    '''Select the index of a QListWidget'''
    firstItem = listWidget.item(index)
    listWidget.setCurrentItem(firstItem)


def select_item_by_text(listWidget, text, data_position=None):
    '''Select the index of a QListWidget'''
    index = -1
    if type(listWidget) == QtWidgets.QListWidget:
        items = [listWidget.item(i).text() for i in range(listWidget.count())]
        if data_position is None:
            index = items.index(text)  # Get text's index
        else:
            for i in range(listWidget.count()):
                if listWidget.item(i).data(data_position) == text:
                    index = i
                    break
        if index != -1:
            listWidget.setCurrentRow(index)
        else:
            print "Index probably not found:"
            print "Input text", text
            print "Index found", index

    elif type(listWidget) ==  QtWidgets.QComboBox:
        index = listWidget.findText(str(text))
        listWidget.setCurrentIndex(index)

    elif type(listWidget) ==  QtWidgets.QListWidget:
        index = listWidget.findText(str(text))
        listWidget.setCurrentIndex(index)
    else:
        print "No supported type provided for 'qtCore.select_item_by_text'"
        print "TYPE:", type(listWidget)

def add_items_to_layout(layout, items):
    for item in items:
        if type(item) == QtWidgets.QSpacerItem:
            layout.addItem(item)
        else:
            layout.addWidget(item)


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
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.ui)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.values = [0,0,0]

    def get_values(self):
        return self.values

    def set_values(self, values):

        self.ui.value01.setValue(values[0])
        self.ui.value02.setValue(values[1])
        self.ui.value03.setValue(values[2])

        self.update_values()

    def set_titles(self, titles):

        self.ui.label01.setText(titles[0])
        self.ui.label02.setText(titles[1])
        self.ui.label03.setText(titles[2])

    def setMaximum(self, max_values):

        self.ui.value01.setMaximum(max_values[0])
        self.ui.value02.setMaximum(max_values[1])
        self.ui.value03.setMaximum(max_values[2])

    def setMinimum(self, min_values):

        self.ui.value01.setMinimum(min_values[0])
        self.ui.value02.setMinimum(min_values[1])
        self.ui.value03.setMinimum(min_values[2])


    def update_values(self):
        self.values = [self.ui.value01.value(), self.ui.value02.value(), self.ui.value03.value()]

    def setDecimal(self, decimalAmount):
        for o in [self.ui.value01, self.ui.value02, self.ui.value03]:
            o.setDecimals(decimalAmount)
            if decimalAmount == 0:
                o.setSingleStep(1)
            elif decimalAmount == 1:
                o.setSingleStep(0.1)
            elif decimalAmount == 2:
                o.setSingleStep(0.01)



class colorInput(QtWidgets.QWidget):
    def __init__(self, parent = None, widget=None):
        super(colorInput, self).__init__()
        self.ui = qtUiLoader("{}colorWidget.ui".format(relativePath + os.sep + "ui" + os.sep))
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.ui)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Adjust size
        self.adjustSize()

        # Connect to color-input
        for button in [self.ui.value01, self.ui.value02, self.ui.value03]:
            button.valueChanged.connect(self.update_values)
        self.ui.color_button.clicked.connect(self.show_picker)
        # Adjust size
        self.adjustSize()

        self.update_values()


    def get_values(self):
        return self.values

    def set_values(self, values):

        self.ui.value01.setValue(values[0])
        self.ui.value02.setValue(values[1])
        self.ui.value03.setValue(values[2])

        self.update_values()

    def set_titles(self, titles):

        self.ui.label01.setText(titles[0])
        self.ui.label02.setText(titles[1])
        self.ui.label03.setText(titles[2])

    def setMaximum(self, max_values):

        self.ui.value01.setMaximum(max_values[0])
        self.ui.value02.setMaximum(max_values[1])
        self.ui.value03.setMaximum(max_values[2])

    def setMinimum(self, min_values):

        self.ui.value01.setMinimum(min_values[0])
        self.ui.value02.setMinimum(min_values[1])
        self.ui.value03.setMinimum(min_values[2])

    def setDecimal(self, decimalAmount):
        for o in [self.ui.value01, self.ui.value02, self.ui.value03]:
            o.setDecimals(decimalAmount)
            if decimalAmount == 0:
                o.setSingleStep(1)
            elif decimalAmount == 1:
                o.setSingleStep(0.1)
            elif decimalAmount == 2:
                o.setSingleStep(0.01)

    def show_picker(self):
        self.color_dialog = QtWidgets.QColorDialog()
        self.color_dialog.colorSelected.connect(self.trigger_color)

        self.color_dialog.show()

    def trigger_color(self, color):
        self.set_values(color.getRgb())

    def update_values(self):
        self.values = [self.ui.value01.value(), self.ui.value02.value(), self.ui.value03.value()]

        # Set color of the button
        self.ui.color_button.setStyleSheet('background-color: rgb({},{},{});border-radius: 5px;'.format(self.values[0], self.values[01], self.values[2]))


def create_spacer(mode="vertical"):
    if mode == "vertical":
        spacer = QtWidgets.QSpacerItem(20, 1000, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    if mode == "horizontal":
        spacer = QtWidgets.QSpacerItem(1000, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    return spacer

class QHLine(QtWidgets.QFrame):
    '''Class to make a horizontal line break'''
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


def read_stylesheet(widget, filepath):
    '''
    Create a stylesheet file from
    :param widget: Widget to apply style to
    :param filepath: Filepath to the stylesheet
    :type widget: QWidget
    :type filepath: path
    :return: None
    '''
    # Apply stylesheet to layout
    if os.path.exists(filepath):
        with open(filepath, "r") as sheet:
           widget.setStyleSheet(sheet.read())
    else:
        print "ERROR The CSS path dont exists:"
        print  filepath

def label_checkbox(object, on_title="On", off_title="Off"):
    '''Name a checkbox by a value'''
    if object.isChecked():
        object.setText(on_title)
    else:
        object.setText(off_title)


# Resize the text-area to fit
def resize_textEdit_to_content(inputObject, max=500):
    '''Resize a text-edit widget to its content'''

    fontMetrics = QtGui.QFontMetrics(inputObject.font())  # a QFontMetrics based on our font
    textSize = fontMetrics.size(0, inputObject.toPlainText())
    textHeight = textSize.height() + 12  # constant may need to be tweaked

    if textHeight <= max:
        inputObject.setMaximumHeight(textHeight)
        inputObject.setMinimumHeight(textHeight)
    else:
        inputObject.setMaximumHeight(max)
        inputObject.setMinimumHeight(max)
    #inputObject.resize(textWidth, textHeight)  # good if you want this to be standalone

