// CmdPen.C

#include "CmdPen.H"
#include <QDebug>

static CBuilder<CmdPen> cbPen("pen");

bool CmdPen::usage() {
  return error("Usage: pen [ID] color|width|miterjoin|beveljoin|roundjoin|flatcap|squarecap|roundcap|solid|dash|dot|dashdot|dashdotdot|none ...");
}

static int strokestyle(QString s) {
  if (s=="solid")
    return Qt::SolidLine;
  else if (s=="dash")
    return Qt::DashLine;
  else if (s=="dot")
    return Qt::DotLine;
  else if (s=="dashdot")
    return Qt::DashDotLine;
  else if (s=="dashdotdot")
    return Qt::DashDotDotLine;
  else if (s=="none")
    return Qt::NoPen;
  else
    return -1;
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
      else if (strokestyle(w)>=0)
	continue;
      else if (QColor(w).isValid())
	continue;
      else
	return usage();
    }
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
      p.setWidthF(s[k].num);
    } else if (s[k].typ==Token::BAREWORD) {
      QString w = s[k].str;
      if (joinstyle(w)>=0)
	p.setJoinStyle(Qt::PenJoinStyle(joinstyle(w)));
      else if (capstyle(w)>=0)
	p.setCapStyle(Qt::PenCapStyle(capstyle(w)));
      else if (strokestyle(w)>=0)
	p.setStyle(Qt::PenStyle(strokestyle(w)));
      else if (QColor(w).isValid())
	p.setColor(w);
      else
	qDebug() << "pen render surprise";
    }
  }
  f.painter().setPen(p);
}


