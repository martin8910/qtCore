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

def pixmap_on_icon(icon, path):
    '''Load a pixmap icon from a path'''
    if type(icon) == QtWidgets.QPushButton:

        # QPixmap pixmap(imageFileName);
        pixmap = QtGui.QPixmap(path)

        # if (pixmap.isNull()) return false;
        #
        # int w = std::min(pixmap.width(),  label->maximumWidth());
        # int h = std::min(pixmap.height(), label->maximumHeight());

        width_factor = pixmap.width() / icon.size().width()
        height_factor = pixmap.height() / icon.size().height()
        print pixmap.width(), pixmap.height()
        print icon.size().width(), icon.size().height()
        print "--------"

        #
        #

        # pixmap = pixmap.scaled(QSize(w, h), Qt::KeepAspectRatio, Qt::SmoothTransformation);
        #pixmap.scaled(QtCore.QSize(icon.size().width(), icon.size().height()), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        #pixmap.scaled(QtCore.QSize(icon.size().width(), icon.size().height()), QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
        #QtCore.QSize(icon.size().width(), icon.size().height())

        #pixmap.scaled(640, 440, QtCore.Qt.KeepAspectRatio)
        pixmap.scaled(640, 440)

        # label->setPixmap(pixmap);
        icon.setIcon(pixmap)







        #pixmap.scaledToHeight(icon.size().width())
        #pixmap.scaledToWidth(icon.size().height())
        #size = QtCore.QSize(icon.size().width(), icon.size().height())
        #icon.setScaledContents(True)
        #pixmap.scaled(size, QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)

        #pixmap.setSize(size)

        #icon.setIcon(pixmap)
    else:
        icon.setPixmap(QtGui.QPixmap(path))



#
# static bool SetLabelImage(QLabel *label, QString imageFileName)
# {
#     QPixmap pixmap(imageFileName);
#     if (pixmap.isNull()) return false;
#
#     int w = std::min(pixmap.width(),  label->maximumWidth());
#     int h = std::min(pixmap.height(), label->maximumHeight());
#     pixmap = pixmap.scaled(QSize(w, h), Qt::KeepAspectRatio, Qt::SmoothTransformation);
#     label->setPixmap(pixmap);
#     return true;
# }