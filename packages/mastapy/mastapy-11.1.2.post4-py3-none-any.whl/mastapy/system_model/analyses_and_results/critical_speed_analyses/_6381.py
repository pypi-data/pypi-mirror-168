"""_6381.py

StraightBevelSunGearCriticalSpeedAnalysis
"""


from mastapy.system_model.part_model.gears import _2299
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6374
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'StraightBevelSunGearCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearCriticalSpeedAnalysis',)


class StraightBevelSunGearCriticalSpeedAnalysis(_6374.StraightBevelDiffGearCriticalSpeedAnalysis):
    """StraightBevelSunGearCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearCriticalSpeedAnalysis.TYPE'):
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
