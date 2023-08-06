"""_3803.py

ConceptGearMeshPowerFlow
"""


from mastapy.gears.rating.concept import _516
from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets.gears import _2056
from mastapy.system_model.analyses_and_results.static_loads import _6565
from mastapy.system_model.analyses_and_results.power_flows import _3833
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ConceptGearMeshPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshPowerFlow',)


class ConceptGearMeshPowerFlow(_3833.GearMeshPowerFlow):
    """ConceptGearMeshPowerFlow

    This is a mastapy class.
    """

    TYPE = _CONCEPT_GEAR_MESH_POWER_FLOW

    def __init__(self, instance_to_wrap: 'ConceptGearMeshPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rating(self) -> '_516.ConceptGearMeshRating':
        """ConceptGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rating

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_detailed_analysis(self) -> '_516.ConceptGearMeshRating':
        """ConceptGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDetailedAnalysis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design(self) -> '_2056.ConceptGearMesh':
        """ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6565.ConceptGearMeshLoadCase':
        """ConceptGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
