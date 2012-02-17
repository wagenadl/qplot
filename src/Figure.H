// Figure.H

#ifndef FIGURE_H

#define FIGURE_H

#include "Axis.H"
#include "Panel.H"
#include "Marker.H"
#include "Align.H"
#include "GroupData.H"

#include <QRectF>
#include <QPainter>
#include <QMap>
#include <QPen>
#include <QBrush>

class Figure {
public:
  Figure();
  void setSize(QSizeF wh_pt);
  void setExtent(QRectF xywh_pt);
  /*:N Iff this is a genuine change, I will reset axis mapping. Thus, the
       render() of a program can be rerun multiple times without axis reset.
       In particular, that means that results from "fudge" will be preserved.
  */
  QRectF const &extent() const;
  void setDashScale(double);
  double dashScale() const;
  Axis &xAxis();
  Axis &yAxis();
  /*:N Note that the yAxis normally runs up, that is, the minimum of its
       data range has a paper coordinate greater than the maximum of its
       data range. */
  QPointF map(double x, double y) const; // data to paper
  QPointF map(QPointF const &xy) const; // data to paper, convenience function
  QPointF maprel(double dx, double dy) const; // data to paper
  QTransform xform() const; // return data to paper transformation matrix
  void clearBBox(bool full=false);
  void setBBox(QRectF const &); // sets lastbbox, updates fullbbox and cumulbbox
  void setAnchor(QPointF const &, double phi=0); // in paper coords
  void setAnchor(double x, double y, double dx=1, double dy=0); // in data coords
  double angle(double dx, double dy) const; // paper angle from data displacement
  QPointF const &anchor() const;
  double const &anchorAngle() const;
  QRectF const &lastBBox() const;
  QRectF const &cumulBBox() const;
  QRectF const &fullBBox() const;
  void setVAlign(Align::VAlign a);
  void setHAlign(Align::HAlign a);
  Align::VAlign vAlign() const;
  Align::HAlign hAlign() const;
  void setRefText(QString str);
  QString refText() const;
  QPainter &painter();
  Marker &marker();
  void storePen();
  void storeBrush();
  void choosePen(QString);
  void chooseBrush(QString);
  double hairline() const;
  void setHairline(double h);
  void choosePanel(QString);
  void leavePanel();
  void reset(); // this is a soft reset. semantics need to be documented
  void hardReset(); // this is like restarting the program
  Panel &panelRef(QString); // blithely creates a dummy panel for unknown ID
  bool hasPanel(QString) const;
  QString currentPanelName() const;
  void startGroup();
  void endGroup();
  void endGroups();
  QString panelAt(QPointF const &xy);
  void setLocation(QString id, QPointF const &xy);
  QPointF getLocation(QString id)  const;
  void markFudged();
  bool checkFudged() const;
private:
  QRectF figextent;
  Axis xax, yax;
  QRectF fullbbox, cumulbbox, lastbbox;
  QPainter pntr;
  QPointF anch;
  double anchang;
  Align::VAlign valign;
  Align::HAlign halign;
  QString reftxt;
  Marker mrkr;
  QMap<QString, QPen> pens; 
  QMap<QString, QBrush> brushes; 
  QMap<QString, Panel> panels;
  /* Note that the *current* pen/brush/panel is not saved in the maps.
     Instead, the current pen and brush are kept in the painter, and the
     current panel is kept in the xax, yax, and figextent properties. */
  QString currentPen;
  QString currentBrush;
  QString currentPanel;
  double hairline_; // stored in points, not internal units!
  QList<GroupData> groupstack;
  double dashscale;
  QMap<QString, QPointF> locations;
  bool fudged;
private:
  void replaceAxes();
};

#endif
