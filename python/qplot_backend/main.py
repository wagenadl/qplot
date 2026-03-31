#!/usr/bin/python3

# main.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

import os
import sys

from PyQt6.QtCore import Qt, QCommandLineOption, QCommandLineParser, QProcessEnvironment
from PyQt6.QtWidgets import QApplication

from .program import Program
from .figure import Figure
from .command import Command
from .qpwidget import QPWidget
from .filereader import FileReader, Contents
from .pipereader import PipeReader
from .error import Error
from .factor import pt2iu, set_factor
from .renderer import Renderer
from .statement import Statement

# Import all Cmd* modules so their @Command.register decorators fire
#from . import cmdalign
#from . import cmdalignaxes
#from . import cmdat
#from . import cmdbrush
#from . import cmdcaligraph
#from . import cmdcommonscale
#from . import cmdendgroup
#from . import cmdfigsize
#from . import cmdfont
#from . import cmdgline
#from . import cmdgroup
#from . import cmdhairline
#from . import cmdhatch
#from . import cmdimage
#from . import cmdimageg
#from . import cmdmark
#from . import cmdmarker
#from . import cmdpanel
#from . import cmdpen
#from . import cmdplot
#from . import cmdrebalance
#from . import cmdreftext
#from . import cmdsave
#from . import cmdshrink
#from . import cmdtext
#from . import cmdtextonpath
#from . import cmdxlim
#from . import cmdxzimage
#from . import cmdylim
#from . import cmdzyimage

try:
    from config import QPLOT_VERSION
except ImportError:
    QPLOT_VERSION = "(unknown)"

_autoraise = False

# ---------------------------------------------------------------------------
# Interactive mode — display window, read from file or stdin
# ---------------------------------------------------------------------------

def interactive(ifn: str, ttl: str, renderer: Renderer,
                app: QApplication) -> int:
    win = QPWidget()
    idx = ttl.rfind('/')
    win.setWindowTitle("qplot: " + (ttl[idx+1:] if idx >= 0 else ttl))
    win.set_contents(renderer.figure(), renderer.program())
    win.set_margin(pt2iu(20))
    win.show()
    win.auto_size()

    is_stdin = ifn in ("-", "")

    if is_stdin:
        pipereader = PipeReader()

        def on_pipe_ready():
            ss = pipereader.read_queue()
            if ss:
                n0 = len(renderer.program())
                for s in ss:
                    if len(s) and s[0].str == "figsize":
                        renderer.prerender()
                        n1 = len(renderer.program())
                        renderer.dosaves(n0, n1)
                        renderer.program().append(s)
                        n0 = len(renderer.program())
                    else:
                        renderer.program().append(s)
                renderer.prerender()
                n1 = len(renderer.program())
                renderer.dosaves(n0, n1)
                win.update()

        pipereader.ready.connect(on_pipe_ready,
                                 Qt.ConnectionType.QueuedConnection)
        pipereader.finished.connect(app.quit)
        pipereader.start()

    else:
        filereader = FileReader(ifn)
        c = filereader.contents()
        if c.valid:
            renderer.program().read(c.contents)
        else:
            Error() << c.error

        if _autoraise:
            filereader.ready.connect(win.raise_)

        def on_file_ready():
            c = filereader.contents()
            if c.valid:
                renderer.program().read(c.contents)
            else:
                Error() << c.error
            renderer.prerender()
            if c.valid:
                renderer.dosaves()
            win.update()

        filereader.ready.connect(on_file_ready,
                                 Qt.ConnectionType.QueuedConnection)
        filereader.start()

    renderer.prerender()
    return app.exec()

# ---------------------------------------------------------------------------
# Non-interactive mode — read file, render to output
# ---------------------------------------------------------------------------

def noninteractive(ifn: str, ofn: str, renderer: Renderer) -> int:
    reader   = FileReader(ifn)
    contents = reader.contents()
    if contents.valid:
        renderer.program().set_label(ifn)
        try:
            renderer.program().read(contents.contents)
        except Exception as e:
            print(f"Exception reading program: {e}")
            sys.exit(1)
        return 0 if renderer.save(ofn) else 2
    else:
        Error() << contents.error
        return 2

# ---------------------------------------------------------------------------
# Version display
# ---------------------------------------------------------------------------

def show_version() -> int:
    sys.stderr.write(f"QPlot {QPLOT_VERSION}\n")
    sys.stderr.write("Copyright (C) 2014-2024 Daniel A. Wagenaar\n\n")
    sys.stderr.write(
        "QPlot is free software: you can redistribute it and/or modify "
        "it under the terms of the GNU General Public License as published "
        "by the Free Software Foundation, either version 3 of the License, "
        "or (at your option) any later version.\n\n"
        "QPlot is distributed in the hope that it will be useful, but "
        "WITHOUT ANY WARRANTY; without even the implied warranty of "
        "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU "
        "General Public License for more details.\n\n"
        "You should have received a copy of the GNU General Public License "
        "along with this program. If not, see "
        "www.gnu.org/licenses/gpl.html.\n"
    )
    return 0

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    global _autoraise

    app = QApplication(sys.argv)
    app.setApplicationName("QPlot")
    app.setApplicationVersion(QPLOT_VERSION)

    env = QProcessEnvironment.systemEnvironment()
    default_maxtries = (env.value("QPLOT_MAXITER")
                        if env.contains("QPLOT_MAXITER") else "10")

    cli_help      = QCommandLineOption("help",
                        "Display help on commandline options")
    cli_autoraise = QCommandLineOption("autoraise",
                        "Automatically raise the window on update")
    cli_width     = QCommandLineOption("w",
                        "Override output width (points)", "w")
    cli_height    = QCommandLineOption("h",
                        "Override output height (points)", "h")
    cli_reso      = QCommandLineOption(["r", "res", "resolution"],
                        "Specify output resolution", "res", "300")
    cli_qual      = QCommandLineOption(["q", "quality"],
                        "Specify output jpeg quality", "qual", "95")
    cli_maxtries  = QCommandLineOption("maxtries",
                        "Override max tries for shrink",
                        "N", default_maxtries)
    cli_version   = QCommandLineOption(["v", "version"],
                        "Show version information")
    cli_title     = QCommandLineOption("title",
                        "Override window title", "title")

    cli = QCommandLineParser()
    cli.setApplicationDescription(
        "\nQPlot is Publication-quality plotting for Python, Octave, or "
        "Matlab.\nMore information is at https://danielwagenaar.net/qplot.")
    cli.addPositionalArgument("input",
                              "Input filename (\"-\" for stdin)")
    cli.addPositionalArgument("output",
                              "Output filename (\"-.ext\" for stdout)",
                              "[output]")
    cli.addOption(cli_help)
    cli.addOption(cli_reso)
    cli.addOption(cli_qual)
    cli.addOption(cli_width)
    cli.addOption(cli_height)
    cli.addOption(cli_autoraise)
    cli.addOption(cli_maxtries)
    cli.addOption(cli_title)
    cli.addOption(cli_version)
    cli.process(app)

    if cli.isSet("help"):
        cli.showHelp()
    if cli.isSet("version"):
        return show_version()

    _autoraise = cli.isSet("autoraise")

    args = cli.positionalArguments()
    if len(args) < 1 or len(args) > 2:
        cli.showHelp(1)

    renderer = Renderer()
    if cli.isSet("w"):
        renderer.override_width(float(cli.value("w")))
    if cli.isSet("h"):
        renderer.override_height(float(cli.value("h")))
    renderer.set_max_tries(int(cli.value("maxtries")))
    renderer.set_bitmap_resolution(float(cli.value("r")))
    renderer.set_bitmap_quality(int(cli.value("q")))

    ttl = args[0]
    if cli.isSet("title"):
        ttl = cli.value("title")

    if len(args) == 1:
        return interactive(args[0], ttl, renderer, app)
    else:
        return noninteractive(args[0], args[1], renderer)


if __name__ == "__main__":
    sys.exit(main())


