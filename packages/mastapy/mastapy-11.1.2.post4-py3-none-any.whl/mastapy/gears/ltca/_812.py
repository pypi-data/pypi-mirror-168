"""_812.py

GearSetLoadDistributionAnalysis
"""


from mastapy._internal import constructor
from mastapy.gears.analysis import _1180
from mastapy._internal.python_net import python_net_import

_GEAR_SET_LOAD_DISTRIBUTION_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.LTCA', 'GearSetLoadDistributionAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetLoadDistributionAnalysis',)


class GearSetLoadDistributionAnalysis(_1180.GearSetImplementationAnalysis):
    """GearSetLoadDistributionAnalysis

    This is a mastapy class.
    """

    TYPE = _GEAR_SET_LOAD_DISTRIBUTION_ANALYSIS

    def __init__(self, instance_to_wrap: 'GearSetLoadDistributionAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_a_system_deflection_analysis(self) -> 'bool':
        """bool: 'IsASystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IsASystemDeflectionAnalysis

        if temp is None:
            return None

        return temp
