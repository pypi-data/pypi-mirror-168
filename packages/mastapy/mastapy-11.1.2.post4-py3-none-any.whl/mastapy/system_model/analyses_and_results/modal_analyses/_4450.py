"""_4450.py

ZerolBevelGearMeshModalAnalysis
"""


from mastapy.system_model.connections_and_sockets.gears import _2082
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6714
from mastapy.system_model.analyses_and_results.system_deflections import _2583
from mastapy.system_model.analyses_and_results.modal_analyses import _4328
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MESH_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ZerolBevelGearMeshModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMeshModalAnalysis',)


class ZerolBevelGearMeshModalAnalysis(_4328.BevelGearMeshModalAnalysis):
    """ZerolBevelGearMeshModalAnalysis

    This is a mastapy class.
    """

    TYPE = _ZEROL_BEVEL_GEAR_MESH_MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMeshModalAnalysis.TYPE'):
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

    @property
    def system_deflection_results(self) -> '_2583.ZerolBevelGearMeshSystemDeflection':
        """ZerolBevelGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
