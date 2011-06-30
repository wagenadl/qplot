// Text.H

#ifndef TEXT_H

#define TEXT_H

class Text {
public:
  Text();
  void clear();
  void setFont(QFont const &);
  Text &operator<<(QString const &);
  void setSuper();
  void setSub();
  void setSlant();
  void setBold();
  void restore();
private:
  QVector<QPointF> startpos;
  QVector<QFont> font;
  QVector<QString> text;
  QRectF bbox;
  double nextx;
  struct Span {
    double baseline;
    double ptsize;
    bool slant;
    bool bold;
  };
  Span current;
  QVector<Span> stack;
};

#endif
