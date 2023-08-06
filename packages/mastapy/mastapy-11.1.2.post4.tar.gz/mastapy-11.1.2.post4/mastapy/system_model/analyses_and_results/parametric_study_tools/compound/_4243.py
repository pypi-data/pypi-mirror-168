"""_4243.py

GearSetCompoundParametricStudyTool
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
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4103
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4281
from mastapy._internal.python_net import python_net_import

_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'GearSetCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetCompoundParametricStudyTool',)


class GearSetCompoundParametricStudyTool(_4281.SpecialisedAssemblyCompoundParametricStudyTool):
    """GearSetCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'GearSetCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_set_duty_cycle_results(self) -> '_334.GearSetDutyCycleRating':
        """GearSetDutyCycleRating: 'GearSetDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearSetDutyCycleResults

        if temp is None:
            return None

        if _334.GearSetDutyCycleRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_set_duty_cycle_results to GearSetDutyCycleRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_set_duty_cycle_results_of_type_worm_gear_set_duty_cycle_rating(self) -> '_347.WormGearSetDutyCycleRating':
        """WormGearSetDutyCycleRating: 'GearSetDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearSetDutyCycleResults

        if temp is None:
            return None

        if _347.WormGearSetDutyCycleRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_set_duty_cycle_results to WormGearSetDutyCycleRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_set_duty_cycle_results_of_type_face_gear_set_duty_cycle_rating(self) -> '_421.FaceGearSetDutyCycleRating':
        """FaceGearSetDutyCycleRating: 'GearSetDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearSetDutyCycleResults

        if temp is None:
            return None

        if _421.FaceGearSetDutyCycleRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_set_duty_cycle_results to FaceGearSetDutyCycleRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_set_duty_cycle_results_of_type_cylindrical_gear_set_duty_cycle_rating(self) -> '_433.CylindricalGearSetDutyCycleRating':
        """CylindricalGearSetDutyCycleRating: 'GearSetDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearSetDutyCycleResults

        if temp is None:
            return None

        if _433.CylindricalGearSetDutyCycleRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_set_duty_cycle_results to CylindricalGearSetDutyCycleRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_set_duty_cycle_results_of_type_conical_gear_set_duty_cycle_rating(self) -> '_507.ConicalGearSetDutyCycleRating':
        """ConicalGearSetDutyCycleRating: 'GearSetDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearSetDutyCycleResults

        if temp is None:
            return None

        if _507.ConicalGearSetDutyCycleRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_set_duty_cycle_results to ConicalGearSetDutyCycleRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_set_duty_cycle_results_of_type_concept_gear_set_duty_cycle_rating(self) -> '_518.ConceptGearSetDutyCycleRating':
        """ConceptGearSetDutyCycleRating: 'GearSetDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearSetDutyCycleResults

        if temp is None:
            return None

        if _518.ConceptGearSetDutyCycleRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_set_duty_cycle_results to ConceptGearSetDutyCycleRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_analysis_cases(self) -> 'List[_4103.GearSetParametricStudyTool]':
        """List[GearSetParametricStudyTool]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4103.GearSetParametricStudyTool]':
        """List[GearSetParametricStudyTool]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
