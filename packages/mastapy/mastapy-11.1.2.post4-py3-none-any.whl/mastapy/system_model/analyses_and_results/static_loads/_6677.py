"""_6677.py

ShaftLoadCase
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.shaft_model import _2232
from mastapy.system_model.analyses_and_results.static_loads import _6531
from mastapy._internal.python_net import python_net_import

_SHAFT_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ShaftLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftLoadCase',)


class ShaftLoadCase(_6531.AbstractShaftLoadCase):
    """ShaftLoadCase

    This is a mastapy class.
    """

    TYPE = _SHAFT_LOAD_CASE

    def __init__(self, instance_to_wrap: 'ShaftLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def diameter_scaling_factor(self) -> 'float':
        """float: 'DiameterScalingFactor' is the original name of this property."""

        temp = self.wrapped.DiameterScalingFactor

        if temp is None:
            return None

        return temp

    @diameter_scaling_factor.setter
    def diameter_scaling_factor(self, value: 'float'):
        self.wrapped.DiameterScalingFactor = float(value) if value else 0.0

    @property
    def component_design(self) -> '_2232.Shaft':
        """Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[ShaftLoadCase]':
        """List[ShaftLoadCase]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
