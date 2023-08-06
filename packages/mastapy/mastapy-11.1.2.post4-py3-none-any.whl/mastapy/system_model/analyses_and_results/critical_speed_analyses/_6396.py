"""_6396.py

ZerolBevelGearMeshCriticalSpeedAnalysis
"""


from mastapy.system_model.connections_and_sockets.gears import _2082
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6714
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6284
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MESH_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'ZerolBevelGearMeshCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMeshCriticalSpeedAnalysis',)


class ZerolBevelGearMeshCriticalSpeedAnalysis(_6284.BevelGearMeshCriticalSpeedAnalysis):
    """ZerolBevelGearMeshCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _ZEROL_BEVEL_GEAR_MESH_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMeshCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2082.ZerolBevelGearMesh':
        """ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6714.ZerolBevelGearMeshLoadCase':
        """ZerolBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
