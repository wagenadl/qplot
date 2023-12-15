// CmdRebalance.cpp - This file is part of QPlot

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

// CmdRebalance.C

#include "CmdRebalance.h"

#include <QDebug>
#include <math.h>
#include "Error.h"
#include "Range.h"
#include "WhichAxis.h"

static CBuilder<CmdRebalance> cbRebalance("rebalance");

constexpr double SCALETOLERANCE = 2e-3;
constexpr double SPACETOLERANCE = 1e-2; // pt


struct SpaceNeeds {
public:
  QRectF fullextent;
  QMap<QString, double> leftnondatause; // or top
  QMap<QString, double> rightnondatause; // or bottom
  QMap<QString, Range> datarange;
  QMap<QString, double> oldwidth;
public:
  SpaceNeeds();
  SpaceNeeds(Figure const &f, QStringList ids, WhichAxis const &wa) {
    // Get space available
    for (QString id: ids) {
      Panel const &p(f.panel(id));
      if (fullextent.isEmpty())
        fullextent = p.desiredExtent;
      else
        fullextent |= p.desiredExtent;
    }

    for (QString id: ids) {
      Panel const &p(f.panel(id));
      Axis const &axis(wa.axis(p));
      Range fullbb(wa.rectRange(p.fullbbox));
      Range desibb(wa.rectRange(p.desiredExtent));
      oldwidth[id] = desibb.range();
      Range databb(wa.axisPRange(axis));
      double prespace = databb.min() - fullbb.min();
      double postspace = fullbb.max() - databb.max();
      leftnondatause[id] = prespace;
      rightnondatause[id] = postspace;
      datarange[id] = Range(axis.min(), axis.max());
    }
  }
  double meanOldWidth() const {
    double ow = 0;
    for (double w: oldwidth)
      ow += w;
    return ow / oldwidth.size();
  }
  double maxNonData() const {
    return maxLeftNonData() + maxRightNonData();
  }
  double maxLeftNonData() const {
    double x = 0;
    for (double nd: leftnondatause)
      if (nd>x)
        x = nd;
    return x;
  }
  double maxRightNonData() const {
    double x = 0;
    for (double nd: rightnondatause)
      if (nd>x)
        x = nd;
    return x;
  }
  Range overallDataRange() const { // union of ranges
    Range dr;
    for (Range const &r: datarange)
      dr.unionize(r);
    return dr;
  }
};


bool CmdRebalance::usage() {
  return error("Usage: rebalance ID ...\n");
}

static QList<QStringList> blocks(Statement const &s) {
  QList<QStringList> result;
  QStringList current;
  for (int i=2; i<s.length(); i++) {
    if (s[i].typ==Token::CAPITAL) {
      current << s[i].str;
    } else if (s[i].typ==Token::DASH) {
      if (!current.isEmpty())
        result << current;
      current = QStringList();
    } else {
      return QList<QStringList>(); // fail if unexpected token
    }
  }
  if (!current.isEmpty())
    result << current; // we tolerate final DASH
  if (result.isEmpty())
    return QList<QStringList>(); // fail if nothing read
  for (QStringList const &lst: result)
    if (lst.size() < 2)
      return QList<QStringList>(); // fail if not at least two IDs in each list
  return result;
}
  

bool CmdRebalance::parse(Statement const &s) {
  if (s.length()<3)
    return usage(); // we could allow this null case, but that might confuse

  if (s[1].typ!=Token::BAREWORD)
    return usage();
  if (!(s[1].str=="x" || s[1].str=="y" || s[1].str=="xy"))
    return usage();
  if (blocks(s).isEmpty())
    return usage();
  return true;
}


static void rebalance(Figure &f, QList<QStringList> blocks,
                      WhichAxis const &wa) {
  qDebug() << "rebalance" << blocks;

  /* First step is to measure the "groups" within each block, i.e., the
     columns if wa=X or rows is wa=Y. There must be an equal number of
     groups in each block, or the operation does not make sense.
  */

  int B = blocks.size();
  if (B==0)
    return;

  QList<QList<QStringList>> groupsbyblock; // block# -> group# -> ids
  QList<QList<SpaceNeeds>> groupneedsbyblock;
  int N = -1; // groups per block
  for (QStringList block: blocks) {
    QList<QStringList> groups = wa.orderedGroups(f, block);
    if (N<0)
      N = groups.size();
    if (groups.size()!=N) {
      Error() << "Group mismatch";
      return;
    }
    groupsbyblock << groups;

    QList<SpaceNeeds> groupneeds;
    for (QStringList const &group: groups)
      groupneeds << SpaceNeeds(f, group, wa);
    groupneedsbyblock << groupneeds;
  }

  /* Next, the total nondata use within each "hypercolumn", i.e.,
     stack of columns across blocks. [I'll use "columns" which is
     correct for X; read "rows" for Y.] Also, total nondatause across
     all hypercolumns together. The rest is available for data.
  */
  QList<double> hypercolumnleftnondata;
  QList<double> hypercolumnrightnondata;
  double totalnondata;
  for (int n=0; n<N; n++) {
    double lnd = 0;
    double rnd = 0;
    for (QList<SpaceNeeds> const &needs: groupneedsbyblock) {
      double lnd1 = needs[n].maxLeftNonData();
      if (lnd1>lnd)
        lnd = lnd1;
      double rnd1 = needs[n].maxRightNonData();
      if (rnd1>rnd)
        rnd = rnd1;
    }
    hypercolumnleftnondata << lnd;
    hypercolumnrightnondata << rnd;
    totalnondata += lnd + rnd;
  }

  // Figure out full extent of each block
  QList<Range> fullextents;
  for (QList<SpaceNeeds> const &needs: groupneedsbyblock) {
    Range fe;
    for (SpaceNeeds const &need: needs)  // loop over columns
      fe.unionize(wa.rectRange(need.fullextent));
    fullextents << fe;
  }
  
  // Figure out the scale of the first block
  QList<double> scales; // will eventually contain scale for each block
  double totaldata = 0;
  for (SpaceNeeds const &need: groupneedsbyblock[0]) // loop over columns
    totaldata += need.overallDataRange().range();
  scales << (fullextents[0].range() - totalnondata) / totaldata;
  
  // Figure out new proposal for sharing space in first block
  bool trivial = true;
  QList<double> propwidth; // per column
  for (int n=0; n<N; n++) {
    SpaceNeeds const &need(groupneedsbyblock[0][n]);
    double desired = hypercolumnleftnondata[n] + hypercolumnrightnondata[n] 
      + need.overallDataRange().range() * scales[0];
    propwidth << desired;
    if (fabs(desired - need.meanOldWidth()) > SPACETOLERANCE)
      trivial = false;
  }

  // Now figure out scales for other blocks using same space distr
  for (int b=1; b<B; b++) {
    QList<SpaceNeeds> const &needs(groupneedsbyblock[b]);
    double scl = -1;
    for (int n=0; n<N; n++) { // loop over columns
      SpaceNeeds const &need(needs[n]);
      double dr = need.overallDataRange().range();
      double lnd = hypercolumnleftnondata[n];
      double rnd = hypercolumnrightnondata[n];

      double s = (propwidth[n] - lnd - rnd) / dr;
      if (scl<0 || s<scl)
        scl = s;
      if (fabs(propwidth[n] - need.meanOldWidth()) > SPACETOLERANCE)
        trivial = false;
    }
    scales << scl;
  }
    
  if (trivial)
      return;

  // Apply the scale to all panels
  for (int b=0; b<B; b++) {
    QList<SpaceNeeds> const &needs(groupneedsbyblock[b]);
    double x0 = fullextents[b].min();
    double scale = scales[b];
    for (int n=0; n<N; n++) {
      SpaceNeeds const &need(needs[n]);
      Range dr = need.overallDataRange();
      double x1 = x0 + propwidth[n];
      double xleft = x0 + hypercolumnleftnondata[n];
      for (QString id: groupsbyblock[b][n]) {
        Panel &panel(f.panelRef(id));
        QRectF ext = wa.rerect(panel.desiredExtent, x0, x1);
        f.overridePanelExtent(id, ext);
        Axis &axis(wa.axis(panel));
        axis.setDataRange(dr.min(), dr.max());
        bool rev = wa.point(axis.maprel(1)) < 0;
        double xright = xleft + dr.range()*scale;
        double px0 = rev ? xright : xleft;
        double px1 = rev ? xleft : xright;
        axis.setPlacement(wa.repoint(axis.minp(), px0),
                          wa.repoint(axis.maxp(), px1));
        qDebug() << id << dr.min() << dr.max() << xleft << xright << rev << ext;
      }
      x0 = x1;
    }
  }

  f.markFudged();
}

void CmdRebalance::render(Statement const &s, Figure &f, bool) {
  bool shareX = s[1].str.contains("x");
  bool shareY = s[1].str.contains("y");

  
  QList<QStringList> blks = blocks(s);
  for (QStringList blk: blks) {
    for (QString id: blk) {
      if (!f.hasPanel(id)) {
        Error() << "Unknown panel: " << id;
        return;
      }
    }
  }

  f.leavePanel();

  if (shareX) 
    rebalance(f, blks, WhichAxis::x());
  if (shareY) 
    rebalance(f, blks, WhichAxis::y());
}
