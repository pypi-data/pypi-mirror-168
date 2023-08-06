"""_2692.py

ShaftDutyCycleSystemDeflection
"""


from typing import List

from mastapy.shafts import _19
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.shaft_model import _2232
from mastapy.system_model.analyses_and_results.system_deflections import _2548
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SHAFT_DUTY_CYCLE_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ShaftDutyCycleSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftDutyCycleSystemDeflection',)


class ShaftDutyCycleSystemDeflection(_0.APIBase):
    """ShaftDutyCycleSystemDeflection

    This is a mastapy class.
    """

    TYPE = _SHAFT_DUTY_CYCLE_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'ShaftDutyCycleSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def shaft_damage_results(self) -> '_19.ShaftDamageResults':
        """ShaftDamageResults: 'ShaftDamageResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftDamageResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def shaft_design(self) -> '_2232.Shaft':
        """Shaft: 'ShaftDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def shaft_static_analyses(self) -> 'List[_2548.ShaftSystemDeflection]':
        """List[ShaftSystemDeflection]: 'ShaftStaticAnalyses' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftStaticAnalyses

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
