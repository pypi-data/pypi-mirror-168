# UI files from qt
UI_FILES = $(wildcard *.ui)

# Resources files from qt
RES_FILES = $(wildcard *.qrc)

### CONFIGURABLE
OUT_FOLDER = ./

# Binaries
PYUIC = pyside2-uic
PYRCC = pyside2-rcc

PY_UI_FILES = $(UI_FILES:%.ui=ui_%.py)
PY_RES_FILES = $(RES_FILES:%.qrc=rc_%.py)

all : resources ui

resources : $(PY_RES_FILES)
rc_%.py : %.qrc
	$(PYRCC) $< -o $(OUT_FOLDER)$@

ui : $(PY_UI_FILES)
ui_%.py : %.ui
	$(PYUIC) $< -o $(OUT_FOLDER)$@

clean :
	$(RM) $(OUT_FOLDER)$(PY_UI_FILES)