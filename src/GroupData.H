// GroupData.H

#ifndef GROUPDATA_H

#define GROUPDATA_H

#include "Align.H"
#include <QRectF>
#include <QPen>
#include <QBrush>
#include <QString>
#include <QFont>

struct GroupData {
public:
  QRectF bbox;
  QPen pen;
  QString penName;
  QBrush brush;
  QString brushName;
  QFont font;
  Align::VAlign valign;
  Align::HAlign halign;
  QString reftext;
  double hairline;
};

#endif
