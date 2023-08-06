"""_6383.py

SynchroniserHalfCriticalSpeedAnalysis
"""


from mastapy.system_model.part_model.couplings import _2353
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6695
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6384
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'SynchroniserHalfCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfCriticalSpeedAnalysis',)


class SynchroniserHalfCriticalSpeedAnalysis(_6384.SynchroniserPartCriticalSpeedAnalysis):
    """SynchroniserHalfCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _SYNCHRONISER_HALF_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'SynchroniserHalfCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2353.SynchroniserHalf':
        """SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6695.SynchroniserHalfLoadCase':
        """SynchroniserHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
