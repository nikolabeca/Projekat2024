from astropy.wcs import WCS
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits
import matplotlib.pyplot as plt
from photutils.aperture import aperture_photometry
from photutils.aperture import SkyCircularAperture
from photutils.aperture import CircularAperture

aperture = CircularAperture((1,2), r=3.0)

fits_file = fits.open('corrected_i.fits')
data = fits_file[0].data 

phot_table = aperture_photometry(data, aperture)
phot_table['aperture_sum'].info.format = '%.8g'  # for consistent table output
print(phot_table)
