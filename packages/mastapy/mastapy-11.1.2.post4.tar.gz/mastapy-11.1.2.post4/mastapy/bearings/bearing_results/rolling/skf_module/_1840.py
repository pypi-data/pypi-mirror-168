"""_1840.py

Frequencies
"""


from mastapy.bearings.bearing_results.rolling.skf_module import _1841, _1853, _1855
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_FREQUENCIES = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'Frequencies')


__docformat__ = 'restructuredtext en'
__all__ = ('Frequencies',)


class Frequencies(_1855.SKFCalculationResult):
    """Frequencies

    This is a mastapy class.
    """

    TYPE = _FREQUENCIES

    def __init__(self, instance_to_wrap: 'Frequencies.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def frequency_of_over_rolling(self) -> '_1841.FrequencyOfOverRolling':
        """FrequencyOfOverRolling: 'FrequencyOfOverRolling' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FrequencyOfOverRolling

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rotational_frequency(self) -> '_1853.RotationalFrequency':
        """RotationalFrequency: 'RotationalFrequency' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RotationalFrequency

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
