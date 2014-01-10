// CmdImage.C

#include "CmdImage.H"
#include <QDebug>
#include <math.h>


static CBuilder<CmdImage> cbImage("image");

bool CmdImage::usage() {
  return error("Usage: image x y w h K cdata\n"
	       "       image [ dataxywh ] [ paperxywh ] [ W H C ] cdata");
}

static bool hasComplexSyntax(Statement const &s) {
  return s.length()>=2 && s[1].typ==Token::OPENBRACKET;
}

bool CmdImage::parse_complex(Statement const &s) {
  int id1 = s.nextIndex(1);
  int id2 = s.nextIndex(id1);
  int id3 = s.nextIndex(id2);

  if (!s.isNumeric(1) || !s.isNumeric(id1) || !s.isNumeric(id2))
    usage();
  if (!s.isNumeric(id3))
    usage();

  if (s.data(1).size() != 4) // check dataxywh
    usage();
  if (s.data(id1).size() != 4) // check paperxywh
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
  /* The datarange for an image with paper transformation is not meaningful.
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
  int idataxywh = 1;
  int ipaperxywh = s.nextIndex(idataxywh);
  int isizespec = s.nextIndex(ipaperxywh);
  int idata = s.nextIndex(isizespec);

  int X = s.data(isizespec)[0];
  int Y = s.data(isizespec)[1];
  int C = s.data(isizespec)[2];

  double x = s.data(idataxywh)[0];
  double y = s.data(idataxywh)[1];
  double w = s.data(idataxywh)[2];
  double h = s.data(idataxywh)[3];
  bool nax = isnan(x);
  bool nay = isnan(y);
  if (nax)
    x=0;
  if (nay)
    y=0;
  
  QPointF d0(x, y);
  QSizeF dd(w, h);
  QRectF d(d0, dd);
  QPointF p1 = f.map(d.left(), d.bottom());
  QPointF p2 = f.map(d.right(), d.top());
  if (nax) {
    p1.setX(0);
    p2.setX(f.xAxis().maprel(w).x());
  }
  if (nay) {
    p1.setY(0);
    p2.setY(f.yAxis().maprel(h).y());
  }

  p1 += QPointF(pt2iu(s.data(ipaperxywh)[0]), pt2iu(s.data(ipaperxywh)[1]));
  p2 += QPointF(pt2iu(s.data(ipaperxywh)[0] + s.data(ipaperxywh)[2]),
		pt2iu(s.data(ipaperxywh)[1] + s.data(ipaperxywh)[3]));

  QRectF bbox = QRectF(p1,p2).normalized();
  f.setBBox(bbox);

  if (dryrun)
    return;

  QImage img(X, Y, QImage::Format_ARGB32);
  build_image(X, Y, C, s.data(idata), img);
  f.painter().drawImage(bbox, img);
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
  
