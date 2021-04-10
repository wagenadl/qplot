// Program.cpp - This file is part of QPlot

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

// Program.C

#include "Program.h"
#include <QDebug>
#include "Error.h"

Program::Program() {
  isOK = false;
}

bool Program::error(QString const &s) {
  Error() << s;
  return false;
}

bool Program::error(QString const &s, int l) {
  return error(s + " at " + stmt[l].label());
}

void Program::reset() {
  isOK = false;
  stmt.clear();
  foreach (Command *c, cmds)
    if (c)
      delete c;
  cmds.clear();
}

bool Program::read(QFile &ts, QString label) {
  reset();  
  int line = 1; // count lines in a file from 1
  while (!ts.atEnd()) {
    stmt.append(Statement());
    QString ll = label + " line " + QString::number(line);
    int dn = stmt.last().read(ts, ll);
    if (dn)
      line += dn;
    else
      return error("Read error");
  }
  return parse(true);
}

bool Program::append(QFile &ts, QString label, bool all) {
  int line = stmt.size() + 1;
  bool hasreset = false;
  bool first = true;
  // actually, canReadLine does not work on stdin, so
  // we rely on the socket notifier to call us repeatedly
  while (first || (all ? !ts.atEnd() : ts.canReadLine())) {
    first = false;
    stmt.append(Statement());
    QString ll = label + " line " + QString::number(line);
    int dn = stmt.last().read(ts, ll);
    if (dn)
      line += dn;
    else
      return error("Read error");
    if (stmt.last()[0].str=="figsize") {
      Statement s = stmt.last();
      reset();
      line = 1;
      stmt.append(s);
      hasreset = true;
    }
  }
  return parse(hasreset);
}    

bool Program::parse(bool fromscratch) {
  if (fromscratch) {
    foreach (Command *c, cmds)
      delete c;
    cmds.clear();
  }

  bool ok = true;

  for (int l=cmds.size(); l<stmt.size(); l++) {
    if (stmt[l].length()==0) {
      cmds.append(0);
    } else if (stmt[l][0].typ == Token::BAREWORD) {
      cmds.append(Command::construct(stmt[l][0].str));
      if (!cmds[l]) 
	ok = error("Unknown keyword: " + stmt[l][0].str, l);
      else if (!cmds[l]->parse(stmt[l]))
	ok = error("Syntax error", l);
    } else {
      ok = error("Commands should start with a keyword", l);
    }
  }
  isOK = ok;
  return ok;  
}

Program::~Program() {
  reset();
}

int Program::length() const {
  return stmt.size();
}

static Statement nullStatement;

Statement const &Program::operator[](int idx) const {
  if (idx>=0 && idx<stmt.size())
    return stmt[idx];
  else
    return nullStatement;
}

QSet<QString> Program::panels() {
  QSet<QString> pp;
  pp.insert("-");
  for (int l=0; l<stmt.size(); l++) 
    if (stmt[l].length()>=2 && stmt[l][0].str=="panel")
      pp.insert(stmt[l][1].str);
  return pp;
}

QRectF Program::dataRange(QString p) {
  QRectF r;
  bool in = p=="-";
  for (int l=0; l<stmt.size(); l++) {
    if (stmt[l].length()>=2 && stmt[l][0].str=="panel")
      in = stmt[l][1].str==p;
    if (in && cmds[l])
      r |= cmds[l]->dataRange(stmt[l]);
  }
  return r;
}

void Program::render(Figure &f, bool dryrun) {
  //qDebug() << "Prorgram ok: " << isOK;
  f.reset();
  //qDebug() << "Program: fudged0? " << f.checkFudged();
  if (!isOK)
    return; // won't render if not ok
  for (int l=0; l<stmt.size(); l++) {
    if (cmds[l]) {
      cmds[l]->render(stmt[l], f, dryrun);
      if (dryrun && f.checkFudged()) {
	//qDebug() << "Program: fudged! " << stmt[l].label() << ": " << stmt[l][0].str;
	f.endGroups();
	break;
      }
    }
  } 
  //qDebug() << "Program: fudged? " << f.checkFudged();
  f.endGroups(); // this prevents panel change warning when file is incomplete
  f.leavePanel();
}
