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
  if (!parse(s, line))
    isOK = false;
  line += s.lineCount();
}

bool Program::parse(Statement const &s, int line1) {
  if (s.length()==0) {
    cmds.append(0); // maintain 1:1 b/w statemnts and commands
    return true;
  }

  if (s[0].typ != Token::BAREWORD) {
    Error() << QString("Missing keyword at “%2” line %3")
      .arg(label).arg(line1);
    cmds.append(0);  // maintain 1:1 b/w statemnts and commands
    return false;
  }
      
  Command *c = Command::construct(s[0].str);
  if (!c) {
    Error() << QString("Unknown keyword “%1” at “%2” line %3")
      .arg(s[0].str).arg(label).arg(line1);
    cmds.append(0);  // maintain 1:1 b/w statemnts and commands
    return false;
  }
  
  if (!c->parse(s)) {
    Error() << QString("Syntax error at “%2” line %3")
      .arg(label).arg(line1);
    cmds.append(0);  // maintain 1:1 b/w statemnts and commands
    return false;
  }
  
  cmds.append(c);
  return true;
}

Program::~Program() {
  reset();
}

int Program::length() const {
  return cmds.size();
}

static Statement nullStatement;

Statement const &Program::operator[](int idx) const {
  if (idx>=0 && idx<stmt.size())
    return stmt[idx];
  else
    return nullStatement;
}

Command const *Program::command(int idx) const {
  if (idx>=0 && idx<cmds.size())
    return cmds[idx];
  else
    return 0;
}

QSet<QString> Program::panels(int upto) {
  QSet<QString> pp;
  pp.insert("-");
  if (upto<0)
    upto = cmds.size();
  for (int k=0; k<upto; k++) {
    Statement const &s(stmt[k]); 
    if (s.length()>=2 && s[0].str=="panel")
      pp.insert(s[1].str);
  }
  return pp;
}

QRectF Program::dataRange(QString p, int upto) {
  QRectF r;
  bool in = p=="-";
  if (upto<0)
    upto = cmds.size();
  for (int k=0; k<upto; k++) {
    Statement const &s(stmt[k]); 
    if (s.length()>=2 && s[0].str=="panel")
      in = s[1].str==p;
    if (in && cmds[k]) {
      Range xl = cmds[k]->xlim(s);
      if (!xl.empty()) {
        r.setLeft(xl.min());
        r.setRight(xl.max());
        continue;
      } 
      Range yl = cmds[k]->ylim(s);
      if (!yl.empty()) {
        r.setTop(yl.min());
        r.setBottom(yl.max());
        continue;
      } 
      QRectF r1 = cmds[k]->dataRange(s);
      if (r1.isValid()) {
        r |= r1;
      }
    }
  }
  return r;
}

void Program::render(Figure &f, bool dryrun, int upto) {
  f.reset();

  if (!isOK)
    return; // won't render if not ok

  if (upto<0) 
    upto = cmds.size();

  for (int l=0; l<upto; l++) {
    if (cmds[l]) {
      cmds[l]->render(stmt[l], f, dryrun);
      if (dryrun && f.checkFudged()) {
	//f.endGroups();
	//break;
      }
    }
  } 

  f.endGroups(); // this prevents panel change warning when file is incomplete
  f.leavePanel();
}
