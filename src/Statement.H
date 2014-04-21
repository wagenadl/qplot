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

#include "Token.H"
#include <QFile>
#include <QMap>
#include <QList>
#include <QPair>
#include <QVector>

class Statement {
public:
  Statement();
  int read(QFile &source, QString label); // returns number of lines processed
  void reset();
  int length() const;
  Token const &operator[](int idx) const;
  bool isNumeric(int idx) const;
  int nextIndex(int idx) const;
  
  QVector<double> const &data(int idx) const; // only valid if isNumeric says so
  QString const &label() const;
private:
  void process(QString);
  bool cacheVector(int idx) const; // true if ok
private:
  QString lbl;
  QList<Token> toks;
  mutable QMap<int, QVector<double> > dat;
  mutable QMap<int, int> nextIdx;
private:
  // while processing:
  bool inString;
  QString strDelim;
  QString str;
  int lev;
  QVector< QPair<int, QString> > dataRefs;
};

#endif
