import os

PROJ_ROOT_DIR = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
PROJ_SRC_DIR = os.path.join(PROJ_ROOT_DIR, "example")
UI_FILE_DIR = os.path.join(PROJ_ROOT_DIR, "resources", "ui")
RC_FILE_DIR = os.path.join(PROJ_ROOT_DIR, "resources")
GUI_COMPILE_OUTPUT = os.path.join(PROJ_ROOT_DIR, "example", "gui")
