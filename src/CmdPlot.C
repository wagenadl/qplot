// CmdPlot.C

#include "CmdPlot.H"

static CBuilder<CmdPlot> cbPlot("plot");

bool CmdPlot::usage() {
  return error("Usage: plot xdata ydata");
}

bool CmdPlot::parse(Statement const &s) {
  int id1 = s.nextIndex(1);
  int id2 = s.nextIndex(id1);
  if (id2==s.length() && s.isNumeric(1) && s.isNumeric(id1) &&
      s.data(1).size()==s.data(id1).size())
    return true;
  else
    return usage();
}

QRectF CmdPlot::dataRange(Statement const &s) {
  QVector<double> const &xdata = s.data(1);
  QVector<double> const &ydata = s.data(s.nextIndex(1));

  if (xdata.isEmpty())
    return QRectF();

  double minx = xdata[0];
  double maxx = xdata[0];
  double miny = ydata[0];
  double maxy = ydata[0];

  for (int k=1; k<xdata.size(); k++)
    if (xdata[k]<minx)
      minx=xdata[k];
    else if (xdata[k]>maxx)
      maxx=xdata[k];
  for (int k=1; k<ydata.size(); k++)
    if (ydata[k]<miny)
      miny=ydata[k];
    else if (ydata[k]>maxy)
      maxy=ydata[k];
  return QRectF(QPointF(minx,miny), QPointF(maxx,maxy));
}

void CmdPlot::render(Statement const &s, Figure &f, bool dryrun) {
  QVector<double> const &xdata = s.data(1);
  QVector<double> const &ydata = s.data(s.nextIndex(1));
  if (xdata.isEmpty()) {
    f.setBBox(QRectF());
    return;
  }

  QRectF extent = dataRange(s);

  QPointF p1 = f.map(extent.left(),extent.top());
  QPointF p2 = f.map(extent.right(),extent.bottom());
  QRectF bbox = QRectF(p1,p2).normalized();
  double w = f.painter().pen().widthF();
  if (w>0)
    bbox.adjust(-w/2, -w/2, w/2, w/2);
  /* Adjust for line width.
     This does not take protruding miters into account.
  */
  f.setBBox(bbox);

  if (dryrun)
    return;

  QPolygonF p(xdata.size());
  for (int k=0; k<xdata.size(); k++)
    p[k] = f.map(xdata[k],ydata[k]);
  f.painter().drawPolyline(p);

  // now add a zero-thick line if requested
  if (f.hairline()) {
    QPen pen(f.painter().pen());
    f.painter().save();
    pen.setWidth(0);
    f.painter().setPen(pen);
    f.painter().drawPolyline(p);
    f.painter().restore();
  }
}
