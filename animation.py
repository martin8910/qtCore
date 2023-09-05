from __future__ import print_function
# -*- coding: utf-8 -*-

__author__ = "Martin Gunnarsson"
__email__ = "hello@deerstranger.com"

from .external.Qt import QtWidgets, QtCore, QtGui, QtSvg

windowAnim = True


def fadeAnimation(start=0, end=1, duration=300, object=None, finishAction=None):
    if windowAnim is True:
        style = QtCore.QEasingCurve()
        style.setType(QtCore.QEasingCurve.OutQuint)

        if start == "current": start = object.opacity()
        if end == "current": end = object.opacity()

        # Animate window opasity
        opasicyAnimation = QtCore.QPropertyAnimation(object, b"opacity", object)
        opasicyAnimation.setEasingCurve(style)
        opasicyAnimation.setDuration(duration)
        opasicyAnimation.setStartValue(start)
        opasicyAnimation.setEndValue(end)
        opasicyAnimation.start(QtCore.QPropertyAnimation.DeleteWhenStopped)
        if finishAction != None:
            opasicyAnimation.finished.connect(finishAction)
    else:
        object.setOpacity(end)

def fadeWindowAnimation(start=0, end=1, duration=300, object=None, finishAction=None):
    if windowAnim is True:
        style = QtCore.QEasingCurve()
        style.setType(QtCore.QEasingCurve.OutQuint)

        # Animate window opasity
        opasicyAnimation = QtCore.QPropertyAnimation(object, b"windowOpacity", object)
        opasicyAnimation.setEasingCurve(style)
        opasicyAnimation.setDuration(duration)
        opasicyAnimation.setStartValue(start)
        opasicyAnimation.setEndValue(end)
        opasicyAnimation.start()
        if finishAction != None:
            opasicyAnimation.finished.connect(finishAction)
    else:
        object.setWindowOpacity(end)
        if finishAction != None:
            object.close()

def resizeWindowAnimation(start=(0, 0), end=(0, 0), duration=300, object=None, finishAction=None,attribute="maximumHeight"):
    if windowAnim is True:
        style = QtCore.QEasingCurve()
        style.setType(QtCore.QEasingCurve.OutQuint)

        if start[0] == "current": start[0] = object.size().height()
        if start[1] == "current": start[1] = object.size().width()

        # Animate window opasity
        positionAnimation = QtCore.QPropertyAnimation(object, attribute, object)
        positionAnimation.setEasingCurve(style)
        positionAnimation.setDuration(duration)
        positionAnimation.setStartValue(QtCore.QSize(start[0], start[1]))
        positionAnimation.setEndValue(QtCore.QSize(end[0], end[1]))
        positionAnimation.start()

        if finishAction != None:
            positionAnimation.finished.connect(finishAction)
    else:
        object.resize(end[0], end[1])
        if finishAction != None:
            object.close()
    pass

def slideWindowAnimation(start=-100, end=0, duration=300, object=None, animationStyle=None,finishAction=None):
    if windowAnim is True:
        # Get current position
        pos = object.pos()

        # Create animation and properties
        slideAnimation = QtCore.QPropertyAnimation(object, b'pos', object)
        slideAnimation.setDuration(duration)
        style = QtCore.QEasingCurve()
        # Change curve if the value is end or beginning
        if start >= end:
            style.setType(QtCore.QEasingCurve.OutExpo)
        else:
            style.setType(QtCore.QEasingCurve.InOutExpo)
        if animationStyle != None:  style.setType(animationStyle)

        # Connect finish animation
        if finishAction != None: slideAnimation.finished.connect(finishAction)

        slideAnimation.setEasingCurve(style)
        slideAnimation.setStartValue(QtCore.QPoint(pos.x(), pos.y() + start))
        slideAnimation.setEndValue(QtCore.QPoint(pos.x(), pos.y() + end))
        slideAnimation.start()

def slideWindowBothAnimation(start=(-100, 0), end=(0, 0), duration=300, object=None, animationStyle=None,finishAction=None):
    if windowAnim is True:
        # Get current position
        pos = object.pos()

        # Create animation and properties
        slideAnimation = QtCore.QPropertyAnimation(object, b'pos', object)
        slideAnimation.setDuration(duration)
        style = QtCore.QEasingCurve()
        # Change curve if the value is end or beginning

        if start[0] >= end[0]:
            style.setType(QtCore.QEasingCurve.OutExpo)
        else:
            style.setType(QtCore.QEasingCurve.InOutExpo)
        if animationStyle != None:  style.setType(animationStyle)

        # Connect finish animation
        if finishAction != None: slideAnimation.finished.connect(finishAction)

        slideAnimation.setEasingCurve(style)
        slideAnimation.setStartValue(QtCore.QPoint(pos.x() + start[1], pos.y() + start[0]))
        slideAnimation.setEndValue(QtCore.QPoint(pos.x() + end[1], pos.y() + end[0]))
        slideAnimation.start()

def simple_property_animation(startValue=None, endValue=None, duration=500,object=None, property="size", easing="InOutQuint"):

    # Create animation
    animation = QtCore.QPropertyAnimation(object, property, object)

    # Easing
    style = QtCore.QEasingCurve()
    #style.setType(QtCore.QEasingCurve.InOutQuint)
    style.setType(QtCore.QEasingCurve.InBounce)

    #animation.setEasingCurve(style)

    # Set Duration
    animation.setDuration(duration)

    # Set values
    animation.setStartValue(startValue)
    animation.setEndValue(endValue)

    #Start animation
    animation.start(QtCore.QPropertyAnimation.DeleteWhenStopped)

def propertyAnimation(start=[0, 0], end=[30, 0], duration=300, object=None, property="iconSize",mode="InOutQuint", finishAction=None):
    animation = QtCore.QPropertyAnimation(object, property.encode("utf-8"), object)

    style = QtCore.QEasingCurve()
    if mode == "Linear": style.setType(QtCore.QEasingCurve.Linear)
    elif mode == "InQuad": style.setType(QtCore.QEasingCurve.InQuad)
    elif mode == "OutQuad":style.setType(QtCore.QEasingCurve.OutQuad)
    if mode == "InOutQuad": style.setType(QtCore.QEasingCurve.InOutQuad)
    elif mode == "OutInQuad": style.setType(QtCore.QEasingCurve.OutInQuad)
    elif mode == "InCubic":style.setType(QtCore.QEasingCurve.InCubic)
    if mode == "OutCubic": style.setType(QtCore.QEasingCurve.OutCubic)
    elif mode == "InOutCubic": style.setType(QtCore.QEasingCurve.InOutCubic)
    elif mode == "OutInCubic":style.setType(QtCore.QEasingCurve.OutInCubic)
    if mode == "InQuart": style.setType(QtCore.QEasingCurve.InQuart)
    elif mode == "OutQuart": style.setType(QtCore.QEasingCurve.OutQuart)
    elif mode == "InOutQuart":style.setType(QtCore.QEasingCurve.InOutQuart)
    if mode == "OutInQuart": style.setType(QtCore.QEasingCurve.OutInQuart)
    elif mode == "InQuint": style.setType(QtCore.QEasingCurve.InQuint)
    elif mode == "InBounce":style.setType(QtCore.QEasingCurve.InBounce)
    elif mode == "OutExpo":style.setType(QtCore.QEasingCurve.OutExpo)
    elif mode == "InExpo": style.setType(QtCore.QEasingCurve.InExpo)
    elif mode == "InOutQuint": style.setType(QtCore.QEasingCurve.InOutQuint)
    elif mode == "OutBounce":
        style.setType(QtCore.QEasingCurve.OutBounce)
        style.setAmplitude(0.5)
    else:
        print("Mode not supported:",mode)
        style.setType(QtCore.QEasingCurve.InOutQuint)

    animation.setEasingCurve(style)

    # Set Duration
    animation.setDuration(duration)

    # Get default attribute from name:
    # Set start values
    if start[0] == "current":
        if property == "iconSize":
            startValueX = object.iconSize().height()
        if property == "maximumSize" or property == "minimumSize":
            startValueY = object.size().height()
    else:
        startValueX = start[0]
    if start[1] == "current":
        if property == "iconSize":
            startValueY = object.iconSize().width()
        if property == "maximumSize" or property == "minimumSize":
            startValueY = object.size().width()
    else:
        startValueY = start[1]
    animation.setStartValue(QtCore.QSize(startValueX, startValueY))
    animation.setEndValue(QtCore.QSize(end[0], end[0]))
    animation.start()

    if finishAction != None:
        animation.finished.connect(finishAction)

    # Animate
    animation.start(QtCore.QPropertyAnimation.DeleteWhenStopped)



# Version 1.5 of the aninmation widgetsize that works for horizontal elements as well
def animateWidgetSize(element, start=(300, 100), end=(300, 150),expanding=False, attributelist=("minimumSize", "maximumSize"), duration=False, bounce=True,finishAction=None):
    '''Animate an objects width/height'''

    # Generate automatic duration based on length if not specified
    if not duration:
        duration = min(abs(start[1] - end[1]) * 5, 500)

    #for attribute in ["minimumSize", "maximumSize"]:
    for attribute in attributelist:
        if attribute == "minimumSize":
            element.setMinimumHeight(0)
            element.setMinimumWidth(0)
            #element.setMinimumHeight(0)
            #element.setMinimumWidth(0)
        elif attribute == "maximumSize":
            element.setMaximumHeight(1699999)
            element.setMaximumWidth(1699999)
            # pass

        # Create animation property and set start and end point
        animation = QtCore.QPropertyAnimation(element, QtCore.QByteArray(attribute.encode("utf-8")), element)

        # Set start and end values
        animation.setStartValue(QtCore.QSize(start[0], start[1]))
        animation.setEndValue(QtCore.QSize(end[0], end[1]))

        # Create easing style
        style = QtCore.QEasingCurve()
        if start[1] <= end[1]:
            if bounce:
                style.setType(QtCore.QEasingCurve.OutBounce)
                style.setAmplitude(0.2)
            else:
                style.setType(QtCore.QEasingCurve.OutExpo)

        else:
            style.setType(QtCore.QEasingCurve.OutExpo)
        animation.setEasingCurve(style)


        if expanding:
            if attribute == "maximumSize":
                [animation.finished.connect(x) for x in [lambda: element.setMaximumHeight(1699999), lambda: element.setMaximumWidth(1699999)]]
                #animation.finished.connect(lambda: element.setBaseSize(1699999,1699999))
                #animation.finished.connect(lambda: element.setSizeHint(QtCore.QSize(end[0], end[1])))
            else:
                [animation.finished.connect(x) for x in [lambda: element.setMinimumHeight(0), lambda: element.setMinimumWidth(0)]]
        animation.setDuration(duration)

        # Connect Finish Action
        if finishAction != None:
            if type(finishAction) is list or type(finishAction) is tuple:
                for action in finishAction:
                    animation.finished.connect(action)
            else:
                animation.finished.connect(finishAction)

        # Start animation and delete when finished
        animation.start(QtCore.QPropertyAnimation.DeleteWhenStopped)