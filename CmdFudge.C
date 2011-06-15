// CmdFudge.C

#include "CmdFudge.H"

static CBuilder<CmdFudge> cbFudge("fudge");

#define FUDGE_DEFAULT 1.0

bool CmdFudge::usage() {
  return error("Usage:\n  fudge\n  fudge margin_pt\n");
}

bool CmdFudge::parse(Statement const &s) {
  if (s.length()==1)
    return true;
  else if (s.length()==2 && s[1].typ==Token::NUMBER)
    return true;
  else
    return usage();
}

void CmdFudge::render(Statement const &s, Figure &f, bool dryrun) {
  double mrg = FUDGE_DEFAULT;
  if (s.length()==2)
    mrg = s[1].num;
  QRectF actual = f.fullBBox();
  QSizeF desired = f.size();

  double dleft = actual.left(); // +ve means it's OK
  double dright = desired.width() - actual.right();
  double dtop =  actual.top();
  double dbottom = actual.bottom() - desired.height();

  QPointF x0 = f.xaxis().minp();
  QPointF x1 = f.xaxis().maxp();
  QPointF y0 = f.yaxis().minp();
  QPointF y1 = f.yaxis().maxp();

  if (dleft<mrg)
    x0 -= QPointF(2*mrg-dleft, 0);
  if (dright<mrg)
    x1 += QPointF(2*mrg-dright, 0);
  if (dtop<mrg)
    y1 -= QPointF(2*mrg-dtop, 0);
  if (dbottom<mrg)
    y0 += QPointF(2*mrg-dbottom, 0);

  f.xAxis().setPlacement(x0, x1);
  f.yAxis().setPlacement(y0, y1);
}

