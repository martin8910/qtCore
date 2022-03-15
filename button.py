from __future__ import print_function
# -*- coding: utf-8 -*-

__author__ = "Martin Gunnarsson"
__email__ = "hello@deerstranger.com"

from .external.Qt import QtWidgets, QtCompat, QtCore, QtGui, QtSvg, Qt
from . import animation, dialog
from . import icon as qt_icon

import os
try:
    import pymel.core as pm
except:
    pass

relativePath = os.path.dirname(os.path.realpath(__file__)) + os.sep

class fadeButton(QtWidgets.QToolButton):
    """Create star-icon on card """

    def __init__(self, parent):
        super(fadeButton, self).__init__()
        # QToolButton.__init__(self, parent)

        self.width = 20
        self.height = 20
        self.opacity = 0.3
        self.endOpacity = 0.8
        self.inAnimDuration = 300
        self.outAnimDuration = 800

        # Create opacity effect
        self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacityEffect)
        self.setAutoFillBackground(True)
        self.setOpacity(self.opacity)
        self.activeButton = False

        # Set cursor
        self.setCursor(QtCore.Qt.PointingHandCursor)

        # Set sizing of the button
        # self.setSize(self.width, self.height)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

    def setOpacity(self, opacity):
        self.opacityEffect.setOpacity(opacity)
        self.opacity = opacity

    def setAnimateOpacity(self, opacity, duration=500):
        #self.opacityEffect.setOpacity(opacity)
        animation.fadeAnimation(start="current", end=opacity, duration=duration,object=self.opacityEffect)
        QtWidgets.QApplication.processEvents()
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
    def fadeUp(self):
        animation.fadeAnimation(start="current", end=self.opacity, duration=1500, object=self.opacityEffect)

    # def mousePressEvent(self, event):
    #     super(fadeButton).mousePressEvent(event)
    #     animation.fadeAnimation(start="current", end=1, duration=200, object=self.opacityEffect,finishAction=self.fadeUp)




class popButton(QtWidgets.QPushButton):
    """Create star-icon on card """

    def __init__(self, parent):
        super(popButton, self).__init__()
        # QToolButton.__init__(self, parent)

        self.width = 20
        self.height = 20
        self.normalIconSize = 20
        self.inAnimDuration = 200
        self.outAnimDuration = 200
        self.growValue = 25

        # Set sizing policy on button
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)

        self.clicked.connect(self.clickEvent)

        # Create opacity effect
        self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacityEffect)
        self.setAutoFillBackground(True)
        self.opacityEffect.setOpacity(1)

        # Set sizing of the button
        # self.setSize(self.width, self.height)
        #self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

        self.setStyleSheet('''QPushButton {color: rgb(250, 250, 250);background-color: rgb(0, 250, 0,0);border-style: None;border-width: 0px;}QPushButton:menu-indicator { image: none; }''')


    def setSize(self, width, height):
        self.setIconSize(QtCore.QSize(self.normalIconSize, self.normalIconSize))

        self.width = width
        self.height = height

    def enterEvent(self, event):
        animation.propertyAnimation(start=["current", "current"], end=[self.growValue, self.growValue], duration=self.inAnimDuration, object=self,property="iconSize", mode="OutExpo")

    def leaveEvent(self, event):
        animation.propertyAnimation(start=[self.growValue, self.growValue], end=[self.normalIconSize, self.normalIconSize], duration=self.outAnimDuration, object=self,property="iconSize", mode="OutExpo")
    def clickEvent(self):
        animation.fadeAnimation(start="current", end=0.5, duration=200, object=self.opacityEffect)
        animation.propertyAnimation(start=["current", "current"], end=[(self.width * 0.6), (self.height * 0.6)], duration=200, object=self,property="iconSize", mode="OutExpo", finishAction=self.fadeUp)


    def fadeUp(self):
        animation.propertyAnimation(start=["current", "current"], end=[self.growValue, self.growValue], duration=300, object=self,property="iconSize", mode="OutExpo")
        animation.fadeAnimation(start="current", end=1, duration=self.outAnimDuration, object=self.opacityEffect)



class valueButton(QtWidgets.QToolButton):
    '''Create a button that can store values for us'''
    def __init__(self):
        super(valueButton, self).__init__()

        # Initialise value
        self.value = None
        self.missing_value = []
        self.static_value = None
        self.multiple = True
        self.originalTitle = None

        # Create communication slot for updates
        self.emitter = communicate(self)

        # Store other objects that should update when this button is updated
        self.value_connector = []

        self.menu_items = []


        # Create opacity effect
        #self.opacity = 1
        self.endOpacity = 1
        self.inAnimDuration = 100
        self.outAnimDuration = 400
        #self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(self)
        #self.setGraphicsEffect(self.opacityEffect)
        #self.setAutoFillBackground(True)

        self.clicked.connect(self.add_value)

        self.textCutoff = 20

        # Set style
        self.inactiveStyleSheet = "QToolButton\n{\npadding: 1px;\nborder-radius: 10px;\nbackground-color: rgb(250,250,250,20);\ncolor: rgb(250,250,250,200);\n}QToolButton::menu-indicator{width:0px;}"
        self.errorStyleSheet = "QToolButton\n{\npadding: 1px;\nborder-radius: 10px;\nbackground-color: rgb(234,100,61,20);\ncolor: rgb(250,250,250,200);\n\n}\n\nQToolButton:focus\n{\nbackground-color: rgb(250,250,250,20);\nborder-style: solid;\n}QToolButton::menu-indicator{width:0px;}"
        self.activeStyleSheet = "QToolButton\n{\npadding: 1px;\nborder-radius: 10px;\nbackground-color: rgb(0, 153, 51);\ncolor: rgb(250,250,250,200);\n\n}\n\nQToolButton:focus\n{\nbackground-color: rgb(0, 153, 51);\n}QToolButton:disabled{background-color: rgb(0, 153, 51, 30);}QToolButton::menu-indicator{width:0px;}"

        # Stylesheet
        self.setStyleSheet(self.inactiveStyleSheet)

        # Add context menu
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.add_menu_items()

    def add_menu_items(self):
        items = []
        items.append(["Select Objects", self.select_value])
        if len(pm.ls(sl=True)) >= 1:
            items.append(["Add selected", self.add_more_from_menu])
            #if self.check_if_selection_exists():
            #    items.append(["Remove Selected", self.remove_selected_from_menu])
        items.append(["Reset Values", self.reset_value])
        if self.missing_value:
            items.append(["Remove missing", self.remove_missing_values])


        if len(self.menu_items) != 0:
            for action in self.menu_items:
                self.removeAction(action)
        self.menu_items = []
        for item in items:
            action = QtWidgets.QAction(self)
            action.setText(item[0])
            action.triggered.connect(item[1])
            self.menu_items.append(action)
            self.addAction(action)

    def add_more_from_menu(self):
        current_values = self.get_value(static=False)
        selection = pm.ls(sl=True)
        if len(selection) >= 1:
            for object in selection:
                valueName = object.name()
                if valueName not in current_values:
                    if type(current_values[0]) == str or type(current_values[0]) == unicode:
                        self.value.append(object.name())
                    else:
                        self.value.append(object)
                else:
                    print("WARNING: '{}' already exist as a value".format(valueName))
            self.set_header()
            self.emitter.value.emit(1)
        else:
            print("WARNING: No selection to add from!")

    def remove_selected_from_menu(self):
        print("This will remove existing items")

        # Get current selection
        current_values = self.get_value(static=False)
        selection = pm.ls(sl=True)
        if len(selection) >= 1:
            for object in selection:
                valueName = object.name()
                if valueName in current_values:
                    if type(current_values[0]) == str or type(current_values[0]) == unicode:
                        self.value.remove(object.name())
                    else:
                        self.value.remove(object)
                else:
                    print("WARNING: '{}' dont exist as a value".format(valueName))
            self.set_header()
            self.emitter.value.emit(1)

    def check_if_selection_exists(self):
        # Get current selection
        return_value = False
        current_values = self.get_value(static=False)
        print("current_values:", current_values)
        if current_values:
            selection = pm.ls(sl=True)
            if len(selection) >= 1:
                for object in selection:
                    valueName = object.name()
                    if valueName in current_values:
                        return_value = True
        return return_value

    def remove_missing_values(self):

        # Get current value and
        current_value = self.get_value(static=True)
        new_values = [x for x in current_value if x not in self.missing_value]
        self.set_value(new_values)
        self.emitter.value.emit(1)

    def update_valueItems(self):
        if len(self.value_connector) is not 0:
            for object in self.value_connector:
                valueName = [o.name() for o in self.value]
                valueName = "".join(valueName)
                object.setText(valueName)

    def add_value(self):
        # Get current selection from the scene and add as values to this object
        selection = pm.ls(sl=True)
        if len(selection) >= 1:
            if self.multiple:
                valueName = [object.name() for object in selection]
                valueName = " , ".join(valueName)

                if type(selection) == list or type(selection) == tuple:
                    self.set_value(selection, valueName=valueName)
                else:
                    pass
                    #self.set_value([selection], valueName=valueName)
            else:
                self.set_value(selection[0], valueName=selection[0].name())


            self.opacity = 1
            self.setStyleSheet(self.activeStyleSheet)
            # Set value on attached objects if any
            self.update_valueItems()

        else:
            self.opacity = 0.6

            dialog.activatePopup(self, "No Selection detected")
            self.set_value([], valueName=self.originalTitle)
            self.setStyleSheet(self.inactiveStyleSheet)

    def reset_value(self):
        self.set_value([], valueName=self.originalTitle)
        self.setStyleSheet(self.inactiveStyleSheet)
        self.emitter.value.emit(1)
    def set_value(self, value, valueName=None, animate=False):

        self.value = value

        # Convert to list if not already
        if type(value) == list or type(value) == tuple:
            pass
        else:
            value = [value]
            # New line to handle offset
            self.value = value

        # Set stylesheet
        if len(value) != 0:
            self.setStyleSheet(self.activeStyleSheet)

        # Set Static values
        if len(value) is not 0:
            if type(value[0]) == str or type(value[0]) == unicode:
                self.static_value = value
            else:
                self.static_value = [v.name() for v in value]
        else:
            self.static_value = None


        self.set_header(valueName=None, animate=animate)


    def set_header(self, valueName=None, animate=False):
        height = self.size().height()
        width = self.size().width()

        value = self.value
        if valueName != None:
            self.set_text(valueName)
        else:
            # If not None
            if value is not None:
                # If List
                if type(value) == list or type(value) == tuple:
                    # If length is not 0
                    if len(value) != 0:
                        # If first list-item is unicode
                        if type(value[0]) == str or type(value[0]) == unicode:
                            valueName = [object for object in value]
                        # If first list-item is object
                        else:
                            valueName = [object.name() for object in value]

                        valueName = ",".join(valueName)[:20]
                        static_value = valueName
                    else:
                        valueName = "Nothing selected..."
                # Not a list
                else:
                    # If unicode
                    if type(value) == str or type(value) == unicode:
                        valueName = value
                    # If Pymel
                    else:
                        valueName = value.name()
                self.set_text(valueName)

                # Check missing geo
                if self.value is not None:
                    if len(self.value) != 0:
                        existing_geo = [x for x in self.static_value if pm.objExists(x)]
                        self.missing_value = list(set(self.static_value) - set(existing_geo))
                        if self.missing_value:
                            print("The following item dont exist in the scene:")
                            for x in self.missing_value:
                                print("MISSING OBJECT:", x)
                            self.setStyleSheet(self.errorStyleSheet)
                            self.add_menu_items()
            else:
                self.set_text("No Value")

        # Calculate new size

        # Get max size from parent
        metrics = QtGui.QFontMetrics(self.font())
        newWidth = metrics.width(valueName[:self.textCutoff]) + 20

        # Animate size
        if animate:
            animation.animateWidgetSize(self,start=(width, height),end=(newWidth, height), expanding=True, duration=700, bounce=False)
        else:
            #self.setMaximumWidth(newWidth)
            #self.setMinimumWidth(newWidth)
            #self.minimumSizeHint(newWidth, self.sizeHint().height())

            self.setMaximumSize(QtCore.QSize(newWidth, self.sizeHint().height()))
            #self.adjustSize()
            #self.resize(self.sizeHint())

    def set_text(self, input):
        self.setText(input[:self.textCutoff])
        if self.originalTitle == None: self.originalTitle = input

    def get_value(self, static=False):
        if static:
            return self.static_value
        else:
            return self.value

    def select_value(self):
        pm.select(self.value)

    # def mousePressEvent(self, event):
    #     '''re-implemented to suppress Right-Clicks from selecting items.'''
    #
    #     if event.type() == QtCore.QEvent.MouseButtonPress:
    #         if event.button() == QtCore.Qt.RightButton:
    #             self.
    #         else:
    #             super(MyView, self).mousePressEvent(event)

    # def enterEvent(self, event):
    #     animation.fadeAnimation(start="current", end=self.endOpacity, duration=self.inAnimDuration,object=self.opacityEffect)
    #     # self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
    #
    # def leaveEvent(self, event):
    #     animation.fadeAnimation(start="current", end=self.opacity, duration=self.outAnimDuration,object=self.opacityEffect)
    #     # self.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)

class dropButton(valueButton):
    '''Create a button that can store values for us'''
    def __init__(self):
        super(dropButton, self).__init__()

        # Initialise value
        self.setAcceptDrops(True)


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

class pathButton(QtWidgets.QPushButton):
    '''Create a button that can store values for us'''
    def __init__(self):
        super(pathButton, self).__init__()

        # Initialise value
        self.value = None
        self.pathField = None
        self.mode = "Directory"
        self.my_value = None
        self.message = "Open something for us. [Specify this with self.message]"
        # self.mode = ExistingFiles, DirectoryOnly, Directory, ExistingFile, SaveFile, AnyFile
        self.filter = None
        #self.filter = "Maya file(*.mb)"

        icon = qt_icon.load_svg((relativePath + os.sep + "icons" + os.sep + "folderIcon.svg"))
        self.setIcon(icon)
        # Set color of button
        self.setStyleSheet('background-color: rgb(250,250,250,0')
        self.setFlat(True)

        self.clicked.connect(self.add_path)


    def set_value(self, value):
        '''Set the default value of the button'''
        self.value = value
        self.setText(self.value)

    def get_value(self):
        if self.pathField != None:
            if len(self.pathField.text()) >= 1:
                return self.pathField.text()
            else:
                return self.value
        else:
            return self.value

    def add_path(self):
        file = dialog.picker_dialog(mode=self.mode, filter=self.filter)
        if self.pathField != None:
            self.pathField.setText(file[0])
            self.value = file[0]


class communicate(Qt.QtCore.QObject):
    '''Create a new signal that other Uis can pick up from'''
    value = Qt.QtCore.Signal(int)