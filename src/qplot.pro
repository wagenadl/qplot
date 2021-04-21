# QMake project file for qplot |            -*- mode: shell-script; -*-
# -----------------------------'

QT += gui svg
CONFIG += debug_and_release
CONFIG += c++11
TEMPLATE = app
TARGET = qplot
CONFIG(debug, debug|release) { TARGET=$${TARGET}_debug }
DEPENDPATH += .
INCLUDEPATH += .

# Input
HEADERS += Align.h \
           Axis.h \
           CmdAlign.h \
           CmdAt.h \
           CmdBrush.h \
           CmdCaligraph.h \
           CmdEndGroup.h \
           CmdFigSize.h \
           CmdFont.h \
           CmdGLine.h \
           CmdGroup.h \
           CmdHairline.h \
           CmdImage.h \
           CmdMark.h \
           CmdMarker.h \
           CmdPanel.h \
           CmdPen.h \
           CmdPlot.h \
           CmdRefText.h \
           CmdShareLim.h \
           CmdShrink.h \
           CmdText.h \
           CmdTextOnPath.h \
           CmdXLim.h \
           CmdYLim.h \
           Command.h \
           Error.h \
           Factor.h \
           Figure.h \
           GroupData.h \
           Marker.h \
           Program.h \
           QPWidget.h \
           Range.h \
           Rotate.h \
           ScrollWidget.h \
           Slightly.h \
           Statement.h \
           Text.h \
           TextShiftAccum.h \
           Token.h \
           FileReader.h \
           PipeReader.h \
           Image.h \
           Renderer.h \
           CmdSave.h

SOURCES += Axis.cpp \
           CmdSave.cpp \
           CmdAlign.cpp \
           CmdAt.cpp \
           CmdBrush.cpp \
           CmdCaligraph.cpp \
           CmdFigSize.cpp \
           CmdEndGroup.cpp \
           CmdFont.cpp \
           CmdShareLim.cpp \
           CmdShrink.cpp \
           CmdGLine.cpp \
           CmdGroup.cpp \
           CmdHairline.cpp \
           CmdImage.cpp \
           CmdImageG.cpp \
           CmdMark.cpp \
           CmdMarker.cpp \
           CmdPanel.cpp \
           CmdPen.cpp \
           CmdPlot.cpp \
           CmdRefText.cpp \
           CmdText.cpp \
           CmdTextOnPath.cpp \
           CmdXLim.cpp \
           CmdYLim.cpp \
           CmdXZImage.cpp \
           CmdZYImage.cpp \
           Command.cpp \
           Error.cpp \
           Factor.cpp \
           Figure.cpp \
           main.cpp \
           Program.cpp \
           QPWidget.cpp \
           Range.cpp \	
           Rotate.cpp \
           ScrollWidget.cpp \
           Slightly.cpp \
           Statement.cpp \
           Text.cpp \
           TextShiftAccum.cpp \
           Token.cpp \
           FileReader.cpp \
           PipeReader.cpp \
           Image.cpp \
           Renderer.cpp
