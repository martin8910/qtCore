import os
from maya import OpenMayaUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin, MayaQDockWidget
import pymel.core as pm

from external.Qt import QtWidgets, QtCore
import main
from animation import animateWidgetSize
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


class pymel_holder(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(pymel_holder, self).__init__(parent)

        item_list = []
        self.value = None
        self.multiple_mode = True

        # Load Global Stylesheet
        stylesheet_path = relativePath + "stylesheets" + os.sep + "context_maya.css"
        with open(stylesheet_path, "r") as sheet:
            self.setStyleSheet(sheet.read())

        self.select_button = valueButton()
        self.select_button.set_text("Add From Selected")
        item_list.append(self.select_button)
        self.select_button.setObjectName("pymel_select_button")
        self.select_button.clicked.connect(self.add_from_button)

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
                              end=(widget.size().width(), 0), expanding=False, duration=1000, bounce=True,
                              finishAction=lambda: widget.setHidden(True))
        else:
            widget.setHidden(False)
            animateWidgetSize(widget, start=(widget.size().width(), 0),
                                     end=(widget.size().width(), widget.sizeHint().height()),
                                     expanding=True, duration=1000, bounce=False)




    def reset_all_values(self):
        print "Resetting values"
        self.value = []
        self.select_button.reset_value()
        self.toggle_buttons()

        if self.holder_frame.isHidden() is False:
            self.toggle_view()

    def toggle_buttons(self):
        buttons = [self.reset_all_button, self.expand_button]
        #buttons = [self.expand_button]
        # if self.multiple_mode == False:
        #     print "FOR MULTIPLE"
        #     for button in buttons:
        #         width = button.sizeHint().width()
        #         height = button.sizeHint().height()
        #         if button.isHidden():
        #             button.setHidden(False)
        #             animateWidgetSize(button, start=(0, height), end=(width, height), duration=500,attributelist=("maximumSize", "minimumSize"), bounce=False, expanding=True)
        #
        #     # Hide expand button
        #     if self.expand_button.isHidden() is False:
        #         width = self.expand_button.sizeHint().width()
        #         height = self.expand_button.size().height()
        #         animateWidgetSize(self.expand_button, start=(width, height), end=(0, height), duration=500,
        #                           attributelist=("maximumSize", "minimumSize"), expanding=True, bounce=False,
        #                           finishAction=lambda: self.expand_button.setHidden(True))
        if len(self.value) >= 1:
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
        print "Added from the button"
        button_value = self.select_button.get_value(static=True)

        print "BUTTON-VALUE:", button_value
        if button_value is not None:
            if len(button_value) is not 0:
                self.set_value(button_value)

            self.toggle_buttons()
            self.add_layout_items()
        else:
            self.value = []

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
            widget.setMaximumHeight(30)
            widget.setStyleSheet("background-color: rgb(250,0,0)")
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

        add_more_button = QtWidgets.QPushButton("Add more")
        self.holder_frame.layout().addWidget(add_more_button)
        add_more_button.setObjectName("pymel_select_button")
        #add_more_button.clicked.connect(self.add_more)



    def remove_item(self):
        sender = self.sender()
        sender.widget.setHidden(True)

        # Remove from local value
        self.value.remove(sender.object)

    def get_value(self):
        print "context_MAYA: GETTING VALUE", self.value
        return self.value

    def set_value(self, in_value, animate=True):

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
        # else:
        #     print "WARNING: Items in the scene does not exists:"
        #     for item in in_value:
        #         print item