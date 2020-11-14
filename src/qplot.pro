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
HEADERS += Align.H \
           Axis.H \
           CmdAlign.H \
           CmdAt.H \
           CmdBrush.H \
           CmdCaligraph.H \
           CmdEndGroup.H \
           CmdFigSize.H \
           CmdFont.H \
           CmdGLine.H \
           CmdGroup.H \
           CmdHairline.H \
           CmdImage.H \
           CmdMark.H \
           CmdMarker.H \
           CmdPanel.H \
           CmdPen.H \
           CmdPlot.H \
           CmdRefText.H \
           CmdShareLim.H \
           CmdShrink.H \
           CmdText.H \
           CmdTextOnPath.H \
           CmdXLim.H \
           CmdYLim.H \
           Command.H \
           Error.H \
           Factor.H \
           Figure.H \
           GroupData.H \
           Marker.H \
           Program.H \
           QPWidget.H \
           Range.H \
           Rotate.H \
           ScrollWidget.H \
           Slightly.H \
           Statement.H \
           Text.H \
           TextShiftAccum.H \
           Token.H \
           Watcher.H \
           Image.H

SOURCES += Axis.cpp \
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
           Watcher.cpp \
           Image.cpp
