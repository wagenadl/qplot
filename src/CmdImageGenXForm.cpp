// CmdImageGenXForm.cpp - This file is part of QPlot

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

// CmdImage.C

#include "CmdImage.h"
#include <QDebug>


static CBuilder<CmdImage> cbImage("image");


class IXForm {
public:
  IXForm(QVector<double> const &def) {
    int N = def.size();
    x0 = (N>=1) ? def[0] : 0;
    y0 = (N>=2) ? def[1] : 0;
    xx = (N>=3) ? def[2] : 1;
    yy = (N>=4) ? def[3] : 1;
    xy = (N>=5) ? def[4] : 0;
    yx = (N>=6) ? def[5] : 0;
  }
  QPointF map(QPointF const &p) {
    return QPointF(x0 + p.x()*xx + p.y()*xy,
		   y0 + p.x()*yx + p.y()*yy);
  }
  QPointF maprel(QPointF const &p, QPointF const &origin) {
    return QPointF(x0 + origin.x()
		   + (p.x()-origin.x())*xx + (p.y()-origin.y())*xy,
		   y0 + origin.y()
		   + (p.x()-origin.x())*yx + (p.y()-origin.y())*yy);
  }
public:
  double x0, y0, xx, yy, xy, yx;
};

bool CmdImage::usage() {
  return error("Usage: image x y w h K cdata\n"
	       "       image [ dataxform ] [ paperxform ] [ W H C ] cdata");
}

static bool hasComplexSyntax(Statement const &s) {
  return s.length()>=2 && s[1].typ==Token::OPENBRACKET;
}

bool CmdImage::parse_complex(Statement const &s) {
  /* For dataxform we accept a full transformation matrix
       [ x0 y0 xx yy xy yx ]
     such that the data location for pixel (i,j) is:
       x = x0 + i*xx + j*xy
       y = y0 + i*yx + j*yy
     We also accept shorter forms, and substitute default values:
       [ 0 0 1 1 0 0 ]
     After data to paper transformation, the paperxform matrix is applied,
     but with a slight twist. Let (X(i,j), Y(i,j)) be the paper positions
     of pixels before the final transformation, then the final paper positions
     are:
       X'(i,j) = X0 + X(0,0) + (X(i,j)-X(0,0))*XX + (Y(i,j)-Y(0,0))*XY
       Y'(i,j) = Y0 + Y(0,0) + (X(i,j)-X(0,0))*YX + (Y(i,j)-Y(0,0))*YY
     where the paperxform is
       [ X0 Y0 XX YY XY YX]
     That is, the paperxform scaling is performed relative to the origin set
     by the dataxform rather than to the figures global origin.

NOTE:     All of this is correct, but not useful. What I *want* is a way
          to position an image in data space and then to shift it in paper
	  space and override the length and/or width. So the *better* way
	  to go about it, is first to simply specify xywh in data space,
	  and then to *add* to that a certain xywh in paper space. There
	  *might* be a use for this rotation business, but I won't do it right
	  now.
  */
  int id1 = s.nextIndex(1);
  int id2 = s.nextIndex(id1);
  int id3 = s.nextIndex(id2);

  if (!s.isNumeric(1) || !s.isNumeric(id1) || !s.isNumeric(id2))
    usage();
  if (!s.isNumeric(id3))
    usage();

  if (s.data(1).size() > 6) // check dataxform
    usage();
  if (s.data(id1).size() > 6) // check paperxform
    usage();
  if (s.data(id2).size() != 3) // check size spec
    usage();
  if (s.data(id3).size() != s.data(id2)[0]*s.data(id2)[1]*s.data(id2)[2])
    usage(); // check data size

  return true;
}

bool CmdImage::parse_simple(Statement const &s) {
  if (s.length()<7)
    return usage();
  for (int k=1; k<6; k++)
    if (s[k].typ!=Token::NUMBER)
      return usage();
  int id1 = s.nextIndex(6);
  if (id1 != s.length() || !s.isNumeric(6))
    return usage();
  int K = s[5].num;
  int N = s.data(6).size();
  if (N % (3*K) != 0)
    return usage();
  return true;
}

bool CmdImage::parse(Statement const &s) {
  if (hasComplexSyntax(s)) 
    return parse_complex(s);
  else
    return parse_simple(s);
}

static QRectF dataRange_complex(Statement const &) {
  /* The datarange for an image with complex transformation is tricky.
     If the paper transform is not trivial, it doesn't even make any sense
     at all.
     We're just going to ignore such images in the range calculations for now.
  */
  return QRectF();
}

static QRectF dataRange_simple(Statement const &s) {
  double minx = s[1].num;
  double maxx = s[1].num + s[3].num;
  double miny = s[2].num;
  double maxy = s[2].num + s[4].num;
  return QRectF(QPointF(minx,miny), QPointF(maxx,maxy));
}

QRectF CmdImage::dataRange(Statement const &s) {
  if (hasComplexSyntax(s))
    return dataRange_complex(s);
  else
    return dataRange_simple(s);
}

static void build_image(int X, int Y, int C,
			QVector<double> const &cdata,
			QImage &img) {
  // QImage img(X, Y, QImage::Format_ARGB32);
  uchar *dst = img.bits();
  QVector<double>::const_iterator src = cdata.begin();
  if (C==1) {
    for (int y=0; y<Y; y++) {
      for (int x=0; x<X; x++) {
	double v = *src++;
	int d = (v<0) ? 0 : (v>1) ? 255 : int(v * 255.999);
	for (int c=0; c<3; c++)
	  *dst++ = d;
        *dst++ = 255;
      }
    }
  } else if (C==3) {
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
  } else if (C==4) {
    for (int y=0; y<Y; y++) {
      for (int x=0; x<X; x++) {
	double const *s1 = src+3;
	for (int c=0; c<3; c++) {
	  double v = *s1--;
	  *dst++ = (v<0) ? 0 : (v>1) ? 255 : int(v * 255.999);
	}
	src+=4;
      }
    }
  }
}

void CmdImage::render_complex(Statement const &s, Figure &f, bool dryrun) {
  int idataxform = 1;
  int ipaperxform = s.nextIndex(idataxform);
  int isizespec = s.nextIndex(ipaperxform);
  int idata = s.nextIndex(isizespec);

  int X = s.data(isizespec)[0];
  int Y = s.data(isizespec)[1];
  int C = s.data(isizespec)[2];
  qDebug() << "X:"<<X<< " Y:"<<Y<< " C:"<<C;
  
  IXForm dataxform(s.data(idataxform));
  IXForm paperxform(s.data(ipaperxform));

  QPointF d00 = dataxform.map(QPointF(0,0));
  QPointF d01 = dataxform.map(QPointF(0,Y));
  QPointF d10 = dataxform.map(QPointF(X,0));
  QPointF d11 = dataxform.map(QPointF(X,Y));

  qDebug() << "d00:"<<d00<< " d01:"<<d01<< " d10:"<<d10 << " d11:"<<d11;

  QPointF p00 = f.map(d00);
  QPointF p01 = f.map(d01);
  QPointF p10 = f.map(d10);
  QPointF p11 = f.map(d11);

    qDebug() << "p00:"<<p00<< " p01:"<<p01<< " p10:"<<p10 << " p11:"<<p11;

  QPointF q00 = paperxform.maprel(p00, p00);
  QPointF q01 = paperxform.maprel(p01, p00);
  QPointF q10 = paperxform.maprel(p10, p00);
  QPointF q11 = paperxform.maprel(p11, p00);
  
 qDebug() << "q00:"<<q00<< " q01:"<<q01<< " q10:"<<q10 << " q11:"<<q11;

  QRectF bbox = QRectF(q00,q11).normalized()
    . united(QRectF(q01, q10).normalized());
  f.setBBox(bbox);

  if (dryrun)
    return;

  QImage img(X, Y, QImage::Format_ARGB32);
  build_image(X, Y, C, s.data(idata), img);

  // And now to render it. That's not so simple.
  QTransform t0 = f.painter().transform();

  f.painter().translate(p00);
  f.painter().setTransform(QTransform(paperxform.xx, paperxform.xy,
				      paperxform.yx, paperxform.yy,
				      pt2iu(paperxform.x0), pt2iu(paperxform.y0)),
			   true);
  f.painter().translate(-p00);

  f.painter().setTransform(f.xform(), true);

  f.painter().setTransform(QTransform(dataxform.xx, dataxform.xy,
				      dataxform.yx, dataxform.yy,
				      dataxform.x0, dataxform.y0),
			   true);

  f.painter().drawImage(QRectF(0, 0, X, Y), img);

  f.painter().setTransform(t0, false);
}

void CmdImage::render_simple(Statement const &s, Figure &f, bool dryrun) {
  int X = s[5].num;
  QVector<double> const &cdata = s.data(6);
  int C = 3;
  int Y = cdata.size()/C/X;

  QRectF extent = dataRange(s);
  QPointF p1 = f.map(extent.left(),extent.top());
  QPointF p2 = f.map(extent.right(),extent.bottom());
  QRectF bbox = QRectF(p1,p2).normalized();
  f.setBBox(bbox);

  if (dryrun)
    return;

  QImage img(X, Y, QImage::Format_ARGB32);
  build_image(X, Y, C, cdata, img);
  f.painter().drawImage(bbox, img);
}

void CmdImage::render(Statement const &s, Figure &f, bool dryrun) {
  if (hasComplexSyntax(s)) 
    render_complex(s, f, dryrun);
  else
    render_simple(s, f, dryrun);
}
  
