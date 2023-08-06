"""_3571.py

HypoidGearSetStabilityAnalysis
"""


from typing import List

from mastapy.system_model.part_model.gears import _2284
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6633
from mastapy.system_model.analyses_and_results.stability_analyses import _3572, _3570, _3512
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'HypoidGearSetStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetStabilityAnalysis',)


class HypoidGearSetStabilityAnalysis(_3512.AGMAGleasonConicalGearSetStabilityAnalysis):
    """HypoidGearSetStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _HYPOID_GEAR_SET_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'HypoidGearSetStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2284.HypoidGearSet':
        """HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6633.HypoidGearSetLoadCase':
        """HypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def hypoid_gears_stability_analysis(self) -> 'List[_3572.HypoidGearStabilityAnalysis]':
        """List[HypoidGearStabilityAnalysis]: 'HypoidGearsStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidGearsStabilityAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def hypoid_meshes_stability_analysis(self) -> 'List[_3570.HypoidGearMeshStabilityAnalysis]':
        """List[HypoidGearMeshStabilityAnalysis]: 'HypoidMeshesStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidMeshesStabilityAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
