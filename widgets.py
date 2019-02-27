from external.Qt import QtWidgets, QtCompat, QtCore, QtGui, QtSvg

import main
import animation
import button

reload(animation)
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
        self.header = button.fadeButton(layout)
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
