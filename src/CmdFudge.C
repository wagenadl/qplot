// CmdFudge.C

#include "CmdFudge.H"
#include <QDebug>
#include <math.h>
#include "Error.H"

static CBuilder<CmdFudge> cbFudge("fudge");

#define FUDGE_DEFAULT 0.2

bool CmdFudge::usage() {
  return error("Usage: fudge [margin_pt] [ratio]\n");
}

bool CmdFudge::parse(Statement const &s) {
  if (s.length()==1)
    return true;
  else if (s.length()==2 && s[1].typ==Token::NUMBER)
    return true;
  else if (s.length()==3 && (s[1].typ==Token::NUMBER || s[1].typ==Token::DASH)
	   && (s[2].typ==Token::NUMBER))
    return true;
  else
    return usage();
}

void CmdFudge::render(Statement const &s, Figure &f, bool) {
  double mrg = pt2iu(FUDGE_DEFAULT);
  if (s.length()>=2 && s[1].typ==Token::NUMBER)
    mrg = pt2iu(s[1].num);
  bool hasRatio = s.length()>=3;
  double ratio = s[2].num;
  QRectF actual = f.fullBBox();
  QRectF desired = f.extent();

  double dleft = actual.left() - desired.left(); // +ve means it's OK
  double dright = desired.right() - actual.right();
  double dtop =  actual.top() - desired.top();
  double dbottom = desired.bottom() - actual.bottom();

  QPointF x0 = f.xAxis().minp();
  QPointF x1 = f.xAxis().maxp();
  QPointF y0 = f.yAxis().minp();
  QPointF y1 = f.yAxis().maxp();

  //qDebug() << "fudge" << dleft << dright << dtop << dbottom << mrg;
  //qDebug() << "  " << x0 << x1 << y0 << y1;

  double olddx = x1.x()-x0.x();
  double olddy = y1.y()-y0.y();
  
  if (dleft<mrg)
    x0 += QPointF(2*mrg-dleft, 0);
  if (dright<mrg)
    x1 -= QPointF(2*mrg-dright, 0);
  if (dtop<mrg)
    y1 += QPointF(0, 2*mrg-dtop);
  if (dbottom<mrg)
    y0 -= QPointF(0, 2*mrg-dbottom);

  double newdx = x1.x()-x0.x();
  double newdy = y1.y()-y0.y();

  if (newdx < .5*olddx || newdy < .5*olddy) {
    Error() << "Fudge failed";
    return;
  }

  if (hasRatio) {
    double dpx = fabs(x1.x() - x0.x());
    double dpy = fabs(y1.y() - y0.y());
    double xrat = fabs(dpx / (f.xAxis().max() - f.xAxis().min()));
    double yrat = fabs(dpy / (f.yAxis().max() - f.yAxis().min()));
    double myrat = yrat/xrat;
    qDebug() << dpx << dpy << xrat << yrat << myrat << ratio;
    if (myrat>ratio) {
      // I am too tall
      y1 += QPointF(0, .5*dpy*(1-ratio/myrat));
      y0 -= QPointF(0, .5*dpy*(1-ratio/myrat));
    } else if (myrat<ratio) {
      // I am too wide
      x1 -= QPointF(.5*dpx*(1-myrat/ratio), 0);
      x0 += QPointF(.5*dpx*(1-myrat/ratio), 0);
    }
  }      

  f.xAxis().setPlacement(x0, x1);
  f.yAxis().setPlacement(y0, y1);
}

