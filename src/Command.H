// Command.H - This file is part of QPlot

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

// Command.H

#ifndef COMMAND_H

#define COMMAND_H

#include "Statement.H"
#include "Figure.H"
#include "Factor.H"
#include <QMap>

class Command {
public:
  virtual ~Command() {}
  virtual bool parse(Statement const &)=0;
  /*:F parse
   *:D Should check whether the statement is valid.
   */
  virtual void render(Statement const &s, Figure &f, bool dryrun)=0;
  /*:F render
   *:D Should actually plot the statement to the figure.
   *   You may assume that parse() has returned OK, so you shouldn't need
       to check the statement's validity again.
   *   You may use all style information in the figure, and update it
       as you see fit.
   *   You should update the figure's bbox, unless you are a command that
       only sets style.
   *   If dryrun is true, you shouldn't actually draw anything.       
  */
  virtual QRectF dataRange(Statement const &s);
  /*:F dataRange
   *:D Commands that actually plot data should implement this and return
       the extent of the data (in axes coordinates). Commands that only
       set style or that annotate based on paper coordinates need not
       implement this.
  */
protected:
  bool error(QString const &);
public:
  static Command *construct(QString x);
  static void addBuilder(QString x, class CBuilder_ *b);
private:
  static QMap<QString, class CBuilder_ *> *builders;
};

class CBuilder_ {
public:
  virtual Command *build()=0;
};

template <class X> class CBuilder: public CBuilder_ {
public:
  CBuilder(QString x) {
    Command::addBuilder(x, this);
  }
  Command *build() {
    return new X();
  }
};
#endif
