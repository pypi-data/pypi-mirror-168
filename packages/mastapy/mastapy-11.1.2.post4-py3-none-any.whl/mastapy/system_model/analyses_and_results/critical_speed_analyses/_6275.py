"""_6275.py

BearingCriticalSpeedAnalysis
"""


from typing import List

from mastapy.system_model.part_model import _2191
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6543
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6303
from mastapy._internal.python_net import python_net_import

_BEARING_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'BearingCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingCriticalSpeedAnalysis',)


class BearingCriticalSpeedAnalysis(_6303.ConnectorCriticalSpeedAnalysis):
    """BearingCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _BEARING_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'BearingCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2191.Bearing':
        """Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6543.BearingLoadCase':
        """BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[BearingCriticalSpeedAnalysis]':
        """List[BearingCriticalSpeedAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
