// Geometry.C

#include "Geometry.H"
#include <math.h>

UnitVector::UnitVector(): xy_d(1,0) {
}

UnitVector::UnitVector(QPointF const &xy) {
  set(xy);
}

void UnitVector::set(QPointF const &xy) {
  double d = sqrt(xy.x()*xy.x() + xy.y()*xy.y());
  xy_d = QPointF(xy.x()/d, xy.y()/d);
  ang = atan2(xy_d.y(), xy_d.x());
  xform.reset(); xform.rotateRadians(ang);
}

double UnitVector::angle() const {
  return ang;
}

QPointF UnitVector::xy() const {
  return xy_d;
}

QTransform rectMapping(QRectF const &src, QRectF const &dst) {
  double scx = dst.width()/src.width();
  double scy = dst.height()/src.height();
  double dx = dst.left() - src.left()*scx;
  double dy = dst.top() - src.top()*scy;
  return QTransform(scx,0,0, 0,scy,0, dx,dy);
}

DataOnPaper::DataOnPaper(QRectF const &dataRect, QRectF const &paperRect):
  dataR(dataRect), paperR(paperRect) {
  mapper = rectMapping(dataR, paperR);
}

void DataOnPaper::setDataRect(QRectF const &dr) {
  dataR = dr;
  mapper = rectMapping(dataR, paperR);
}

void DataOnPaper::setPaperRect(QRectF const &pr) {
  paperR = pr;
  mapper = rectMapping(dataR, paperR);
}
		 
QRectF const &DataOnPaper::dataRect() const {
  return dataR;
}

QRectF const &DataOnPaper::paperRect() const {
  return paperR;
}

QPointF DataOnPaper::dataToPaper(QPointF const &dataPt) const {
  return mapper.map(dataPt);
}

QTransform const &DataOnPaper::transform() const {
  return mapper;
}

MetricOnData::MetricOnData(DataOnMetric const &base): base(base) {
}

MetricOnData::MetricOnData(DataOnMetric const &base, QPointF const &xy_data):
  base(base), orig(xy_data) {
}

MetricOnData::MetricOnData(DataOnMetric const &base, QPointF const &xy_data,
			   UnitVector const &rot_data):
  base(base), orig(xy_data), rot(rot_data) {
}

void MetricOnData::setOrigin(QPointF const &xy_data) {
  orig = xy_data;
}

void MetricOnData::setRotation(UnitVector const &rot_data) {
  rot = rot_data;
}

QPointF MetricOnData::metricToData(QPointF const &xy) const {
  QTransform paperToData(base.transform().inverted());
  QPointF dxy = paperToData(rot.xform().map(xy));
  return dxy + orig;
}

QPointF MetricOnData::metricToPaper(QPointF const &xy) const {
  return base.transform().map(metricToData(xy));
}

QPointF MetricOnData::origin() const {
  return orig;
}

UnitVector MetricOnData::rotation() const {
  return rot;
}
