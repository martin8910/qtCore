import os
from maya import OpenMayaUI
import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQDockWidget
import pymel.core as pm

from external.Qt import QtWidgets, QtCore, QtCompat, QtGui, Qt
import main

from animation import animateWidgetSize
import icon

from widgets import combobox_multiple
from button import valueButton, fadeButton
from icon import svg_icon
import animation
from dialog import activatePopup

relativePath = os.path.dirname(os.path.realpath(__file__)) + os.sep
parentPath = os.path.abspath(os.path.join(relativePath, os.pardir))

#Shiboken

try:
    from shiboken import wrapInstance
    import shiboken
except:
    from shiboken2 import wrapInstance
    import shiboken2 as shiboken



class floating_combobox_multiple(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(floating_combobox_multiple, self).__init__(parent)

        item_list = []
        self.options = None
        self.value = []
        self.checkboxes = []

        # Create communication slot
        self.emitter = communicate(self)


        self.active_icon_path = relativePath + os.sep + "icons" + os.sep + "checkbox_checked.svg"
        self.inactive_icon_path = relativePath + os.sep + "icons" + os.sep + "checkbox_unchecked.svg"

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

        self.expand_button = QtWidgets.QToolButton(self)
        self.expand_button.setText("Select Attr")
        self.expand_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.expand_button.setIconSize(QtCore.QSize(10, 10))
        icon.svg_icon(button=self.expand_button, path=relativePath + os.sep + "icons" + os.sep + "tab_closed.svg")
        item_list.append(self.expand_button)

        # Create menu
        self.menu = QtWidgets.QMenu(self)
        self.expand_button.setMenu(self.menu)
        self.expand_button.setPopupMode(QtWidgets.QToolButton.InstantPopup)


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


    def add_layout_items(self):
        # Reset checkboxes
        self.checkboxes = []
        self.actions = []
        # Clear menu
        self.menu.clear()

        # Add actions
        for item in self.options:
            # Add actions
            action = QtWidgets.QAction(self)
            action.setText(item)
            action.setCheckable(True)
            action.triggered.connect(self.update_values)
            self.menu.addAction(action)
            self.actions.append(action)

            # Check checked already if value
            if item in self.value:
                action.setChecked(True)

    def update_values(self):
        sender = self.sender()
        # Reset value
        list = []
        for action in self.actions:
            if action.isChecked():
                list.append(action.text())

        self.set_value(list, animate=True)

        # Emit update connection
        self.emitter.value.emit(1)

        # Show the menu again to get multiple selections
        self.menu.exec_()

    def get_value(self):
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

        #self.add_layout_items()






def Dock(Widget, width=300, show=True, label=None):
    """Dock `Widget` into Maya
    Arguments:
        Widget (QWidget): Class
        show (bool, optional): Whether to show the resulting dock once created
    """

    name = Widget.__name__
    if label is None:
        label = getattr(Widget, "label", name)
    try:
        cmds.deleteUI(name)
    except RuntimeError:
        pass

    dockControl = cmds.workspaceControl(
        name,
        tabToControl=["AttributeEditor", -1],
        initialWidth=400,
        minimumWidth=100,
        widthProperty="minimum",
        label=label
    )

    dockPtr = OpenMayaUI.MQtUtil.findControl(dockControl)
    dockWidget = QtCompat.wrapInstance(long(dockPtr), QtWidgets.QWidget)
    dockWidget.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    child = Widget(dockWidget)
    dockWidget.layout().addWidget(child)

    if show:
        cmds.evalDeferred(
            lambda *args: cmds.workspaceControl(
                dockControl,
                edit=True,
                restore=True
            )
        )
    return child

def get_window():
    '''Return the main maya-window as an instance to parent to'''
    window = OpenMayaUI.MQtUtil.mainWindow()
    mayaWindow = shiboken.wrapInstance( long( window ), QtWidgets.QMainWindow)
    return mayaWindow

class generic_dockable_window(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    def __init__(self, interfacePath, parent=None):
        super(generic_dockable_window, self).__init__(parent)
        self.interfacePath = interfacePath
        self.ui = main.qtUiLoader(self.interfacePath)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.ui)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

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


    def animate_window_size(self, start=(300,400),end=(500,300),duration=800):
        animation.resizeWindowAnimation(start=start, end=end, duration=800, object=self.window(),attribute="size")


class generic_window(QtWidgets.QWidget):
    def __init__(self, interfacePath, parent=None):
        super(generic_window, self).__init__(parent)
        self.interfacePath = interfacePath
        self.setWindowTitle("Unnamed")
        self.ui = main.qtUiLoader(self.interfacePath)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.ui)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


        #Set unice objectname
        self.setObjectName(str(self.objectName))

        # Install filter
        self.installEventFilter(self)

    def animate_window_size(self, start=(300,400),end=(500,300),duration=800):
        pass
        #animation.resizeWindowAnimation(start=start, end=end, duration=800, object=self.window(),attribute="size")

class attribute_holder(QtWidgets.QWidget):
    '''Holds a pymel object and extract its attributes in a list. Multiple let you choose multiple attributes.'''
    def __init__(self, parent=None):
        super(attribute_holder, self).__init__(parent)

        item_list = []
        self.value = {"object":None, "attributes":[]}
        self.multiple_mode = True

        # Create communication slot
        self.emitter = communicate(self)

        # Load Global Stylesheet
        stylesheet_path = relativePath + "stylesheets" + os.sep + "context_maya.css"
        with open(stylesheet_path, "r") as sheet:
            self.setStyleSheet(sheet.read())

        # Main value-button
        self.select_button = valueButton()
        self.select_button.multiple = False
        self.select_button.set_text("Add From Selected")
        item_list.append(self.select_button)
        self.select_button.setObjectName("pymel_select_button")
        self.select_button.clicked.connect(self.update_attributes)
        self.select_button.emitter.value.connect(self.update_attributes)

        # Create drop-down holder
        self.attribute_button = floating_combobox_multiple(self)
        item_list.append(self.attribute_button)
        self.attribute_button.setHidden(True)
        self.attribute_button.emitter.value.connect(self.update_value)

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

    def set_multiple(self, value):
        self.multiple_mode = value
        self.select_button.multiple = value

    def update_attributes(self):
        # Get object
        button_value = self.select_button.get_value(static=True)
        if button_value != None:
            node_type = pm.nodeType(button_value)
            classifications = pm.getClassification(node_type)[-1]
            if node_type == "blendShape":
                attributes = pm.listAttr(str(button_value[0]) + ".w", m=True)
            elif "utility" in classifications:
                input_attr = pm.listAttr(button_value, keyable=True, visible=True, locked=False)
                output_attr = pm.listAttr(button_value, output=True, readOnly=True)
                attributes = input_attr + output_attr
            else:
                attributes = pm.listAttr(button_value, keyable=True, visible=True, locked=False, shortNames=True)
            self.attribute_button.set_options(attributes)
            self.attribute_button.setHidden(False)
            self.value["object"] = button_value
        else:
            self.attribute_button.setHidden(True)
            self.value["object"] = None
            self.value["attributes"] = ()
        self.emitter.value.emit(1)

    def get_value(self):
        return self.value

    def update_value(self):
        self.value = {"object": self.select_button.get_value(static=True), "attributes": self.attribute_button.get_value()}
        self.emitter.value.emit(1)

    def set_value(self, object=None, attributes=[]):
        self.value = {"object":object, "attributes":attributes}

        # Set value on buttons
        if object != None:
            self.select_button.set_value(object)

        # Set attributes
        if len(attributes) >= 1:
            self.attribute_button.set_value(attributes)

        self.update_attributes()





class pymel_holder(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(pymel_holder, self).__init__(parent)

        item_list = []
        self.value = None
        self.multiple_mode = True

        # Create communication slot
        self.emitter = communicate(self)

        # Load Global Stylesheet
        stylesheet_path = relativePath + "stylesheets" + os.sep + "context_maya.css"
        with open(stylesheet_path, "r") as sheet:
            self.setStyleSheet(sheet.read())

        self.select_button = valueButton()
        self.select_button.set_text("Add From Selected")
        item_list.append(self.select_button)
        self.select_button.setObjectName("pymel_select_button")
        self.select_button.clicked.connect(self.add_from_button)
        self.select_button.emitter.value.connect(self.add_from_button)

        self.expand_button = fadeButton(self)
        svg_icon(button=self.expand_button, path=relativePath + os.sep + "icons" + os.sep + "threeLines.svg")
        self.expand_button.clicked.connect(self.toggle_view)

        self.reset_all_button = fadeButton(self)
        svg_icon(button=self.reset_all_button,path=relativePath + os.sep + "icons" + os.sep + "crossIcon.svg")
        self.reset_all_button.clicked.connect(self.reset_all_values)

        # Add properties to buttons
        for button in [self.expand_button, self.reset_all_button]:
            button.setMaximumWidth(20)
            button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
            button.setMaximumWidth(10)
            item_list.append(button)

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
        self.expand_button.setHidden(True)
        self.reset_all_button.setHidden(True)

        # Set main layout
        self.setLayout(self.topLayout)

    def set_multiple(self, value):
        self.multiple_mode = value
        self.select_button.multiple = value

    def toggle_view(self):
        widget = self.holder_frame
        if self.holder_frame.isHidden() is False:
            animateWidgetSize(widget, start=(widget.size().width(), widget.size().height()),
                              end=(widget.size().width(), 0), expanding=False, duration=50, bounce=True,
                              finishAction=lambda: widget.setHidden(True))
        else:
            widget.setHidden(False)
            animateWidgetSize(widget, start=(widget.size().width(), 0),
                                     end=(widget.size().width(), widget.sizeHint().height()),
                                     expanding=True, duration=50, bounce=False)


    def reset_all_values(self):
        self.value = None
        self.select_button.reset_value()
        self.toggle_buttons()

        if self.holder_frame.isHidden() is False:
            self.toggle_view()

        # Emit update connection
        self.emitter.value.emit(1)

    def toggle_buttons(self):
        buttons = [self.reset_all_button, self.expand_button]

        if self.value is not None:
            for button in buttons:
                width = button.sizeHint().width()
                height = button.sizeHint().height()
                if button.isHidden():
                    button.setHidden(False)
                    animateWidgetSize(button, start=(0, height), end=(width, height), duration=500,attributelist=("maximumSize", "minimumSize"), bounce=False, expanding=True)

        else:
            for button in buttons:
                width = button.sizeHint().width()
                height = button.size().height()
                if button.isHidden() is False:
                    animateWidgetSize(button, start=(width, height), end=(0, height), duration=500,attributelist=("maximumSize", "minimumSize"), expanding=True, bounce=False, finishAction = lambda: [b.setHidden(True) for b in buttons])
    def add_from_button(self):
        button_value = self.select_button.get_value(static=True)

        if button_value is not None:
            if len(button_value) is not 0:
                self.set_value(button_value)

            self.toggle_buttons()
            self.add_layout_items()
        else:
            self.value = []

        # Emit update connection
        self.emitter.value.emit(1)

    def add_layout_items(self):
        # Clear layout
        main.clearLayout(self.holder_frame.layout())
        # Create layout
        for item in self.value:
            widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout()
            layout.setSpacing(3)
            layout.setContentsMargins(0,0, 0, 0)
            widget.setLayout(layout)
            widget.setMaximumHeight(20)
            self.holder_frame.layout().addWidget(widget)

            # Remove button
            remove_button = fadeButton(self)
            svg_icon(button=remove_button, path=relativePath + os.sep + "icons" + os.sep + "crossIcon.svg")
            remove_button.setMaximumWidth(20)
            remove_button.setMinimumWidth(20)
            remove_button.object = item
            remove_button.widget = widget
            remove_button.clicked.connect(self.remove_item)
            remove_button.setMinimumWidth(20)
            layout.addWidget(remove_button)

            label = QtWidgets.QLabel(item)
            layout.addWidget(label)

        self.add_more_button = QtWidgets.QPushButton("Add more")
        self.holder_frame.layout().addWidget(self.add_more_button)
        self.add_more_button.setObjectName("pymel_select_button")
        self.add_more_button.clicked.connect(self.add_more)



    def remove_item(self):
        sender = self.sender()
        sender.widget.setHidden(True)

        # Remove from local value
        self.value.remove(sender.object)

        # Emit update connection
        self.emitter.value.emit(1)

    def add_more(self):
        '''Add the current selection to the list'''

        selection = pm.ls(sl=True)
        if len(selection) >= 1:
            for object in selection:
                valueName = object.name()
                self.value.append(valueName)
        else:
            print "No selection to add from"

        # Update interface
        self.set_value(self.value, animate=False)

        # Emit update connection
        self.emitter.value.emit(1)

    def get_value(self):
        return self.value

    def set_value(self, in_value, animate=False):

        # Convert item to list if not by default
        if type(in_value) == list or type(in_value) == tuple:
            pass
        else:
            value = [in_value]

        # Make sure its a string
        for item in in_value:
            if "pymel" in type(item).__module__:
                print "pymel_holder: ERROR, you are trying to feed me a pymel object instead of a string input"
                break

        # Sanity to see that all of the objects exists
        # if None not in out_value:

        # Set value in button
        self.select_button.set_value(in_value, animate=animate)
        self.value = in_value

        self.toggle_buttons()
        self.add_layout_items()



class dict_holder(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(dict_holder, self).__init__(parent)
        item_list = []
        self.value = None
        self.multiple_mode = True

        # Create communication slot
        self.emitter = communicate(self)


        # Load Global Stylesheet
        stylesheet_path = relativePath + "stylesheets" + os.sep + "context_maya.css"
        with open(stylesheet_path, "r") as sheet:
            self.setStyleSheet(sheet.read())

        # Remove button
        self.remove_button = QtWidgets.QPushButton("Remove")
        item_list.append(self.remove_button)
        self.remove_button.setObjectName("small_button")
        self.remove_button.clicked.connect(self.remove_item)
        self.remove_button.setHidden(True)

        # Insert button
        self.insert_button = QtWidgets.QPushButton("Insert")
        item_list.append(self.insert_button)
        self.insert_button.setObjectName("small_button")
        self.insert_button.clicked.connect(self.insert_item)
        self.insert_button.setHidden(True)

        # Duplicate button
        self.dup_button = QtWidgets.QPushButton("Duplicate")
        item_list.append(self.dup_button)
        self.dup_button.setObjectName("small_button")
        self.dup_button.clicked.connect(self.duplicate_item)
        self.dup_button.setHidden(True)


        # Main add item button
        self.add_button = QtWidgets.QPushButton("+ Add Item")
        item_list.append(self.add_button)
        self.add_button.setObjectName("small_button")
        self.add_button.clicked.connect(self.add_item)

        # Create layout
        self.topLayout = QtWidgets.QVBoxLayout()
        self.topLayout.setContentsMargins(5, 0, 5, 0)
        self.topLayout.setSpacing(5)
        self.topLayout.setAlignment(QtCore.Qt.AlignTop)

        # Create main widget
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(3)
        layout.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        layout.setContentsMargins(0,0, 0, 0)
        widget.setLayout(layout)
        widget.setMinimumHeight(20)
        widget.setMaximumHeight(20)
        self.topLayout.addWidget(widget)

        spacer = main.create_spacer(mode="vertical")
        layout.addItem(spacer)

        # Add items to layout
        main.add_items_to_layout(layout, item_list)

        # Create table
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.itemSelectionChanged.connect(self.update_buttons)
        self.tableWidget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().setMinimumSectionSize(30)
        self.tableWidget.setCornerWidget(None)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.currentCellChanged.connect(self.update_values)
        self.tableWidget.setTabKeyNavigation(False)
        self.topLayout.addWidget(self.tableWidget)

        # Set main layout
        self.setLayout(self.topLayout)

        self.rows = None

    def dropEvent(self, event):
        self.emitter.value.emit(1)

    def add_item(self):
        '''Add a empty value from the button'''

        if self.value is not None:
            item = {key.title: None for key in self.rows}
            self.value.append(item)

        self.add_layout_items()

        # Emit signal so other uis connected to this will get updated
        self.emitter.value.emit(1)

    def insert_item(self):
        '''Insert an item after the selected one'''

        # Get current index
        selected_index = self.tableWidget.currentRow()
        print selected_index
        if self.value is not None:
            item = {key.title: None for key in self.rows}
            self.value.insert(selected_index + 1, item)

        self.add_layout_items()

        # Emit signal so other uis connected to this will get updated
        self.emitter.value.emit(1)

    def duplicate_item(self):
        '''Duplicate an item after the selected one'''

        # Get current index
        selected_index = self.tableWidget.currentRow()
        if self.value is not None:
            item = self.value[selected_index]
            print "ITEM:", item
            self.value.insert(selected_index + 1, item)

        self.add_layout_items()

        # Emit signal so other uis connected to this will get updated
        self.emitter.value.emit(1)

    def set_value(self, in_value, animate=True):

        self.value = in_value

        self.add_layout_items()

    def remove_item(self):
        '''Remove a item from the list'''

        selected_index = self.tableWidget.currentRow()

        # Remove value
        del self.value[selected_index]

        self.tableWidget.removeRow(selected_index)

        # Trigger update
        self.emitter.value.emit(1)

    def get_values(self):
        data = []
        type_list = [x.type for x in self.rows]
        for index in range(self.tableWidget.rowCount()):
            values = []

            for row in xrange(len(self.rows)):
                item = self.tableWidget.cellWidget(index, row)
                # Get value from item
                value = main.get_value(item, static=True)

                values.append(value)

            # Combind values with titles
            title_list = [x.title for x in self.rows]

            dictionary = dict(zip(title_list, values))

            data.append(dictionary)

        return data

    def update_buttons(self):
        '''Show remove button if selected item'''
        # Show delete button if rows are selected
        selected = self.tableWidget.currentRow()
        if selected is not -1:
            self.remove_button.setHidden(False)
            self.insert_button.setHidden(False)
            self.dup_button.setHidden(False)
        else:
            self.remove_button.setHidden(True)
            self.insert_button.setHidden(True)
            self.dup_button.setHidden(True)

    def update_values(self):
        '''Update the values when value change'''

        self.value = self.get_values()

        # Emit signal so other uis connected to this will get updated
        self.emitter.value.emit(1)

    def update_layout(self):
        vertHeader = self.tableWidget.verticalHeader()
        horHeader = self.tableWidget.horizontalHeader()

        margin = self.tableWidget.getContentsMargins()
        height_sum = (vertHeader.length() + margin[0]) + horHeader.height() + margin[0]
        self.tableWidget.setMaximumHeight(height_sum)
        self.tableWidget.setMinimumHeight(height_sum)

        self.tableWidget.resizeRowsToContents()
    def add_layout_items(self):
        '''Add items to the object based on current data'''
        print "context_maya.add_layout_items"
        if self.rows is None:
            pass
        else:
            title_list = [x.title for x in self.rows]
            options_list = [x.options for x in self.rows]
            defaultValue_list = [x.defaultValue for x in self.rows]
            multiple_list = [x.multiple for x in self.rows]
            type_list = [x.type for x in self.rows]

            item_value_list = [[item[title] for title in title_list] for item in self.value]

            self.tableWidget.setColumnCount(len(title_list))
            self.tableWidget.setHorizontalHeaderLabels(title_list)
            horHeader = self.tableWidget.horizontalHeader()
            horHeader.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            horHeader.setCascadingSectionResizes(True)

            # Disable updates
            self.tableWidget.setUpdatesEnabled(False)
            self.tableWidget.blockSignals(True)

            # Load data
            self.tableWidget.setRowCount(len(item_value_list))
            row_widgets = []
            for index, value in enumerate(item_value_list):
                # For every header
                widgets = []
                for row, type in enumerate(type_list):
                    # Create item holder
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(index, row, item)
                    # Create based on type
                    if type == "str":
                        widget = QtWidgets.QLineEdit("")
                        widget.setText("Undefined")
                        if defaultValue_list[row] is not None:
                            widget.setText(defaultValue_list[row])
                    elif type == "float":
                        widget =  QtWidgets.QDoubleSpinBox()
                        widget.setMaximum(99999)
                        widget.setMinimum(-99999)
                        widget.setSingleStep(0.01)
                        widget.setDecimals(3)
                    elif type == "int":
                        widget = QtWidgets.QSpinBox()
                        widget.setMaximum(99999)
                        widget.setMinimum(-99999)
                    elif type == "selectSingle":
                        widget = QtWidgets.QComboBox()
                        # Add options
                        widget.addItems([str(option) for option in options_list[row]])
                        if defaultValue_list[row] is not None:
                            widget.setCurrentText(defaultValue_list[row])
                    elif type == "selectMultiple":
                        widget = combobox_multiple()
                        widget.emitter.value.connect(self.update_layout)
                        widget.set_options(options_list[row])
                        if defaultValue_list[row] is not None:
                            widget.set_value(defaultValue_list[row], animate=False)
                    elif type == "bool":
                        widget = QtWidgets.QCheckBox()
                        if defaultValue_list[row] is not None:
                            widget.setChecked(defaultValue_list[row])
                        # Add in labels for on/off using the options list
                        #widget.setText(options_list[row][1])
                    elif type == "vector":
                        widget = main.vectorInput()
                    elif type == "color":
                        widget = main.colorInput()
                    elif type == "objectSingle":
                        widget = valueButton()
                        widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
                        widget.multiple = False
                        widget.set_text("Add Object")
                    elif type == "objectAttribute":
                        widget = attribute_holder()
                        widget.emitter.value.connect(self.update_layout)
                        widget.emitter.value.connect(self.update_values)
                        print "Multiple:", multiple_list[row]
                        widget.set_multiple(multiple_list[row])
                        #multiple_list
                    elif type == "objectMultiple":
                        widget = valueButton()
                        widget.set_text("Add Object(s)")
                    else:
                        print "Type not supported"
                        widget = QtWidgets.QPushButton("?")
                    # Add to table
                    self.tableWidget.setCellWidget(index, row, widget)
                    widgets.append(widget)

                    # Set value from data
                    if value[row] is not None:
                        main.set_value(widget, value[row])

                    # Set update
                    main.connect_value_change(widget, connection=(self.update_values))

                row_widgets.append(widgets)

            # Disable updates
            self.tableWidget.setUpdatesEnabled(True)
            self.tableWidget.blockSignals(False)

            self.update_layout()

            # Set tab behavior by row instead of column
            if len(row_widgets) >= 2:
                for item in zip(*row_widgets):
                    for number, x in enumerate(item):
                        self.tableWidget.setTabOrder(item[number - 1], x)  # c to d



class communicate(Qt.QtCore.QObject):
    '''Create a new signal that other Uis can pick up from'''
    value = Qt.QtCore.Signal(int)

