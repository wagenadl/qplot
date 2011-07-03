// CmdArea.C

#include "CmdArea.H"
#include "Rotate.H"

static CBuilder<CmdArea> cbArea("area");

bool CmdArea::usage() {
  return error("Usage: area xdata ydata");
}

bool CmdArea::parse(Statement const &s) {
  int id1 = s.nextIndex(1);
  int id2 = s.nextIndex(id1);
  if (id2==s.length() && s.isNumeric(1) && s.isNumeric(id1) &&
      s.data(1).size()==s.data(id1).size())
    return true;
  else
    return usage();
}

void CmdArea::render(Statement const &s, Figure &f, bool dryrun) {
  QVector<double> const &xdata = s.data(1);
  QVector<double> const &ydata = s.data(s.nextIndex(1));
  if (xdata.isEmpty()) 
    return;

  QPolygonF p(xdata.size());
  double a = f.anchorAngle();
  QPointF xy0 = f.anchor();
  for (int k=0; k<xdata.size(); k++) {
    QPointF xy(pt2iu(xdata[k]), pt2iu(ydata[k]));
    if (a)
      xy = ::rotate(xy, a);
    xy += xy0;
    p[k] = xy;
  }
  QRectF bbox = p.boundingRect();
  double w = f.painter().pen().widthF();
  if (w>0)
    bbox.adjust(-w/2, -w/2, w/2, w/2);
  f.setBBox(bbox);

  if (dryrun)
    return;

  f.painter().drawPolygon(p);
}
