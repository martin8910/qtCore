from external.Qt import QtWidgets, QtCompat, QtCore, QtGui, QtSvg

import main
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


