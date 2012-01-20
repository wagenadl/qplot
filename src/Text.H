// Text.H

#ifndef TEXT_H

#define TEXT_H

#include <QString>
#include <QFont>
#include <QRectF>
#include <QVector>

class Text {
public:
  Text();
  ~Text();
  void addInterpreted(QString txt);
  void clear();
  void setFont(QString family, double size);
  void setFont(QFont const &);
  Text &operator<<(QString const &);
  void add(QString); // same as operator<<
  void setSuper();
  void setSub();
  void toggleSlant();
  void toggleBold();
  void restore();
  QRectF bbox() const;
  void render(QPainter &, QPointF const &);
private:
  struct Span {
    QPointF startpos;
    QFont font;
    QString text;
  };
  QVector<Span> spans;
  double nextx;
  QRectF bb;
  struct State {
    QString fontfamily;
    double baseline;
    double fontsize;
    bool slant;
    bool bold;
  };
  QVector<State> stack;
private:
  QFont makeFont(State const &s);
};

#endif
