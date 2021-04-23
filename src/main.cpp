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

#include <iostream>
#include <string>

#include <QCommandLineParser>
#include <QApplication>
#include <QWidget>
#include <QDebug>
#include <QImage>
#include <QFile>
#include <QDir>
#include <QFileInfo>
#include <QDateTime>
#include <QProcessEnvironment>
#include <QDebug>

#include <math.h>
#include <sys/types.h>
#include <stdio.h>

#include "Program.h"
#include "Figure.h"
#include "Command.h"
#include "QPWidget.h"
#include "FileReader.h"
#include "PipeReader.h"
#include "Error.h"
#include "Factor.h"
#include "Renderer.h"


static bool autoraise = false;

int interactive(QString ifn, QString ttl, Renderer *renderer,
                QApplication *app) {
  QPWidget win;
  int idx = ttl.lastIndexOf('/');
  win.setWindowTitle("qplot: " + ((idx>=0) ? ttl.mid(idx+1) : ttl));
  win.setContents(renderer->figure(), renderer->program());
  win.setMargin(pt2iu(20));
  win.show();
  win.autoSize();

  bool isstdin = ifn=="-" || ifn=="";

  FileReader *filereader = 0;
  PipeReader *pipereader = 0;

  if (isstdin) {
    pipereader = new PipeReader();
    QObject::connect(pipereader, &PipeReader::ready,
                     &win, [&pipereader, &win, &renderer]() {
                       QList<Statement> ss = pipereader->readQueue();
                       if (ss.size()) {
                         int n0 = renderer->program()->length();
                         for (auto s: ss) 
                           renderer->program()->append(s);
                         renderer->prerender();
                         int n1 = renderer->program()->length();
                         renderer->dosaves(n0, n1);
                         win.update();
                       }
                     },
                     Qt::QueuedConnection);
    QObject::connect(pipereader, &PipeReader::finished,
                     app, &QApplication::quit);
    pipereader->start();
  } else {
    filereader = new FileReader(ifn);
    if (filereader->contents().valid) 
      renderer->program()->read(filereader->contents().contents);
    else
      Error() << filereader->contents().error;

    if (autoraise)
      QObject::connect(filereader, &FileReader::ready,
                       &win, &QWidget::raise);

    QObject::connect(filereader, &FileReader::ready,
                     &win, [filereader, &win, &renderer]() {
                       FileReader::Contents c(filereader->contents());
                       if (c.valid)
                         renderer->program()->read(c.contents);
                       else
                         Error() << c.error;
                       renderer->prerender();
                       if (c.valid)
                         renderer->dosaves();
                       win.update();
                     },
                     Qt::QueuedConnection);

    filereader->start(); // starts the thread
  }
  
  renderer->prerender();

  return app->exec();
}

int noninteractive(QString ifn, QString ofn, Renderer *renderer) {
  FileReader reader(ifn);
  FileReader::Contents contents = reader.contents();
  if (contents.valid) {
    renderer->program()->setLabel(ifn);
    renderer->program()->read(contents.contents);
    if (renderer->save(ofn))
      return 0;
    else
      return 2;
  } else {
    Error() << contents.error;
    return 2;
  }
}

int showVersion() {
  std::cerr << "QPlot 0.3.0\n";
  std::cerr << "Copyright (C) 2014-2021 Daniel A. Wagenaar\n";
  std::cerr << "\n";
  std::cerr << "QPlot is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.\n\n";
  std::cerr << "QPlot is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.\n\n";
  std::cerr << "You should have received a copy of the GNU General Public License along with this program. If not, see www.gnu.org/licenses/gpl.html.\n";
  return 0;
};



int main(int argc, char **argv) {
  QApplication app(argc, argv);
  app.setApplicationName("QPlot");
  app.setApplicationVersion("0.3.0");
  
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
  QCommandLineOption cli_version(QStringList() << "v" << "version",
                                 "Show version information");
  QCommandLineOption cli_title("title", "Override window title", "title");
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
  cli.addOption(cli_title);
  cli.addOption(cli_version);

  cli.setApplicationDescription("\n"
                                "QPlot is Publication-quality plotting for Python, Octave, or Matlab.\n"
                                "More information is at https://danielwagenaar.net/qplot.");
                                    
  cli.process(app);

  if (cli.isSet("version")) 
    return showVersion();

  autoraise = cli.isSet("autoraise");
  
  QStringList args = cli.positionalArguments();
  if (args.size() < 1 || args.size() > 2)
    cli.showHelp(1);

  Renderer renderer;
  if (cli.isSet("w"))
    renderer.overrideWidth(cli.value("w").toDouble());
  if (cli.isSet("h"))
    renderer.overrideWidth(cli.value("h").toDouble());
  renderer.setMaxTries(cli.value("maxtries").toInt());
  renderer.setBitmapResolution(cli.value("r").toInt());
  renderer.setBitmapQuality(cli.value("q").toInt());

  QString ttl = args[0];
  if (cli.isSet("title"))
    ttl = cli.value("title");
  
  if (args.size()==1) 
    return interactive(args[0], ttl, &renderer, &app);
  else 
    return noninteractive(args[0], args[1], &renderer);
}
