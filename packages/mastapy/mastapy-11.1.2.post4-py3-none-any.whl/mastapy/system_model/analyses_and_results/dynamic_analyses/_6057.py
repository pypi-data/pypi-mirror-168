"""_6057.py

FaceGearMeshDynamicAnalysis
"""


from mastapy.system_model.connections_and_sockets.gears import _2062
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6609
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6062
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'FaceGearMeshDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshDynamicAnalysis',)


class FaceGearMeshDynamicAnalysis(_6062.GearMeshDynamicAnalysis):
    """FaceGearMeshDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _FACE_GEAR_MESH_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'FaceGearMeshDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2062.FaceGearMesh':
        """FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6609.FaceGearMeshLoadCase':
        """FaceGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
