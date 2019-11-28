from PySide2.QtCore import QObject, Slot
from PySide2.QtQml import QQmlApplicationEngine
from src.QmlOpenGLWindowInteractor import QmlOpenGLWindowInteractor


class MainWindow(QObject):
    def __init__(self, engine):
        super(MainWindow, self).__init__()
        self.__engine = engine

    @Slot(int, int, int)
    def mousePressHandler(self, button:int, x:int, y:int):
        print(button)
        print((x,y))
        rootObject = self.__engine.rootObjects()[0]
        self.__interactor:QmlOpenGLWindowInteractor = rootObject.findChild(QmlOpenGLWindowInteractor, "interactor")
        if self.__interactor:
            self.__interactor.test_method()
        else:
            print("no interactor found")

