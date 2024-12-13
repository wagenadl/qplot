// CmdHatch.cpp

#include "CmdHatch.h"
#include "Rotate.h"
#include "Range.h"
#include <QDebug>
#include <cmath>
#include <QPainterPath>
#include "CmdMark.h"

static CBuilder<CmdHatch> cbHatch("hatch");
static CBuilder<CmdHatch> cbPHatch("phatch");

bool CmdHatch::usage() {
  return error("Usage: hatch|phatch xdata ydata angle spacing (offset)");
}
  

QRectF CmdHatch::dataRange(Statement const &s) {
  if (s[0].str=="phatch")
    return QRectF();
  else
    return CmdPlot::dataRange(s);
}

bool CmdHatch::parse(Statement const &s) {
  int idx_x = 1;
  int idx_y = s.nextIndex(idx_x);
  int idx_a = s.nextIndex(idx_y);
  int idx_s = s.nextIndex(idx_a);
  int idx_o = s.nextIndex(idx_s);
  int idx_end = s.nextIndex(idx_o);
  if (s.isNumeric(idx_x) && s.isNumeric(idx_y)
      && s.data(idx_x).size()==s.data(idx_y).size()
      && (s.token(idx_a).typ==Token::NUMBER
          || (s.token(idx_a).typ==Token::STRING
              && (s.token(idx_a).str=="*" || s.token(idx_a).str==":")))
      && s.token(idx_s).typ==Token::NUMBER
      && (idx_o==s.length() || s.token(idx_o).typ==Token::NUMBER)
      && (idx_o==s.length() || idx_end==s.length())
      && s.token(idx_s).num>0)
    return true;
  else
    return usage();
}
    
void CmdHatch::render(Statement const &s, Figure &f, bool dryrun) {
  int idx_x = 1;
  int idx_y = s.nextIndex(idx_x);
  int idx_a = s.nextIndex(idx_y);
  int idx_s = s.nextIndex(idx_a);
  int idx_o = s.nextIndex(idx_s);
  QVector<double> const &xdata = s.data(idx_x);
  QVector<double> const &ydata = s.data(idx_y);
  double angle = s.token(idx_a).num;
  bool ishex = s.token(idx_a).typ==Token::STRING && s.token(idx_a).str=="*";
  bool isrect = s.token(idx_a).typ==Token::STRING && s.token(idx_a).str==":";
  double spacing = pt2iu(s.token(idx_s).num);
  double offset = pt2iu(s.token(idx_o).num);
  // above is safe even if no offset given, because num==0 for NONE tokens
  
  /* Convert (xdata, ydata) to polygons in actual paper space,
     applying data to paper transformation or any transformation
     implied by AT.

     The data may contain NaNs, which separate polygons.
   */
  QList<QPolygonF> polygons;
  QPolygonF current;
  bool ispaper = s[0].str=="phatch";
  double atangle = f.anchorAngle();
  QPointF atxy = f.anchor();
  for (int k=0; k<xdata.size(); k++) {
    if (std::isnan(xdata[k]) || std::isnan(ydata[k])) {
      if (current.size())
        polygons << current;
      current = QPolygonF();
    } else {
      current << 
        (ispaper
         ? (::rotate(QPointF(pt2iu(xdata[k]), pt2iu(ydata[k])),
                     atangle)
            + atxy)
         : f.map(xdata[k], ydata[k]));
    }
  }
  if (current.size())
    polygons << current;

  if (!polygons.size()) {
    f.setBBox(QRectF());
    return;
  }

  QRectF bbox = polygons[0].boundingRect();
  for (int k=1; k<polygons.size(); k++)
    bbox |= polygons[k].boundingRect();
  f.setBBox(bbox); // lines don't protrude by w/2, because of clipping

  if (dryrun)
    return;
    
  /* Our strategy is to take the polygons, rotate them by negative
     ANGLE, find the bbox and center, define vertical lines (in the
     rotated space) that cover the bbox, rotate those back to real
     space, and draw them.

     We call paper coordinates X and Y, and grid coordinates XI and
     ETA.

     The OFFSET is relative to the centroid of all the polygon
     centers, which in turn are defined as the average of the vertex
     coordinates, not as the center of mass of the polygon area.
  */
  QList<QPolygonF> antirotated;
  for (QPolygonF const &poly: polygons) {
    QPolygonF rot;
    for (QPointF const &p: poly)
      rot << ::rotate(p, -angle);
    antirotated << rot;
  }

  QPointF anticenter;
  for (QPolygonF const &poly: antirotated) {
    QPointF ac1;
    for (QPointF const &p: poly)
      ac1 += p;
    ac1 /= poly.size();
    anticenter += ac1;
  }
  anticenter /= antirotated.size();
  anticenter.setX(anticenter.x() + offset);

  for (int k=0; k<polygons.size(); k++) {
    QPainterPath clip;
    clip.addPolygon(polygons[k]);
    clip.closeSubpath();
    f.painter().setClipPath(clip);
    QRectF bbox = antirotated[k].boundingRect();
    double xi0 = bbox.left();
    double xi1 = bbox.right();
    double eta0 = bbox.top();
    double eta1 = bbox.bottom();
    xi0 = std::floor((xi0 - anticenter.x()) / spacing) * spacing
      + anticenter.x();
    if (ishex) {
      float yspace = 1.732 * spacing; // sqrt3
      eta0 = std::floor((eta0 - anticenter.y()) / yspace) * yspace
        + anticenter.y();
      QPolygonF pp;
      for (double eta=eta0; eta<eta1; eta+=yspace) {
        for (double xi=xi0; xi<xi1; xi+=spacing) 
          pp << ::rotate(QPointF(xi, eta), angle);
        for (double xi=xi0 + spacing/2; xi<xi1; xi+=spacing) 
          pp << ::rotate(QPointF(xi, eta + yspace/2), angle);
      }
      CmdMark::draw(pp, f);
    } else if (isrect) {
      eta0 = std::floor((eta0 - anticenter.y()) / spacing) * spacing
        + anticenter.y();
      QPolygonF pp;
      for (double eta=eta0; eta<eta1; eta+=spacing)
        for (double xi=xi0; xi<xi1; xi+=spacing) 
          pp << ::rotate(QPointF(xi, eta), angle);
      CmdMark::draw(pp, f);
    } else {
      for (double xi=xi0; xi<xi1; xi+=spacing) 
        f.painter().drawLine(::rotate(QPointF(xi, eta0), angle),
                             ::rotate(QPointF(xi, eta1), angle));
    }
    f.painter().setClipping(false);
  }
}
