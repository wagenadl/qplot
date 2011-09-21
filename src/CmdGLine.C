// CmdGLine.C

#include "CmdGLine.H"
#include "Rotate.H"
#include <math.h>

static CBuilder<CmdGLine> cbGLine("gline");
static CBuilder<CmdGLine> cbGArea("garea");

bool CmdGLine::usage() {
  return error("Usage: gline|garea ptspec ...");
}

enum GLineKW {
  KW_ERROR,
  KW_absdata,
  KW_abspaper,
  KW_reldata,
  KW_relpaper,
  KW_rotdata,
  KW_rotpaper,
  KW_retract,
};

static GLineKW glineKW(QString s) {
  if (s=="absdata")
    return KW_absdata;
  else if (s=="abspaper")
    return KW_abspaper;
  else if (s=="reldata")
    return KW_reldata;
  else if (s=="relpaper")
    return KW_relpaper;
  else if (s=="rotdata")
    return KW_rotdata;
  else if (s=="rotpaper")
    return KW_rotpaper;
  else if (s=="retract")
    return KW_retract;
  else
    return KW_ERROR;
}
  
bool CmdGLine::parse(Statement const &s) {
  int k=0;
  while (k<s.length()) {
    if (s[k].typ!=Token::OPENPAREN)
      usage();
    k++;
    if (k>=s.length())
      usage();
    while (s[k].typ!=Token::CLOSEPAREN) {
      if (s[k].typ!=Token::BAREWORD)
        usage();
      GLineKW kw = glineKW(s[k].str);
      if (kw==KW_ERROR)
        usage();
      k++;
      if (k>=s.length())
        usage();
      switch (kw) { // checking first number
      case KW_absdata: case KW_abspaper:
        if (s[k].typ!=Token::NUMBER && s[k].typ!=Token::BAREWORD)
  	usage();
        break;
      default:
        if (s[k].typ!=Token::NUMBER)
  	usage();
        break;
      }
      k++;
      if (k>=s.length())
        usage();
      switch (kw) { // checking second number
      case KW_absdata: case KW_abspaper:
        if (s[k].typ!=Token::NUMBER && s[k].typ!=Token::BAREWORD)
  	usage();
        break;
      case KW_retract:
        if (s[k].typ==Token::CLOSEPAREN)
	  --k; // no second number
        else if (s[k].typ!=Token::NUMBER)
  	usage();
        break;
      case KW_rotpaper:
	--k; // no second number
	break;
      default:
        if (s[k].typ!=Token::NUMBER)
  	usage();
        break;
      }
      k++;
      if (k>=s.length())
        usage();
    }
  }

  return true;
}

void CmdGLine::render(Statement const &s, Figure &f, bool dryrun) {
  QPolygonF pts;
  QVector<double> retractL;
  QVector<double> retractR;

  int k=0;
  while (k<s.length()) {
    // build a new point
    QPointF p(0,0);
    double phi=0;
    double rL=0, rR=0;
    
    k++; // we already know we have parentheses

    while (s[k].typ!=Token::CLOSEPAREN) {
      GLineKW kw = glineKW(s[k].str); // we already know keyword is valid
      QPointF p1;
      switch (kw) {
      case KW_absdata:
        p1 = f.map(s[k+1].typ==Token::NUMBER ? s[k+1].num : f.xAxis().min(),
  		 s[k+2].typ==Token::NUMBER ? s[k+2].num : f.yAxis().min());
        if (s[k+1].typ==Token::NUMBER)
  	p.setX(p1.x());
        if (s[k+2].typ==Token::NUMBER)
  	p.setY(p1.y());
        break;
      case KW_abspaper:
        if (s[k+1].typ==Token::NUMBER)
  	p.setX(s[k+1].num);
        if (s[k+2].typ==Token::NUMBER)
  	p.setY(s[k+2].num);
        break;
      case KW_reldata:
        p1 = f.maprel(s[k+1].num, s[k+2].num);
        p.setX(p.x()+p1.x());
        p.setY(p.y()+p1.y());
        break;
      case KW_relpaper:
        p.setX(p.x()+s[k+1].num*cos(phi) - s[k+2].num*sin(phi));
        p.setY(p.y()+s[k+1].num*sin(phi) + s[k+2].num*cos(phi));
        break;
      case KW_rotdata:
        p1 = f.maprel(s[k+1].num, s[k+2].num);
        phi = atan2(p1.y(), p1.x());
        break;
      case KW_rotpaper:
        phi = s[k+1].num;
        --k; // only one number
        break;
      case KW_retract:
        rL = s[k+1].num;
        if (s[k+2].typ==Token::NUMBER) {
	  rR = s[k+1].num;
        } else {
	  rR = rL;
	  --k; // only one number
        }
	break;
      case KW_ERROR: // cannot happen
        break;
      }
      k+=3; // skip keyword and both numbers
    }
    k++; // skip close paren
    pts.push_back(p);
    retractL.push_back(rL);
    retractR.push_back(rR);
  }

  int N = pts.size();
  QPolygonF pp(N);
  for (int n=0; n<N; n++) {
    QPointF p = pts[n];
    if (n>0 && retractL[n]!=0) {
      QPointF dp = p-pts[n-1];
      double phi = atan2(dp.y(), dp.x());
      p -= QPointF(cos(phi)*retractL[n], sin(phi)*retractL[n]);
    }
    if (n<N-1 && retractR[n]!=0) {
      QPointF dp = p-pts[n+1];
      double phi = atan2(dp.y(), dp.x());
      p -= QPointF(cos(phi)*retractR[n], sin(phi)*retractR[n]);
    }
    pp[n] = p;
  }

  QRectF bbox = pp.boundingRect();
  double w = f.painter().pen().widthF();
  if (w>0)
    bbox.adjust(-w/2, -w/2, w/2, w/2);
  f.setBBox(bbox);

  if (dryrun)
    return;

  if (s[0].str=="garea")
    f.painter().drawPolygon(pp);
  else
    f.painter().drawPolyline(pp);

  if (f.hairline() && s[0].str=="gline") {
    // now add a zero-thick gline
    QPen pen(f.painter().pen());
    f.painter().save();
    pen.setWidth(0);
    f.painter().setPen(pen);
    f.painter().drawPolygon(pp);
    f.painter().restore();
  }
}
