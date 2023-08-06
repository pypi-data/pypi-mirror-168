"""_6610.py

FaceGearSetLoadCase
"""


from typing import List

from mastapy.system_model.part_model.gears import _2278
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6608, _6609, _6619
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'FaceGearSetLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetLoadCase',)


class FaceGearSetLoadCase(_6619.GearSetLoadCase):
    """FaceGearSetLoadCase

    This is a mastapy class.
    """

    TYPE = _FACE_GEAR_SET_LOAD_CASE

    def __init__(self, instance_to_wrap: 'FaceGearSetLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2278.FaceGearSet':
        """FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gears(self) -> 'List[_6608.FaceGearLoadCase]':
        """List[FaceGearLoadCase]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Gears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def face_gears_load_case(self) -> 'List[_6608.FaceGearLoadCase]':
        """List[FaceGearLoadCase]: 'FaceGearsLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceGearsLoadCase

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def face_meshes_load_case(self) -> 'List[_6609.FaceGearMeshLoadCase]':
        """List[FaceGearMeshLoadCase]: 'FaceMeshesLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceMeshesLoadCase

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
