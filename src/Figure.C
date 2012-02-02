// Figure.C

#include "Figure.H"
#include "Error.H"
#include <math.h>
#include <QDebug>

Figure::Figure() {
  hardReset();
}

void Figure::hardReset() {
  dashscale = 1;
  figextent = QRectF(QPointF(0,0), QSizeF(72*6, 72*4));
  currentPanel = "-";
  panels.clear();
  replaceAxes();
  reset();
}

void Figure::reset() {
  halign = Align::CENTER;
  valign = Align::BASE;
  currentPen = "A";
  currentBrush = "A";
  currentPanel = "-"; // i.e., main
  pens.clear();
  brushes.clear();
  hairline_ = false;
  mrkr = Marker();
  anch = QPointF(0,0);
  anchang = 0;
  clearBBox(true);
  foreach (QString p, panels.keys()) {
    panels[p].fullbbox=QRectF();
    panels[p].cumulbbox=QRectF();
    panels[p].lastbbox=QRectF();
  }
  groupstack.clear();
  if (pntr.isActive()) {
    QFont font("Helvetica");
    font.setPixelSize(pt2iu(10));
    pntr.setFont(font);
    pntr.setPen("black");
  }
  fudged = false;
}

void Figure::setDashScale(double s) {
  dashscale = s;
}

double Figure::dashScale() const {
  return dashscale;
}

void Figure::setHairline(bool h) {
  hairline_ = h;
}

bool Figure::hairline() const {
  return hairline_;
}

void Figure::setHAlign(Align::HAlign a) {
  halign = a;
}

void Figure::setVAlign(Align::VAlign a) {
  valign = a;
}

Align::HAlign Figure::hAlign() const {
  return halign;
}

Align::VAlign Figure::vAlign() const {
  return valign;
}


void Figure::setExtent(QRectF xywh_pt) {
 if (figextent==xywh_pt)
    return;

  figextent = xywh_pt;
  replaceAxes();
}

void Figure::setSize(QSizeF wh_pt) {
  if (figextent.size() == wh_pt)
    return;
  
  figextent = QRectF(QPointF(0,0), wh_pt);
  replaceAxes();
}

void Figure::replaceAxes() {
  xax.setPlacement(QPointF(figextent.left(),0),
		   QPointF(figextent.right(),0));
  yax.setPlacement(QPointF(0,figextent.bottom()),
		   QPointF(0,figextent.top()));
}

Axis &Figure::xAxis() {
  return xax;
}

Axis &Figure::yAxis() {
  return yax;
}

QPointF Figure::map(double x, double y) const {
  return xax.map(x) + yax.map(y);
}

QPointF Figure::map(QPointF const &xy) const {
  return xax.map(xy.x()) + yax.map(xy.y());
}

QPointF Figure::maprel(double dx, double dy) const {
  return xax.maprel(dx) + yax.maprel(dy);
}

QTransform Figure::xform() const {
  return QTransform(xax.maprel(1).x(), 0,
		    0, yax.maprel(1).y(),
		    xax.map(0).x(),
		    yax.map(0).y());
}

void Figure::clearBBox(bool full) {
  lastbbox = QRectF();
  cumulbbox = QRectF();
  if (full)
    fullbbox = QRectF();
}

void Figure::setBBox(QRectF const &b) {
  lastbbox = b;
  cumulbbox |= b;
  fullbbox |= b;
}

QRectF const &Figure::lastBBox() const {
  return lastbbox;
}

QRectF const &Figure::cumulBBox() const {
  return cumulbbox;
}

QRectF const &Figure::fullBBox() const {
  return fullbbox;
}

double Figure::angle(double dx, double dy) const {
  QPointF frm = map(0, 0);
  QPointF to = map(dx, dy);
  QPointF d = to-frm;
  return atan2(d.y(), d.x());
}

void Figure::setAnchor(double x, double y, double dx, double dy) {
  setAnchor(map(x,y), angle(dx,dy));
}

void Figure::setAnchor(QPointF const &x, double a) {
  anch = x;
  anchang = a;
}

QPointF const &Figure::anchor() const {
  return anch;
}

double const &Figure::anchorAngle() const {
  return anchang;
}

QPainter &Figure::painter() {
  return pntr;
}

Marker &Figure::marker() {
  return mrkr;
}

QRectF const &Figure::extent() const {
  return figextent;
}

void Figure::setRefText(QString s) {
  reftxt = s;
}

QString Figure::refText() const {
  return reftxt;
}

void Figure::choosePen(QString s) {
  pens[currentPen] = pntr.pen();
  pntr.setPen(pens[currentPen=s]);
}

void Figure::chooseBrush(QString s) {
  brushes[currentBrush] = pntr.brush();
  pntr.setBrush(brushes[currentBrush=s]);
}

void Figure::leavePanel() {
  choosePanel("-");
}

void Figure::choosePanel(QString s) {
  if (s==currentPanel)
    return;

  if (!groupstack.isEmpty()) {
    Error() << "Warning: panel change while group stack not empty";
    groupstack.clear();
  }
  
  Panel &store(panels[currentPanel]);
  store.xaxis = xax;
  store.yaxis = yax;
  store.desiredExtent = figextent;
  store.fullbbox = fullbbox;
  store.cumulbbox = cumulbbox;
  store.lastbbox = lastbbox;

  currentPanel = s;
  
  Panel &src(panels[currentPanel]);
  xax = src.xaxis;
  yax = src.yaxis;
  figextent = src.desiredExtent;
  fullbbox = src.fullbbox;
  cumulbbox = src.cumulbbox;
  lastbbox = src.lastbbox;
  
  setAnchor(figextent.topLeft());

  if (s=="-") {
    // dropping to toplevel, include last panel's bbox in our calc.
    fullbbox |= store.fullbbox;
    cumulbbox |= store.fullbbox;
    lastbbox = store.fullbbox;
  }
}

Panel &Figure::panelRef(QString p) {
  return panels[p];
}

bool Figure::hasPanel(QString p) const {
  return panels.contains(p);
}

QString Figure::currentPanelName() const {
  return currentPanel;
}

void Figure::startGroup() {
  GroupData g;
  g.bbox = cumulbbox;

  g.pen = pntr.pen();
  g.brush = pntr.brush();
  g.penName = currentPen;
  g.brushName = currentBrush;
  g.valign = valign;
  g.halign = halign;
  g.reftext = reftxt;
  g.hairline = hairline_;
  g.font = pntr.font();

  groupstack.push_back(g);
  cumulbbox = QRectF();
}

void Figure::endGroup() {
  if (groupstack.isEmpty()) {
    Error() << "Warning: pop from empty group stack";
    return;
  }

  lastbbox = cumulbbox;
    
  GroupData g(groupstack.takeLast());
  if (currentPen!=g.penName)
    choosePen(g.penName);
  pntr.setPen(g.pen);
  if (currentBrush!=g.brushName)
    chooseBrush(g.brushName);
  pntr.setBrush(g.brush);
  halign = g.halign;
  valign = g.valign;
  reftxt = g.reftext;
  pntr.setFont(g.font);
  hairline_ = g.hairline;
  
  cumulbbox = g.bbox;
  cumulbbox |= lastbbox;
}

QString Figure::panelAt(QPointF const &xy) {
  if (currentPanel!="-") 
    if (figextent.contains(xy))
      return currentPanel;
  foreach (QString p, panels.keys())
    if (p!=currentPanel)
      if (panels[p].desiredExtent.contains(xy))
	return p;
  return "-";
}

void Figure::setLocation(QString id, QPointF const &xy) {
  locations[id] = xy;
}

QPointF Figure::getLocation(QString id) const {
  if (locations.contains(id))
    return locations[id];
  else
    return QPointF(0,0);
}

void Figure::markFudged() {
  fudged = true;
}

bool Figure::checkFudged() const {
  return fudged;
}
