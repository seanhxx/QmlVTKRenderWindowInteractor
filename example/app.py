import sys
import logging
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide2.QtCore import QUrl
from PySide2 import QtCore
from src.QmlOpenGLWindowInteractor import QmlOpenGLWindowInteractor
from example.gui.main_window import MainWindow


class ExampleApp(QApplication):
    def __init__(self, sys_argv):
        super(ExampleApp, self).__init__(sys_argv)


def main():
    from misc.ui_generator import UiGenerator
    import example.constants as const
    ui_generator = UiGenerator(ui_dir=const.UI_FILE_DIR, rc_dir=const.RC_FILE_DIR, out_dir=const.GUI_COMPILE_OUTPUT)
    ui_generator.compile_all()

    import example.gui.rc_qml as rc_qml
    rc_qml.qInitResources()

    from misc.debug import qt_message_handler
    QtCore.qInstallMessageHandler(qt_message_handler)
    app = ExampleApp(sys.argv)

    engine = QQmlApplicationEngine()
    qmlRegisterType(QmlOpenGLWindowInteractor, "QmlVTK", 1, 0, "Interactor")

    context = engine.rootContext()
    main_window = MainWindow()
    engine.setContextForObject(main_window, context)
    context.setContextProperty("mainWindow", main_window)

    engine.load(QUrl.fromLocalFile(":/qml/app.qml"))

    if len(engine.rootObjects()) == 0:
        logging.error("No QML file is loaded. Application Exit!")
        return


    sys.exit(app.exec_())


if __name__ == '__main__':
    from misc.debug import except_hook
    sys.excepthook = except_hook

    main()
