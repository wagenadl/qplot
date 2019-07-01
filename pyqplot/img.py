# Everything in the Images category

# image
# imsc
# lut

import qi
import utils

def image(data, rect=None, xx=None, yy=None):
    '''IMAGE - Plot an image
    IMAGE(data) plots an image at (0,0)+(XxY). Note that that differs
    by 0.5 units from matlab conventions. The image must be YxXx1 or YxXx3
    and may be either UINT8 or FLOAT.
    IMAGE(data, rect=(x, y, w, h)) specifies location and scale.
    If H is negative, the image is plotted upside down.
    If W is negative, the image is flipped right to left.
    Instead of RECT, optional arguments XX and YY may be used to specify
    bin centers. Only the first and last elements of the vectors are
    actually used.'''
    if rect is None:
        X = S[1]
        Y = S[0]
        if xx is None and yy is None:
            rect = (0, 0, X, Y)
        else:
            if X==1:
                dx = 1
            else:
                dx = (xx[-1] - xx[0]) / (X-1)
            if Y==1:
                dy = 1
            else:
                dy = (yy[-1] - yy[0]) / (Y-1)
            rect = (xx[0]-dx/2, yy[0]-dy/2, X*dx, Y*dy)
    if rect[2] < 0:
        data = np.flip(data, 1)
        rect = (rect[0] + rect[2], rect[1], -rect[2], rect[3])
    if rect[3] < 0:
        data = np.flip(data, 0)
        rect = (rect[0], rect[1] + rect[3], rect[2], -rect[3])

    S = data.shape
    Y = S[0]
    X = S[1]
    if len(S)==2:
        C = 1
    else:
        C = S[2]
    if data.size != Y*X*C:
        qi.error('Data has inconsistent size')
    qi.ensure()
    if data.dtype!='uint8':
        data = (255*data+.5).astype('uint8')
    if C==1:
        qi.f.write('imageg %g %g %g %g %i *uc%i\n'
                   % (rect[0], rect[1], rect[2], rect[3], X, X*Y*C))
    elif C==3:
        qi.f.write('image %g %g %g %g %i *uc%i\n'
                   % (rect[0], rect[1], rect[2], rect[3], X, X*Y*C))
    else:
        qi.error('Image data must be YxX or YxXx3')
    qi.f.writeuc(data)
    qi.f.imrect = rect

def imsc(data, rect=None, xx=None, yy=None, c0=None, c1=None):
    '''IMSC - Plot 2D data as an image using lookup table
    IMSC(data) plots the DATA as an image using a lookup previously
    set by QLUT. The color axis limits default to the min and max of the data.
    Optional arguments C0 and C1 override those limits.
    Optional argument RECT specifies (x, y, w, h) rectangle for placement
    as for IMAGE. Alternatively, XX and YY arguments can be used.'''
    lut = qi.f.lut
    nanc = qi.f.lut_nan
    if np.isnan(c0):
        c0 = np.min(data)
    if np.isnan(c1):
        c1 = np.max(data)
    qi.f.clim = (c0, c1)
    N = lut.shape[0]
    data = np.floor((N-.0001)*(data-c0)/(c1-c0))
    isn = np.isnan(data).nonzero()[0]
    data[isn] = 0
    data[data<0] = 0
    data[data>=N] = N-1
    data = data.astype('int')
    data = lut[data[:], :]
    K = isn.size
    if K>0:
        nanc = np.repeat(np.reshape(np.array(nanc),(1,3)),K,0)
        data[isn,:] = nanc
    image(data, rect, xx, yy)

def lut(cc=None, nanc=None):
    '''LUT - Set lookup table for future IMSC.
    LUT(cc) where CC is Nx3 sets a new lookup table for IMSC.
    LUT(cc, nanc) where NANC is a 3-tuple sets a special color to use
    for NaN values. (The default is white.)
    lut, nanc = LUT returns current values.'''

    qi.ensure()
    if cc is not None:
        qi.f.lut = cc
    if nanc is not None:
        qi.f.lut_nan = nanc
    return (qi.f.lut, qi.f.lut_nan)
