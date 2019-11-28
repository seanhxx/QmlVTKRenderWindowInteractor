
from PySide2.QtCore import QSize, qDebug
from PySide2.QtGui import QOpenGLFramebufferObject, QOpenGLFramebufferObjectFormat, QMouseEvent
from PySide2.QtQuick import QQuickFramebufferObject


class QmlVTKOpenGLRenderWindowInteractor(QQuickFramebufferObject.Renderer):
    def __init__(self):
        super(QmlVTKOpenGLRenderWindowInteractor, self).__init__()
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
