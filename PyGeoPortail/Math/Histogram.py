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

import math

import numpy as np
# from scipy import stats

####################################################################################################

from .Binning import Binning1D
from .Interval import Interval

####################################################################################################

class DataSetMoment(object):

    ##############################################

    def __init__(self):

        self.number_of_entries = 0
        self.sum_x = 0
        self.sum_x2 = 0
        self.sum_x3 = 0
        self.sum_x4 = 0

    ##############################################

    def fill(self, x):

        self.number_of_entries += 1
        self.sum_x += x
        self.sum_x2 += x**2
        self.sum_x3 += x**3
        self.sum_x4 += x**4

    ##############################################

    def __iadd__(self, obj):

        self.number_of_entries += obj.number_of_entries
        self.sum_x += obj.sum_x
        self.sum_x2 += obj.sum_x2
        self.sum_x3 += obj.sum_x3
        self.sum_x4 += obj.sum_x4

        return self

    ##############################################

    @property
    def mean(self):
        return self.sum_x / self.number_of_entries

    ##############################################

    @property
    def biased_variance(self):
        return self.sum_x2 / self.number_of_entries - self.mean**2

    ##############################################

    @property
    def unbiased_variance(self):
        return self.number_of_entries / (self.number_of_entries -1) * self.biased_variance

    ##############################################

    @property
    def biased_standard_deviation(self):
        return math.sqrt(self.biased_variance)

    ##############################################

    @property
    def standard_deviation(self):
        return math.sqrt(self.unbiased_variance)

    ##############################################

    @property
    def skew(self):
        return ((self.sum_x3 / self.number_of_entries - 3*self.mean*self.biased_variance - self.mean**3)
                / (self.biased_variance*self.biased_standard_deviation))

    ##############################################

    @property
    def kurtosis(self):
        # Need an expansion in terms of sum_x**i
        return NotImplementedError

####################################################################################################

class WeightedDataSetMoment(object):

    ##############################################

    def __init__(self):

        self.sum_weight = 0
        self.sum_weight2 = 0
        self.sum_weight_x = 0
        self.sum_weight_x2 = 0
        self.sum_weight_x3 = 0
        self.sum_weight_x4 = 0

    ##############################################

    def fill(self, x, weight=1.):

        self.sum_weight += weight
        self.sum_weight2 += weight**2
        weight_x = weight * x
        self.sum_weight_x += weight_x
        self.sum_weight_x2 += weight_x**2
        self.sum_weight_x3 += weight_x**3
        self.sum_weight_x4 += weight_x**4

    ##############################################

    @property
    def number_of_effective_entries(self):
        return self.sum_weight**2 / self.sum_weight2

    ##############################################

    @property
    def mean(self):
        return self.sum_weight_x / self.number_of_effective_entries

####################################################################################################

class Histogram(object):

    ##############################################

    def __init__(self, binning):

        # Fixme: direct mode

        if isinstance(binning, Binning1D):
            self._binning = binning
        else:
            raise ValueError
        
        array_size = self._binning.array_size
        self._accumulator = np.zeros(array_size)
        self._sum_weight_square = np.zeros(array_size)
        self.data_set_moment = DataSetMoment()
        
        self.clear_feature()

    ##############################################

    def clear(self, value=.0):

        self._accumulator[:] = value
        self._sum_weight_square[:] = value**2
        self.data_set_moment = DataSetMoment()
        self.clear_feature()

    ##############################################

    def clear_feature(self):

        self._errors = None
        self._integral = None
        self._mean = None
        self._biased_variance = None

    ##############################################

    @property
    def binning(self):
        return self._binning

    ##############################################

    @property
    def accumulator(self):
        return self._accumulator

    ##############################################

    @property
    def binning_accumulator(self):
        return self._accumulator[1:-1]

    ##############################################

    @property
    def x_values(self):
        return self._binning.bin_centers

    ##############################################

    def is_consistent_with(self, obj):

        return self._binning == obj._binning

    ##############################################

    def __iadd__(self, obj):

        if self.is_consistent_with(obj):
            self._accumulator += obj._accumulator
            self._sum_weight_square += obj._sum_weight_square
            self.data_set_moment += obj.data_set_moment
            self.clear_feature()
        else:
            raise ValueError
        return self

    ##############################################

    def normalise(self):

        self._accumulator /= self.integral
        self.clear_feature()

    ##############################################

    def fill(self, x, weight=1.):

        if weight < 0:
            raise ValueError
        
        i = self._binning.find_bin(x)
        self._accumulator[i] += weight
        # if weight == 1.: weight_square = 1.
        self._sum_weight_square[i] += weight**2
        self.data_set_moment.fill(x)
        self.clear_feature()

    ##############################################

    def compute_errors(self):

        if self._errors is None:
            self._errors = np.sqrt(self._sum_weight_square)

    ##############################################

    def get_bin_error(self, i):

        self.compute_errors()
        
        return self._errors[i]

    ##############################################

    @property
    def min(self):
        return min(self._accumulator) # - self._errors
    inf = min

    ##############################################

    @property
    def max(self):
        return max(self._accumulator) # + self._errors
    sup = max

    ##############################################

    @property
    def integral(self):
        if self._integral is None:
            self._integral = self._accumulator.sum()
        return self._integral

    ##############################################

    @property
    def number_of_effective_entries(self):
        return self.integral**2 / self._sum_weight_square.sum()

    ##############################################

    @property
    def mean(self):
        if self._mean is None:
            # if weighted: / self.number_of_effective_entries
            self._mean = np.sum(self.binning_accumulator * self.x_values) / self.integral
        return self._mean

    ##############################################

    @property
    def biased_variance(self):
        if self._biased_variance is None:
            self._biased_variance = np.sum(self.binning_accumulator * self.x_values**2) / self.integral - self.mean**2
        return self._biased_variance

    ##############################################

    @property
    def unbiased_variance(self):
        return self.integral / (self.integral -1) * self.biased_variance

    ##############################################

    @property
    def biased_standard_deviation(self):
        return math.sqrt(self.biased_variance)

    ##############################################

    @property
    def standard_deviation(self):
        return math.sqrt(self.unbiased_variance)

    ##############################################

    @property
    def skew(self):
        # self.biased_variance * self.biased_standard_deviation
        return (np.sum(self.binning_accumulator * (self.x_values - self.mean)**3)
                / (self.biased_standard_deviation**3 * self.integral))

    ##############################################

    @property
    def kurtosis(self):
        return (np.sum(self.binning_accumulator * (self.x_values - self.mean)**4)
                / (self.biased_variance**2 * self.integral)
                -3)

    ##############################################

    def to_graph(self):

        self.compute_errors()
        
        binning = self._binning
        bin_slice = binning.bin_slice()
        
        x_values = self.x_values
        
        y_values = np.copy(self._accumulator[bin_slice])
        y_errors = np.copy(self._errors[bin_slice])
        
        x_errors = np.empty(x_values.shape)
        x_errors[:] = .5*binning.bin_width
        
        return x_values, y_values, x_errors, y_errors

   ###############################################

    def __str__(self):

        binning = self._binning
        
        string_format = """
Histogram 1D
  interval: %s
  number of bins: %u
  bin width: %g
"""
        
        text = string_format % (str(binning._interval), binning._number_of_bins, binning._bin_width)
        for i in binning.bin_iterator(xflow=True):
            text += '%3u %s = %g +- %g\n' % (i,
                                             str(binning.bin_interval(i)),
                                             self._accumulator[i],
                                             self.get_bin_error(i),
                                             )
        
        return text

   ###############################################

    def find_non_zero_bin_range(self):

        inf = 0
        while self._accumulator[inf] == 0:
            inf += 1
        
        sup = len(self._accumulator) -1
        while self._accumulator[sup] == 0:
            sup -= 1
        
        return Interval(inf, sup)

   ###############################################

    def non_zero_bin_range_histogram(self):

        bin_range = self.find_non_zero_bin_range()
        # print bin_range
        binning = self._binning.sub_binning(self._binning.sub_interval(bin_range))
        # print binning
        histogram = self.__class__(binning)
        src_slice = slice(bin_range.inf, bin_range.sup +1)
        dst_slice = slice(binning.first_bin, binning.over_flow_bin)
        histogram._accumulator[dst_slice] = self._accumulator[src_slice]
        histogram._sum_weight_square[dst_slice] = self._sum_weight_square[src_slice]
        histogram._errors[dst_slice] = self._errors[src_slice]
        
        return histogram

####################################################################################################
#
# End
#
####################################################################################################
