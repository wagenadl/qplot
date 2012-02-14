// CmdPlot.C

#include "CmdPlot.H"
#include "Rotate.H"

#include <QDebug>

static CBuilder<CmdPlot> cbPlot("plot");
static CBuilder<CmdPlot> cbPatch("patch");
static CBuilder<CmdPlot> cbLine("line");
static CBuilder<CmdPlot> cbArea("area");

bool CmdPlot::usage() {
  return error("Usage: plot|patch|line|area xdata ydata");
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
  if (s[0].str=="line" || s[0].str=="area")
    return QRectF();
  
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

  QPolygonF p(xdata.size());

  if (s[0].str=="plot" || s[0].str=="patch") {
    for (int k=0; k<xdata.size(); k++)
      p[k] = f.map(xdata[k],ydata[k]);
  } else {
    double a = f.anchorAngle();
    QPointF xy0 = f.anchor();
    for (int k=0; k<xdata.size(); k++) {
      QPointF xy(pt2iu(xdata[k]), pt2iu(ydata[k]));
      if (a)
	xy = ::rotate(xy, a);
      xy += xy0;
      p[k] = xy;
    }
  }

  QRectF bbox = p.boundingRect();
  double w = f.painter().pen().widthF();
  if (w>0)
    bbox.adjust(-w/2, -w/2, w/2, w/2);
  /* Adjust for line width.
     This does not take protruding miters into account.
  */
  f.setBBox(bbox);

  if (dryrun)
    return;

  if (s[0].str=="patch" || s[0].str=="area")
    f.painter().drawPolygon(p);
  else
    f.painter().drawPolyline(p);

}
