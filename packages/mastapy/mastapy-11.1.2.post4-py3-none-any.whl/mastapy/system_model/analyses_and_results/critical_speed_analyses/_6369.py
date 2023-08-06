"""_6369.py

SpiralBevelGearMeshCriticalSpeedAnalysis
"""


from mastapy.system_model.connections_and_sockets.gears import _2074
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6682
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6284
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_MESH_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'SpiralBevelGearMeshCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearMeshCriticalSpeedAnalysis',)


class SpiralBevelGearMeshCriticalSpeedAnalysis(_6284.BevelGearMeshCriticalSpeedAnalysis):
    """SpiralBevelGearMeshCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _SPIRAL_BEVEL_GEAR_MESH_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'SpiralBevelGearMeshCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

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
