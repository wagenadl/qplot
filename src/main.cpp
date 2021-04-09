// main.cpp - This file is part of QPlot

/* QPlot - Publication quality 2D graphs with dual coordinate systems
   Copyright (C) 2014  Daniel Wagenaar
  
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
  
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
  
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

// main.C

#include <QCommandLineParser>
#include <QApplication>
#include <QWidget>
#include <QDebug>
#include <QImage>
#include <QFile>
#include <QDir>
#include <QPdfWriter>
#include <QSvgGenerator>
#include <QFileInfo>
#include <QTemporaryFile>
#include <QDateTime>
#include <QProcessEnvironment>
#include <QDebug>

#include <math.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>

#include "Program.h"
#include "Figure.h"
#include "Command.h"
#include "QPWidget.h"
#include "Watcher.h"
#include "Error.h"
#include "Factor.h"
#include "Render.h"



int usage(int ex=1) {
  Error() << "Usage: qplot input.txt";
  Error() << "       qplot input.txt output.pdf|svg|ps";
  Error() << "       qplot [-rDPI] input.txt output.png|tif|jpg";
  Error() << "       qplot -wWIDTH -hHEIGHT ... overrides output size (pts)";
  Error() << "       qplot --maxtries N ... overrides max tries for shrink";
  Error() << "       qplot --autoraise ... automatically raises"
                                                     " the window on update";
  Error() << "";
  Error() << "For noninteractive use, input.txt may be '-' for stdin, and";
  Error() << "output.EXT may be '-.EXT' for stdout.";

  return ex;
}



static bool autoraise = false;

int interactive(Render *render, QApplication *app) {
  QString ifn = render->inputFilename();
  if (ifn=="-") {
    Error() << "Input may not be “-” for interactive use";
    return 1;
  }
  render->figure()->setHairline(0);
  render->prerender();

  QPWidget win;
  Watcher wtch(ifn, render, &win);
  int idx = ifn.lastIndexOf('/');
  win.setWindowTitle("qplot: " + ((idx>=0) ? ifn.mid(idx+1) : ifn));
  if (autoraise)
    QObject::connect(&wtch, SIGNAL(ping()), &win, SLOT(raise()));
  QObject::connect(&wtch, SIGNAL(ping()), &win, SLOT(update()));
  win.setContents(render->figure(), render->program());
  win.setMargin(pt2iu(20));
  win.show();
  win.autoSize();
  wtch.reread(true);
  QFileInfo fi(ifn);
  QString path = fi.path();
  QString leaf = fi.fileName();
  QFile pidfile(path + "/.qp-" + leaf + ".pid");
  QFile fbfile(path + "/.qp-" + leaf + ".fb");
  if (fbfile.exists())
    win.setFeedbackFile(fbfile.fileName());
  pidfile.open(QIODevice::WriteOnly);
  char pid[100];
  snprintf(pid, 100, "%i\n", getpid());
  pidfile.write(pid, strlen(pid));
  pidfile.close();
  int r = app->exec();
  pidfile.remove();
  return r;
}


int main(int argc, char **argv) {
  QApplication app(argc, argv);
  app.setApplicationName("qplot");
  app.setApplicationVersion("1.0");
  
  QCommandLineOption cli_autoraise("autoraise",
                             "Automatically raise the window on update");
  QCommandLineOption cli_width("w", "Override output width (points)",
                               "w");
  QCommandLineOption cli_height("h", "Override output height (points)",
                               "h");
  QCommandLineOption cli_reso(QStringList() << "r" << "res" << "resolution",
                              "Specify output resolution",
                              "res", "300");
  QCommandLineOption cli_qual(QStringList() << "q" << "quality",
                              "Specify output jpeg quality",
                              "qual", "95");
  QCommandLineOption cli_maxtries("maxtries",
                                  "Override max tries for shrink",
                                  "N", "100");
  QProcessEnvironment env(QProcessEnvironment::systemEnvironment());
  if (env.contains("QPLOT_MAXITER"))
    cli_maxtries.setDefaultValue(env.value("QPLOT_MAXITER"));

  QCommandLineParser cli;
  cli.addHelpOption();
  cli.addPositionalArgument("input", "Input filename (“-” for stdin)");
  cli.addPositionalArgument("output", "Output filename (“-.ext” for stdout)",
                            "[output]");
  cli.addOption(cli_reso);
  cli.addOption(cli_qual);
  cli.addOption(cli_width);
  cli.addOption(cli_height);
  cli.addOption(cli_autoraise);
  cli.addOption(cli_maxtries);

  cli.process(app);

  QStringList args = cli.positionalArguments();
  if (args.size() < 1 || args.size() > 2)
    cli.showHelp(1);

  Render render(args[0]);
  if (cli.isSet("w"))
    render.overrideWidth(cli.value("w").toDouble());
  if (cli.isSet("h"))
    render.overrideWidth(cli.value("h").toDouble());
  render.setMaxTries(cli.value("maxtries").toInt());
  render.setBitmapResolution(cli.value("r").toInt());
  render.setBitmapQuality(cli.value("q").toInt());

  if (args.size()==1) {
    return interactive(&render, &app);
  } else {
    render.loadall();
    if (render.save(args[1]))
      return 0;
  }
  return 2;
}
