// TextShiftAccum.H

#ifndef TEXTSHIFTACCUM_H

#define TEXTSHIFTACCUM_H

class TextShiftAccum {
public:
  TextShiftAccum();
  void reset();
  void setBase(double x, double y);
  void update(double dx, double dy);
  double x();
  double y();
  bool isActive();
private:
  double x_;
  double y_;
  bool has;
};

#endif
