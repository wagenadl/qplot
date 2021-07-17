// Slightly.cpp - This file is part of QPlot

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

// Slightly.C

#include "Slightly.h"

#define EPSI (1e-25)

double Slightly::less(double x) {
  double epsi = EPSI;
  double x0 = x-epsi;
  while (x0==x) {
    epsi *= 10;
    x0 = x-epsi;
  }
  return x0;
}
    
double Slightly::more(double x) {
  double epsi = EPSI;
  double x0 = x+epsi;
  while (x0==x) {
    epsi *= 10;
    x0 = x+epsi;
  }
  return x0;
}
    
