from external.Qt import QtWidgets, QtCore, QtGui, QtSvg

# Load the svg
def load_svg(iconPath, size=(20,20)):
    pixmap =  load_svg_pixmap(iconPath, size=size)
    icon = QtGui.QIcon(pixmap)

    return icon

def load_svg_pixmap(iconPath, size=(20,20)):
    svg_renderer = QtSvg.QSvgRenderer(iconPath)
    image = QtGui.QImage(size[0], size[1], QtGui.QImage.Format_ARGB32)
    image.fill(0x00000000)
    svg_renderer.render(QtGui.QPainter(image))
    pixmap = QtGui.QPixmap.fromImage(image)

    return pixmap

def svg_icon(button=None, path=None):
    '''Load a svg icon onto a button respecting its size'''
    if type(button) == QtWidgets.QPushButton:
        size = (button.iconSize().width(), button.iconSize().height())
    elif "fadeButton" in str(type(button)) or "popButton" in str(type(button)):
        size = (button.iconSize().width(), button.iconSize().height())
    elif type(button) == QtWidgets.QToolButton:
        size = (button.iconSize().width(), button.iconSize().height())
    elif type(button) == QtWidgets.QLabel:
        size = (button.width(), button.height())
    else:
        print "Unsupported type:", type(button)
        try:
            size = (button.iconSize().width(), button.iconSize().height())
            print "Manage to find the size from iconSize()"
        except: size = None

    # Create pixmap from path
    svg_pixmap = load_svg_pixmap(path, size=(50, 50))

    if type(button) == QtWidgets.QPushButton or "fadeButton" in str(type(button)) or "popButton" in str(type(button)):
        button.setIcon(QtGui.QIcon(svg_pixmap))
    elif type(button) == QtWidgets.QLabel:
        button.setPixmap(svg_pixmap)
    elif type(button) == QtWidgets.QLabel:
        button.setIcon(QtGui.QIcon(svg_pixmap))
    else:
        print "Unsupported type:", type(button)
        try:
            button.setIcon(QtGui.QIcon(svg_pixmap))
            print "Manage to set the size from icon.setIcon()"
        except: pass
    return svg_pixmap