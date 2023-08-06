"""_6714.py

ZerolBevelGearMeshLoadCase
"""


from mastapy.system_model.connections_and_sockets.gears import _2082
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6552
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ZerolBevelGearMeshLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMeshLoadCase',)


class ZerolBevelGearMeshLoadCase(_6552.BevelGearMeshLoadCase):
    """ZerolBevelGearMeshLoadCase

    This is a mastapy class.
    """

    TYPE = _ZEROL_BEVEL_GEAR_MESH_LOAD_CASE

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMeshLoadCase.TYPE'):
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
