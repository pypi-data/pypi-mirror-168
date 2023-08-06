"""_7192.py

GearSetCompoundAdvancedSystemDeflection
"""


from typing import List

from mastapy.gears.rating import _334
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.worm import _347
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.face import _421
from mastapy.gears.rating.cylindrical import _433
from mastapy.gears.rating.conical import _507
from mastapy.gears.rating.concept import _518
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7061
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7230
from mastapy._internal.python_net import python_net_import

_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'GearSetCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetCompoundAdvancedSystemDeflection',)


class GearSetCompoundAdvancedSystemDeflection(_7230.SpecialisedAssemblyCompoundAdvancedSystemDeflection):
    """GearSetCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'GearSetCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_duty_cycle_rating(self) -> '_334.GearSetDutyCycleRating':
        """GearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearDutyCycleRating

        if temp is None:
            return None

        if _334.GearSetDutyCycleRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to GearSetDutyCycleRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_duty_cycle_rating_of_type_worm_gear_set_duty_cycle_rating(self) -> '_347.WormGearSetDutyCycleRating':
        """WormGearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearDutyCycleRating

        if temp is None:
            return None

        if _347.WormGearSetDutyCycleRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to WormGearSetDutyCycleRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_duty_cycle_rating_of_type_face_gear_set_duty_cycle_rating(self) -> '_421.FaceGearSetDutyCycleRating':
        """FaceGearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearDutyCycleRating

        if temp is None:
            return None

        if _421.FaceGearSetDutyCycleRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to FaceGearSetDutyCycleRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_duty_cycle_rating_of_type_cylindrical_gear_set_duty_cycle_rating(self) -> '_433.CylindricalGearSetDutyCycleRating':
        """CylindricalGearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearDutyCycleRating

        if temp is None:
            return None

        if _433.CylindricalGearSetDutyCycleRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to CylindricalGearSetDutyCycleRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_duty_cycle_rating_of_type_conical_gear_set_duty_cycle_rating(self) -> '_507.ConicalGearSetDutyCycleRating':
        """ConicalGearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearDutyCycleRating

        if temp is None:
            return None

        if _507.ConicalGearSetDutyCycleRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to ConicalGearSetDutyCycleRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_duty_cycle_rating_of_type_concept_gear_set_duty_cycle_rating(self) -> '_518.ConceptGearSetDutyCycleRating':
        """ConceptGearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearDutyCycleRating

        if temp is None:
            return None

        if _518.ConceptGearSetDutyCycleRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to ConceptGearSetDutyCycleRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_analysis_cases(self) -> 'List[_7061.GearSetAdvancedSystemDeflection]':
        """List[GearSetAdvancedSystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_7061.GearSetAdvancedSystemDeflection]':
        """List[GearSetAdvancedSystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
