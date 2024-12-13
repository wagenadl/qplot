// Image.H

#ifndef IMAGE_H

#define IMAGE_H

#include <QImage>

namespace Image {
  QImage build(int X, int Y, int C,
               QVector<double> const &cdata);
};

#endif
