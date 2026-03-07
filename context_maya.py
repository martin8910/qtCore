from __future__ import print_function
# -*- coding: utf-8 -*-

import os, sys
from maya import OpenMayaUI
import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQDockWidget
import pymel.core as pm

from .external.Qt import QtWidgets, QtCore, QtCompat, QtGui, Qt
from . import main, icon
from .animation import animateWidgetSize, resizeWindowAnimation
from .button import valueButton, fadeButton
from .icon import svg_icon
from .dialog import inputDialog


if sys.version_info >= (3, ):
    # Python 3 compatibility
    long = int

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
        self.add_options = False

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
        self.expand_button.setText("Select values")
        #self.expand_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        #self.expand_button.setIconSize(QtCore.QSize(10, 10))
        #svg_icon(button=self.expand_button, path=relativePath + os.sep + "icons" + os.sep + "tab_closed.svg")
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

        if self.add_options:
            # Add option to add your own value or not
            add_action = QtWidgets.QAction(self)
            add_action.setText("+ Add New")
            self.menu.addAction(add_action)
            add_action.triggered.connect(self.add_item_popup)


    def add_item_popup(self):
        print("Add input dialog")
        add_name = inputDialog(self, header="Add Item", text="New item")
        if add_name is not None:
            self.options.append(add_name)
        self.update_values()




    def update_values(self):
        sender = self.sender()
        # Reset value

        list = []
        for action in self.actions:
            if action.isChecked():
                list.append(action.text())

        self.set_value(list, animate=True)

        # Show the menu again to get multiple selections
        self.menu.exec_()

        # Emit update connection
        self.emitter.value.emit(1)

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
            valueName = "[ None ]"

        self.expand_button.setText(valueName)
        self.value = value

        if self.options is not None:
            self.add_layout_items()






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

#


def get_window():
    '''Return the main maya-window as an instance to parent to'''
    window = OpenMayaUI.MQtUtil.mainWindow()
    #mayaWindow = shiboken.wrapInstance( long( window ), QtWidgets.QMainWindow)
    mayaWindow = shiboken.wrapInstance(long(OpenMayaUI.MQtUtil.mainWindow()), QtWidgets.QMainWindow)
    return mayaWindow

# def get_window():
#     '''Return the main maya-window as an instance to parent to'''
#     mayaWindow = getMayaWindow()
#     if not mayaWindow:
#         return None
#     mainWindowPtr = OpenMayaUI.MQtUtil.mainWindow()
#     mainWindow = wrapInstance(long(mainWindowPtr), QtWidgets.QMainWindow)
#     return mainWindow

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
        resizeWindowAnimation(start=start, end=end, duration=800, object=self.window(),attribute="size")


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

class attribute_holder(QtWidgets.QWidget):
    '''Holds a pymel object and extract its attributes in a list. Multiple let you choose multiple attributes.'''
    def __init__(self, parent=None):
        super(attribute_holder, self).__init__(parent)

        item_list = []
        self.value = {"object":None, "attributes":[]}
        self.multiple_mode = True
        self.only_keyable = True

        # Create communication slot
        self.emitter = communicate(self)

        # Load Global Stylesheet
        stylesheet_path = relativePath + "stylesheets" + os.sep + "context_maya.css"
        with open(stylesheet_path, "r") as sheet:
            self.setStyleSheet(sheet.read())

        # Main value-button
        self.select_button = valueButton()
        self.select_button.multiple = False
        self.select_button.set_text("  +  ")
        item_list.append(self.select_button)
        self.select_button.setObjectName("pymel_select_button")
        self.select_button.clicked.connect(self.update_attributes)
        self.select_button.emitter.value.connect(self.update_attributes)
        #self.select_button.setMaximumWidth(20)

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
            all_attributes = []
            attribute_lists = []

            existing_geo = [x for x in button_value if pm.objExists(x)]
            missing_geo = list(set(button_value) - set(existing_geo))
            for x in existing_geo:
                node_type = pm.nodeType(x)
                classifications = pm.getClassification(node_type)[-1]
                if node_type == "blendShape":
                    attribute_lists.append(pm.listAttr(str(x) + ".w", m=True))
                elif "utility" in classifications:
                    input_attr = pm.listAttr(x, keyable=True, visible=True, locked=False)
                    output_attr = pm.listAttr(x, output=True, readOnly=True)
                    attribute_lists.append(input_attr + output_attr)
                elif "deformer" in classifications:
                    input_attr = pm.listAttr(x, keyable=True, visible=True, locked=False)
                    output_attr = pm.listAttr(x, output=True, readOnly=True)
                    attribute_lists.append(input_attr + output_attr)
                else:
                    attribute_lists.append(pm.listAttr(x, keyable=True, visible=True, locked=False, shortNames=False))

            #Sort and filter out only attributes existing in all controllers
            unice_attributes = set([x for y in attribute_lists for x in y])
            common_attributes = [x for x in unice_attributes if all(x in list for list in attribute_lists) == True]
            self.attribute_button.set_options(sorted(common_attributes))
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
        self.select_button.set_text("  +  ")
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

        buttons = [self.reset_all_button, self.expand_button]
        for button in buttons:
            button.setMinimumSize(button.sizeHint().width(), button.sizeHint().width())



        # Set main layout
        self.setLayout(self.topLayout)

    def set_multiple(self, value):
        self.multiple_mode = value
        self.select_button.multiple = value

    def toggle_view(self):
        widget = self.holder_frame
        if self.holder_frame.isHidden() is False:
            animateWidgetSize(widget, start=(widget.size().width(), widget.size().height()),
                              end=(widget.size().width(), 0), expanding=False, duration=10, bounce=True,
                              finishAction=lambda: widget.setHidden(True))
        else:
            widget.setHidden(False)
            animateWidgetSize(widget, start=(widget.size().width(), 0),
                                     end=(widget.size().width(), widget.sizeHint().height()),
                                     expanding=True, duration=10, bounce=False)


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
                    #animateWidgetSize(button, start=(0, height), end=(width, height), duration=0,attributelist=("maximumSize", "minimumSize"), bounce=False, expanding=True)

        else:
            for button in buttons:
                width = button.sizeHint().width()
                height = button.size().height()
                button.setHidden(True)
                #if button.isHidden() is False:
                    #animateWidgetSize(button, start=(width, height), end=(0, height), duration=0,attributelist=("maximumSize", "minimumSize"), expanding=True, bounce=False, finishAction = lambda: [b.setHidden(True) for b in buttons])
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
            print("No selection to add from")

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
                print("pymel_holder: ERROR, you are trying to feed me a pymel object instead of a string input")
                break

        # Sanity to see that all of the objects exists
        # if None not in out_value:

        # Set value in button
        self.select_button.set_value(in_value, animate=animate)
        self.value = in_value

        self.toggle_buttons()
        self.add_layout_items()



import os, copy
from Qt import QtCore, QtWidgets

class dict_holder(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(dict_holder, self).__init__(parent)

        # --- data ---
        self.value = []                 # committed data (only after Save)
        self._working_rows = []         # live UI data (unsaved)
        self._dirty = False             # unsaved changes?
        self._building = False          # guard while rebuilding UI
        self.multiple_mode = True
        self.rows = None                # column schema

        # --- comms ---
        self.emitter = communicate(self)

        # --- style (keep yours if you had one) ---
        stylesheet_path = relativePath + "stylesheets" + os.sep + "context_maya.css"
        if os.path.exists(stylesheet_path):
            with open(stylesheet_path, "r") as sheet:
                self.setStyleSheet(sheet.read())

        # --- header controls ---
        self.title = QtWidgets.QLabel("Dict Holder")
        self.title.setStyleSheet("color: rgb(250,250,250);")

        self.save_button = QtWidgets.QPushButton("💾 Save Changes")
        self.save_button.setObjectName("small_button")
        self.save_button.clicked.connect(self.save_changes)
        self.save_button.setEnabled(False)

        self.status_label = QtWidgets.QLabel("All changes saved")
        self.status_label.setStyleSheet("color: rgb(120,200,120);")

        self.remove_button = QtWidgets.QPushButton("❌ Remove")
        self.remove_button.setObjectName("small_button")
        self.remove_button.clicked.connect(self.remove_item)
        self.remove_button.setHidden(True)

        self.insert_button = QtWidgets.QPushButton("Insert")
        self.insert_button.setObjectName("small_button")
        self.insert_button.clicked.connect(self.insert_item)
        self.insert_button.setHidden(True)

        self.dup_button = QtWidgets.QPushButton("Duplicate")
        self.dup_button.setObjectName("small_button")
        self.dup_button.clicked.connect(self.duplicate_item)
        self.dup_button.setHidden(True)

        self.add_button = QtWidgets.QPushButton("➕ Add Item")
        self.add_button.setObjectName("small_button")
        self.add_button.clicked.connect(self.add_item)

        # --- header layout ---
        header = QtWidgets.QWidget()
        h = QtWidgets.QHBoxLayout(header)
        h.setContentsMargins(2, 2, 2, 2)
        h.setSpacing(6)
        h.addWidget(self.title)
        h.addStretch(1)
        h.addWidget(self.status_label)
        h.addWidget(self.save_button)
        h.addSpacing(8)
        h.addWidget(self.remove_button)
        h.addWidget(self.insert_button)
        h.addWidget(self.dup_button)
        h.addWidget(self.add_button)

        # --- table ---
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.verticalHeader().setMinimumSectionSize(30)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setStyleSheet("selection-background-color: rgba(250,250,250,10)")
        self.tableWidget.itemSelectionChanged.connect(self._update_row_buttons)

        # Enable moving rows by dragging the header (doesn’t auto-save)
        vh = self.tableWidget.verticalHeader()
        vh.setSectionsMovable(True)
        vh.sectionMoved.connect(self._on_row_reordered)

        # --- top layout ---
        self.topLayout = QtWidgets.QVBoxLayout(self)
        self.topLayout.setContentsMargins(5, 0, 5, 0)
        self.topLayout.setSpacing(5)
        self.topLayout.addWidget(header)
        self.topLayout.addWidget(self.tableWidget)

    # ------------------ public API ------------------

    def set_title(self, title):
        self.title.setText(title)

    def set_value(self, in_value, animate=True):
        """Load committed data and reset working copy + UI."""
        self.value = copy.deepcopy(in_value or [])
        self._working_rows = copy.deepcopy(self.value)
        self._set_dirty(False)
        self.add_layout_items()

    # ------------------ save / dirty ------------------

    def save_changes(self):
        """Commit the table into self.value and broadcast."""
        self._squash_working_from_table()
        self.value = copy.deepcopy(self._working_rows)
        self._set_dirty(False)
        self.emitter.value.emit(1)

    def _mark_dirty(self, *args, **kwargs):
        if self._building:
            return
        self._set_dirty(True)

    def _set_dirty(self, dirty):
        self._dirty = bool(dirty)
        if self._dirty:
            self.status_label.setText("Unsaved changes")
            self.status_label.setStyleSheet("color: rgb(255,200,0);")
            self.save_button.setEnabled(True)
        else:
            self.status_label.setText("All changes saved")
            self.status_label.setStyleSheet("color: rgb(120,200,120);")
            self.save_button.setEnabled(False)

    # ------------------ row operations (work on working copy) ------------------

    def add_item(self):
        if self.rows is None:
            return
        self._squash_working_from_table()
        new_item = {key.title: None for key in self.rows}
        self._working_rows.append(new_item)
        self._set_dirty(True)
        self.add_layout_items()

    def insert_item(self):
        if self.rows is None or self.tableWidget.rowCount() == 0:
            return
        self._squash_working_from_table()
        lr = self.tableWidget.currentRow()
        if lr < 0:
            return
        vr = self.tableWidget.verticalHeader().visualIndex(lr)
        item = {key.title: None for key in self.rows}
        self._working_rows.insert(vr + 1, item)
        self._set_dirty(True)
        self.add_layout_items()

    def duplicate_item(self):
        if self.rows is None or self.tableWidget.rowCount() == 0:
            return
        self._squash_working_from_table()
        lr = self.tableWidget.currentRow()
        if lr < 0:
            return
        vr = self.tableWidget.verticalHeader().visualIndex(lr)
        if 0 <= vr < len(self._working_rows):
            self._working_rows.insert(vr + 1, copy.deepcopy(self._working_rows[vr]))
            self._set_dirty(True)
            self.add_layout_items()

    def remove_item(self):
        if self.tableWidget.rowCount() == 0:
            return
        self._squash_working_from_table()
        lr = self.tableWidget.currentRow()
        if lr < 0:
            return
        vr = self.tableWidget.verticalHeader().visualIndex(lr)
        if 0 <= vr < len(self._working_rows):
            del self._working_rows[vr]
            self._set_dirty(True)
            self.add_layout_items()

    # ------------------ table <-> data helpers ------------------

    def _on_row_reordered(self, logical, oldVisual, newVisual):
        """Dragging a row doesn’t save; it only marks dirty and updates working order."""
        self._squash_working_from_table()  # reflect the new visual order
        self._set_dirty(True)

    def _squash_working_from_table(self):
        """Read the table (visual order) into the working copy."""
        self._working_rows = self.get_values()

    def get_values(self):
        """Read values from the table in visual (on-screen) order."""
        data = []
        if not self.rows:
            return data

        title_list = [x.title for x in self.rows]
        vh = self.tableWidget.verticalHeader()
        rc = self.tableWidget.rowCount()

        for v in range(rc):
            lr = vh.logicalIndex(v)  # map visual -> logical
            row_vals = []
            for c in range(len(self.rows)):
                widget = self.tableWidget.cellWidget(lr, c)
                row_vals.append(main.get_value(widget, static=True) if widget is not None else None)
            data.append(dict(zip(title_list, row_vals)))
        return data

    # ------------------ UI plumbing ------------------

    def _update_row_buttons(self):
        has_sel = self.tableWidget.currentRow() != -1
        self.remove_button.setHidden(not has_sel)
        self.insert_button.setHidden(not has_sel)
        self.dup_button.setHidden(not has_sel)

    def update_layout(self):
        """Keep this cheap; no column autosize here."""
        vertHeader = self.tableWidget.verticalHeader()
        horHeader  = self.tableWidget.horizontalHeader()
        m = self.tableWidget.getContentsMargins()
        height_sum = (vertHeader.length() + m[0]) + horHeader.height() + m[0]
        self.tableWidget.setMaximumHeight(height_sum)
        self.tableWidget.setMinimumHeight(height_sum)

    # ------------------ build table from working copy ------------------

    def _purge_table_widgets(self):
        # Remove and delete any existing cell widgets
        rows = self.tableWidget.rowCount()
        cols = self.tableWidget.columnCount()
        for r in range(rows):
            for c in range(cols):
                w = self.tableWidget.cellWidget(r, c)
                if w is not None:
                    self.tableWidget.removeCellWidget(r, c)
                    w.deleteLater()
        # Clear items/headers after widgets are gone
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)

    def add_layout_items(self):
        if self.rows is None:
            return

        title_list    = [x.title        for x in self.rows]
        options_list  = [x.options      for x in self.rows]
        default_list  = [x.defaultValue for x in self.rows]
        multiple_list = [x.multiple     for x in self.rows]
        type_list     = [x.type         for x in self.rows]

        # Ensure working rows exist (mirror committed if empty)
        if self._working_rows is None:
            self._working_rows = copy.deepcopy(self.value or [])

        item_value_list = [[item.get(t) for t in title_list] for item in (self._working_rows or [])]

        vh = self.tableWidget.verticalHeader()


        self._building = True
        self.tableWidget.setUpdatesEnabled(False)
        self.tableWidget.blockSignals(True)
        vh.blockSignals(True)

        self._purge_table_widgets()

        self.tableWidget.setColumnCount(len(title_list))
        self.tableWidget.setHorizontalHeaderLabels(title_list)
        self.tableWidget.setRowCount(len(item_value_list))


        self.tableWidget.setColumnCount(len(title_list))
        self.tableWidget.setHorizontalHeaderLabels(title_list)
        self.tableWidget.setRowCount(len(item_value_list))

        widget_classes = {
            "str": QtWidgets.QLineEdit,
            "float": QtWidgets.QDoubleSpinBox,
            "int": QtWidgets.QSpinBox,
            "selectSingle": QtWidgets.QComboBox,
            "selectMultiple": floating_combobox_multiple,
            "bool": QtWidgets.QCheckBox,
            "vector": main.vectorInput,
            "color": main.colorInput,
            "objectSingle": valueButton,
            "objectAttribute": attribute_holder,
            "objectMultiple": valueButton,
        }

        for r, row_vals in enumerate(item_value_list):
            for c, typ in enumerate(type_list):
                cls = widget_classes.get(typ)
                if not cls:
                    continue
                w = cls()

                # Defaults / setup
                if typ == "str":
                    w.setStyleSheet("selection-background-color: rgba(0,250,250,150)")
                    if default_list[c] is not None:
                        w.setText(default_list[c])
                elif typ == "float":
                    w.setMaximum(99999); w.setMinimum(-99999)
                    w.setSingleStep(0.01); w.setDecimals(3)
                    if default_list[c] is not None:
                        w.setValue(default_list[c])
                elif typ == "int":
                    w.setMaximum(99999); w.setMinimum(-99999)
                    if default_list[c] is not None:
                        w.setValue(default_list[c])
                elif typ == "selectSingle":
                    w.addItems([str(o) for o in options_list[c]])
                    if default_list[c] is not None:
                        w.setCurrentText(default_list[c])
                elif typ == "selectMultiple":
                    w.set_options(options_list[c])
                elif typ == "bool":
                    if default_list[c] is not None:
                        w.setChecked(default_list[c])
                elif typ == "objectSingle":
                    w.multiple = False
                    w.set_text("Add Object")
                elif typ == "objectAttribute":
                    w.set_multiple(multiple_list[c])
                elif typ == "objectMultiple":
                    w.set_text("Add Object(s)")

                # Place cell
                self.tableWidget.setItem(r, c, QtWidgets.QTableWidgetItem())
                self.tableWidget.setCellWidget(r, c, w)

                # Apply current working value (if present)
                if c < len(row_vals) and row_vals[c] is not None:
                    main.set_value(w, row_vals[c])

                # Wire signals: edits mark dirty (no autosave),
                # some widgets also ping layout sizing
                if typ == "selectMultiple":
                    w.emitter.value.connect(self._mark_dirty)
                    w.menu.triggered.connect(self.update_layout)
                elif typ == "objectAttribute":
                    w.emitter.value.connect(self._mark_dirty)
                    w.emitter.value.connect(self.update_layout)

                # Generic value change → dirty
                main.connect_value_change(w, connection=self._mark_dirty)

        # Do heavy sizing ONCE here (not per keystroke)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.update_layout()

        # Re-enable
        vh.setSectionsMovable(True)
        vh.blockSignals(False)
        self.tableWidget.blockSignals(False)
        self.tableWidget.setUpdatesEnabled(True)
        self._building = False




class communicate(Qt.QtCore.QObject):
    '''Create a new signal that other Uis can pick up from'''
    value = Qt.QtCore.Signal(int)

