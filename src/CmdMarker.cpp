// CmdMarker.cpp - This file is part of QPlot

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

// CmdMarker.C

#include "CmdMarker.H"

static CBuilder<CmdMarker> cbMarker("marker");

bool CmdMarker::usage() {
  return error("Usage: marker size|open|solid|white|brush|circle|square|diamond|left|right|up|down|penta|hexa|hbar|vbar|plus|cross");
}

static int fillstyle(QString s) {
  if (s=="open")
    return Marker::OPEN;
  else if (s=="solid")
    return Marker::CLOSED;
  else if (s=="brush")
    return Marker::BRUSH;
  else if (s=="spine")
    return Marker::SPINE;
  else
    return -1;
}

static int markertype(QString s) {
  if (s=="circle")
    return Marker::CIRCLE;
  else if (s=="square")
    return Marker::SQUARE;
  else if (s=="diamond")
    return Marker::DIAMOND;
  else if (s=="left")
    return Marker::LEFTTRIANGLE;
  else if (s=="right")
    return Marker::RIGHTTRIANGLE;
  else if (s=="up")
    return Marker::UPTRIANGLE;
  else if (s=="down")
    return Marker::DOWNTRIANGLE;
  else if (s=="penta")
    return Marker::PENTAGRAM;
  else if (s=="hexa")
    return Marker::HEXAGRAM;
  else if (s=="hbar")
    return Marker::HBAR;
  else if (s=="vbar")
    return Marker::VBAR;
  else if (s=="plus")
    return Marker::PLUS;
  else if (s=="cross")
    return Marker::CROSS;
  else
    return -1;
}

bool CmdMarker::parse(Statement const &s) {
  if (s.length()<2)
    return usage();
  for (int k=1; k<s.length(); k++) {
    if (s[k].typ==Token::NUMBER) {
      continue; // OK, this is size
    } else if (s[k].typ==Token::BAREWORD) {
      QString w = s[k].str;
      if (markertype(w)>=0)
	continue;
      else if (fillstyle(w)>=0)
	continue;
      else
	return usage();
    } else
      return usage();
  }
  return true;
}

void CmdMarker::render(Statement const &s, Figure &f, bool) {
  for (int k=1; k<s.length(); k++) {
    if (s[k].typ==Token::NUMBER) {
      f.marker().radius = pt2iu(s[k].num) / 2;
    } else if (s[k].typ==Token::BAREWORD) {
      QString w = s[k].str;
      if (markertype(w)>=0)
	f.marker().type = Marker::Type(markertype(w));
      else if (fillstyle(w)>=0)
	f.marker().fill = Marker::Fill(fillstyle(w));
    }
  }
}
