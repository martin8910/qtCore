__author__ = "Martin Gunnarsson"
__email__ = "hello@deerstranger.com"

from external.Qt import QtWidgets, QtCompat, QtCore, QtGui, QtSvg

def get_children_from_treeWidgetItem(treeWidgetItem):
    '''Return all items from a qTreeWidgetItem'''
    items = [treeWidgetItem.child(number) for number in xrange(treeWidgetItem.childCount())]

    return items

def remove_children_from_treeWidgetItem(treeWidgetItem):
    '''Remove all the children from a QTreeWidgetItem'''

    for item in reversed(range(treeWidgetItem.childCount())):
        treeWidgetItem.removeChild(treeWidgetItem.child(item))