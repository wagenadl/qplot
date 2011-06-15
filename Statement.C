// Statement.C

#include "Statement.H"
#include <math.h>
#include <QStringList>


Statement::Statement() {
}

void Statement::reset() {
  toks.clear();
  dat.clear();
}

int Statement::read(QTextStream &source, QString label) {
  lbl = label;
  int nlines = 0;
  reset();

  inString = false;
  lev = 0;

  QString line = source.readLine();
  nlines ++;
  QStringList words = line.split(QRegExp("\\s+"));
  foreach (QString w, words) 
    process(w);

  while (lev>0) {
    QString line = source.readLine();
    nlines ++;
    if (line.isNull())
      break;
    QStringList words = line.split(QRegExp("\\s+"));
    foreach (QString w, words) 
      process(w);
  }
  
  return nlines;
}

void Statement::process(QString w) {
  if (inString) {
    int idx = w.indexOf(strDelim);
    if (idx>0) {
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
    if (w.startsWith("[")) {
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
    } else if (w.size()==1 && w>="A" && w<="Z") {
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

Token const &Statement::operator[](int idx) const {
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
  
  QList<double> v;
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

static QList<double> nullData;

QList<double> const &Statement::data(int idx) const {
  if (cacheVector(idx))
    return dat[idx];
  else
    return nullData;
}

QString const &Statement::label() const {
  return lbl;
}
