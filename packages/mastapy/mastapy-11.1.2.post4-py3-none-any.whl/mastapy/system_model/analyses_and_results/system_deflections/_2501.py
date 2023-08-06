"""_2501.py

FEPartSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model import _2203
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6611
from mastapy.nodal_analysis.component_mode_synthesis import _213
from mastapy.nodal_analysis import _75
from mastapy.system_model.analyses_and_results.power_flows import _3831
from mastapy.math_utility.measured_vectors import _1371, _1367
from mastapy.system_model.fe import _2160
from mastapy.system_model.analyses_and_results.system_deflections import _2435
from mastapy._internal.python_net import python_net_import

_FE_PART_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'FEPartSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartSystemDeflection',)


class FEPartSystemDeflection(_2435.AbstractShaftOrHousingSystemDeflection):
    """FEPartSystemDeflection

    This is a mastapy class.
    """

    TYPE = _FE_PART_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'FEPartSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2203.FEPart':
        """FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6611.FEPartLoadCase':
        """FEPartLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def full_fe_results(self) -> '_213.StaticCMSResults':
        """StaticCMSResults: 'FullFEResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FullFEResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mass_in_world_coordinate_system_mn_rad_s_kg(self) -> '_75.NodalMatrix':
        """NodalMatrix: 'MassInWorldCoordinateSystemMNRadSKg' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MassInWorldCoordinateSystemMNRadSKg

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results(self) -> '_3831.FEPartPowerFlow':
        """FEPartPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def stiffness_in_world_coordinate_system_mn_rad(self) -> '_75.NodalMatrix':
        """NodalMatrix: 'StiffnessInWorldCoordinateSystemMNRad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessInWorldCoordinateSystemMNRad

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def applied_internal_forces_in_world_coordinate_system(self) -> 'List[_1371.VectorWithLinearAndAngularComponents]':
        """List[VectorWithLinearAndAngularComponents]: 'AppliedInternalForcesInWorldCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AppliedInternalForcesInWorldCoordinateSystem

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def node_results_in_shaft_coordinate_system(self) -> 'List[_1367.ForceAndDisplacementResults]':
        """List[ForceAndDisplacementResults]: 'NodeResultsInShaftCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NodeResultsInShaftCoordinateSystem

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planetaries(self) -> 'List[FEPartSystemDeflection]':
        """List[FEPartSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def export(self) -> '_2160.SystemDeflectionFEExportOptions':
        """SystemDeflectionFEExportOptions: 'Export' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Export

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def export_displacements(self):
        """ 'ExportDisplacements' is the original name of this method."""

        self.wrapped.ExportDisplacements()

    def export_forces(self):
        """ 'ExportForces' is the original name of this method."""

        self.wrapped.ExportForces()
