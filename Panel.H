// Panel.H

#ifndef PANEL_H

#define PANEL_H

#include <Axis.H>
#include <QRectF>

struct Panel {
  Axis xaxis;
  Axis yaxis;
  QRectF desiredExtent;
  QRectF fullbbox, cumulbbox, lastbbox;
};

#endif
