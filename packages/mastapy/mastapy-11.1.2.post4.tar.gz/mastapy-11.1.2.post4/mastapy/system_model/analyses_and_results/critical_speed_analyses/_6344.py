"""_6344.py

MassDiscCriticalSpeedAnalysis
"""


from typing import List

from mastapy.system_model.part_model import _2212
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6647
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6391
from mastapy._internal.python_net import python_net_import

_MASS_DISC_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'MassDiscCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscCriticalSpeedAnalysis',)


class MassDiscCriticalSpeedAnalysis(_6391.VirtualComponentCriticalSpeedAnalysis):
    """MassDiscCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _MASS_DISC_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'MassDiscCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2212.MassDisc':
        """MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6647.MassDiscLoadCase':
        """MassDiscLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[MassDiscCriticalSpeedAnalysis]':
        """List[MassDiscCriticalSpeedAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
