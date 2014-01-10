// Rotate.C

#include "Rotate.H"
#include <math.h>

QPointF rotate(QPointF const &p, double phirad) {
  return QPointF(p.x()*cos(phirad)-p.y()*sin(phirad),
		 p.y()*cos(phirad)+p.x()*sin(phirad));
}

QRectF rotate(QRectF const &r, double phirad) {
  QPointF x1 = rotate(r.topLeft(),phirad);
  QPointF x2 = rotate(r.bottomLeft(),phirad);
  QPointF x3 = rotate(r.topRight(),phirad);
  QPointF x4 = rotate(r.bottomRight(),phirad);
  return QRectF(x1,x3) | QRectF(x2,x4);
}
