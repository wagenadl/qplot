// CmdXZImage.cpp - This file is part of QPlot

/* QPlot - Publication quality 2D graphs with dual coordinate systems
   Copyright (C) 2014  Daniel Wagenaar
  
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
  
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
  
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

// CmdXZImage.C

#include "CmdXZImage.H"
#include <QDebug>
#include <math.h>
#include "Image.H"

static CBuilder<CmdXZImage> cbXZImage("xzimage");

bool CmdXZImage::usage() {
  return error("Usage: xzimage x z w d xz yz X Z cdata\n");
}

bool CmdXZImage::parse(Statement const &s) {
  if (s.length()<10)
    return usage();
  for (int k=1; k<9; k++)
    if (s[k].typ!=Token::NUMBER)
      return usage();
  int id1 = s.nextIndex(9);
  if (id1 != s.length() || !s.isNumeric(9))
    return usage();
  int X = s[7].num;
  int Z = s[8].num;
  int N = s.data(9).size();
  if (N % (X*Z) != 0)
    return usage();
  if (N / (X*Z) < 1 || N / (X*Z) > 4)
    return usage();
  return true;
}

QRectF CmdXZImage::dataRange(Statement const &s) {
  double minx = s[1].num;
  double maxx = s[1].num + s[3].num;
  double minz = s[2].num;
  double maxz = s[2].num + s[4].num;
  double xz = s[5].num;
  double yz = s[5].num;
  QRectF r1(QPointF(minx + xz*minz, yz*minz),
            QPointF(maxx + xz*maxz, yz*maxz));
  QRectF r2(QPointF(maxx + xz*minz, yz*minz),
            QPointF(minx + xz*maxz, yz*maxz));
  return (r1 | r2).normalized();
}

void CmdXZImage::render(Statement const &s, Figure &f, bool dryrun) {
  int X = s[7].num;
  int Z = s[8].num;
  QVector<double> const &cdata = s.data(9);
  int C = cdata.size()/X/Z;
  QRectF extent = dataRange(s);
  QPointF p1 = f.map(extent.left(), extent.top());
  QPointF p2 = f.map(extent.right(), extent.bottom());
  QRectF bbox = QRectF(p1, p2).normalized();
  f.setBBox(bbox);

  if (dryrun)
    return;

  double x0 = s[1].num;
  double z0 = s[2].num;
  double w = s[3].num;
  double d = s[4].num;
  double xz = s[5].num;
  double yz = s[6].num;
  
  QImage img = Image::build(X, Z, C, cdata);
  f.painter().save();
  QTransform data2paper(f.xform());
  QTransform img2data(w/X,      0,      0,
                      xz*d/Z,   yz*d/Z, 0,
                      x0+xz*z0, yz*z0,  1);
  f.painter().setTransform(data2paper, true);
  f.painter().setTransform(img2data, true);
  f.painter().drawImage(QPointF(0,0), img);
  f.painter().restore();
}
