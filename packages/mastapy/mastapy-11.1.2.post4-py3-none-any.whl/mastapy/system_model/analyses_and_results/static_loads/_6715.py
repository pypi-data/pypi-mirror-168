"""_6715.py

ZerolBevelGearSetLoadCase
"""


from typing import List

from mastapy.system_model.part_model.gears import _2303
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6713, _6714, _6553
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ZerolBevelGearSetLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetLoadCase',)


class ZerolBevelGearSetLoadCase(_6553.BevelGearSetLoadCase):
    """ZerolBevelGearSetLoadCase

    This is a mastapy class.
    """

    TYPE = _ZEROL_BEVEL_GEAR_SET_LOAD_CASE

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2303.ZerolBevelGearSet':
        """ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gears(self) -> 'List[_6713.ZerolBevelGearLoadCase]':
        """List[ZerolBevelGearLoadCase]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Gears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def zerol_bevel_gears_load_case(self) -> 'List[_6713.ZerolBevelGearLoadCase]':
        """List[ZerolBevelGearLoadCase]: 'ZerolBevelGearsLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZerolBevelGearsLoadCase

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def zerol_bevel_meshes_load_case(self) -> 'List[_6714.ZerolBevelGearMeshLoadCase]':
        """List[ZerolBevelGearMeshLoadCase]: 'ZerolBevelMeshesLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZerolBevelMeshesLoadCase

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
