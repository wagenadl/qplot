// Statement.H - This file is part of QPlot

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

// Statement.H

#ifndef STATEMENT_H

#define STATEMENT_H

#include "Token.h"
#include <QFile>
#include <QMap>
#include <QList>
#include <QPair>
#include <QVector>

class Statement {
public:
  Statement();
  int read(QFile &source, QString label=QString()); // returns number of lines processed
  int read(std::istream &source, QString label=QString()); // returns number of lines processed
  int read(class Reader &source, QString label=QString()); // returns number of lines processed
  void clear();
  int lineCount() const; // number of lines processed
  int length() const; // number of tokens
  Token const &operator[](int idx) const; // returns null token if out-of-range
  bool isNumeric(int idx) const; // true if token is number, numeric vector or "-"
  int nextIndex(int idx) const; // skips over multitoken vectors
  
  QVector<double> const &data(int idx) const; // only valid if isNumeric says so
  QString const &label() const; // label passed to read(), if any
private:
  void process(QString);
  bool cacheVector(int idx) const; // true if ok
private:
  QString lbl;
  QList<Token> toks;
  mutable QMap<int, QVector<double> > dat; // cachevector changes this
  mutable QMap<int, int> nextIdx; // cacheVector changes this
  int nlines;
private:
  // while processing:
  bool inString;
  QString strDelim;
  QString str;
  int lev;
  QVector< QPair<int, QString> > dataRefs;
};

#endif
