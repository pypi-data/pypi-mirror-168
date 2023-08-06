"""_7123.py

TransmissionErrorToOtherPowerLoad
"""


from mastapy._internal import constructor
from mastapy.math_utility import _1320
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_TRANSMISSION_ERROR_TO_OTHER_POWER_LOAD = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'TransmissionErrorToOtherPowerLoad')


__docformat__ = 'restructuredtext en'
__all__ = ('TransmissionErrorToOtherPowerLoad',)


class TransmissionErrorToOtherPowerLoad(_0.APIBase):
    """TransmissionErrorToOtherPowerLoad

    This is a mastapy class.
    """

    TYPE = _TRANSMISSION_ERROR_TO_OTHER_POWER_LOAD

    def __init__(self, instance_to_wrap: 'TransmissionErrorToOtherPowerLoad.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def mean_te(self) -> 'float':
        """float: 'MeanTE' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanTE

        if temp is None:
            return None

        return temp

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @property
    def peak_to_peak_te(self) -> 'float':
        """float: 'PeakToPeakTE' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PeakToPeakTE

        if temp is None:
            return None

        return temp

    @property
    def fourier_series_of_te(self) -> '_1320.FourierSeries':
        """FourierSeries: 'FourierSeriesOfTE' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FourierSeriesOfTE

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
