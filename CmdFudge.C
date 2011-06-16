// CmdFudge.C

#include "CmdFudge.H"
#include <QDebug>

static CBuilder<CmdFudge> cbFudge("fudge");

#define FUDGE_DEFAULT 1.0

bool CmdFudge::usage() {
  return error("Usage: fudge [margin_pt]\n");
}

bool CmdFudge::parse(Statement const &s) {
  if (s.length()==1)
    return true;
  else if (s.length()==2 && s[1].typ==Token::NUMBER)
    return true;
  else
    return usage();
}

void CmdFudge::render(Statement const &s, Figure &f, bool) {
  double mrg = FUDGE_DEFAULT;
  if (s.length()==2)
    mrg = s[1].num;
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

  if (dleft<mrg)
    x0 += QPointF(2*mrg-dleft, 0);
  if (dright<mrg)
    x1 -= QPointF(2*mrg-dright, 0);
  if (dtop<mrg)
    y1 += QPointF(0, 2*mrg-dtop);
  if (dbottom<mrg)
    y0 -= QPointF(0, 2*mrg-dbottom);

  f.xAxis().setPlacement(x0, x1);
  f.yAxis().setPlacement(y0, y1);
}

