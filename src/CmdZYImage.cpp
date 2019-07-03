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
  return error("Usage: zyimage z y d h x xz yz Z Y cdata\n");
}

enum Arg {
  Argz=1,
  Argy,
  Argd,
  Argh,
  Argx,
  Argxz,
  Argyz,
  ArgZ,
  ArgY,
  Argcdata
};
  

bool CmdZYImage::parse(Statement const &s) {
  if (s.length()<Argcdata+1)
    return usage();
  for (int k=Argz; k<=ArgY; k++)
    if (s[k].typ!=Token::NUMBER)
      return usage();
  int id1 = s.nextIndex(Argcdata);
  if (id1 != s.length() || !s.isNumeric(Argcdata))
    return usage();
  int Z = s[ArgZ].num;
  int Y = s[ArgY].num;
  int N = s.data(Argcdata).size();
  if (N % (Z*Y) != 0)
    return usage();
  if (N / (Z*Y) < 1 || N / (Z*Y) > 4)
    return usage();
  return true;
}

QRectF CmdZYImage::dataRange(Statement const &s) {
  double minz = s[Argz].num;
  double maxz = s[Argz].num + s[Argd].num;
  double miny = s[Argy].num;
  double maxy = s[Argy].num + s[Argh].num;
  double x = s[Argx].num;
  double xz = s[Argxz].num;
  double yz = s[Argyz].num;
  QRectF r1(QPointF(x + xz*minz, miny + yz*minz),
            QPointF(x + xz*maxz, maxy + yz*maxz));
  QRectF r2(QPointF(x + xz*minz, maxy + yz*minz),
            QPointF(x + xz*maxz, miny + yz*maxz));
  return (r1 | r2).normalized();
}

void CmdZYImage::render(Statement const &s, Figure &f, bool dryrun) {
  int Z = s[ArgZ].num;
  int Y = s[ArgZ].num;
  QVector<double> const &cdata = s.data(Argcdata);
  int C = cdata.size()/Z/Y;
  QRectF extent = dataRange(s);
  QPointF p1 = f.map(extent.left(), extent.top());
  QPointF p2 = f.map(extent.right(), extent.bottom());
  QRectF bbox = QRectF(p1, p2).normalized();
  f.setBBox(bbox);

  if (dryrun)
    return;

  double z0 = s[Argz].num;
  double y0 = s[Argy].num;
  double d = s[Argd].num;
  double h = s[Argh].num;
  double x = s[Argx].num;
  double xz = s[Argxz].num;
  double yz = s[Argyz].num;
  
  QImage img = Image::build(Z, Y, C, cdata);
  f.painter().save();
  QTransform data2paper(f.xform());
  QTransform img2data(xz*d/Z, yz*d/Z,  0,
                      0,      h/Y,     0,
                      x+xz*z0, y0+yz*z0, 1);
  f.painter().setTransform(data2paper, true);
  f.painter().setTransform(img2data, true);
  f.painter().drawImage(QPointF(0,0), img);
  f.painter().restore();
}
