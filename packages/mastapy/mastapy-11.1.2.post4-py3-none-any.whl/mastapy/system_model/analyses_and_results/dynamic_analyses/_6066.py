"""_6066.py

HypoidGearMeshDynamicAnalysis
"""


from mastapy.system_model.connections_and_sockets.gears import _2066
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6632
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6007
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'HypoidGearMeshDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshDynamicAnalysis',)


class HypoidGearMeshDynamicAnalysis(_6007.AGMAGleasonConicalGearMeshDynamicAnalysis):
    """HypoidGearMeshDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _HYPOID_GEAR_MESH_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'HypoidGearMeshDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2066.HypoidGearMesh':
        """HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6632.HypoidGearMeshLoadCase':
        """HypoidGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
