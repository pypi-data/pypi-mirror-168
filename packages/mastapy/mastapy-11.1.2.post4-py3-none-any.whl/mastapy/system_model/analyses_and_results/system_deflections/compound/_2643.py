"""_2643.py

CylindricalGearMeshCompoundSystemDeflection
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.connections_and_sockets.gears import _2060
from mastapy.gears.rating.cylindrical import _436
from mastapy.system_model.analyses_and_results.system_deflections import _2485
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2655
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'CylindricalGearMeshCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshCompoundSystemDeflection',)


class CylindricalGearMeshCompoundSystemDeflection(_2655.GearMeshCompoundSystemDeflection):
    """CylindricalGearMeshCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def maximum_operating_backlash(self) -> 'float':
        """float: 'MaximumOperatingBacklash' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumOperatingBacklash

        if temp is None:
            return None

        return temp

    @property
    def minimum_operating_backlash(self) -> 'float':
        """float: 'MinimumOperatingBacklash' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumOperatingBacklash

        if temp is None:
            return None

        return temp

    @property
    def minimum_operating_tip_root_clearance(self) -> 'float':
        """float: 'MinimumOperatingTipRootClearance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumOperatingTipRootClearance

        if temp is None:
            return None

        return temp

    @property
    def minimum_operating_transverse_contact_ratio(self) -> 'float':
        """float: 'MinimumOperatingTransverseContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumOperatingTransverseContactRatio

        if temp is None:
            return None

        return temp

    @property
    def component_design(self) -> '_2060.CylindricalGearMesh':
        """CylindricalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design(self) -> '_2060.CylindricalGearMesh':
        """CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_mesh_rating(self) -> '_436.CylindricalMeshDutyCycleRating':
        """CylindricalMeshDutyCycleRating: 'CylindricalMeshRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalMeshRating

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_2485.CylindricalGearMeshSystemDeflectionWithLTCAResults]':
        """List[CylindricalGearMeshSystemDeflectionWithLTCAResults]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshCompoundSystemDeflection]':
        """List[CylindricalGearMeshCompoundSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_2485.CylindricalGearMeshSystemDeflectionWithLTCAResults]':
        """List[CylindricalGearMeshSystemDeflectionWithLTCAResults]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
