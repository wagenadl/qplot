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
