// Program.C

#include "Program.H"
#include <QDebug>

Program::Program() {
}

bool Program::error(QString const &s) {
  qDebug() << s;
  return false;
}

bool Program::error(QString const &s, int l) {
  return error(s + " at " + stmt[l].label());
}

bool Program::read(QTextStream &ts, QString label) {
  int line = 1; // count lines in a file from 1
  while (!ts.atEnd()) {
    stmt.append(Statement());
    QString ll = label + " line " + QString::number(line);
    line += stmt.last().read(ts, ll);
  }

  bool ok = true;

  for (int l=0; l<stmt.size(); l++) {
    if (stmt[l].length()==0) {
      cmds.append(0);
    } else if (stmt[l][0].typ == Token::BAREWORD) {
      cmds.append(Command::construct(stmt[l][0].str));
      if (!cmds[l]) 
	ok = error("Unknown keyword", l);
      else if (!cmds[l]->parse(stmt[l]))
	ok = error("Syntax error", l);
    } else {
      qDebug() << stmt[l].length();
      qDebug() << stmt[l][0].typ << stmt[l][0].num << stmt[l][0].str;
      ok = error("Commands should start with a keyword", l);
    }
  }
  return ok;  
}

Program::~Program() {
  foreach (Command *c, cmds)
    if (c)
      delete c;
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
  
void Program::render(Figure &f, bool dryrun) {
  f.clearBBox(true);
  for (int l=0; l<stmt.size(); l++)
    if (cmds[l])
      cmds[l]->render(stmt[l], f, dryrun);
}
