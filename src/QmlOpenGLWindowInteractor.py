from PySide2.QtCore import QSize, qDebug
from PySide2.QtGui import QMouseEvent
from PySide2.QtQuick import QQuickFramebufferObject
from .QmlVTKOpenGLRenderWIndowInteractor import QmlVTKOpenGLRenderWindowInteractor
import logging


class QmlOpenGLWindowInteractor(QQuickFramebufferObject):
    def __init__(self, parent=None):
        # super().__init__()
        super(QmlOpenGLWindowInteractor, self).__init__(parent)

    def createRenderer(self) -> QQuickFramebufferObject.Renderer:
        qDebug("create renderer now")
        fb_item_renderer = QmlVTKOpenGLRenderWindowInteractor()
        self.__renderer = fb_item_renderer
        return self.__renderer

    def mousePressEvent(self, event:QMouseEvent):
        qDebug("mouse press event")
        # print("mouse press event: {}".format(event.button()) )

    def test_method(self):
        qDebug("test print")
        # print("test print")
