// CmdAt.C

#include "CmdAt.H"

#define EPSI (1e-25)

static CBuilder<CmdAt> cbAt("at");

bool CmdAt::usage() {
  return error("Usage: at x y [dx dy]|phi | -");
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
  if (s.length()==2 && s[1].typ==Token::DASH)
    return true;
  if (s.length()<3)
    return usage();
  if (!(s[1].typ==Token::NUMBER || s[1].typ==Token::DASH ||
	(s[1].typ==Token::BAREWORD && horiAlign(s[1].str)>=0)))
    return usage();
  if (!(s[2].typ==Token::NUMBER || s[2].typ==Token::DASH ||
	(s[2].typ==Token::BAREWORD && vertAlign(s[2].str)>=0)))
    return usage();
  if (s.length()==3)
    return true;
  if (s[3].typ!=Token::NUMBER)
    return usage();
  if (s.length()==4)
    return true;
  if (s[4].typ!=Token::NUMBER)
    return usage();
  return s.length()==5;
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
  if (s.length()<=2) {
    f.setAnchor(QPointF(0,0));
    return;
  }
  
  double x = s[1].typ==Token::NUMBER ? s[1].num : f.xAxis().min(); 
  double y = s[2].typ==Token::NUMBER ? s[2].num : f.yAxis().min(); 
  QPointF anchor = f.map(x,y);
  if (s[1].typ==Token::BAREWORD) {
    // that means x is as yet undefined. no matter:
    int a = horiAlign(s[1].str);
    anchor.setX(f.lastBBox().left()
		+ a*f.lastBBox().width()/2);
  } else if (s[1].typ==Token::DASH) {
    anchor.setX(0);
  }
  if (s[2].typ==Token::BAREWORD) {
    // that means y is as yet undefined. no matter:
    int a = vertAlign(s[2].str);
    anchor.setY(f.lastBBox().top()
		+ a*f.lastBBox().height()/2);
  } else if (s[2].typ==Token::DASH) {
    anchor.setY(0);
  }
  
  if (s.length()==5) 
    f.setAnchor(anchor, f.angle(s[3].num,s[4].num));
  else if (s.length()==4)
    f.setAnchor(anchor, s[3].num);
  else 
    f.setAnchor(anchor);
}
