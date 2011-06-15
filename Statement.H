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
  int read(QTextStream &source, QString label); // returns number of lines processed
  void reset();
  int length() const;
  Token const &operator[](int idx) const;
  bool isNumeric(int idx) const;
  int nextIndex(int idx) const;
  QList<double> const &data(int idx) const; // only valid if isNumeric says so
  QString const &label() const;
private:
  void process(QString);
  bool cacheVector(int idx) const; // true if ok
private:
  QString lbl;
  QList<Token> toks;
  mutable QMap<int, QList<double> > dat;
  mutable QMap<int, int> nextIdx;
private:
  // while processing:
  bool inString;
  QString strDelim;
  QString str;
  int lev;
};

#endif
