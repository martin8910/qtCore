from __future__ import print_function
# -*- coding: utf-8 -*-

from .external.Qt import QtWidgets, QtCore, QtGui, QtSvg

# Load the svg
def load_svg(iconPath, size=(20,20), assign_rgb=False):
    pixmap = load_svg_pixmap(iconPath, size=size, assign_rgb=assign_rgb)
    icon = QtGui.QIcon(pixmap)
    return icon

def load_svg_pixmap(iconPath, size=(20,20), assign_rgb=False):
    svg_renderer = QtSvg.QSvgRenderer(iconPath)
    image = QtGui.QImage(size[0], size[1], QtGui.QImage.Format_ARGB32_Premultiplied)
    image.fill(0x00000000)
    svg_renderer.render(QtGui.QPainter(image))

    if assign_rgb:
        paint = QtGui.QPainter()
        paint.begin(image)
        paint.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        paint.fillRect(image.rect(), QtGui.QColor(assign_rgb[0], assign_rgb[1], assign_rgb[2]))
        paint.end()

    pixmap = QtGui.QPixmap.fromImage(image)
    return pixmap

def svg_icon(button=None, path=None, assign_rgb=False):
    '''Load a svg icon onto a button respecting its size'''
    button_type = button.__class__.__name__

    if button_type in ["QPushButton", "QToolButton", "fadeButton", "popButton"]:
        size = (button.iconSize().width(), button.iconSize().height())
    elif button_type == "QAction":
        size = (50, 50)
    elif button_type == "QLabel":
        size = (button.width(), button.height())
    else:
        try:
            size = (button.iconSize().width(), button.iconSize().height())
        except AttributeError:
            print("Unsupported type for icon:", button_type)
            size = (50, 50)

    # Create pixmap from path
    svg_pixmap = load_svg_pixmap(path, size=size, assign_rgb=assign_rgb)

    if isinstance(button, (QtWidgets.QPushButton, QtWidgets.QToolButton, QtWidgets.QAction)):
        button.setIcon(QtGui.QIcon(svg_pixmap))
    elif isinstance(button, QtWidgets.QLabel):
        button.setPixmap(svg_pixmap)
    else:
        print("Unsupported type:", type(button))
        try:
            button.setIcon(QtGui.QIcon(svg_pixmap))
            print("Managed to set the size from icon.setIcon()")
        except:
            pass
    return svg_pixmap

def pixmap_on_icon(icon, path):
    '''Load a pixmap icon from a path'''
    if isinstance(icon, QtWidgets.QPushButton):
        pixmap = QtGui.QPixmap(path)
        pixmap = pixmap.scaled(icon.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        icon.setIcon(QtGui.QIcon(pixmap))
    else:
        icon.setPixmap(QtGui.QPixmap(path))