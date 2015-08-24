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

import cv2

####################################################################################################

class ImageFormat(object):

    RGB = ('red', 'green', 'blue')
    BGR = ('blue', 'green', 'red')
    HLS = ('hue', 'luminosity', 'saturation')

    Gray = ('intensity',)
    Label = ('label',) # should be unsigned integer
    Binary = ('mask',) # boolean interpretation

    ##############################################

    def __init__(self, height, width, number_of_channels=1, data_type=np.uint8,
                 normalised=False, channels=None):

        error_string = ' must be >= 1'
        if height < 1:
            raise ValueError('height' + error_string)
        if width < 1:
            raise ValueError('width' + error_string)
        if number_of_channels < 1:
            raise ValueError('number of planes' + error_string)

        self._height = height
        self._width = width
        self._number_of_channels = number_of_channels
        self._data_type = data_type
        self._normalised = normalised # only for float data type
        self._channels = channels
        if channels is not None:
            if len(channels) != number_of_channels:
                raise NameError("channels don't match number_of_channels")
            self._channel_map = {channel:i for i, channel in enumerate(channels)}
        else:
            self._channel_map = None

    ##############################################

    def clone(self, **kwargs):

        d = dict(height=self._height, width=self._width, number_of_channels=self._number_of_channels,
                 data_type=self._data_type, normalised=self._normalised, channels=self._channels)
        d.update(kwargs)

        return self.__class__(**d)

    ##############################################

    def transpose(self):

        return self.clone(height=self._width, width=self._height)

    ##############################################

    def __repr__(self):

        return "ImageFormat shape = ({}, {}, {})\n" \
            "  dtype = {} normalised = {}\n" \
            "  channels = {}".format(self._height, self._width, self._number_of_channels,
                                     self._data_type, self._normalised,
                                     self._channels)

    ##############################################

    def __getitem__(self, i):

        if self._channels is not None:
            # not duck typing
            if isinstance(i, int):
                return self._channels[i]
            else:
                return self._channel_map[i]
        else:
            return None

    ##############################################

    @property
    def width(self):
        return self._width

    ##############################################

    @property
    def height(self):
        return self._height

    ##############################################

    @property
    def number_of_pixels(self):
        return self._height * self._width

    ##############################################

    @property
    def number_of_channels(self):
        return self._number_of_channels

    ##############################################

    @property
    def channels(self):
        return self._channels

    ##############################################

    @property
    def shape(self):
        if self.number_of_channels == 1:
            return (self._height, self._width)
        else:
            return (self._height, self._width, self._number_of_channels)

    ##############################################

    @property
    def dimension(self):
        return (self._width, self._height)

    ##############################################

    @property
    def data_type(self):
        return self._data_type

    ##############################################

    @property
    def normalised(self):
        return self._normalised

    ##############################################

    @property
    def number_of_bytes(self):
        return (self._height * self._width * self._number_of_channels *
                self.data_type_number_of_bytes)

    ##############################################

    @property
    def data_type_number_of_bytes(self):
        return np.nbytes[self._data_type]

    ##############################################

    @property
    def data_type_number_of_bits(self):
        return 8 * self.data_type_number_of_bytes

    ##############################################

    @property
    def is_integer(self):
        return self.is_unsigned_integer or self.is_signed_integer

    ##############################################

    @property
    def is_signed_integer(self):
        return self._data_type in (np.int8, np.int16, np.int32, np.int64)

    ##############################################

    @property
    def is_unsigned_integer(self):
        return self._data_type in (np.uint8, np.uint16, np.uint32, np.uint64)

    ##############################################

    @property
    def is_float(self):
        # == (np.float, np.double)
        return self._data_type in (np.float32, np.float64)

    ##############################################

    @property
    def is_normalised(self):
        return self._normalised

    ##############################################

    @property
    def inf(self):

        if self.is_unsigned_integer:
            return 0
        elif self.is_signed_integer:
            return - 2**(self.data_type_number_of_bits -1)
        elif self.is_float and self._normalised:
            return .0
        else:
            raise NotImplementedError

    ##############################################

    @property
    def sup(self):

        if self.is_unsigned_integer:
            return 2**self.data_type_number_of_bits -1
        elif self.is_signed_integer:
            return 2**(self.data_type_number_of_bits -1) -1
        elif self.is_float and self._normalised:
            return 1.
        else:
            raise NotImplementedError

####################################################################################################

class Image(np.ndarray):

    ##############################################

    def __new__(cls, *args, **kwargs):

        input_array = None
        number_of_args = len(args)
        if number_of_args == 1:
            obj = args[0]
            if isinstance(obj, ImageFormat):
                image_format = obj.clone(**Image._kwargs_for_image_format(kwargs))
            elif isinstance(obj, Image):
                input_array = obj
                image_format = input_array.image_format.clone(**Image._kwargs_for_image_format(kwargs))
            elif isinstance(obj, np.ndarray):
                input_array = obj
                height, width = input_array.shape[:2]
                if input_array.ndim == 3:
                    number_of_channels = input_array.shape[2]
                else:
                    number_of_channels = 1
                kwargs_for_image_format = dict(height=height, width=width, number_of_channels=number_of_channels,
                                               data_type=input_array.dtype)
                kwargs_for_image_format.update(Image._kwargs_for_image_format(kwargs))
                image_format = ImageFormat(**kwargs_for_image_format)
            else:
                raise ValueError("Bad argument " + str(type(obj)))
        else:
            image_format = ImageFormat(*args, **kwargs)

        # print(image_format)

        if input_array is None:
            # print('1', image_format)
            obj = np.ndarray.__new__(cls, image_format.shape, image_format.data_type,
                                     buffer=None, offset=0, strides=None, order=None)
        else:
            if input_array.shape != image_format.shape:
                raise NameError("Shape mismatch")
            if kwargs.get('share', False):
                # print('2', image_format)
                obj = input_array.view(cls)
            else:
                # print('3', image_format)
                obj = np.asarray(input_array, dtype=image_format.data_type).view(cls)

        obj.image_format = image_format

        return obj

    ##############################################

    @staticmethod
    def _kwargs_for_image_format(kwargs):

        kwargs = dict(kwargs)
        for key in ('share',):
            if key in kwargs:
                del kwargs[key]
        return kwargs

    ##############################################

    def __array_finalize__(self, obj):

        # print('__array_finalize__')
        # called height times ???

        if obj is None:
            return

        # _image_format
        self.image_format = getattr(obj, 'image_format', None)

    ##############################################

    # def __repr__(self):

    #     return 'Image\n' + repr(self.image_format)

    ##############################################

    def set(self, value):

        # cv2 ?
        # cv.Set(self, value)
        self[...] = value

    ##############################################

    def clear(self):
        self.set(0)

    ##############################################

    def to_normalised_float(self, float_image=None, double=False):

        if float_image is None:
            if double:
                data_type = np.float64
            else:
                data_type = np.float32
            float_image = self.__class__(self, data_type=data_type, normalised=True)
        else:
            float_image[...] = self
        float_image *= 1./self.image_format.sup

        return float_image

    ##############################################

    def convert_colour(self, channels, hls_image=None):

        # Fixme: check hls_image

        image_format = self.image_format
        if channels is ImageFormat.HLS:
            if image_format.channels is ImageFormat.RGB:
                if image_format.is_unsigned_integer:
                    float_image = self.to_normalised_float()
                    if hls_image is None:
                        hls_image = self.__class__(float_image, share=True, channels=ImageFormat.HLS)
                elif image_format.is_float and image_format.normalised:
                    float_image = self
                    if hls_image is None:
                        hls_image = self.__class__(image_format, channels=ImageFormat.HLS)
                else:
                    raise NotImplementedError
                # Fixme: catch error
                cv2.cvtColor(float_image, cv2.COLOR_RGB2HLS, hls_image)
                hls_image[:,:,0] *= 1./360 # normalised float, else have to define sup !
                return hls_image
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

    ##############################################

    def swap_channels(self, channels):

        image_format = self.image_format
        if ((channels is ImageFormat.BGR and image_format.channels is ImageFormat.RGB) or 
            (channels is ImageFormat.RGB and image_format.channels is ImageFormat.BGR)):
            output = self.__class__(image_format, channels=channels)
            cv2.mixChannels([self], [output], (0,2, 1,1, 2,0))
            return output
            # ???
        else:
            raise NotImplementedError

    ##############################################

    def split_channels(self):

        channel_arrays = cv2.split(self)
        image_format = self.image_format
        return [self.__class__(channel_array, share=True, number_of_channels=1, channels=(channel,))
                for channel, channel_array in zip(image_format.channels, channel_arrays)]

        # cv2.merge(mv)

    ##############################################

    def flip_vertically(self):

        cv2.flip(self, 0, self)

    ##############################################

    def flip_horizontally(self):

        cv2.flip(self, 1, self)

    ##############################################

    def transpose(self):

        output = self.__class__(self.image_format.transpose())
        cv2.transpose(self, output)
        return output

    ##############################################

    def histogram(self, channels=[0], inf=None, sup=None, number_of_bins=None):

        # Fixme: Histogram.py vs cv

        number_of_channels = len(channels)
        _channels = []
        for channel in channels:
            if isinstance(channel, str):
                channel = self.image_format[channel]
            _channels.append(channel)
        
        # if binnings is not None
        image_format = self.image_format
        if inf is None:
            inf = image_format.inf
        if sup is None:
            sup = image_format.sup
        intervals = [inf, sup]*number_of_channels

        if number_of_bins is None:
            number_of_bins = sup - inf
        _number_of_bins = [number_of_bins]*number_of_channels
        
        # mask = None
        histogram = cv2.calcHist([self], _channels, None, _number_of_bins, intervals)
        return histogram

####################################################################################################
#
# End
#
####################################################################################################
