// Statement.H

#ifndef STATEMENT_H

#define STATEMENT_H

#include "Token.H"
#include <QTextStream>
#include <QMap>
#include <QList>

class Statement {
public:
  Statement();
  int read(QTextStream &source); // returns number of lines processed
  void reset();
  int length() const;
  Token const &operator[](int idx) const;
  bool isNumeric(int idx) const;
  int nextIndex(int idx) const;
  QList<double> const &data(int idx) const; // only valid if isNumeric says so
private:
  void process(QString);
  bool cacheVector(int idx); // true if ok
private:
  QList<Token> toks;
  QMap<int, QList<double> > dat;
  QMap<int, int> nextIdx;
private:
  // while processing:
  bool inString;
  QString strDelim;
  QString str;
  int lev;
};

#endif
