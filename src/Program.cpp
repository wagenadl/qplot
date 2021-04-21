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

#include "Error.h"
#include "Program.h"
#include <QDebug>

Program::Program(QString lbl) {
  reset();
  setLabel(lbl);
}

void Program::reset() {
  line = 1;
  isOK = true;
  stmt.clear();
  foreach (Command *c, cmds)
    if (c)
      delete c;
  cmds.clear();
}

void Program::setLabel(QString lbl) {
  label = lbl;
}

void Program::read(QList<Statement> const &ss) {
  reset();
  for (Statement const &s: ss) {
    append(s);
    if (!isOK)
      return;
  }
}

void Program::append(Statement const &s) {
  if (s.length() && s[0].str=="figsize") 
    reset();
  stmt.append(s);
  if (parse(s, line)) 
    line += s.lineCount();
  else 
    isOK = false;
}

bool Program::parse(Statement const &s, int line1) {
  if (s.length()==0) {
    cmds.append(0); // maintain 1:1 b/w statemnts and commands
    return true;
  }

  if (s[0].typ != Token::BAREWORD) {
    Error() << QString("Missing keyword at “%2” line %3")
      .arg(label).arg(line1);
    return false;
  }
      
  Command *c = Command::construct(s[0].str);
  if (!c) {
    Error() << QString("Unknown keyword “%1” at “%2” line %3")
      .arg(s[0].str).arg(label).arg(line1);
    return false;
  }
  
  if (!c->parse(s)) {
    Error() << QString("Syntax error at “%2” line %3")
      .arg(label).arg(line1);
    return false;
  }
  
  cmds.append(c);
  return true;
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
  for (Statement const &s: stmt) 
    if (s.length()>=2 && s[0].str=="panel")
      pp.insert(s[1].str);
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
  f.reset();

  if (!isOK)
    return; // won't render if not ok

  for (int l=0; l<stmt.size(); l++) {
    if (cmds[l]) {
      cmds[l]->render(stmt[l], f, dryrun);
      if (dryrun && f.checkFudged()) {
	f.endGroups();
	break;
      }
    }
  } 

  f.endGroups(); // this prevents panel change warning when file is incomplete
  f.leavePanel();
}
