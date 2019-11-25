import fnmatch
import os
import sys
import logging

if sys.platform == "win32":
    try:
        PY_EXE_PATH = os.path.dirname(sys.executable)
        PYSIDE2_RCC = os.path.join(PY_EXE_PATH, "Scripts", "pyside2-rcc.exe")
        PYSIDE2_UIC = os.path.join(PY_EXE_PATH, "Scripts", "pyside2-uic.exe")
        assert (os.path.exists(PYSIDE2_RCC) and os.path.exists(PYSIDE2_UIC))
    except AssertionError:
        logging.error("PySide2 is not found! PySide2 may be installed on Anaconda!")
        try:
            import PySide2
            PYSIDE2_PKG_PATH = os.path.abspath(os.path.join(PySide2.__file__, os.pardir))
            PYSIDE2_RCC = os.path.join(PYSIDE2_PKG_PATH, "pyside2-rcc.exe")
            PYSIDE2_UIC = None
        except ImportError:
            logging.error("PySide2 is not installed! Please install PySide2 first.")
else:
    raise NotImplementedError


class UiGenerator:
    def __init__(self, ui_dir=None, rc_dir=None, out_dir=None):
        self.py_file_list = []
        self.__ui_dir = ui_dir
        self.__rc_dir = rc_dir
        self.__out_dir = out_dir
        self.__check_if_output_exist(out_dir)

    def compile_all(self, rc_dir=None, ui_dir=None, out_dir=None):
        if rc_dir:
            self.__rc_dir = rc_dir
        if ui_dir:
            self.__ui_dir = ui_dir
        if out_dir:
            self.__out_dir = out_dir
            self.__check_if_output_exist(out_dir)

        if self.__ui_dir and self.__rc_dir:
            self.__compile_resource_files(self.__rc_dir)
            self.__compile_ui_files(self.__ui_dir)
        else:
            logging.warning("Please specify a resources file directory and a ui file directory!")

    def compile_rc_files(self, rc_dir=None, out_dir=None):
        if rc_dir:
            self.__rc_dir = rc_dir
        if out_dir:
            self.__out_dir = out_dir
            self.__check_if_output_exist(out_dir)

        if self.__ui_dir:
            self.__compile_resource_files(self.__rc_dir)
        else:
            logging.warning("Please specify a resources file directory!")

    def compile_ui_files(self, ui_dir=None, out_dir=None):
        if ui_dir:
            self.__ui_dir = ui_dir
        if out_dir:
            self.__out_dir = out_dir
            self.__check_if_output_exist(out_dir)

        if self.__ui_dir:
            self.__compile_ui_files(self.__ui_dir)
        else:
            logging.warning("Please specify a ui file directory!")

    def __check_if_output_exist(self, out_dir):
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)

    def __compile_resource_files(self, rc_dir):
        # To compile qrc file from cmd line, use following line
        # pyside2-rcc.exe *.qrc -o rc_*.py

        # Compile .qrc file from scripts
        for root, dirs, files in os.walk(rc_dir):
            for basename in files:
                pattern = "*.qrc"
                if fnmatch.fnmatch(basename, pattern):
                    name_str, ext = os.path.splitext(basename)
                    rc_file_path = os.path.join(root, basename)
                    if self.__out_dir:
                        py_file_path = os.path.join(self.__out_dir, "rc_" + name_str + ".py")
                    else:
                        py_file_path = os.path.join(root, "rc_" + name_str + ".py")
                    cmd_string = "{0} {1} -o {2}".format(PYSIDE2_RCC, rc_file_path, py_file_path)
                    os.system(cmd_string)

    def __compile_ui_files(self, ui_dir):
        # To compile ui file from cmd line, use following line
        # pyside2-uic.exe *.ui -o ui_*.py
        # Compile .ui file from scripts
        for root, dirs, files in os.walk(ui_dir):
            for basename in files:
                pattern = "*.ui"
                if fnmatch.fnmatch(basename, pattern):
                    name_str, ext = os.path.splitext(basename)
                    ui_file_path = os.path.join(root, basename)
                    if self.__out_dir:
                        py_file_path = os.path.join(self.__out_dir, "ui_" + name_str + ".py")
                    else:
                        py_file_path = os.path.join(root, "ui_" + name_str + ".py")
                    cmd_string = "{0} {1} -o {2}".format(PYSIDE2_UIC, ui_file_path, py_file_path)
                    os.system(cmd_string)
