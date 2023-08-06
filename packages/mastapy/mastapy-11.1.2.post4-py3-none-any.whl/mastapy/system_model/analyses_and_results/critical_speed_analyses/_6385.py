"""_6385.py

SynchroniserSleeveCriticalSpeedAnalysis
"""


from mastapy.system_model.part_model.couplings import _2355
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6698
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6384
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'SynchroniserSleeveCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveCriticalSpeedAnalysis',)


class SynchroniserSleeveCriticalSpeedAnalysis(_6384.SynchroniserPartCriticalSpeedAnalysis):
    """SynchroniserSleeveCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _SYNCHRONISER_SLEEVE_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2355.SynchroniserSleeve':
        """SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6698.SynchroniserSleeveLoadCase':
        """SynchroniserSleeveLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
