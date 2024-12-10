#!/usr/bin/python3

import numpy as np
import qplot as qp

#%%
whitenoise = np.random.randn(256, 256)
ft_arr = np.fft.fftshift(np.fft.fft2(whitenoise))
xx, yy = np.mgrid[0:ft_arr.shape[0], 0:ft_arr.shape[1]]
f = np.hypot(xx - ft_arr.shape[0] / 2, yy - ft_arr.shape[1] / 2)
pink_ft_arr = ft_arr / (1 + f**1.5)
pink_ft_arr = np.nan_to_num(pink_ft_arr, nan=0, posinf=0, neginf=0) 
pinknoise = np.fft.ifft2(np.fft.ifftshift(pink_ft_arr)).real
zz = pinknoise
zz = zz / np.std(zz)

#%%
qp.figure('eg_imsc', 3, 2.5)
qp.luts.set('RdBu', 100, reverse=True)
qp.imsc(zz, xx=xx, yy=yy, c0=-3, c1=3)
qp.cbar(256, 0, 256)
qp.caxis('Density', qp.arange(-3, 3, 3), ticklen=5)
qp.minorticks(qp.arange(-2, 2, 1), ticklen=3)
qp.shrink(1, 1)
