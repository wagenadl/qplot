# Everything in the Images category

# image
# imsc
# lut
# gimage
# cbar (vcbar)
# hcbar

from . import qi
from . import axes
from . import utils

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
    S = data.shape
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

def gimage(img, drect=None, prect=None):
    '''GIMAGE - Place an image with data and paper coordinates
    GIMAGE(img, drect, prect) places an image on a location in
    the graph specified by both data coordinates and image coordinates.
    For example: GIMAGE(img, [5, 5, 0, 0], [0, 0, 36, 72]) creates an 
    image of 0.5x1" at data location (5,5). 
    GIMAGE(img, [5, np.nan, 0, 5], [0, 36, 72, 0]) creates an 
    image 1" wide, 5 data units high, at x=5, 1" below the top of the graph.
    Etc.'''
    
    S = img.shape
    Y = S[0]
    X = S[1]
    if len(S)==2:
        C = 1
    else:
        C = S[2]
    if C==1 or C==3 or C==4:
        pass
    else:
        error('Image must have 1, 3, or 4 planes')

    if drect is None:
        drect = [ np.nan, np.nan, 0, 0]
    if prect is None:
        prect = [ 0, 0, 0, 0 ]
    
    if len(drect)!=4 or len(prect)!=4:
        error('Position must given as [x y w h]')

    out = [ 'image', '[' ]
    for v in drect:
        out.append('%g' % v)
    out.append(']')
    out.append('[')
    for v in prect:
        out.append('%g' % v)
    out.append(']')
    out.append('[')
    out.append('%i' % X)
    out.append('%i' % Y)
    out.append('%i' % C)
    out.append(']')
    out.append('%uc%i' % X*Y*C)
    qi.ensure()
    qi.f.write(out)
    if img.dtype!='uint8':
        img = 255*img+.5
        img[img<0] = 0
        img[img>255] = 255
        img = img.astype('uint8')
    qi.f.writeuc(img)

class CBarInfo:
    def __init__(self, clim, orient, drect, prect, rev):
        self.clim = clim
        self.orient = orient
        self.drect = drect
        self.prect = prect
        self.rev = rev
        def ctodat(self, cc):
            crel = (cc - self.clim[0]) / (self.clim[1] - self.clim[0])
            if self.orient=='y':
                d0 = self.drect[1]
                dw = self.drect[3]
            else:
                d0 = self.drect[0]
                dw = self.drect[2]
            if self.rec:
                d0 += dw
                dw = -dw
            return d0 + dw*crel

def cbar(x0=None, y0=None, y1=None, width=5, dist=10):
    '''CBAR - Add a vertical color bar to a figure
    CBAR() without arguments creates a color bar to the right of the
    latest IMSC.
    CBAR(x0, y0, y1) adds a vertical color bar to the figure between
    (X0, Y0) and (X0, Y1), expressed in data coordinates.
    If Y1>Y0, the color bar runs up, otherwise it runs down.
    Optional argument WIDTH specifies the width of the color bar in points 
    (default: 5 points). If WIDTH is positive, the bar extends to the right
    of X0, otherwise to the left.
    Optional argument DIST creates distance between X0 and the color bar by
    shifting the color bar to the right. (Negative DIST shifts it to the left.)
    This only works after a preceding IMSC and uses the lookup table (LUT)
    used by that IMSC.
    Use CAXIS to place an axis along the bar.
    See also HCBAR.'''
    
    qi.ensure()
    if qi.f.imrect is None or qi.f.lut is None or qi.f.clim is None:
        qi.error('VCBAR must have a previous imsc')    
    if x0 is None or y0 is None or y1 is None:
        x0 = qi.f.imrect[0] + qi.f.imrect[2]
        y0 = qi.f.imrect[1]
        y1 = qi.f.imrect[1] + qi.f.imrect[3]
        print('vcbar(%g, %g, %g, %g)\n' % (x0, y0, y1, w))

    isup = y1>y0
    if isup:
        drect = [x0, y0, 0, y1-y0]
    else:
        drect = [x0, y1, 0, y0-y1]

    if width<0:
        prect = [dist+width, 0, -width, 0]
    else:
        prect = [dist, 0, width, 0]

    lut = qi.f.lut
    if isup:
        lut = np.flip(lut, 0)
    C = lut.shape[0]
    gimage(np.reshape(lut, (C,1,3)), drect, prect)
    qi.f.cbar = CBarInfo(qi.f.clim, 'y', drect, prect, not isup)

def hcbar(y0=None, x0=None, x1=None, width=5, dist=10):
    '''HCBAR - Add a horizontal color bar to a figure
    HCBAR without arguments creates a color bar below the latest IMSC.
    HCBAR(y0, x0, x1) adds a horizontal color bar to the figure between
    (X0, Y0) and (X1, Y0), expressed in data coordinates.
    If X1>X0, the color bar to the right; otherwise it runs to the left.
    Optional argument WIDTH specifies the width of the color bar in 
    points (default: 5 pt). If WIDTH is positive, the bar extends down 
    below Y0, otherwise above.
    Optional argument DIST creates distance between Y0 and the color bar by
    shifting the color bar down. (Negative DIST shifts it up.)
    This only works after a preceding IMSC and uses the lookup table (LUT)
    used by that IMSC.
    HCBAR only works after a preceding IMSC and uses the lookup table (QLUT)
    used by that IMSC.
    Use CAXIS to place an axis along the bar.'''

    qi.ensure()
    if qi.f.imrect is None or qi.f.lut is None or qi.f.clim is None:
        qi.error('HCBAR must have a previous imsc')    
    
    if y0 is None or x0 is None or x1 is None:
        y0 = qi.f.imrect[1]
        x0 = qi.f.imrect[0]
        x1 = qi.f.imrect[0] + qi.f.imrect[2]

    isright = x1>x0
    if isright:
        drect = [x0, y0, x1-x0, 0]
    else:
        drect = [x1, y0, x0-x1, 0]
        
    if width<0:
        prect = [0, dist-width, 0, -width]
    else:
        prect = [0, dist, 0, width]

    C = lut.shape[0]
    gimage(np.reshape(lut, (1,C,3)), drect, prect)
    qi.f.cbar = CBarInfo(qi.f.clim, 'x', drect, prect, not isright)
    
def xzimage(data, rect, proj, y=0):
    '''XZIMAGE - Plot an image in projected xz-plane.
    XZIMAGE(data, (x0, z0, w, d), (xz, yz)) plots an image in the 
    xz-plane projected to the paper plane by x' = x + xz*z, y' = y + yz*z.
    The image must be YxXxC, where C=1 for grayscale, C=2 for grayscale+alpha,
    C=3 for RGB, C=4 for RGB+alpha. The image may be either UINT8 or FLOAT.
    If W is negative, the image is flipped right to left.
    If D is negative, the image is flipped in the z-dimension.
    Optional argument Y specifies y-axis intersect of the image plane.
    If None is given as a second argument, the pixel size of the image is 
    used.'''
    S = data.shape
    if rect is None:
        X = S[1]
        Z = S[0]
        rect = (0, 0, X, Z)
    if rect[2] < 0:
        data = np.flip(data, 1)
        rect = (rect[0] + rect[2], rect[1], -rect[2], rect[3])
    if rect[3] < 0:
        data = np.flip(data, 0)
        rect = (rect[0], rect[1] + rect[3], rect[2], -rect[3])

    S = data.shape
    Z = S[0]
    X = S[1]
    if len(S)==2:
        C = 1
    else:
        C = S[2]
    if data.size != Z*X*C:
        qi.error('Data has inconsistent size')
    qi.ensure()
    if data.dtype!='uint8':
        data = (255*data+.5).astype('uint8')
    qi.f.write('xzimage %g %g %g %g %g %g %g %i %i *uc%i\n'
                   % (rect[0], rect[1], rect[2], rect[3],
                      y, proj[0], proj[1], X, Z, X*Z*C))
    qi.f.writeuc(data)

def zyimage(data, rect, proj):
    '''ZYIMAGE - Plot an image in projected zy-plane.
    ZYIMAGE(data, (z0, y0, d, h), (xz, yz)) plots an image in the 
    zy-plane projected to the paper plane by x' = x + xz*z, y' = y + yz*z.
    The image must be YxXxC, where C=1 for grayscale, C=2 for grayscale+alpha,
    C=3 for RGB, C=4 for RGB+alpha. The image may be either UINT8 or FLOAT.
    If D is negative, the image is flipped in the z-dimension.
    If H is negative, the image is flipped vertically.
    If None is given as a second argument, the pixel size of the image is 
    used.'''
    S = data.shape
    if rect is None:
        Z = S[1]
        Y = S[0]
        rect = (0, 0, Z, Y)
    if rect[2] < 0:
        data = np.flip(data, 1)
        rect = (rect[0] + rect[2], rect[1], -rect[2], rect[3])
    if rect[3] < 0:
        data = np.flip(data, 0)
        rect = (rect[0], rect[1] + rect[3], rect[2], -rect[3])

    S = data.shape
    Y = S[0]
    Z = S[1]
    if len(S)==2:
        C = 1
    else:
        C = S[2]
    if data.size != Y*Z*C:
        qi.error('Data has inconsistent size')
    qi.ensure()
    if data.dtype!='uint8':
        data = (255*data+.5).astype('uint8')
    qi.f.write('zyimage %g %g %g %g %g %g %i %i *uc%i\n'
                   % (rect[0], rect[1], rect[2], rect[3],
                      proj[0], proj[1], Z, Y, Z*Y*C))
    qi.f.writeuc(data)
