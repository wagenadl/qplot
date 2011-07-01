// Factor.C

#include "Factor.H"

#define FACTOR 30.0

double pt2iu(double x) {
  return FACTOR * x;
}

double iu2pt(double x) {
  return x / FACTOR;
}
