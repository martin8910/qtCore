from external.Qt import QtWidgets, QtCompat, QtCore, QtGui, QtSvg, Qt

import main
import animation
from button import valueButton, fadeButton
from icon import svg_icon

import icon
import os

relativePath = os.path.dirname(os.path.realpath(__file__)) + os.sep
parentPath = os.path.abspath(os.path.join(relativePath, os.pardir))

def create_header(title="My Amazing header", layout=None, icon=None):
    # Create instance
    headerWidget = header_card_ui()

    # Set name
    headerWidget.set_title(title)

    if icon != None: headerWidget.setIcon(icon, absolute=True)

    # Add widget and set card size
    headerWidgetHolder = QtWidgets.QListWidgetItem(layout)

    headerWidgetHolder.setFlags(QtCore.Qt.ItemIsSelectable == False)

    # Set a name of the widget to the WidgetItem
    headerWidgetHolder.setData(109, headerWidget)
    # headerWidgetHolder.setData(100, name)
    headerWidgetHolder.setSizeHint(QtCore.QSize(100, 35))

    # Add instance to list
    layout.setItemWidget(headerWidgetHolder, headerWidget)

    return headerWidgetHolder

def create_simple_card(title="My Amazing Card", layout=None, icon=None, info=None, path=None, height=20):
    # Create instance
    cardWidget = card_simple_ui()

    # Set name
    cardWidget.setTitle(title)

    if icon != None: cardWidget.setIcon(icon, absolute=True)

    # Add widget and set card size
    cardWidgetHolder = QtWidgets.QListWidgetItem(layout)

    if path != None:
        cardWidget.set_path(path)

    # Set a name of the widget to the WidgetItem
    cardWidgetHolder.setData(109, cardWidget)
    cardWidgetHolder.setSizeHint(QtCore.QSize(150, height))

    # Add instance to list
    layout.setItemWidget(cardWidgetHolder, cardWidget)

    return cardWidgetHolder

def create_icon_card(prefix=None, moduleName=None, layout=None, icon=None, info=None, fullPath=None, identifier=None, height=30):
    # Create instance
    cardWidget = card_icon_ui()

    # Set name
    cardWidget.set_title(prefix)

    if icon != None:
        cardWidget.setIcon(icon, absolute=True)

    # Set icon size
    cardWidget.set_icon_size(height - 10)

    if moduleName != None:
        cardWidget.set_moduleName(moduleName)

    if fullPath != None:
        cardWidget.set_fullPath(fullPath)

    if identifier != None:
        cardWidget.set_id(identifier)

    # Add widget and set card size
    cardWidgetHolder = QtWidgets.QListWidgetItem(layout)

    # Set a name of the widget to the WidgetItem
    cardWidgetHolder.setData(109, cardWidget)
    cardWidgetHolder.setSizeHint(QtCore.QSize(150, height))

    # Add instance to list
    layout.setItemWidget(cardWidgetHolder, cardWidget)

    return cardWidget




########## Create Header UI ##########
class header_card_ui(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(header_card_ui, self).__init__(parent)
        self.built = True
        self.headerName = None

        ##### CREATE UI #####
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.mainFrame = QtWidgets.QFrame(self)

        # Create discription label
        self.descriptionLabel = QtWidgets.QLabel(self.mainFrame)
        self.descriptionLabel.setStyleSheet("color: rgb(250,250,250,50)")
        self.descriptionLabel.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        # Description bold
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(14)
        self.descriptionLabel.setFont(font)

        self.gridLayout.addWidget(self.descriptionLabel)

    def set_title(self, title):
        self.headerName = title
        self.descriptionLabel.setText(title + ":")

    def get_title(self):
        return self.headerName

### Module Card

class card_icon_ui(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(card_icon_ui, self).__init__(parent)

        self.prefix = None
        self.fullPath = "Undefined"
        self.idenfier = None
        self.iconPath = None
        self.sizeFactor = 30

        # Create opacity effect
        self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacityEffect)

        ##### CREATE UI #####
        self.gridLayout = QtWidgets.QHBoxLayout(self)
        self.gridLayout.setContentsMargins(2, 2, 2,2)
        self.gridLayout.setSpacing(5)
        self.mainFrame = QtWidgets.QFrame(self)
        self.mainFrame.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)

        # Create module icon
        self.iconButton = QtWidgets.QPushButton()
        self.iconButton.setFlat(True)
        #self.iconButton.setEnabled(False)
        self.iconButton.setIconSize(QtCore.QSize(20, 20))
        self.iconButton.setMaximumWidth(20)
        self.iconButton.setMaximumHeight(20)
        #self.iconButton.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addWidget(self.iconButton)

        # Create name label
        self.nameLabel = QtWidgets.QLabel(self.mainFrame)
        self.gridLayout.addWidget(self.nameLabel)
        # Description bold
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(10)
        self.nameLabel.setFont(font)

        # Create module label
        self.moduleName = QtWidgets.QLabel(self.mainFrame)
        self.moduleName.setText("Default text here")
        self.gridLayout.addWidget(self.moduleName)


    def activatePopup(self):
        self.popup = popup(self, self)
        self.popup.show()



    def enterEvent(self, event):
        #print "This is when you enter the card"
        #self.popupTimer = QtCore.QTimer(singleShot=True)
        #self.popupTimer.timeout.connect(self.activatePopup)
        #self.popupTimer.start(300)
        #self.activatePopup()
        #self.setFocus()
        pass

    def leaveEvent(self, event):
        #print "This is when you leave the card"
        #self.popup.hide()
        pass
    def set_icon(self, path):
        self.iconPath = path
        #self.iconImage = QtGui.QPixmap(path)
        icon = qtCore.load_svg(path, size=(self.sizeFactor, self.sizeFactor))
        self.iconButton.setIcon(icon)

    def set_title(self, title):
        self.title = title
        self.nameLabel.setText(title.capitalize().replace("_", " "))
        main.autoFieldWidth(self.nameLabel, offset=10)
    def get_title(self):
        return self.title
    def set_moduleName(self, title):
        self.moduleName.setText(title)
    def get_moduleName(self):
        return self.moduleName.text()
    def get_prefix(self):
        return self.title

    def set_fullPath(self, path):
        self.fullPath = path
    def get_icon_path(self):
        return self.iconPath
    def get_fullPath(self):
        return self.fullPath
    def get_id(self):
        return self.idenfier
    def set_id(self, id):
        self.idenfier = id
    def get_opacityEffect(self):
        return self.opacityEffect

    def set_icon_size(self, factor):
        self.sizeFactor = factor
        '''Set the size of the cards icon'''
        self.iconButton.setIconSize(QtCore.QSize(factor, factor))
        self.iconButton.setMaximumWidth(factor)
        self.iconButton.setMaximumHeight(factor)

########## Create Card UI ##########
class card_simple_ui(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(card_simple_ui, self).__init__(parent)

        self.title = None
        self.path = None

        ##### CREATE UI #####
        self.gridLayout = QtWidgets.QHBoxLayout(self)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setSpacing(0)
        self.mainFrame = QtWidgets.QFrame(self)
        self.mainFrame.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        #self.mainFrame.setSize(QtCore.QSize(100, 35))
        # Create discription label
        self.nameLabel = QtWidgets.QLabel(self.mainFrame)
        #self.nameLabel.setSizePolicy(QtCore.QSizePolicy.Expanding, QtCore.QSizePolicy.Expanding)
        self.nameLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.infoButton = QtWidgets.QToolButton()
        self.infoButton.setText("?")
        self.infoButton.setStyleSheet("background-color: rgb(250,250,0,100);color: rgb(0,0,0), border-radius: 3px;")

        #self.infoLabel = QtWidgets.QLabel(self.mainFrame)
        #self.infoLabel.setStyleSheet('color: rgb(250,250,250,60)')

        # self.descriptionLabel.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        self.nameLabel.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        # Description bold
        font = QtGui.QFont()
        font.setBold(True)
        #font.setPointSize(6)
        self.nameLabel.setFont(font)

        self.gridLayout.addWidget(self.nameLabel)
        self.gridLayout.addWidget(self.infoButton)


    def activatePopup(self):
        self.popup = popup(self, self)
        self.popup.show()



    def enterEvent(self, event):
        #print "This is when you enter the card"
        #self.popupTimer = QtCore.QTimer(singleShot=True)
        #self.popupTimer.timeout.connect(self.activatePopup)
        #self.popupTimer.start(300)
        #self.activatePopup()
        #self.setFocus()
        pass

    def leaveEvent(self, event):
        #print "This is when you leave the card"
        #self.popup.hide()
        pass

    def setTitle(self, title):
        self.title = title
        self.nameLabel.setText(title.capitalize().replace("_", " "))
    def setInfo(self, title):
        self.infoLabel.setText(title)
    def getTitle(self):
        return self.title

    def set_path(self, path):
        self.path = path

    def get_path(self):
        return self.path


def create_custom_widget(custom_widget=None, listWidget=None, size=(150,150)):
    # Create instance
    headerWidget = custom_widget()

    # Set name
    #headerWidget.set_title(title)

    #if icon != None: headerWidget.setIcon(icon, absolute=True)

    # Add widget and set card size
    headerWidgetHolder = QtWidgets.QListWidgetItem(listWidget)

    headerWidgetHolder.setFlags(QtCore.Qt.ItemIsSelectable == False)

    # Set a name of the widget to the WidgetItem
    headerWidgetHolder.setData(109, headerWidget)
    # headerWidgetHolder.setData(100, name)
    headerWidgetHolder.setSizeHint(QtCore.QSize(size[0], size[1]))

    # Add instance to list
    listWidget.setItemWidget(headerWidgetHolder, headerWidget)

    return headerWidgetHolder


class collapsable_tab():
    '''Create a exspandable tab that can be open or closed from a header'''
    def __init__(self,layout=None, name="Header Title", layoutDirection="vertical"):

        self.open_state = False
        self.open_icon_path = relativePath + os.sep + "icons" + os.sep + "tab_open.svg"
        self.closed_icon_path = relativePath + os.sep + "icons" + os.sep + "tab_closed.svg"
        self.layoutDir = layoutDirection


        # Create header
        #self.header = QtWidgets.QPushButton(name)
        self.header = fadeButton(layout)
        self.header.setText(name)
        self.header.setOpacity(0.5)
        self.header.setIconSize(QtCore.QSize(10, 10))
        self.header.setStyleSheet("padding-left: 5px;text-align: left;background-color: rgb(0,0,0,0);border-style: none;")
        self.header.setMaximumHeight(25)
        self.header.setMinimumHeight(25)
        # Add icon to header
        icon.svg_icon(button=self.header, path=self.closed_icon_path)
        layout.addWidget(self.header)

        # Create collapsable widget to store content in
        self.holder = QtWidgets.QFrame()
        self.holder.setMaximumWidth(10000)
        self.holder.setMaximumHeight(1)
        self.holder.setObjectName("frameHolder")
        self.holder.setStyleSheet("QFrame#frameHolder{background-color: rgb(0,0,0,0)}")
        layout.addWidget(self.holder)

        self.holder.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Add layout
        if layoutDirection is "vertical":
            self.layout = QtWidgets.QVBoxLayout()
        else:
            self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(4)
        self.holder.setLayout(self.layout)


        self.header.clicked.connect(self.change_state)

    def change_state(self, animate=True):
        '''Change the current state of the holder'''
        current_width = self.holder.size().width()
        #print "WIDTH:", current_width
        current_height = self.holder.size().height()
        expanding = False

        if self.open_state:
            # Close the layout
            self.open_state = False

            new_height = 1
            new_width = current_width


            # Set closed icon
            icon.svg_icon(button=self.header, path=self.closed_icon_path)
        else:
            # Open the layout
            self.open_state = True

            # Add layout spacing
            spacing = self.layout.spacing() * 2
            new_height = self.holder.sizeHint().height()
            new_width = self.holder.minimumSizeHint().width()


            if new_height is 0:
                new_height = 200
            expanding = True
            icon.svg_icon(button=self.header, path=self.open_icon_path)

        # Animate change
        if animate is True:
            animation.animateWidgetSize(self.holder, start=(current_width, current_height), end=(current_width, new_height),bounce=False, duration=600,attributelist=("maximumSize", "minimumSize"), expanding = expanding)
            if expanding is False:
                self.header.setAnimateOpacity(0.5)
            else:
                self.header.setOpacity(0.9)
        else:
            animation.animateWidgetSize(self.holder, start=(current_width, current_height), end=(current_width, new_height),bounce=False, duration=1,attributelist=("maximumSize", "minimumSize"), expanding = expanding)

    def set_open(self):
        '''Open the layout'''
        pass

    def set_closed(self):
        '''Open the layout'''
        pass


class editable_header(QtWidgets.QFrame):
    '''Create a header-object that can be edited by clicking on its header'''
    def __init__(self, parent=None):
        super(editable_header, self).__init__(parent)

        # Create communication slot
        self.emitter = communicate(self)

        self.mode = "view"
        self.header_text = "Unnamed Session"

        # Add layout
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)
        self.setLayout(self.layout)

        # Set stylesheet
        stylesheet_path = relativePath + "stylesheets" + os.sep + "widgets.css"
        with open(stylesheet_path, "r") as sheet:
            self.setStyleSheet(sheet.read())

        # Create title
        self.label = QtWidgets.QPushButton(self.header_text)
        self.label.setObjectName("labelButton")
        self.label.clicked.connect(self.switch_mode)
        self.layout.addWidget(self.label)

        # Add title edit field
        self.input = QtWidgets.QLineEdit(self.header_text)
        self.input.setHidden(True)
        self.input.textChanged.connect(self.update_text)
        self.input.returnPressed.connect(self.switch_mode)
        self.input.textChanged.connect(lambda: self.set_text(self.input.text()))
        self.layout.addWidget(self.input)

    def set_text(self, input):
        self.header_text = input
        self.label.setText(input)
        self.input.setText(input)


    def get_text(self):
        return self.header_text


    def update_text(self):
        main.autoFieldWidth(self.label, offset=5, animate=False)
        main.autoFieldWidth(self.input, offset=5, animate=False)

    def enable_font(self, bold=True, size=20):
        '''Set a font for this header'''
        # Add Font
        font = QtGui.QFont()
        if bold:
            font.setBold(True)
        font.setPointSize(size)
        # Apply font
        self.label.setFont(font)
        self.input.setFont(font)

    def switch_mode(self):
        '''Switch from edit mode to view mode'''

        if self.input.isHidden():
            source = self.label
            destination = self.input
        else:
            source = self.input
            destination = self.label

        destination.setMinimumWidth(source.width())
        destination.setMaximumWidth(16999)
        #destination.setText(source.text())
        if self.input.isHidden():
            destination.setFocus()
            destination.selectAll()
        source.setHidden(True)
        destination.setHidden(False)

        main.autoFieldWidth(destination, offset=1, animate=True)

        # Emit update connection
        self.emitter.value.emit(1)



class combobox_multiple(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(combobox_multiple, self).__init__(parent)

        item_list = []
        self.options = None
        self.value = []
        self.checkboxes = []

        # Create communication slot
        self.emitter = communicate(self)


        self.active_icon_path = relativePath + os.sep + "icons" + os.sep + "checkbox_checked.svg"
        self.inactive_icon_path = relativePath + os.sep + "icons" + os.sep + "checkbox_unchecked.svg"


        self.expand_button = fadeButton(self)
        self.expand_button.setOpacity(0.8)
        self.expand_button.setText("Unassigned")
        self.expand_button.setIconSize(QtCore.QSize(10, 10))
        icon.svg_icon(button=self.expand_button, path=relativePath + os.sep + "icons" + os.sep + "tab_closed.svg")
        self.expand_button.clicked.connect(self.toggle_view)
        item_list.append(self.expand_button)


        # Create layout
        self.topLayout = QtWidgets.QVBoxLayout()
        self.topLayout.setContentsMargins(5, 0, 5, 0)
        self.topLayout.setSpacing(5)

        # Create main widget
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        layout.setContentsMargins(0,0, 0, 0)
        widget.setLayout(layout)
        widget.setMinimumHeight(25)
        widget.setMaximumHeight(25)
        self.topLayout.addWidget(widget)

        spacer = main.create_spacer(mode="vertical")
        layout.addItem(spacer)

        self.holder = QtWidgets.QLineEdit()
        self.holder.setHidden(True)
        item_list.append(self.holder)

        # Add items to layout
        main.add_items_to_layout(layout, item_list)

        # Create holder widget
        self.holder_frame = QtWidgets.QFrame()
        self.holder_frame.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(1)
        layout.setContentsMargins(5, 0, 0, 0)
        self.holder_frame.setLayout(layout)
        self.topLayout.addWidget(self.holder_frame)
        self.holder_frame.setHidden(True)

        # Set main layout
        self.setLayout(self.topLayout)

    def toggle_view(self):
        widget = self.holder_frame
        #self.emitter.value.emit(1)
        if self.holder_frame.isHidden() is False:
            icon.svg_icon(button=self.expand_button, path=relativePath + os.sep + "icons" + os.sep + "tab_closed.svg")
            animation.animateWidgetSize(widget, start=(widget.size().width(), widget.size().height()),
                              end=(widget.size().width(), 0), expanding=False, duration=500, bounce=True,
                              finishAction=[lambda: widget.setHidden(True), lambda: self.emitter.value.emit(1)])
        else:
            widget.setHidden(False)
            icon.svg_icon(button=self.expand_button, path=relativePath + os.sep + "icons" + os.sep + "tab_open.svg")
            animation.animateWidgetSize(widget, start=(widget.size().width(), 0),
                                     end=(widget.size().width(), widget.sizeHint().height()),
                                     expanding=True, duration=500, bounce=False, finishAction=lambda: self.emitter.value.emit(1))


    def add_layout_items(self):
        # Reset checkboxes
        self.checkboxes = []
        # Clear layout
        main.clearLayout(self.holder_frame.layout())
        # Create layout
        for item in self.options:
            widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout()
            layout.setSpacing(3)
            layout.setContentsMargins(0,0, 0, 0)
            widget.setLayout(layout)
            widget.setMaximumHeight(30)
            self.holder_frame.layout().addWidget(widget)

            # Checkbox
            checkbox = QtWidgets.QCheckBox(str(item))
            checkbox.setMinimumSize(30, 22)
            checkbox.setMaximumSize(60, 22)
            checkbox.item = item

            if item in self.value:
                checkbox.setChecked(True)

            layout.addWidget(checkbox)
            checkbox.clicked.connect(self.apply_checkbox_values)
            self.checkboxes.append(checkbox)

    def apply_checkbox_values(self):
        # Reset value
        list = []
        for cb in self.checkboxes:
            if cb.isChecked():
                list.append(cb.item)

        self.set_value(list, animate=True)

        # Emit update connection
        self.emitter.value.emit(1)





    def remove_item(self):
        sender = self.sender()
        sender.widget.setHidden(True)

        # Remove from local value
        self.value.remove(sender.object)

        # Emit update connection
        self.emitter.value.emit(1)

    def get_value(self):
        #print 'Getting value'
        #print self.value
        return self.value

    def set_options(self, options):
        self.options = options
        self.add_layout_items()
    def set_value(self, value, animate=False):
        # Set value in button
        if type(value) == list or type(value) == tuple:
            pass
        else:
            value = [value]

        if len(value) >= 1:
            valueName = " , ".join([str(o) for o in value])
        else:
            valueName = "Unassigned"

        self.expand_button.setText(valueName)
        self.value = value

        self.add_layout_items()


class communicate(Qt.QtCore.QObject):
    '''Create a new signal that other Uis can pick up from'''
    value = Qt.QtCore.Signal(int)