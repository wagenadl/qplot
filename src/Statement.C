// Statement.C

#include "Statement.H"
#include <math.h>
#include <QStringList>
#include "Error.H"

Statement::Statement() {
}

void Statement::reset() {
  toks.clear();
  dat.clear();
}

int Statement::read(QFile &source, QString label) {
  lbl = label;
  reset();

  inString = false;
  lev = 0;
  dataRefs.clear();

  QString line(QString::fromUtf8(source.readLine()));
  if (line.isNull())
    return 0;
  int nlines = 1;
  
  QStringList words = line.split(QRegExp("\\s+"));
  foreach (QString w, words) 
    process(w);

  while (lev>0) {
    QString line(QString::fromUtf8(source.readLine()));
    if (line.isNull())
      break;
    nlines ++;
    QStringList words = line.split(QRegExp("\\s+"));
    foreach (QString w, words) 
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
	QVector<unsigned char> uc(N);
	source.read((char*)uc.data(), N);
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
	QVector<double> data(N);
	source.read((char*)data.data(), N*sizeof(double));
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
