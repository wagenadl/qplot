// CmdPen.C

#include "CmdPen.H"
#include <QDebug>

static CBuilder<CmdPen> cbPen("pen");

#define PEN_DEFAULTLENGTH 3

bool CmdPen::usage() {
  return error("Usage: pen [ID] color | width | miterjoin|beveljoin|roundjoin | flatcap|squarecap|roundcap | solid|none | dash [L1 ...] | dot L ...");
}

static int joinstyle(QString s) {
  if (s=="miterjoin")
    return Qt::MiterJoin;
  else if (s=="beveljoin")
    return Qt::BevelJoin;
  else if (s=="roundjoin")
    return Qt::RoundJoin;
  else
    return -1;
}

static int capstyle(QString s) {
  if (s=="flatcap")
    return Qt::FlatCap;
  else if (s=="squarecap")
    return Qt::SquareCap;
  else if (s=="roundcap")
    return Qt::RoundCap;
  else
    return -1;
}

bool CmdPen::parse(Statement const &s) {
  if (s.length()<2)
    return usage();
  for (int k=1; k<s.length(); k++) {
    if (s[k].typ==Token::CAPITAL && k==1) {
      continue; // OK, this is pen choice
    } else if (s[k].typ==Token::NUMBER) {
      continue; // OK, this is width
    } else if (s[k].typ==Token::BAREWORD) {
      QString w = s[k].str;
      if (joinstyle(w)>=0)
	continue;
      else if (capstyle(w)>=0)
	continue;
      else if (w=="solid" || w=="none")
	continue;
      else if (w=="dash" || w=="dot") {
	if (k+1<s.length() && s.isNumeric(k+1)) {
	  k=s.nextIndex(k)-1;
	  if (k>0)
	    continue;
	  else
	    return usage(); // Bad vector is not OK
	} else {
	  continue; // OK if no vector follows
	}
      } else if (QColor(w).isValid())
	continue;
      else
	return usage();
    } else
      return usage();
  }
  return true;
}

void CmdPen::render(Statement const &s, Figure &f, bool) {
  QPen p(f.painter().pen());
  for (int k=1; k<s.length(); k++) {
    if (s[k].typ==Token::CAPITAL && k==1) {
      f.painter().setPen(p);
      f.choosePen(s[k].str);
      p = f.painter().pen();
    } else if (s[k].typ==Token::NUMBER) {
      p.setWidthF(pt2iu(s[k].num));
      if (p.style()==Qt::NoPen)
	p.setStyle(Qt::SolidLine);
    } else if (s[k].typ==Token::BAREWORD) {
      QString w = s[k].str;
      if (joinstyle(w)>=0)
	p.setJoinStyle(Qt::PenJoinStyle(joinstyle(w)));
      else if (capstyle(w)>=0)
	p.setCapStyle(Qt::PenCapStyle(capstyle(w)));
      else if (w=="none")
	p.setStyle(Qt::NoPen);
      else if (w=="solid")
	p.setStyle(Qt::SolidLine);
      else if (w=="dash") {
	double w = p.widthF();
	if (w==0)
	  w = f.dashScale()/f.painter().transform().m11();
	QVector<qreal> pat;
	bool flatcap = p.capStyle()==Qt::FlatCap;
	if (k+1<s.length() && s.isNumeric(k+1)) {
	  foreach (double x, s.data(k+1)) {
	    if (x==0) 
	      pat.push_back(flatcap ? 1 : .001);
	    else 
	      pat.push_back(pt2iu(x)/w);
	  }
	} else {
	  pat.push_back(pt2iu(PEN_DEFAULTLENGTH)/w);
	}
	int L = pat.size();
	if (L&1)
	  for (int l=0; l<L; l++)
	    pat.push_back(pat[l]);
	p.setDashPattern(pat);
	k = s.nextIndex(k+1)-1;
      } else if (w=="dot") {
	double w = p.widthF();
	if (w==0)
	  w = f.dashScale()/f.painter().transform().m11();
	QVector<qreal> pat;
	bool flatcap = p.capStyle()==Qt::FlatCap;
	if (k+1<s.length() && s.isNumeric(k+1)) {
	  foreach (double x, s.data(k+1)) {
	    pat.push_back(flatcap ? 1 : 0.001);
	    pat.push_back(pt2iu(x)/w);
	  }
	} else {
	  pat.push_back(0.001);
	  pat.push_back(pt2iu(PEN_DEFAULTLENGTH)/w);
	}
	p.setDashPattern(pat);	
	k = s.nextIndex(k+1)-1;
      } else if (QColor(w).isValid()) {
	p.setColor(w);
	if (p.style()==Qt::NoPen)
	  p.setStyle(Qt::SolidLine);
      } else
	qDebug() << "pen render surprise";
    }
  }
  f.painter().setPen(p);
}


