"""_3876.py

SpiralBevelGearMeshPowerFlow
"""


from mastapy.gears.rating.spiral_bevel import _374
from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets.gears import _2074
from mastapy.system_model.analyses_and_results.static_loads import _6682
from mastapy.system_model.analyses_and_results.power_flows import _3790
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_MESH_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'SpiralBevelGearMeshPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearMeshPowerFlow',)


class SpiralBevelGearMeshPowerFlow(_3790.BevelGearMeshPowerFlow):
    """SpiralBevelGearMeshPowerFlow

    This is a mastapy class.
    """

    TYPE = _SPIRAL_BEVEL_GEAR_MESH_POWER_FLOW

    def __init__(self, instance_to_wrap: 'SpiralBevelGearMeshPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rating(self) -> '_374.SpiralBevelGearMeshRating':
        """SpiralBevelGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rating

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_detailed_analysis(self) -> '_374.SpiralBevelGearMeshRating':
        """SpiralBevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDetailedAnalysis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design(self) -> '_2074.SpiralBevelGearMesh':
        """SpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6682.SpiralBevelGearMeshLoadCase':
        """SpiralBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
