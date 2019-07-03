// CmdZYImage.cpp - This file is part of QPlot

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

// CmdZYImage.C

#include "CmdZYImage.H"
#include <QDebug>
#include <math.h>
#include "Image.H"

static CBuilder<CmdZYImage> cbZYImage("zyimage");

bool CmdZYImage::usage() {
  return error("Usage: zyimage z y d g xz yz Z Y cdata\n");
}

bool CmdZYImage::parse(Statement const &s) {
  if (s.length()<10)
    return usage();
  for (int k=1; k<9; k++)
    if (s[k].typ!=Token::NUMBER)
      return usage();
  int id1 = s.nextIndex(9);
  if (id1 != s.length() || !s.isNumeric(9))
    return usage();
  int Z = s[7].num;
  int Y = s[8].num;
  int N = s.data(9).size();
  if (N % (Z*Y) != 0)
    return usage();
  if (N / (Z*Y) < 1 || N / (Z*Y) > 4)
    return usage();
  return true;
}

QRectF CmdZYImage::dataRange(Statement const &s) {
  double minz = s[1].num;
  double maxz = s[1].num + s[3].num;
  double miny = s[2].num;
  double maxy = s[2].num + s[4].num;
  double xz = s[5].num;
  double yz = s[5].num;
  QRectF r1(QPointF(xz*minz, miny + yz*minz),
            QPointF(xz*maxz, maxy + yz*maxz));
  QRectF r2(QPointF(xz*minz, maxy + yz*minz),
            QPointF(xz*maxz, miny + yz*maxz));
  return (r1 | r2).normalized();
}

void CmdZYImage::render(Statement const &s, Figure &f, bool dryrun) {
  int Z = s[7].num;
  int Y = s[8].num;
  QVector<double> const &cdata = s.data(9);
  int C = cdata.size()/Z/Y;
  QRectF extent = dataRange(s);
  QPointF p1 = f.map(extent.left(), extent.top());
  QPointF p2 = f.map(extent.right(), extent.bottom());
  QRectF bbox = QRectF(p1, p2).normalized();
  f.setBBox(bbox);

  if (dryrun)
    return;

  double z0 = s[1].num;
  double y0 = s[2].num;
  double d = s[3].num;
  double h = s[4].num;
  double xz = s[5].num;
  double yz = s[6].num;
  
  QImage img = Image::build(Z, Y, C, cdata);
  f.painter().save();
  QTransform data2paper(f.xform());
  QTransform img2data(xz*d/Z, yz*d/Z,  0,
                      0,      h/Y,     0,
                      xz*z0, y0+yz*z0, 1);
  f.painter().setTransform(data2paper, true);
  f.painter().setTransform(img2data, true);
  f.painter().drawImage(QPointF(0,0), img);
  f.painter().restore();
}
