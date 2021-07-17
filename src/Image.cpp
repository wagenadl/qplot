// Image.cpp

#include "Image.h"

namespace Image {
  QImage build(int X, int Y, int C,
               QVector<double> const &cdata) {
    QImage img = QImage(X, Y, QImage::Format_ARGB32);
    uchar *dst = img.bits();
    QVector<double>::const_iterator src = cdata.begin();
    switch (C) {
    case 1:
      for (int y=0; y<Y; y++) {
        for (int x=0; x<X; x++) {
          double v = *src++;
          int d = (v<0) ? 0 : (v>1) ? 255 : int(v * 255.999);
          for (int c=0; c<3; c++)
            *dst++ = d;
          *dst++ = 255;
        }
      }
      break;
    case 2:
      for (int y=0; y<Y; y++) {
        for (int x=0; x<X; x++) {
          double v = *src++;
          int d = (v<0) ? 0 : (v>1) ? 255 : int(v * 255.999);
          for (int c=0; c<3; c++)
            *dst++ = d;
          v = *src++;
          *dst++ = (v<0) ? 0 : (v>1) ? 255 : int(v * 255.999);
        }
      }
      break;
    case 3:
      for (int y=0; y<Y; y++) {
        for (int x=0; x<X; x++) {
          double const *s1 = src+2;
          for (int c=0; c<3; c++) {
            double v = *s1--;
            *dst++ = (v<0) ? 0 : (v>1) ? 255 : int(v * 255.999);
          }
          *dst++ = 255;
          src+=3;
        }
      }
      break;
    case 4:
      for (int y=0; y<Y; y++) {
        for (int x=0; x<X; x++) {
          double const *s1 = src+2;
          for (int c=0; c<3; c++) {
            double v = *s1--;
            *dst++ = (v<0) ? 0 : (v>1) ? 255 : int(v * 255.999);
          }
          double v = src[3];
          *dst++ = (v<0) ? 0 : (v>1) ? 255 : int(v * 255.999);
          src+=4;
        }
      }
    }
    return img;
  }
};
