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
  return error("Usage: xzimage x z w d y xz yz X Z cdata\n");
}

enum Arg {
  Argx=1,
  Argz,
  Argw,
  Argd,
  Argy,
  Argxz,
  Argyz,
  ArgX,
  ArgZ,
  Argcdata
};
  

bool CmdXZImage::parse(Statement const &s) {
  if (s.length()<Argcdata+1)
    return usage();
  for (int k=Argx; k<=ArgZ; k++)
    if (s[k].typ!=Token::NUMBER)
      return usage();
  int id1 = s.nextIndex(Argcdata);
  if (id1 != s.length() || !s.isNumeric(Argcdata))
    return usage();
  int X = s[ArgX].num;
  int Z = s[ArgZ].num;
  int N = s.data(Argcdata).size();
  if (N % (X*Z) != 0)
    return usage();
  if (N / (X*Z) < 1 || N / (X*Z) > 4)
    return usage();
  return true;
}

QRectF CmdXZImage::dataRange(Statement const &s) {
  double minx = s[Argx].num;
  double maxx = s[Argx].num + s[Argw].num;
  double minz = s[Argz].num;
  double maxz = s[Argz].num + s[Argd].num;
  double y = s[Argy].num;
  double xz = s[Argxz].num;
  double yz = s[Argyz].num;
  QRectF r1(QPointF(minx + xz*minz, y + yz*minz),
            QPointF(maxx + xz*maxz, y + yz*maxz));
  QRectF r2(QPointF(maxx + xz*minz, y + yz*minz),
            QPointF(minx + xz*maxz, y + yz*maxz));
  return (r1 | r2).normalized();
}

void CmdXZImage::render(Statement const &s, Figure &f, bool dryrun) {
  int X = s[ArgX].num;
  int Z = s[ArgZ].num;
  QVector<double> const &cdata = s.data(Argcdata);
  int C = cdata.size()/X/Z;
  QRectF extent = dataRange(s);
  QPointF p1 = f.map(extent.left(), extent.top());
  QPointF p2 = f.map(extent.right(), extent.bottom());
  QRectF bbox = QRectF(p1, p2).normalized();
  f.setBBox(bbox);

  if (dryrun)
    return;

  double x0 = s[Argx].num;
  double z0 = s[Argz].num;
  double w = s[Argw].num;
  double d = s[Argd].num;
  double y = s[Argy].num;
  double xz = s[Argxz].num;
  double yz = s[Argyz].num;
  
  QImage img = Image::build(X, Z, C, cdata);
  f.painter().save();
  QTransform data2paper(f.xform());
  QTransform img2data(w/X,      0,      0,
                      xz*d/Z,   yz*d/Z, 0,
                      x0+xz*z0, y+yz*z0,  1);
  f.painter().setTransform(data2paper, true);
  f.painter().setTransform(img2data, true);
  f.painter().drawImage(QPointF(0,0), img);
  f.painter().restore();
}
