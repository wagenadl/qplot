/* sampleminmax.c */

#include "mex.h"
#include <math.h>
#include <stdio.h>

typedef double idxtype;

void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[]) {
  double *xx;
  double *y_min;
  double *y_max;
  idxtype *ii;
  int X; /* length of xx */
  int N; /* length of ii */
  int n;

  if (nrhs!=2)
    mexErrMsgTxt("SAMPLEMINMAX: Two inputs required.");
  if (nlhs!=2) 
    mexErrMsgTxt("SAMPLEMINMAX: Two outputs required.");
    
  /* Check input argument XX. */
  if (!mxIsDouble(prhs[0]) || mxIsComplex(prhs[0]) ||
      (mxGetN(prhs[0])>1 && mxGetM(prhs[0])>1))
    mexErrMsgTxt("SAMPLEMINMAX: Input XX must be a real vector.");

  /* Check input argument II. */
  if (!mxIsDouble(prhs[1]) || mxIsComplex(prhs[1]) ||
      (mxGetN(prhs[1])>1 && mxGetM(prhs[1])>1))
    mexErrMsgTxt("SAMPLEMINMAX: Input II must be a real vector.");

  xx = mxGetPr(prhs[0]);
  ii = mxGetPr(prhs[1]);

  X = mxGetM(prhs[0])*mxGetN(prhs[0]);
  N = mxGetM(prhs[1])*mxGetN(prhs[1]);

  if (mxGetM(prhs[1])>1) {
    plhs[0] = mxCreateDoubleMatrix(N-1,1,mxREAL);
    plhs[1] = mxCreateDoubleMatrix(N-1,1,mxREAL);
  } else {
    plhs[0] = mxCreateDoubleMatrix(1,N-1,mxREAL);
    plhs[1] = mxCreateDoubleMatrix(1,N-1,mxREAL);
  }

  y_min = mxGetPr(plhs[0]);
  y_max = mxGetPr(plhs[1]);

  /*fprintf(stderr,"N=%i y_min=%p y_max=%p\n",N,y_min,y_max);*/

  for (n=0; n<N-1; n++) {
    double mx;
    double mn;
    int i;
    int i0 = (int)(ii[n])-1; /* convert from matlab style 1,2,3 indexing ... */
    int i1 = (int)(ii[n+1])-1; /* ... to C style 0,1,2 indexing. */
    if (i0<0)
      i0=0;
    if (i1>=X)
      i1=X-1;
    mx=mn=xx[i0];
    for (i=i0; i<i1; i++) {
      if (xx[i]>mx)
	mx=xx[i];
      if (xx[i]<mn)
	mn=xx[i];
    }
    y_min[n] = mn;
    y_max[n] = mx;
  }
}
