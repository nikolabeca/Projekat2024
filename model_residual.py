import numpy as np
from astropy.io import fits 
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from photutils.isophote import EllipseGeometry
from photutils.aperture import EllipticalAperture
from photutils.aperture import aperture_photometry
from photutils.isophote import Ellipse
from photutils.isophote import build_ellipse_model 

#################################################################

#1 pixel = 0.39591036 arcsec

vps = 70.8333 #velika poluosa
mps = 62.5 #mala poluosa

c = np.sqrt((vps**2)-mps**2)
eks = c/vps 

fits_file = fits.open('corrected_i.fits')
data = fits_file[0].data 

geometry1 = EllipseGeometry(x0=1062, y0=1334.8333, sma=vps, eps=eks, pa=0) 
aper = EllipticalAperture((geometry1.x0, geometry1.y0), geometry1.sma, geometry1.sma * (1 - geometry1.eps), geometry1.pa)

plt.imshow(data, origin = "lower", norm = LogNorm(), cmap = "Greys")
plt.colorbar()
aper.plot(color='red')
plt.show()

#################################################################

fits_file = fits.open('corrected_i.fits')
data = fits_file[0].data 

section1 = data[1150:1489, 830:1300]

geometry2 = EllipseGeometry(x0=230, y0=194, sma=180, eps=0.27, pa=3) 
ellip1 = EllipticalAperture((geometry2.x0, geometry2.y0), geometry2.sma, geometry2.sma * (1 - geometry2.eps), geometry2.pa)


ellip1.plot(color="black")

plt.imshow(section1, origin = "lower", norm = LogNorm(), cmap = "Reds")
plt.colorbar()
plt.show()

#centriraj boljje

#################################################################

ellipse = Ellipse(section1, geometry2)
isolist = ellipse.fit_image()

model = build_ellipse_model(section1.shape, isolist)

fig, (ax2) = plt.subplots(figsize=(11, 4), nrows=1, ncols=1)

#smas = np.linspace(10, 50, 5)
#for sma in smas:
#    iso = isolist.get_closest(sma)
#    x, y, = iso.sampled_coordinates()
 #   ax1.plot(x, y, color='white')

ax2.imshow(model, origin='lower', vmin=0, vmax=1)
ax2.set_title('Model površinskog sjaja')

#################################################################

geometry2 = EllipseGeometry(x0=230, y0=194, sma=80, eps=0.27, pa=3) 
ellip2 = EllipticalAperture((geometry2.x0, geometry2.y0), geometry2.sma, geometry2.sma * (1 - geometry2.eps), geometry2.pa)

ellip2.plot(color="black")

plt.imshow(section1, origin = "lower", norm = LogNorm(), cmap = "Reds")
plt.colorbar()
plt.show()

#################################################################

#rezidual

residual = section1 - model

fig, (ax1, ax2, ax3) = plt.subplots(figsize=(14, 5), nrows=1, ncols=3)
fig.subplots_adjust(left=0.04, right=0.98, bottom=0.02, top=0.98)
ax1.imshow(section1, origin='lower', norm = LogNorm(), cmap="Blues")
ax1.set_title('Podaci')

smas = np.linspace(12, 170, 6)
for sma in smas:
    iso = isolist.get_closest(sma)
    x, y, = iso.sampled_coordinates()
    ax1.plot(x, y, color='black')

ax2.imshow(model, origin='lower', vmin=0, vmax=0.7)
ax2.set_title('Model površinskog sjaja')

ax3.imshow(residual, origin="lower", norm = LogNorm()) 
ax3.set_title('Rezidual')

plt.show()

#vidi odakle mu ove elipse koje je opisao na podacima, odrediti r 

#################################################################