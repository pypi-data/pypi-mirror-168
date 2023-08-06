# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sentinel_toolkit',
 'sentinel_toolkit.colorimetry',
 'sentinel_toolkit.colorimetry.illuminants',
 'sentinel_toolkit.colorimetry.tests',
 'sentinel_toolkit.converter',
 'sentinel_toolkit.converter.tests',
 'sentinel_toolkit.ecostress',
 'sentinel_toolkit.ecostress.tests',
 'sentinel_toolkit.product',
 'sentinel_toolkit.product.product_metadata',
 'sentinel_toolkit.product.product_metadata.tests',
 'sentinel_toolkit.product.tests',
 'sentinel_toolkit.srf',
 'sentinel_toolkit.srf.tests']

package_data = \
{'': ['*'],
 'sentinel_toolkit.product.product_metadata.tests': ['test_data/*'],
 'sentinel_toolkit.product.tests': ['test_data/S2B_MSIL2A_20220915T092029_N0400_R093_T34TGN_20220915T112452.SAFE/*',
                                    'test_data/S2B_MSIL2A_20220915T092029_N0400_R093_T34TGN_20220915T112452.SAFE/GRANULE/L2A_T34TGN_A028862_20220915T092030/IMG_DATA/R10m/*',
                                    'test_data/S2B_MSIL2A_20220915T092029_N0400_R093_T34TGN_20220915T112452.SAFE/GRANULE/L2A_T34TGN_A028862_20220915T092030/IMG_DATA/R20m/*'],
 'sentinel_toolkit.srf.tests': ['test_data/*']}

install_requires = \
['colour-science>=0.4.1,<0.5.0',
 'elementpath>=3.0.2,<4.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.4.2,<2.0.0',
 'rasterio>=1.3.2,<2.0.0',
 'spectral>=0.22.4,<0.24.0']

setup_kwargs = {
    'name': 'sentinel-toolkit',
    'version': '5.0.1',
    'description': 'Various sentinel tools',
    'long_description': '# Sentinel-Toolkit\n\n# Description\n\nThis repository provides various utility tools for working with Sentinel data like:\n\n1. Generating of SQLite database for a given Ecostress Spectral Library.\n2. Wrapper class around spectral.EcostressDatabase for querying with specific filters.\n3. Wrapper class around Sentinel-2 Spectral Response Functions Excel file.\n4. Converting a spectral distribution to Sentinel Responses.\n5. Converting Ecostress Spectral Library to Sentinel Responses CSV file.\n\n# Installation\n\nSentinel-Toolkit and its primary dependencies can be easily installed from the Python Package Index by issuing this\ncommand in a shell:\n\n```shell\n$ pip install --user sentinel-toolkit\n```\n\n# Examples\n\n## Loading and working with Ecostress Spectral Library\n\n### Generating SQLite database\n\nGenerate the SQLite database given the Ecostress spectral library directory:\n\n```python\nfrom sentinel_toolkit.ecostress import generate_ecostress_db\n\ngenerate_ecostress_db("ecospeclib-all", "ecostress.db")\n```\n\nFor convenience, there is a main method in ecostress_db_generator.py that can be called from shell like so:\n\n```shell\n$ python ecostress_db_generator.py -d /ecospeclib-all -o ecostress.db\n```\n\n### Working with the generated SQLite database\n\n```python\nfrom spectral import EcostressDatabase\nfrom sentinel_toolkit.ecostress import Ecostress\n\necostress_db = EcostressDatabase("ecostress.db")\necostress = Ecostress(ecostress_db)\n\n# Get all the spectrum ids that contain some values in the given range (420, 830).\nwavelength_range = (420, 830)\nspectrum_ids = ecostress.get_spectrum_ids(wavelength_range)\n\n# Iterate over the found spectrum_ids and get colour.SpectralDistribution objects.\nspectral_distributions_colour = []\nfor spectrum_id in spectrum_ids:\n    spectral_distribution = ecostress.get_spectral_distribution_colour(spectrum_id)\n    spectral_distributions_colour.append(spectral_distribution)\n\n# Iterate over the found spectrum_ids and get numpy arrays.\n# This can be used for gaining better performance\nspectral_distributions_numpy = []\nfor spectrum_id in spectrum_ids:\n    spectral_distribution = ecostress.get_spectral_distribution_numpy(spectrum_id)\n    spectral_distributions_numpy.append(spectral_distribution)\n```\n\n## Reading Sentinel-2 Spectral Response Functions\n\nGiven an Excel file containing the Sentinel-2 Spectral Response Functions,\nretrieve the wavelengths, band names and bands_responses as colour.MultiSpectralDistributions\nand 2D ndarray:\n\n```python\nfrom sentinel_toolkit.srf import S2Srf, S2SrfOptions\n\ns2a_srf = S2Srf("srf.xlsx")\n\n# Retrieve the wavelengths of Sentinel-2A as ndarray.\nwavelengths = s2a_srf.get_wavelengths()\n\n# Retrieve all the band names of Sentinel-2A bands 1, 2 and 3 as ndarray.\nband_names = s2a_srf.get_band_names(band_ids=[1, 2, 3])\n\n# Retrieve B2, B3, B4 of Sentinel-2A satellite in wavelength range (360, 830)\n# as colour.MultiSpectralDistributions.\nsatellite = \'A\'\nband_ids_option = [1, 2, 3]\nwavelength_range = (360, 830)\ns2_srf_options = S2SrfOptions(satellite, band_ids_option, wavelength_range)\nbands_responses_distribution = s2a_srf.get_bands_responses_distribution(s2_srf_options)\n\n# Retrieve all bands responses of Sentinel-2B in wavelength range (360, 830) as 2D ndarray.\nsatellite = \'B\'\nwavelength_range = (360, 830)\ns2_srf_options = S2SrfOptions(satellite=satellite, wavelength_range=wavelength_range)\nbands_responses = s2a_srf.get_bands_responses(s2_srf_options)\n```\n\n## Converting SpectralDistribution to Sentinel-2 Responses\n\nConvert a spectral distribution to Sentinel-2 Responses:\n\n```python\nfrom spectral import EcostressDatabase\nfrom sentinel_toolkit.ecostress import Ecostress\nfrom sentinel_toolkit.srf import S2Srf, S2SrfOptions\nfrom sentinel_toolkit.colorimetry import sd_to_sentinel_numpy, sd_to_sentinel_direct_numpy\nfrom sentinel_toolkit.colorimetry.illuminants import D65_360_830_1NM_VALUES\n\necostress_db = EcostressDatabase("ecostress.db")\necostress = Ecostress(ecostress_db)\ns2a_srf = S2Srf("srf.xlsx")\n\nwavelength_range = (360, 830)\n\nspectrum_id = 1\n# Use the numpy version for better performance\nspectral_data = ecostress.get_spectral_distribution_numpy(spectrum_id, wavelength_range)\n\nspectral_data_min_wavelength = spectral_data.wavelengths[0]\nspectral_data_max_wavelength = spectral_data.wavelengths[-1]\n\nwr_start = max(wavelength_range[0], spectral_data_min_wavelength)\nwr_end = min(wavelength_range[1], spectral_data_max_wavelength)\n\n# Reshape the illuminant to the spectral distribution shape\nilluminant = D65_360_830_1NM_VALUES[wr_start - 360: wr_end - 359]\n\n# Get the sentinel responses for spectrum with id 1 for all bands\n# from satellite \'A\' in wavelength_range (360, 830)\ns2_srf_options = S2SrfOptions(satellite=\'A\', wavelength_range=(wr_start, wr_end))\nsentinel_responses = sd_to_sentinel_numpy(spectral_data,\n                                          s2a_srf,\n                                          s2_srf_options,\n                                          illuminant)\n\n# Another way of doing this would be:\ns2_srf_options = S2SrfOptions(satellite=\'A\', wavelength_range=(wr_start, wr_end))\nbands_responses = s2a_srf.get_bands_responses(s2_srf_options)\nsentinel_responses = sd_to_sentinel_direct_numpy(spectral_data, bands_responses, illuminant)\n```\n\n## Converting full Ecostress Spectral Library to Sentinel-2 Responses CSV file\n\nGenerate a CSV file containing the Sentinel-2 responses for all materials from the Ecostress library:\n\n```python\nfrom spectral import EcostressDatabase\nfrom sentinel_toolkit.ecostress import Ecostress\nfrom sentinel_toolkit.srf import S2Srf\nfrom sentinel_toolkit.converter import EcostressToSentinelConverter\n\necostress_db = EcostressDatabase("ecostress.db")\necostress = Ecostress(ecostress_db)\n\ns2a_srf = S2Srf("srf.xlsx")\n\nconverter = EcostressToSentinelConverter(ecostress, s2a_srf)\nconverter.convert_ecostress_to_sentinel_csv()\n```\n\nFor convenience, there is a main method in converter.py that can be called from shell like so:\n\n```shell\n$ python converter.py -e ecostress.db -s2 S2-SRF_COPE-GSEG-EOPG-TN-15-0007_3.0.xlsx -s A -b 1 2 3 -ws 360 -we 830\n```\n',
    'author': 'Georgi Genchev',
    'author_email': 'gdgenchev97@gmail.com',
    'maintainer': 'Georgi Genchev',
    'maintainer_email': 'gdgenchev97@gmail.com',
    'url': 'https://github.com/sentinel-toolkit/sentinel-toolkit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
