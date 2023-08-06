"""_1872.py

RingFittingThermalResults
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_results.rolling.fitting import _1870
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_RING_FITTING_THERMAL_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.Fitting', 'RingFittingThermalResults')


__docformat__ = 'restructuredtext en'
__all__ = ('RingFittingThermalResults',)


class RingFittingThermalResults(_0.APIBase):
    """RingFittingThermalResults

    This is a mastapy class.
    """

    TYPE = _RING_FITTING_THERMAL_RESULTS

    def __init__(self, instance_to_wrap: 'RingFittingThermalResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def change_in_diameter_due_to_interference_and_centrifugal_effects(self) -> 'float':
        """float: 'ChangeInDiameterDueToInterferenceAndCentrifugalEffects' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ChangeInDiameterDueToInterferenceAndCentrifugalEffects

        if temp is None:
            return None

        return temp

    @property
    def interfacial_clearance_included_in_analysis(self) -> 'bool':
        """bool: 'InterfacialClearanceIncludedInAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InterfacialClearanceIncludedInAnalysis

        if temp is None:
            return None

        return temp

    @property
    def interfacial_normal_stress(self) -> 'float':
        """float: 'InterfacialNormalStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InterfacialNormalStress

        if temp is None:
            return None

        return temp

    @property
    def maximum_hoop_stress(self) -> 'float':
        """float: 'MaximumHoopStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumHoopStress

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
    def interference_values(self) -> 'List[_1870.InterferenceComponents]':
        """List[InterferenceComponents]: 'InterferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InterferenceValues

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
