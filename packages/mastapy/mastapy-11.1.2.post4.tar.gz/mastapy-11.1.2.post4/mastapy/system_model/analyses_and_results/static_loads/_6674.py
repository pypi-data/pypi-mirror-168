"""_6674.py

RollingRingLoadCase
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2345
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6575
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'RollingRingLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingLoadCase',)


class RollingRingLoadCase(_6575.CouplingHalfLoadCase):
    """RollingRingLoadCase

    This is a mastapy class.
    """

    TYPE = _ROLLING_RING_LOAD_CASE

    def __init__(self, instance_to_wrap: 'RollingRingLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2345.RollingRing':
        """RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[RollingRingLoadCase]':
        """List[RollingRingLoadCase]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
