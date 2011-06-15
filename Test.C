// Test.C

#include "Figure.H"
#include <QDebug>

int main() {
  Figure f;
  f.setBBox(QRectF(10, 20, 30, 40));
  f.setBBox(QRectF(20, 10, 40, 30));
  qDebug() << "lastbbox: " << f.lastBBox();
  qDebug() << "cumulbbox: " << f.cumulBBox();
  return 0;
}
