// CmdLine.C

#include "CmdLine.H"
#include "Rotate.H"

static CBuilder<CmdLine> cbLine("line");

bool CmdLine::usage() {
  return error("Usage: line xdata ydata");
}

bool CmdLine::parse(Statement const &s) {
  int id1 = s.nextIndex(1);
  int id2 = s.nextIndex(id1);
  if (id2==s.length() && s.isNumeric(1) && s.isNumeric(id1) &&
      s.data(1).size()==s.data(id1).size())
    return true;
  else
    return usage();
}

void CmdLine::render(Statement const &s, Figure &f, bool dryrun) {
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

  f.painter().drawPolyline(p);

  if (f.hairline()) {
    // now add a zero-thick line
    QPen pen(f.painter().pen());
    f.painter().save();
    pen.setWidth(0);
    f.painter().setPen(pen);
    f.painter().drawPolyline(p);
    f.painter().restore();
  }
}
