"""_6325.py

FEPartCriticalSpeedAnalysis
"""


from typing import List

from mastapy.system_model.part_model import _2203
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6611
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6269
from mastapy._internal.python_net import python_net_import

_FE_PART_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'FEPartCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartCriticalSpeedAnalysis',)


class FEPartCriticalSpeedAnalysis(_6269.AbstractShaftOrHousingCriticalSpeedAnalysis):
    """FEPartCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _FE_PART_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'FEPartCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2203.FEPart':
        """FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6611.FEPartLoadCase':
        """FEPartLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[FEPartCriticalSpeedAnalysis]':
        """List[FEPartCriticalSpeedAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
