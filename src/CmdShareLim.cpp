// CmdShareLim.cpp - This file is part of QPlot

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

// CmdShareLim.C

#include "CmdShareLim.h"

#include <QDebug>
#include <math.h>
#include "Error.h"
#include "Range.h"

static CBuilder<CmdShareLim> cbShareLim("sharelim");

#define SCALETOLERANCE 1e-4
#define SHIFTTOLERANCE 1e-3
#define MINOVERLAP 5

bool CmdShareLim::usage() {
  return error("Usage: sharelim [x|y] ID ...\n");
}

bool CmdShareLim::parse(Statement const &s) {
  if (s.length()<2)
    return usage(); // we could allow this null case, but that might confuse

  bool atleastone = false;
  for (int i=1; i<s.length(); i++) {
    if (s[i].typ==Token::BAREWORD || s[i].typ==Token::CAPITAL) {
      if (i==1 && (s[i].str=="x" ||s[i].str=="y")) {
	// ok: "x" or "y"
      } else if (s[i].str>="A" && s[i].str<="~") {
	atleastone = true;
	// ok: acceptable ID
      } else {
	return usage();
      }
    } else {
      return usage();
    }
  }

  return atleastone;
}

void CmdShareLim::render(Statement const &s, Figure &f, bool) {
  qDebug() << "sharelim at " << s.label();
  bool shareX = true;
  bool shareY = true;
  QSet<QString> ids;
  for (int i=1; i<s.length(); i++) {
    if (s[i].str=="x")
      shareY = false;
    else if (s[i].str=="y")
      shareX = false;
    else if (f.hasPanel(s[i].str))
      ids.insert(s[i].str);
    else {
      Error() << "Unknown panel: " << s[i].str;
      return;
    }
  }
  // Now we know that all IDS are actual panels.
  ids.remove(f.currentPanelName());

  // Find union placement bbox of any of the graphs being considered
  /* Originally, I thought I would simply line up the graphs. But I think
     that's not what I want, because it is reasonable to share, e.g., x-limits
     on graphs that are horizontally stacked. In that case, what we mean is
     that within the extent of each graph we are showing the same range. Or
     is it? Perhaps we mean that the scale should be the same. When two panels
     are vertically stacked we mean that they should be lined up, even if
     their stated extent is not the same, right?
     For now, I am going to assume that what we want is the *scale* to be
     the same across shared axes, and for each of them to show the same
     data coordinate in their physical center irrespective of paper positioning.
     I can't think of a way to preserve symmetry otherwise.
  */
  /* Note that I may not have to do both axes, but the computations are cheap,
     so I'll do them anyway.
  */
  /* The scale in pt/data should become the same for all panels.
     We first need to find out the smallest and the largest value that we
     might want to show.
  */
  /* This is not working. In this way, a second sharelim would reveal more
     and more. I think I need to distinguish two cases:
     (1) The case where paper positions overlap. In that case, I will line up.
         For all panels that have overlapping extents with the current, I'll
	 grab the data range and make it common.
     (2) The case where paper positions do not overlap. In that case, I will
         only create a common scale. This is done by shrinking symmetrically.
     Can this work in case of a mixture? Start with step (1) and note the
     resulting scale. Then do step (2) and again note the scale. Now the
     question is: if the final scale from step (2) is smaller than what we
     got from step (1), can we export that scale to the graphs found in step
     (1) without conflict? No, because that would inevitably increase the
     data range which would result in endless shrinkage.
     So we need to *choose* b/w strategies (1) and (2). (1) is nicer when there
     is overlap, but (2) is the only choice when there isn't. So, I'll first
     determine whether there is overlap b/w all panels, and if so, use strategy
     (1), otherwise revert to (2).
  */
  /* Could I do something easier? No matter which situation, I could first
     scale as per strategy (2). Then, in case (1) I could align. That wouldn't
     necessarily yield the desired result, but a subsequent CmdShrink would
     fix that, I believe. The point is that a panel doesn't *need* to show
     anything outside its current datarange. I guess the question is: what is
     the optimal scale and alignment in case (1)? I can find the smallest number
     represented at the leftmost of any of the current edges and the largest
     number represented at the rightmost of any of the edges and then make
     sure that all graphs represent those numbers there. I think that is
     stable upon iteration.
   */
  if (shareX) {
    // Let's find out if we have paper overlap
    Range px(f.extent().left(), f.extent().right());
    foreach (QString id, ids) {
      Panel const &p(f.panelRef(id));
      px.intersect(Range(p.desiredExtent.left(), p.desiredExtent.right()));
    }
    if (px.range()<MINOVERLAP) {
      // No common overlap. Revert to scaling only.
      scaleX(f, ids);
    } else {
      // Common overlap. Align all.
      alignX(f, ids);
    }
  }

  if (shareY) {
    // Let's find out if we have paper overlap
    Range py(f.extent().top(), f.extent().bottom());
    foreach (QString id, ids) {
      Panel const &p(f.panelRef(id));
      py.intersect(Range(p.desiredExtent.top(), p.desiredExtent.bottom()));
    }
    if (py.range()<MINOVERLAP) {
      // No common overlap. Revert to scaling only.
      scaleY(f, ids);
    } else {
      // Common overlap. Align all.
      alignY(f, ids);
    }
  }
}

void CmdShareLim::scaleX(Figure &f, QSet<QString> ids) {
  // Get the scale
  qDebug() << "scalex";
  double scale = f.xAxis().maprel(1).x();
  // int N = 1;
  foreach (QString id, ids) {
    Panel const &p(f.panelRef(id));
    double sc1 = p.xaxis.maprel(1).x();
    if (sc1<scale)
      scale = sc1;
    // scale *= sc1;
    // N += 1;
  }
  //  scale = pow(scale, 1.0/N);

  auto applyScale = [scale, &f](Axis &axis) {
    double sc1 = axis.maprel(1).x();
    if (sc1>scale*(1+SCALETOLERANCE)) { // || sc1<scale*(1-SCALETOLERANCE)) {
      // Let's actually shrink
      double currentWidth = axis.maxp().x() - axis.minp().x();
      double newWidth = currentWidth * scale/sc1;
      double shift = (currentWidth - newWidth)/2;
      qDebug() << "apply" << scale << sc1/scale << " . " << axis.minp().x() << axis.maxp().x() << shift;
      axis.setPlacement(QPointF(axis.minp().x() + shift, 0),
                        QPointF(axis.maxp().x() - shift, 0));
      f.markFudged();
    } else {
      qDebug() << "done" << scale << " . " << axis.minp().x() << axis.maxp().x();
    }
  };
  
  // Apply the scale to current panel
  applyScale(f.xAxis());
  
  // Apply the scale to other panels
  foreach (QString id, ids) 
    applyScale(f.panelRef(id).xaxis);

}

void CmdShareLim::alignX(Figure &f, QSet<QString> ids) {
  // Find union of extents
  Range px(f.extent().left(), f.extent().right());
  foreach (QString id, ids) {
    Panel const &p(f.panelRef(id));
    px.unionize(Range(p.desiredExtent.left(), p.desiredExtent.right()));
  }
  // Find min and max represented there
  /* Note that I am assuming the axis has negative values on the left.
     I think I make that assumption throughout the program, probably
     to my ultimate detriment.
  */      
  double x0 = f.xAxis().rev(QPointF(px.min(), 0));
  double x1 = f.xAxis().rev(QPointF(px.max(), 0));
  foreach (QString id, ids) {
    Panel const &p(f.panelRef(id));
    double x0a = p.xaxis.rev(QPointF(px.min(), 0));
    double x1a = p.xaxis.rev(QPointF(px.max(), 0));
    if (x0a<x0)
      x0 = x0a;
    if (x1a>x1)
      x1 = x1a;
  }
  /* Now I need to calculate the Placement that will ensure the
     appropriate mapping at the edges.
     I need: a*x0+b = px0   (1)
     a*x1+b = px1   (2)
     Solve for a and b.
     Then use these a and b to set the Placement PX0 and PX1 to
     PX0 = a*X0+b   (3)
     PX1 = a*X1+b   (4)
     where X0 and X1 are the min and max data coord of the Axis.
     Subtract (1) and (2):
     a = (px1-px0) / (x1-x0)
     Then:
     b = px0 - a*x0.
  */
  double a = (px.max()-px.min()) / (x1-x0);
  double b = px.min() - a*x0;

  auto applyPlacement = [px, x0, x1, a, b, &f](Axis &axis) {
    if (axis.map(x0).x()<px.min()-SHIFTTOLERANCE ||
        axis.map(x1).x()>px.max()+SHIFTTOLERANCE)  {
      axis.setPlacement(QPointF(a*axis.min()+b, 0),
                     QPointF(a*axis.max()+b, 0));
      f.markFudged();
    }
  };

  applyPlacement(f.xAxis());
  // Now do the same for each of the panels
  foreach (QString id, ids) 
    applyPlacement(f.panelRef(id).xaxis);
}

void CmdShareLim::scaleY(Figure &f, QSet<QString> ids) {
  // Get the scale
  double scale = fabs(f.yAxis().maprel(1).y());
  foreach (QString id, ids) {
    Panel const &p(f.panelRef(id));
    double sc1 = fabs(p.yaxis.maprel(1).y());
    if (sc1<scale)
      scale = sc1;
  }

  auto applyScale = [scale, &f](Axis &axis) {
    double sc1 = fabs(axis.maprel(1).y());
    if (sc1>scale*(1+SCALETOLERANCE)) {
      // Let's actually shrink
      double currentHeight = axis.minp().y() - axis.maxp().y();
      double newHeight = currentHeight * scale/sc1;
      double shift = (currentHeight - newHeight)/2;
      axis.setPlacement(QPointF(0, axis.minp().y()-shift),
                             QPointF(0, axis.maxp().y()+shift));
      f.markFudged();
    }
  };

  
  // Apply the scale to current panel
  applyScale(f.yAxis());

  // Apply the scale to other panels
  foreach (QString id, ids) 
    applyScale(f.panelRef(id).yaxis);
}

void CmdShareLim::alignY(Figure &f, QSet<QString> ids) {
  // Find union of extents
  Range py(f.extent().top(), f.extent().bottom());
  foreach (QString id, ids) {
    Panel const &p(f.panelRef(id));
    py.unionize(Range(p.desiredExtent.top(), p.desiredExtent.bottom()));
  }
  // Find min and max represented there
  /* Note that I am assuming the axis has negative values on the bottom.
     I think I make that assumption throughout the program, probably
     to my ultimate detriment.
  */      
  double y0 = f.yAxis().rev(QPointF(0, py.max()));
  double y1 = f.yAxis().rev(QPointF(0, py.min()));
  foreach (QString id, ids) {
    Panel const &p(f.panelRef(id));
    double y0a = p.yaxis.rev(QPointF(0, py.max()));
    double y1a = p.yaxis.rev(QPointF(0, py.min()));
    if (y0a<y0)
      y0 = y0a;
    if (y1a>y1)
      y1 = y1a;
  }
  /* Now I need to calculate the Placement that will ensure the
     appropriate mapping at the edges.
     I need: a*y0+b = py0   (1)
     a*y1+b = py1   (2)
     Solve for a and b.
     Then use these a and b to set the Placement PY0 and PY1 to
     PY0 = a*Y0+b   (3)
     PY1 = a*Y1+b   (4)
     where Y0 and Y1 are the min and max data coord of the Axis.
     Subtract (1) and (2):
     a = (py1-py0) / (y1-y0)
     Then:
     b = py0 - a*y0.
  */
  double a = (py.min()-py.max()) / (y1-y0);
  double b = py.max() - a*y0;

  auto applyPlacement = [py, y0, y1, a, b, &f](Axis &axis) {
    if (axis.map(y1).y()<py.min()-SHIFTTOLERANCE ||
        axis.map(y0).y()>py.max()+SHIFTTOLERANCE) {
      axis.setPlacement(QPointF(0, a*axis.min()+b),
                        QPointF(0, a*axis.max()+b));
      f.markFudged();
    }
  };
   
  // Should current panel be shrunk?
  applyPlacement(f.yAxis());
   
  // Now do the same for each of the panels
  foreach (QString id, ids) 
    applyPlacement(f.panelRef(id).yaxis);
}
