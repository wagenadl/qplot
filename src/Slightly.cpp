// Slightly.C

#include "Slightly.H"

#define EPSI (1e-25)

double Slightly::less(double x) {
  double epsi = EPSI;
  double x0 = x-epsi;
  while (x0==x) {
    epsi *= 10;
    x0 = x-epsi;
  }
  return x0;
}
    
double Slightly::more(double x) {
  double epsi = EPSI;
  double x0 = x+epsi;
  while (x0==x) {
    epsi *= 10;
    x0 = x+epsi;
  }
  return x0;
}
    
