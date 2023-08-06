"""_5438.py

ComplianceAndForceData
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_COMPLIANCE_AND_FORCE_DATA = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'ComplianceAndForceData')


__docformat__ = 'restructuredtext en'
__all__ = ('ComplianceAndForceData',)


class ComplianceAndForceData(_0.APIBase):
    """ComplianceAndForceData

    This is a mastapy class.
    """

    TYPE = _COMPLIANCE_AND_FORCE_DATA

    def __init__(self, instance_to_wrap: 'ComplianceAndForceData.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def frequencies_for_compliances(self) -> 'List[float]':
        """List[float]: 'FrequenciesForCompliances' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FrequenciesForCompliances

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)
        return value

    @property
    def frequencies_for_mesh_forces(self) -> 'List[float]':
        """List[float]: 'FrequenciesForMeshForces' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FrequenciesForMeshForces

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)
        return value

    @property
    def gear_a_compliance(self) -> 'List[complex]':
        """List[complex]: 'GearACompliance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearACompliance

        if temp is None:
            return None

        value = conversion.pn_to_mp_complex_list(temp)
        return value

    @property
    def gear_b_compliance(self) -> 'List[complex]':
        """List[complex]: 'GearBCompliance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBCompliance

        if temp is None:
            return None

        value = conversion.pn_to_mp_complex_list(temp)
        return value

    @property
    def mesh_forces_per_unit_te(self) -> 'List[complex]':
        """List[complex]: 'MeshForcesPerUnitTE' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshForcesPerUnitTE

        if temp is None:
            return None

        value = conversion.pn_to_mp_complex_list(temp)
        return value
