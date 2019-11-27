from PySide2.QtCore import QSize, qDebug
from PySide2.QtGui import QOpenGLFramebufferObject, QOpenGLFramebufferObjectFormat, QMouseEvent
from PySide2.QtQuick import QQuickFramebufferObject
import logging


class FbItemRenderer(QQuickFramebufferObject.Renderer):
    def __init__(self):
        super(FbItemRenderer, self).__init__()
        # self.update()

    def createFramebufferObject(self, size:QSize) -> QOpenGLFramebufferObject:
        print("createFramebufferobj")
        gl_format = QOpenGLFramebufferObjectFormat()
        gl_format.setAttachment(QOpenGLFramebufferObject.Depth)
        frame_buffer_object = QOpenGLFramebufferObject(size, gl_format)
        self.__fbo = frame_buffer_object
        return self.__fbo

    def synchronize(self, item:QQuickFramebufferObject):
        print("synchronize")
        pass

    def render(self):
        print("render")
        # self.update()
        pass


class QmlVTKRenderWindowInteractor(QQuickFramebufferObject):
    def __init__(self, parent=None):
        # super().__init__()
        super(QmlVTKRenderWindowInteractor, self).__init__(parent)

    def createRenderer(self) -> QQuickFramebufferObject.Renderer:
        qDebug("create renderer now")
        fb_item_renderer = FbItemRenderer()
        self.__renderer = fb_item_renderer
        return self.__renderer

    def mousePressEvent(self, event:QMouseEvent):
        qDebug("mouse press event")
        # print("mouse press event: {}".format(event.button()) )

    def test_method(self):
        qDebug("test print")
        # print("test print")
