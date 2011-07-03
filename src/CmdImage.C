// CmdImage.C

#include "CmdImage.H"

static CBuilder<CmdImage> cbImage("image");

bool CmdImage::usage() {
  return error("Usage: image x y w h K cdata");
}

bool CmdImage::parse(Statement const &s) {
  if (s.length()<7)
    return usage();
  int id1 = s.nextIndex(6);
  if (id1 != s.length())
    return usage();
  for (int k=1; k<7; k++)
    if (!s.isNumeric(k))
      return usage();
  return true;
}

QRectF CmdImage::dataRange(Statement const &s) {
  double minx = s[1].num;
  double maxx = s[1].num + s[3].num;
  double miny = s[2].num;
  double maxy = s[2].num + s[4].num;
  return QRectF(QPointF(minx,miny), QPointF(maxx,maxy));
}

void CmdImage::render(Statement const &s, Figure &f, bool dryrun) {
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
  uchar *dst = img.bits();
  QVector<double>::const_iterator src = cdata.begin();
  for (int y=0; y<Y; y++) {
    for (int x=0; x<X; x++) {
      double const *s1 = src+2;
      for (int c=0; c<3; c++) {
	double v = *s1;
	if (v<0)
	  *dst=0;
	else if (v>1)
	  *dst=255;
	else
	  *dst = int(v * 255.999);
	dst++;
	s1--;
      }
      *dst = 255;
      dst++;
      src+=3;
    }
  }
  
  f.painter().drawImage(bbox, img);
}
