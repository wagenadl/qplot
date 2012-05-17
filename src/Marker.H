// Marker.H

#ifndef MARKER_H

#define MARKER_H

#include "Factor.H"

struct Marker {
  enum Type {
    CIRCLE,
    SQUARE,
    DIAMOND,
    LEFTTRIANGLE,
    RIGHTTRIANGLE,
    UPTRIANGLE,
    DOWNTRIANGLE,
    PENTAGRAM,
    HEXAGRAM,
    PLUS,
    CROSS,
    HBAR,
    VBAR,
  };
  enum Fill {
    BRUSH,
    OPEN,
    CLOSED,
    SPINE,
  };
  Type type;
  Fill fill;
  double radius;
  Marker() {
    type = CIRCLE;
    fill = CLOSED;
    radius = pt2iu(3);
  }
};

#endif
