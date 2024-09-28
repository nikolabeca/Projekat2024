# %%
#oduzmi sextrator (ucitaj kao fits)

#učitavanje fits fajla galaksije

from astropy.io import fits 
import matplotlib.pyplot as plt
import numpy as np
from photutils.isophote import Ellipse
from astropy.modeling.models import Gaussian2D
from photutils.datasets import make_noise_image
from photutils.aperture import EllipticalAperture
from photutils.isophote import EllipseGeometry
from matplotlib.colors import LogNorm

fits_file = fits.open('corrected_i.fits')
image_data = fits_file[0].data 

#section1 = image_data[1150:1489, 830:1300]

plt.figure()
plt.imshow(image_data, origin = "lower", norm = LogNorm(), cmap = "Greys")
plt.colorbar()
plt.show()

#zanimaju me dimenzije slike u pikselima, da uporedim sa dimenzijom maske
fits_file.info()

# %%
#7)pozadinski objekti (vrv najkorisnije)

#učitavanje maske iz sextractora

fits_file7 = fits.open('objbck.fits')
objct2 = fits_file7[0].data 

plt.figure()
plt.imshow(objct2, origin = "lower", norm = LogNorm(), cmap = "Greys")

#zanimaju me dimenzije
fits_file7.info()



# %%
#fits fajl sa objektima u pozadini nije istih dimenzija kao section1
#image_data = (2048, 1489)
#objct2 = (477,738)
#lako se može napraviti da fajlovi budu istih dimenzija i to je prvo što sam pomislio
#ali to nije dovoljno već mi je potrevno da na istim koordinatama budu isti pikseli kod obe slike
#možda je lakše originalne podatke skalirati tako da se uklope sa maskom (probati prvo)

# %%
section2 = objct2[30:393, 134:604]

plt.figure()
plt.imshow(section2, origin = "lower", norm = LogNorm(), cmap = "Greys")

#neki neuspeli pokušaj

# %%
#oduzeti pozadinski objekti 

#ovde sam shvatio da ne mogu oduzeti jer nisu iste skale

residual1 = image_data - objct2

norm = ImageNormalize(stretch=SqrtStretch())
plt.imshow(residual1, norm=LogNorm() , origin='lower',cmap='Greys', interpolation='nearest')
plt.title('Oduzeta pozadina NGC 941')


