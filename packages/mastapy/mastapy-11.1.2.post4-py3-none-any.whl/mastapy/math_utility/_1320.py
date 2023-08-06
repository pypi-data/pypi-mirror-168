"""_1320.py

FourierSeries
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.math_utility import _1323
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FOURIER_SERIES = python_net_import('SMT.MastaAPI.MathUtility', 'FourierSeries')


__docformat__ = 'restructuredtext en'
__all__ = ('FourierSeries',)


class FourierSeries(_0.APIBase):
    """FourierSeries

    This is a mastapy class.
    """

    TYPE = _FOURIER_SERIES

    def __init__(self, instance_to_wrap: 'FourierSeries.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property."""

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else ''

    @property
    def peakto_peak(self) -> 'float':
        """float: 'PeaktoPeak' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PeaktoPeak

        if temp is None:
            return None

        return temp

    @property
    def unit(self) -> 'str':
        """str: 'Unit' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Unit

        if temp is None:
            return None

        return temp

    @property
    def harmonics_with_zeros_truncated(self) -> 'List[_1323.HarmonicValue]':
        """List[HarmonicValue]: 'HarmonicsWithZerosTruncated' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicsWithZerosTruncated

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def mean_value(self) -> 'float':
        """float: 'MeanValue' is the original name of this property."""

        temp = self.wrapped.MeanValue

        if temp is None:
            return None

        return temp

    @mean_value.setter
    def mean_value(self, value: 'float'):
        self.wrapped.MeanValue = float(value) if value else 0.0

    @property
    def values(self) -> 'List[float]':
        """List[float]: 'Values' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Values

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)
        return value

    def harmonic(self, index: 'int') -> '_1323.HarmonicValue':
        """ 'Harmonic' is the original name of this method.

        Args:
            index (int)

        Returns:
            mastapy.math_utility.HarmonicValue
        """

        index = int(index)
        method_result = self.wrapped.Harmonic(index if index else 0)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def harmonics_above_cut_off(self) -> 'List[_1323.HarmonicValue]':
        """ 'HarmonicsAboveCutOff' is the original name of this method.

        Returns:
            List[mastapy.math_utility.HarmonicValue]
        """

        return conversion.pn_to_mp_objects_in_list(self.wrapped.HarmonicsAboveCutOff())

    def set_amplitude(self, harmonic: 'int', amplitude: 'float'):
        """ 'SetAmplitude' is the original name of this method.

        Args:
            harmonic (int)
            amplitude (float)
        """

        harmonic = int(harmonic)
        amplitude = float(amplitude)
        self.wrapped.SetAmplitude(harmonic if harmonic else 0, amplitude if amplitude else 0.0)

    def set_amplitude_and_phase(self, harmonic: 'int', complex_: 'complex'):
        """ 'SetAmplitudeAndPhase' is the original name of this method.

        Args:
            harmonic (int)
            complex_ (complex)
        """

        harmonic = int(harmonic)
        complex_ = conversion.mp_to_pn_complex(complex_)
        self.wrapped.SetAmplitudeAndPhase(harmonic if harmonic else 0, complex_)

    def set_phase(self, harmonic: 'int', phase: 'float'):
        """ 'SetPhase' is the original name of this method.

        Args:
            harmonic (int)
            phase (float)
        """

        harmonic = int(harmonic)
        phase = float(phase)
        self.wrapped.SetPhase(harmonic if harmonic else 0, phase if phase else 0.0)
