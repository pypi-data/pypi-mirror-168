"""_6685.py

SpringDamperHalfLoadCase
"""


from mastapy.system_model.part_model.couplings import _2350
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6575
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SpringDamperHalfLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfLoadCase',)


class SpringDamperHalfLoadCase(_6575.CouplingHalfLoadCase):
    """SpringDamperHalfLoadCase

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_HALF_LOAD_CASE

    def __init__(self, instance_to_wrap: 'SpringDamperHalfLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2350.SpringDamperHalf':
        """SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
