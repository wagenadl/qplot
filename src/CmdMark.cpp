// CmdMark.C

#include "CmdMark.H"
#include <math.h>
#include <QPolygonF>
#include "Rotate.H"
#include "Slightly.H"

static CBuilder<CmdMark> cbMark("mark");
static CBuilder<CmdMark> cbPMark("pmark");

bool CmdMark::usage() {
  return error("Usage: mark|pmark xdata ydata");
}

static void rendermark(QPainter &p, QPointF const &xy,
		       double r, Marker::Type t, bool asSpine) {
  QPolygonF pf;
  switch (t) {
  case Marker::CIRCLE:
    p.drawEllipse(xy, r, r);
    break;
  case Marker::SQUARE:
    r *= sqrt(M_PI/4);
    if (asSpine) {
      p.drawLine(QPointF(xy)+QPointF(-r,-r), QPointF(xy)+QPointF(r,r));
      p.drawLine(QPointF(xy)+QPointF(-r,r), QPointF(xy)+QPointF(r,-r));
    } else {
      p.drawRect(QRectF(xy + QPointF(-r,-r), QSizeF(2*r, 2*r)));
    }
    break;
  case Marker::DIAMOND: 
    r *= sqrt(2*M_PI/4);
    pf.resize(4);
    pf[0] = xy + QPointF(-r, 0);
    pf[1] = xy + QPointF(0, -r);
    pf[2] = xy + QPointF(r, 0);
    pf[3] = xy + QPointF(0, r);
    if (asSpine) {
      p.drawLine(pf[0], pf[2]);
      p.drawLine(pf[1], pf[3]);
    } else {
      p.drawConvexPolygon(pf);
    }
    break;
  case Marker::LEFTTRIANGLE:
    r *= 2./3;
    pf.resize(3);
    pf[0] = xy + QPointF(-2*r, 0);
    pf[1] = xy + QPointF(r, -sqrt(3)*r);
    pf[2] = xy + QPointF(r, sqrt(3)*r);
    if (asSpine) {
      p.drawLine(xy, pf[0]);
      p.drawLine(xy, pf[1]);
      p.drawLine(xy, pf[2]);
    } else {
      p.drawConvexPolygon(pf);
    }
    break;
  case Marker::DOWNTRIANGLE:
    r *= 2./3;
    pf.resize(3);
    pf[0] = xy + QPointF(0, 2*r);
    pf[1] = xy + QPointF(-sqrt(3)*r, -r);
    pf[2] = xy + QPointF(sqrt(3)*r, -r);
    if (asSpine) {
      p.drawLine(xy, pf[0]);
      p.drawLine(xy, pf[1]);
      p.drawLine(xy, pf[2]);
    } else {
      p.drawConvexPolygon(pf);
    }
    break;
  case Marker::RIGHTTRIANGLE:
    r *= 2./3;
    pf.resize(3);
    pf[0] = xy + QPointF(2*r, 0);
    pf[1] = xy + QPointF(-r, sqrt(3)*r);
    pf[2] = xy + QPointF(-r, -sqrt(3)*r);
    if (asSpine) {
      p.drawLine(xy, pf[0]);
      p.drawLine(xy, pf[1]);
      p.drawLine(xy, pf[2]);
    } else {
      p.drawConvexPolygon(pf);
    }
    break;
  case Marker::UPTRIANGLE:
    r *= 2./3;
    pf.resize(3);
    pf[0] = xy + QPointF(0, -2*r);
    pf[1] = xy + QPointF(-sqrt(3)*r, r);
    pf[2] = xy + QPointF(sqrt(3)*r, r);
    if (asSpine) {
      p.drawLine(xy, pf[0]);
      p.drawLine(xy, pf[1]);
      p.drawLine(xy, pf[2]);
    } else {
      p.drawConvexPolygon(pf);
    }
    break;
  case Marker::PENTAGRAM: {
    r *= .5 + .5*sqrt(5);
    double r1 = .5*sqrt(5)-.5;
    r1=r1*r1;
    pf.resize(10);
    for (int k=0; k<10; k++) {
      double dy = -r*cos(2*M_PI*k/10);
      double dx = r*sin(2*M_PI*k/10);
      if (k&1) {
	dx *= r1;
	dy *= r1;
      }
      pf[k] = xy + QPointF(dx, dy);
    }
    if (asSpine) {
      for (int k=0; k<10; k+=2)
	p.drawLine(xy, pf[k]);
    } else {
      p.drawPolygon(pf);
    }
  } break;
  case Marker::HEXAGRAM: {
    r=r*sqrt(sqrt(3));
    double r1 = 1/sqrt(3);
    pf.resize(12);
    for (int k=0; k<12; k++) {
      double dy = r*cos(2*M_PI*k/12);
      double dx = -r*sin(2*M_PI*k/12);
      if (k&1) {
	dx *= r1;
	dy *= r1;
      }
      pf[k] = xy + QPointF(dx, dy);
    }
    if (asSpine) {
      for (int k=0; k<6; k+=2)
	p.drawLine(pf[k], pf[k+6]);
    } else {
      p.drawPolygon(pf);
    }
  } break;
  case Marker::PLUS:
    p.drawLine(xy + QPointF(r,0), xy + QPointF(-r,0));
    p.drawLine(xy + QPointF(0,r), xy + QPointF(0,-r));
    break;
  case Marker::CROSS:
    r /= sqrt(2);
    p.drawLine(xy + QPointF(r,r), xy + QPointF(-r,-r));
    p.drawLine(xy + QPointF(-r,r), xy + QPointF(r,-r));
    break;
  case Marker::HBAR:
    p.drawLine(xy + QPointF(r,0), xy + QPointF(-r,0));
    break;
  case Marker::VBAR:
    p.drawLine(xy + QPointF(0,r), xy + QPointF(0,-r));
    break;
  }
}      
      
bool CmdMark::parse(Statement const &s) {
  int id1 = s.nextIndex(1);
  int id2 = s.nextIndex(id1);
  if (id2==s.length() && s.isNumeric(1) && s.isNumeric(id1) &&
      s.data(1).size()==s.data(id1).size())
    return true;
  else
    return usage();
}

QRectF CmdMark::dataRange(Statement const &s) {
  if (s[0].str=="pmark")
    return QRectF(); // paper coord -> no data range

  
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
  return QRectF(QPointF(Slightly::less(minx), Slightly::less(miny)),
		QPointF(Slightly::more(maxx), Slightly::more(maxy)));
}

void CmdMark::render(Statement const &s, Figure &f, bool dryrun) {
  QVector<double> const &xdata = s.data(1);
  QVector<double> const &ydata = s.data(s.nextIndex(1));
  if (xdata.isEmpty()) {
    f.setBBox(QRectF());
    return;
  }

  QPolygonF p(xdata.size());

  if (s[0].str=="mark") {
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
  double r = f.marker().radius;
  bbox.adjust(-r, -r, r, r);
  f.setBBox(bbox);
  
  if (dryrun)
    return;

  QPainter &ptr(f.painter());
  ptr.save();

  bool asSpine = false;
  switch (f.marker().fill) {
  case Marker::CLOSED:
    ptr.setBrush(ptr.pen().color());
    break;
  case Marker::OPEN:
    ptr.setBrush(QColor("white"));
    break;
  case Marker::BRUSH:
    break;
  case Marker::SPINE:
    asSpine = true;
    break;
  }

  Marker::Type t = f.marker().type;

  if (s[0].str=="pmark") {
    double a = f.anchorAngle();
    QPointF xy0 = f.anchor();
    for (int k=0; k<xdata.size(); k++) {
      QPointF xy(pt2iu(xdata[k]), pt2iu(ydata[k]));
      if (a)
	xy = ::rotate(xy, a);
      xy += xy0;
      rendermark(ptr, xy, r, t, asSpine);
    }
  } else {
    for (int k=0; k<xdata.size(); k++)
      rendermark(ptr, f.map(xdata[k],ydata[k]), r, t, asSpine);
  }

  ptr.restore();  
}
