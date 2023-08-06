"""_3522.py

BevelDifferentialSunGearStabilityAnalysis
"""


from mastapy.system_model.part_model.gears import _2267
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.stability_analyses import _3520
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'BevelDifferentialSunGearStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialSunGearStabilityAnalysis',)


class BevelDifferentialSunGearStabilityAnalysis(_3520.BevelDifferentialGearStabilityAnalysis):
    """BevelDifferentialSunGearStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'BevelDifferentialSunGearStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2267.BevelDifferentialSunGear':
        """BevelDifferentialSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
