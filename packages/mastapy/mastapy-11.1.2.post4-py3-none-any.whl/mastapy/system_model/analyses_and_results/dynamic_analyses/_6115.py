"""_6115.py

StraightBevelSunGearDynamicAnalysis
"""


from mastapy.system_model.part_model.gears import _2299
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6108
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'StraightBevelSunGearDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearDynamicAnalysis',)


class StraightBevelSunGearDynamicAnalysis(_6108.StraightBevelDiffGearDynamicAnalysis):
    """StraightBevelSunGearDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2299.StraightBevelSunGear':
        """StraightBevelSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
