"""
Colorimetry
================

Colorimetry module provides methods for converting a spectral distribution
to Sentinel-2 spectral responses.
"""

from .sentinel_values import sd_to_sentinel_colour
from .sentinel_values import sd_to_sentinel_direct_colour

from .sentinel_values import sd_to_sentinel_numpy
from .sentinel_values import sd_to_sentinel_direct_numpy

from .illuminants import D65_360_830_1NM_DISTRIBUTION
from .illuminants import D65_360_830_1NM_VALUES
