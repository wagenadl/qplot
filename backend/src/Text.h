// Text.H - This file is part of QPlot

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
  double width() const;
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
  void italicCorrect();
};

#endif
