// Statement.cpp - This file is part of QPlot

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

// Statement.C

#include "Statement.h"
#include <math.h>
#include <QStringList>
#include "Error.h"
#include <iostream>
#include "QRegularExpression"

Statement::Statement() {
  clear();
}

void Statement::clear() {
  toks.clear();
  dat.clear();
  nlines = 0;
}

class Reader {
public:
    Reader(QFile &src): qfile(&src), cin(0), q(true) {}
    Reader(std::istream &src): qfile(0), cin(&src), q(false) {}
    QString readline() {
        if (q) {
            return QString::fromUtf8(qfile->readLine());
        } else {
            std::string s;
            std::getline(*cin, s);
            return QString::fromUtf8(s.data()) + "\n";
        }
    }
    QVector<unsigned char> readbytes(int N) {
        QVector<unsigned char> v(N);
        if (q)
            qfile->read((char*)v.data(), N);
        else
            cin->read((char*)v.data(), N);
    return v;
    }
    QVector<double> readdoubles(int N) {
        QVector<double> v(N);
        if (q)
            qfile->read((char*)v.data(), N*sizeof(double));
        else
            cin->read((char*)v.data(), N*sizeof(double));
    return v;
    }
private:
    QFile *qfile;
    std::istream *cin;
    bool q;
};

int Statement::read(QFile &source, QString label) {
    Reader reader(source);
    return read(reader, label);
}

int Statement::read(std::istream &source, QString label) {
    Reader reader(source);
    return read(reader, label);
}

int Statement::read(Reader &source, QString label) {
  lbl = label;
  clear();

  inString = false;
  lev = 0;
  dataRefs.clear();

  QString line(source.readline());

  if (line.isNull() || !line.endsWith('\n'))
    return 0;

  nlines = 1;
  
  QStringList words = line.split(QRegularExpression("[ \t\n\r]"));
  foreach (QString w, words) 
    if (w.size() || lev || inString)
      process(w);

  while (lev>0) {
    QString line(source.readline());
    if (line.isNull() || !line.endsWith('\n'))
      break;
    nlines ++;
    QStringList words = line.split(QRegularExpression("[ \t\n\r]"));
    foreach (QString w, words)
      if (w.size() || lev || inString)
        process(w);
  }

  QPair<int, QString> x;
  foreach (x, dataRefs) {
    int idx = x.first;
    QString desc = x.second;
    nextIdx[idx] = idx+1;
    bool ok;
    if (desc.startsWith("uc")) {
      // unsigned characters
      int N = desc.mid(2).toInt(&ok);
      if (ok) {
        QVector<unsigned char> uc = source.readbytes(N);
        if (uc.size()<N) {
          Error() << "End-of-file while reading data";
          return 0;
	}
	QVector<double> data(N);
	for (int n=0; n<N; n++)
	  data[n] = uc[n]/255.0;
	dat[idx] = data;
      } else {
	Error() << "Unacceptable data reference";
      }
    } else {
      int N = desc.toInt(&ok);
      if (ok) {
        QVector<double> data = source.readdoubles(N);
        if (data.size()<N) {
	  Error() << "End-of-file while reading data";
	  return 0;
	}
	dat[idx] = data;
      } else {
	Error() << "Unacceptable data reference";
      }
    }
  }
  dataRefs.clear();
  strDelim.clear();
  str.clear();
  return nlines;
}

static bool iscapital(QString w) {
  if (w.isEmpty())
    return false;
  if (w.size()>2)
    return false;
  for (QChar const &c: w) 
    if (c<'A' || c>'Z')
      return false;
  return true;
}

void Statement::process(QString w) {
  if (inString) {
    int idx = w.indexOf(strDelim);
    if (idx>=0) {
      str += w.left(idx);
      w = w.mid(idx+1);
      if (w.startsWith('"') || w.startsWith("'")) {
	// continuation string
	strDelim = w.left(1);
	process(w.mid(1));
      } else {
	toks.append(Token(Token::STRING, str));
	inString = false;
	process(w);
	// or produce error if w not empty
      }
    } else {
      str += w + " ";
    }
  } else {
    if (w=="-") {
      toks.append(Token(Token::DASH, "-"));
    } else if (w.startsWith("[")) {
      toks.append(Token(Token::OPENBRACKET));
      lev++;
      process(w.mid(1));
    } else if (w.startsWith("(")) {
      toks.append(Token(Token::OPENPAREN));
      lev++;
      process(w.mid(1));
    } else if (w.startsWith("'") || w.startsWith('"')) {
      inString = true;
      strDelim = w.left(1);
      process(w.mid(1));
    } else if (w.endsWith("]")) {
      process(w.left(w.size()-1));
      toks.append(Token(Token::CLOSEBRACKET));
      lev--;
    } else if (w.endsWith(")")) {
      process(w.left(w.size()-1));
      toks.append(Token(Token::CLOSEPAREN));
      lev--;
    } else if (w.startsWith("*")) {
      Token t(Token::DATAREF);
      t.str = w.mid(1);
      dataRefs.push_back(QPair<int, QString>(toks.size(), w.mid(1)));
      toks.append(t);
    } else if (iscapital(w)) {
      toks.append(Token(Token::CAPITAL, w));
    } else if (w.isEmpty()) {
      // ignore empty tokens
    } else {
      bool ok;
      double r = w.toDouble(&ok);
      if (ok)
	toks.append(r);
      else
	toks.append(Token(Token::BAREWORD, w));
    }      
  }
}

bool Statement::isNumeric(int idx) const {
  if (idx<0 || idx>=toks.size())
    return false;
  else if (toks[idx].typ==Token::NUMBER)
    return true;
  else if (toks[idx].typ==Token::DASH)
    return true;
  else if (dat.contains(idx))
    return true;
  else if (toks[idx].typ==Token::OPENBRACKET)
    return cacheVector(idx);
  else
    return false;
}

int Statement::nextIndex(int idx) const {
  if (idx<0 || idx>=toks.size())
    return -1;
  else if (toks[idx].typ==Token::NUMBER)
    return idx+1;
  else if (toks[idx].typ==Token::DASH)
    return idx+1;
  else if (cacheVector(idx))
    return nextIdx[idx];
  else
    return idx+1;
}

static Token nullToken;

Token const &Statement::token(int idx) const {
  if (idx>=0 && idx<toks.size())
    return toks[idx];
  else
    return nullToken;
}

int Statement::length() const {
  return toks.size();
}

bool Statement::cacheVector(int idx) const {
  if (dat.contains(idx))
    return true;
  else if (idx<0 || idx>=toks.size())
    return false;
  
  QVector<double> v;
  if (toks[idx].typ == Token::NUMBER) {
    v.append(toks[idx].num);
    nextIdx[idx] = idx+1;
    dat[idx] = v;
    return true;
  } else if (toks[idx].typ == Token::DASH) {
    v.append(nan(""));
    nextIdx[idx] = idx+1;
    dat[idx] = v;
    return true;
  } else if (toks[idx].typ == Token::OPENBRACKET) {
    int i = idx;
    while (++i < toks.size()) {
      if (toks[i].typ==Token::CLOSEBRACKET) {
	nextIdx[idx] = i+1;
	dat[idx] = v;
	return true;
      } else if (toks[i].typ==Token::NUMBER)
	v.append(toks[i].num);
      else if (toks[i].typ==Token::DASH)
	v.append(nan(""));
      else
	return false; // this is an error
    }
    return false;
  } else {
    return false;
  }
}

static QVector<double> nullData;

QVector<double> const &Statement::data(int idx) const {
  if (cacheVector(idx))
    return dat[idx];
  else
    return nullData;
}

QString const &Statement::label() const {
  return lbl;
}

int Statement::lineCount() const {
  return nlines;
}
