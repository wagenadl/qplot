// bintest.cpp - This file is part of QPlot

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

#include <stdio.h>
#include <math.h>

int main() {
  printf("plot *100 *100\n");
  for (int k=0; k<100; k++) {
    double v = k;
    fwrite(&v, sizeof(double), 1, stdout);
  }
  for (int k=0; k<100; k++) {
    double v = cos(2*3.1415*k/100);
    fwrite(&v, sizeof(double), 1, stdout);
  }
  printf("pen red\n");
  printf("plot *100 *100\n");
  for (int k=0; k<100; k++) {
    double v = k;
    fwrite(&v, sizeof(double), 1, stdout);
  }
  for (int k=0; k<100; k++) {
    double v = sin(2*3.1415*k/100);
    fwrite(&v, sizeof(double), 1, stdout);
  }
  printf("fudge\n");  
  return 0;
}
