"""_7057.py

FEPartAdvancedSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model import _2203
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6611
from mastapy.system_model.analyses_and_results.system_deflections import _2501
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6998
from mastapy._internal.python_net import python_net_import

_FE_PART_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'FEPartAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartAdvancedSystemDeflection',)


class FEPartAdvancedSystemDeflection(_6998.AbstractShaftOrHousingAdvancedSystemDeflection):
    """FEPartAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _FE_PART_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'FEPartAdvancedSystemDeflection.TYPE'):
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
    def component_system_deflection_results(self) -> 'List[_2501.FEPartSystemDeflection]':
        """List[FEPartSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentSystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planetaries(self) -> 'List[FEPartAdvancedSystemDeflection]':
        """List[FEPartAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
