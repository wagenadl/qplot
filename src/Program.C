// Program.C

#include "Program.H"
#include <QDebug>
#include "Error.H"

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

bool Program::read(QFile &ts, QString label) {
  isOK = false;
  stmt.clear();
  foreach (Command *c, cmds)
    if (c)
      delete c;
  cmds.clear();
  
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

  bool ok = true;

  for (int l=0; l<stmt.size(); l++) {
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
  if (!isOK)
    return; // won't render if not ok
  f.reset();
  for (int l=0; l<stmt.size(); l++)
    if (cmds[l])
      cmds[l]->render(stmt[l], f, dryrun);
  f.leavePanel();
}
