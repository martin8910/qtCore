from __future__ import print_function
# -*- coding: utf-8 -*-

__author__ = "Martin Gunnarsson"
__email__ = "hello@deerstranger.com"

from .external.Qt import QtWidgets, QtCompat, QtCore, QtGui, QtSvg

###################################################################################################
# Handle QTreeWidget/QTreeWidgetItems
###################################################################################################
def get_children_from_treeWidgetItem(treeWidgetItem):
    '''Return all items from a qTreeWidgetItem'''
    items = [treeWidgetItem.child(number) for number in range(treeWidgetItem.childCount())]

    return items

def get_subtree_nodes(tree_widget_item):
    """Returns all QTreeWidgetItems in the subtree rooted at the given node."""
    nodes = []
    nodes.append(tree_widget_item)
    for i in range(tree_widget_item.childCount()):
        nodes.extend(get_subtree_nodes(tree_widget_item.child(i)))
    return nodes

def get_all_items(tree_widget):
    """Returns all QTreeWidgetItems in the given QTreeWidget."""
    all_items = []
    for i in range(tree_widget.topLevelItemCount()):
        top_item = tree_widget.topLevelItem(i)
        all_items.extend(get_subtree_nodes(top_item))
    return all_items



def remove_children_from_treeWidgetItem(item):
    '''Remove all the children from a QTreeWidgetItem'''

    #for item in reversed(range(treeWidgetItem.childCount())):
    #    treeWidgetItem.removeChild(treeWidgetItem.child(item))
    tree_widget = item.treeWidget()

    parent = item.parent()
    # Get its parent

    if tree_widget.indexOfTopLevelItem(item) > -1:
        # Top-level item, find index and remove
        index = tree_widget.indexOfTopLevelItem(item)
        tree_widget.takeTopLevelItem(index)
    else:
        #Take item from current index
        index = parent.indexOfChild(item)
        parent.takeChild(index)


def traverse_tree(treeWidgetItem):
    '''Traverse a tree for all ites treeWidgetItems'''
    fullList = []
    for number in range(treeWidgetItem.childCount()):
        # Get item
        item = treeWidgetItem.child(number)

        # Add to list
        fullList.append(item)

        if item.childCount() != 0:
            # If children exists
            results = traverse_tree(item)

            for item in results:
                fullList.append(item)

    return fullList


def get_items(treeWidget):
    '''Returns all item from a tree-Widget'''
    return treeWidget.findItems("", QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive)

def select_items(tree, items=[]):
    tree.clearSelection()
    for item in items:
        item.setSelected(True)

    #tree.setSelectionMode(QListWidget.MultiSelection)
    # index = ['data2', 'data3', 'data5']
    # for i in index:
    #     matching_items = tree.findItems(i, Qt.MatchExactly)
    #     for item in matching_items:

