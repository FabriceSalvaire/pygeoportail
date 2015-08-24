####################################################################################################
#
# PyGeoPortail - A IGN GeoPortail Map Viewer
# Copyright (C) 2015 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import numpy as np

####################################################################################################

class Colour(np.ndarray):

    ##############################################

    def __new__(cls, *args, **kwargs):

        if len(args) == 1:
            data = args[0]
        elif len(args) == 3:
            data = args
        
        obj = np.asarray(data, dtype=cls.__dtype__).view(cls)
        
        obj.colour_kwargs = kwargs
        
        return obj

    ##############################################

    def inf(self):

        return self[self.argmin()]

    ##############################################

    def sup(self):

        return self[self.argmax()]

####################################################################################################

class NormalisedColour(Colour):

    __dtype__ = np.float64

    ##############################################

    def __array_finalize__(self, obj):

        if obj is None:
            return
        
        self._normalised = True
        self._dtype_scale = 1.

        # RuntimeError: maximum recursion depth exceeded while calling a Python object
        # if np.any(obj < 0) or np.any(obj > 1):
        #     raise ValueError

####################################################################################################

class IntColour(Colour):

    __dtype__ = np.uint

    ##############################################

    def __array_finalize__(self, obj):

        if obj is None:
            return
        
        self._normalised = False
        self._number_of_bits = getattr(obj, 'number_of_bits', 8)
        self._dtype_scale = 2**self._number_of_bits -1

####################################################################################################

class RgbColourMixin(object): # object ???

    ##############################################

    @property
    def red(self):
        return self[0]

    ##############################################

    @property
    def green(self):
        return self[1]

    ##############################################

    @property
    def blue(self):
        return self[2]

    ##############################################

    def to_hls(self):

        min_rgb = self.inf()
        max_rgb = self.sup()
        chroma = max_rgb - min_rgb # radius, small for grayscale
        
        red, green, blue = self.tolist()
        
        if chroma == .0:
            hue = .0 # undefined
        elif max_rgb == red:
            hue = (green - blue) / chroma # in [-1, 1]
            if hue < 0:
                hue += 6.
        elif max_rgb == green:
            hue = (blue - red) / chroma + 2. # in [1, 3]
        elif max_rgb == blue:
            hue = (red - green) / chroma + 4. # in [3, 5]
        # hue *= 60.
        hue /= 6.
        
        chroma /= self._dtype_scale
        
        two_lightness = (max_rgb + min_rgb) / self._dtype_scale
        lightness = .5 * two_lightness # 0 means black and 1 means white
        
        if lightness == .0 or lightness == 1.:
            saturation = .0
        else:
            saturation = chroma / (1 - abs(two_lightness - 1))
        
        # if (lightness < .5)
        #   saturation = chroma / two_lightness
        # else if (lightness >= .5)
        #   saturation = chroma / (2. - two_lightness)
        
        return HlsNormalisedColour(hue, lightness, saturation) # chroma

####################################################################################################

class RgbIntColour(IntColour, RgbColourMixin):

    ##############################################

    def normalise(self):

        return RgbNormalisedColour(self / self._dtype_scale)

####################################################################################################

class RgbNormalisedColour(NormalisedColour, RgbColourMixin):
    pass

####################################################################################################

class HlsColourMixin:

    ##############################################

    @property
    def hue(self):
        return self[0]

    ##############################################

    @property
    def lightness(self):
        return self[1]

    ##############################################

    @property
    def saturation(self):
        return self[2]

    ##############################################

    def to_rgb(self):

        # assume normalised
        hue, lightness, saturation = self.tolist()
        
        hue *= 6
        chroma = (1 - abs(2 * lightness - 1)) * saturation
        x = chroma * (1 - abs(hue % 2 - 1))
        m = lightness - .5 * chroma
        
        # print(hue, chroma, x, m)
        
        if 0 <= hue < 1:
            r, g, b = chroma, x, 0
        elif 1 <= hue < 2:
            r, g, b = x, chroma, 0
        elif 2 <= hue < 3:
            r, g, b = 0, chroma, x
        elif 3 <= hue < 4:
            r, g, b = 0, x, chroma
        elif 4 <= hue < 5:
            r, g, b = x, 0, chroma
        elif 5 <= hue < 6:
            r, g, b = chroma, 0, x
        
        return RgbNormalisedColour(r + m, g + m, b + m)

####################################################################################################

class HlsIntColour(IntColour, HlsColourMixin):

    ##############################################

    def normalise(self):

        return HlsNormalisedColour(self.hue / 360,
                                   self.lightness / self._dtype_scale,
                                   self.saturation / self._dtype_scale)

####################################################################################################

class HlsNormalisedColour(NormalisedColour, HlsColourMixin):
    pass

####################################################################################################
#
# End
#
####################################################################################################
