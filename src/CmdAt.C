// CmdAt.C

#include "CmdAt.H"
#include <QDebug>
#include "Slightly.H"

static CBuilder<CmdAt> cbAt("at");

bool CmdAt::usage() {
  return error("Usage: at x y [dx dy]|phi | - | x y ID | ID");
}

static bool isAbs(QString s) {
  if (s=="abs")
    return true;
  else if (s=="absolute")
    return true;
  else
    return false;
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
  if (s.length()<2)
    return usage();
  if (s[1].typ==Token::CAPITAL) {
    switch (s.length()) {
    case 2:
      return true;
    case 3:
      return s[2].typ==Token::NUMBER ? true : usage();
    case 4:
      return (s[2].typ==Token::NUMBER && s[3].typ==Token::NUMBER)
	? true : usage();
    default:
      return usage();
    }
  }
  if (s.length()==2 && s[1].typ==Token::DASH)
    return true;
  else if (s.length()<3)
    return usage();
  
  if (!(s[1].typ==Token::NUMBER || s[1].typ==Token::DASH ||
	(s[1].typ==Token::BAREWORD &&
	 (horiAlign(s[1].str)>=0 || isAbs(s[1].str)))))
    return usage();

  if (!(s[2].typ==Token::NUMBER || s[2].typ==Token::DASH ||
	(s[2].typ==Token::BAREWORD
	 && (vertAlign(s[2].str)>=0 || isAbs(s[2].str)))))
    return usage();

  if (s.length()==3)
    return true;

  if (s[3].typ==Token::CAPITAL && s.length()==4)
    return true;

  if (s[3].typ!=Token::NUMBER)
    return usage();

  if (s.length()==4)
    return true;

  if (s[4].typ!=Token::NUMBER)
    return usage();

  return s.length()==5 ? true : usage();
}

    

QRectF CmdAt::dataRange(Statement const &s) {
  if (s.length()<3)
    return QRectF();
  
  if (s[1].typ==Token::NUMBER && s[2].typ==Token::NUMBER) {
    double x = s[1].num;
    double y = s[2].num;
    return QRectF(QPointF(Slightly::less(x),Slightly::less(y)),
		  QPointF(Slightly::more(x),Slightly::more(y)));
  } else {
    return QRectF();
  }
}
  
void CmdAt::render(Statement const &s, Figure &f, bool) {
  if (s[1].typ==Token::CAPITAL) {
    switch (s.length()) {
    case 2:
      f.setAnchor(f.getLocation(s[1].str));
      return;
    case 3:
      f.setAnchor(f.getLocation(s[1].str), s[2].num);
      return;
    case 4:
      f.setAnchor(f.getLocation(s[1].str), f.angle(s[2].num,s[3].num));
      return;
    }
    qDebug() << "Unexpected syntax in AT";
  } 

  if (s.length()<=2) {
    f.setAnchor(f.extent().topLeft());
    return;
  }

  QPointF oldAnc = f.anchor();
  qDebug() << oldAnc;
  
  double x = s[1].typ==Token::NUMBER ? s[1].num : f.xAxis().min(); 
  double y = s[2].typ==Token::NUMBER ? s[2].num : f.yAxis().min(); 
  QPointF anchor = f.map(x,y);

  if (s[1].typ==Token::BAREWORD) {
    // that means x is as yet undefined. no matter:
    if (isAbs(s[1].str)) {
      anchor.setX(f.extent().left());
    } else {
      int a = horiAlign(s[1].str);
      anchor.setX(f.lastBBox().left()
		  + a*f.lastBBox().width()/2);
    }
  } else if (s[1].typ==Token::DASH) {
    anchor.setX(oldAnc.x());
    qDebug() << "using old X";
  }
  
  if (s[2].typ==Token::BAREWORD) {
    // that means y is as yet undefined. no matter:
    if (isAbs(s[2].str)) {
      anchor.setY(f.extent().top());
    } else {
      int a = vertAlign(s[2].str);
      anchor.setY(f.lastBBox().top()
		  + a*f.lastBBox().height()/2);
    }
  } else if (s[2].typ==Token::DASH) {
    anchor.setY(oldAnc.y());
    qDebug() << "using old Y";
  }

  switch (s.length()) {
  case 5:
    f.setAnchor(anchor, f.angle(s[3].num,s[4].num));
    break;
  case 4:
    if (s[3].typ==Token::CAPITAL)
      f.setLocation(s[3].str, anchor);
    else
      f.setAnchor(anchor, s[3].num);
    break;
  case 3: 
    f.setAnchor(anchor);
    break;
  default:
    qDebug() << "Unexpected syntax in AT";
  }
}
