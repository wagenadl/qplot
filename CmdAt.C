// CmdAt.C

#include "CmdAt.H"

#define EPSI (1e-25)

static CBuilder<CmdAt> cbAt("at");

bool CmdAt::usage() {
  return error("Usage: at x y [dx dy]");
}

static int horiAlign(QString s) {
  // These numbers are actually meaningfully used in calc, not just an enum. 
  if (s=="left")
    return 0;
  else if (s=="center")
    return 1;
  else if (s=="right")
    return 2;
  else
    return -1;
}

static int vertAlign(QString s) {
  if (s=="top")
    return 0;
  else if (s=="middle")
    return 1;
  else if (s=="bottom")
    return 2;
  else
    return -1;
}
  

bool CmdAt::parse(Statement const &s) {
  if (!(s.length()==3 || s.length()==5))
    return usage();
  if (!(s[1].typ==Token::NUMBER ||
	(s[1].typ==Token::BAREWORD && horiAlign(s[1].str)>=0)))
    return usage();
  if (!(s[2].typ==Token::NUMBER ||
	(s[2].typ==Token::BAREWORD && vertAlign(s[2].str)>=0)))
    return usage();
  if (s.length()==3)
    return true;
  if (s[3].typ!=Token::NUMBER)
    return usage();
  if (s[4].typ!=Token::NUMBER)
    return usage();
  return true;
}

static double slightlyless(double x) {
  double epsi = EPSI;
  double x0 = x-epsi;
  while (x0==x) {
    epsi *= 10;
    x0 = x-epsi;
  }
  return x0;
}
    
static double slightlymore(double x) {
  double epsi = EPSI;
  double x0 = x+epsi;
  while (x0==x) {
    epsi *= 10;
    x0 = x+epsi;
  }
  return x0;
}
    
    

QRectF CmdAt::dataRange(Statement const &s) {
  if (s[1].typ==Token::NUMBER && s[2].typ==Token::NUMBER) {
    double x = s[1].num;
    double y = s[2].num;
    return QRectF(QPointF(slightlyless(x),slightlyless(y)),
		  QPointF(slightlymore(x),slightlymore(y)));
  } else {
    return QRectF();
  }
}
  
void CmdAt::render(Statement const &s, Figure &f, bool) {
  double x = s[1].typ==Token::NUMBER ? s[1].num : f.xAxis().min(); 
  double y = s[2].typ==Token::NUMBER ? s[2].num : f.yAxis().min(); 
  QPointF anchor = f.map(x,y);
  if (s[1].typ==Token::BAREWORD) 
    // that means x is as yet undefined. no matter:
    anchor.setX(f.lastBBox().left()
		+ horiAlign(s[1].str)*f.lastBBox().width()/2);
  if (s[2].typ==Token::BAREWORD) 
    // that means y is as yet undefined. no matter:
    anchor.setY(f.lastBBox().top()
		+ vertAlign(s[2].str)*f.lastBBox().height()/2);
  
  if (s.length()==5) 
    f.setAnchor(anchor, f.angle(s[3].num,s[4].num));
  else 
    f.setAnchor(anchor);
}
