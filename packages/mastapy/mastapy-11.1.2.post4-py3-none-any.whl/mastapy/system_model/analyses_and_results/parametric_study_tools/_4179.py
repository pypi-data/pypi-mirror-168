"""_4179.py

WormGearSetParametricStudyTool
"""


from typing import List

from mastapy.system_model.part_model.gears import _2301
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6712
from mastapy.system_model.analyses_and_results.system_deflections import _2581
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4178, _4177, _4103
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'WormGearSetParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetParametricStudyTool',)


class WormGearSetParametricStudyTool(_4103.GearSetParametricStudyTool):
    """WormGearSetParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _WORM_GEAR_SET_PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'WormGearSetParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2301.WormGearSet':
        """WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6712.WormGearSetLoadCase':
        """WormGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_system_deflection_results(self) -> 'List[_2581.WormGearSetSystemDeflection]':
        """List[WormGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblySystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def worm_gears_parametric_study_tool(self) -> 'List[_4178.WormGearParametricStudyTool]':
        """List[WormGearParametricStudyTool]: 'WormGearsParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGearsParametricStudyTool

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def worm_meshes_parametric_study_tool(self) -> 'List[_4177.WormGearMeshParametricStudyTool]':
        """List[WormGearMeshParametricStudyTool]: 'WormMeshesParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormMeshesParametricStudyTool

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
