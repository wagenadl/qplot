// CmdPlot.C

#include "CmdPlot.H"

static CommandBuilder cbPlot("plot", &CmdPlot::construct);

CmdPlot::CmdPlot() {
}

CmdPlot::~CmdPlot() {
}

bool CmdPlot::usage() {
  return error("Usage:\n  plot xdata ydata\n");
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


QRectF CmdPlot::bounds(Statement const &s, Figure &f) {
  QList<double> const &xdata = s.data(1);
  QList<double> const &ydata = s.data(s.nextIndex(1));
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
  QPointF tl = f.xAxis().map(minx) + f.yAxis().map(miny);
  QPointF br = f.xAxis().map(maxx) + f.yAxis().map(maxy);
  return QRectF(tl,br).normalized(); 
}

void CmdPlot::render(Statement const &s, Figure &f) {
  QList<double> const &xdata = s.data(1);
  QList<double> const &ydata = s.data(s.nextIndex(1));
  QPolygonF p(xdata.size());
  for (int k=0; k<xdata.size(); k++)
    p[k] = f.xAxis().map(xdata[k]) + f.yAxis().map(ydata[k]);
  f.painter().drawPolyline(p);
}
