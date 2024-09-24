#probaj radial profile

import numpy as np
from astropy.modeling.models import Gaussian2D
from astropy.io import fits 
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from photutils.centroids import centroid_quadratic
from photutils.profiles import RadialProfile


fits_file = fits.open('corrected_i.fits')
data = fits_file[0].data 

section1 = data[1150:1489, 830:1300]
plt.imshow(section1, origin = "lower", norm = LogNorm(), cmap = "Greys")

xycen = centroid_quadratic(section1,xpeak=230, ypeak=195)
print(xycen)  

edge_radii = np.arange(200)
profil = RadialProfile(section1, xycen, edge_radii, mask=None)

---------------------------------------------------------------------

#print(rp.radius) 
#print(rp.profile) 

profil.normalize(method='max')
profil.plot(label='Radial Profile')

---------------------------------------------------------------------

from astropy.visualization import simple_norm

norm = simple_norm(section1, 'sqrt')

plt.figure(figsize=(6, 6))
plt.imshow(section1,origin = "lower", norm=LogNorm(),cmap = "Greys")

profil.apertures[10].plot(color='C0', lw=1)
profil.apertures[90].plot(color='C1', lw=1)
profil.apertures[130].plot(color='C3', lw=1)

---------------------------------------------------------------------

profil.plot(label='Radijalni profil')
plt.plot(profil.radius, profil.gaussian_profile, label='Gausijan')
plt.legend()

---------------------------------------------------------------------