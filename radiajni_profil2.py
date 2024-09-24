from photutils.isophote import Ellipse
import numpy as np
from astropy.modeling.models import Gaussian2D
from photutils.datasets import make_noise_image
import matplotlib.pyplot as plt
from photutils.aperture import EllipticalAperture
from photutils.isophote import EllipseGeometry
from astropy.io import fits 
from matplotlib.colors import LogNorm

fits_file = fits.open('corrected_i.fits')
data = fits_file[0].data 

section1 = data[1150:1489, 830:1300]

geometry2 = EllipseGeometry(x0=230, y0=194, sma=180, eps=0.27, pa=3)
aper = EllipticalAperture((geometry2.x0, geometry2.y0), geometry2.sma,geometry2.sma * (1 - geometry2.eps), geometry2.pa)

plt.imshow(section1, origin='lower', norm = LogNorm(), cmap = "Greys")
aper.plot(color='black')

ellipse = Ellipse(section1, geometry2)
isolist = ellipse.fit_image()
 
isolist.to_table()

#################################################################

from photutils.isophote import build_ellipse_model

fig, (ax1) = plt.subplots(figsize=(11, 4), nrows=1, ncols=1)
ax1.imshow(section1, origin='lower', norm = LogNorm(), cmap="Greys")
ax1.set_title('Podaci')

smas = np.linspace(12, 170, 50)
for sma in smas:
    iso = isolist.get_closest(sma)
    x, y, = iso.sampled_coordinates()
    ax1.plot(x, y, color='black')

model = build_ellipse_model(section1.shape, isolist)
fig, (ax2) = plt.subplots(figsize=(11, 4), nrows=1, ncols=1)
ax2.imshow(model, origin='lower', vmin=0, vmax=1)
ax2.set_title('Model povrsinskog sjaja')

#################################################################

plt.figure(figsize=(6, 6))

#plt.subplots_adjust(hspace=0.35, wspace=0.35)
#plt.subplot(2, 2, 1)

plt.errorbar(isolist.sma, isolist.intens, yerr=isolist.int_err,fmt='o', markersize=2)
plt.xlabel('Velika poluosa (pix)')
plt.ylabel('Intenzitet (pix)')

#################################################################

