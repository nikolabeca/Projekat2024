# %%
from photutils.isophote import Ellipse
import numpy as np
from astropy.modeling.models import Gaussian2D
from photutils.datasets import make_noise_image
import matplotlib.pyplot as plt
from photutils.aperture import EllipticalAperture
from photutils.isophote import EllipseGeometry
from astropy.io import fits 
from matplotlib.colors import LogNorm

# %%
fits_file = fits.open('corrected_i.fits')
data = fits_file[0].data 

section1 = data[1150:1489, 830:1300]
plt.imshow(section1, origin='lower', norm = LogNorm(), cmap = "Greys")
plt.title('NGC 941')

# %%
from astropy.stats import SigmaClip
from photutils.background import Background2D, MedianBackground
from photutils.datasets import make_100gaussians_image


sigma_clip = SigmaClip(sigma=3.0)
bkg_estimator = MedianBackground()
bkg = Background2D(section1, (40, 40), filter_size=(3, 3), sigma_clip=sigma_clip, bkg_estimator=bkg_estimator)

plt.imshow(bkg.background, origin='lower', cmap='Greys', interpolation='nearest')
plt.title('Pozadina NGC 941 (1)')

print(bkg.background_rms_median)  

# %%
from astropy.visualization import SqrtStretch
from astropy.visualization.mpl_normalize import ImageNormalize

residual1 = section1 - bkg.background
norm = ImageNormalize(stretch=SqrtStretch())
plt.imshow(residual1, norm=LogNorm() , origin='lower',cmap='Greys', interpolation='nearest')
plt.title('Oduzeta pozadina NGC 941 (1)')

# %%
coverage_mask = (section1 == 0)

bkg3 = Background2D(section1, (160, 160), filter_size=(3, 3),coverage_mask=coverage_mask, fill_value=0.0, exclude_percentile=87.0)
norm = ImageNormalize(stretch=SqrtStretch())

#box_size (drugi parametar): ispod 160*160 ne postoji odgovarajući fit, a treba mi što manja vrednost 
#probati exclude_percentile varijacije: 100 znači da će isključiti maksimalno piksela (probati približno 100)

plt.imshow(bkg3.background, origin='lower', cmap='Greys_r', norm=norm, interpolation='nearest')
plt.title('Pozadina NGC 941 (2)')

# %%
residual2 = section1 - bkg3.background

norm = ImageNormalize(stretch=SqrtStretch())
plt.imshow(residual2, origin='lower', cmap='Greys', norm=LogNorm(), interpolation='nearest')
plt.title('Oduzeta pozadina NGC 941 (2)')

# %%
geometry2 = EllipseGeometry(x0=230, y0=194, sma=180, eps=0.27, pa=3)
aper = EllipticalAperture((geometry2.x0, geometry2.y0), geometry2.sma,geometry2.sma * (1 - geometry2.eps), geometry2.pa)

plt.imshow(residual2, origin='lower', norm = LogNorm(), cmap = "Greys")
aper.plot(color='black')

ellipse = Ellipse(residual2, geometry2)
isolist = ellipse.fit_image()

# %%
plt.errorbar(isolist.sma, isolist.intens, yerr=isolist.int_err,fmt='o', markersize=2)
plt.xlabel('Velika poluosa (pix)')
plt.ylabel('Intenzitet (pix)')


