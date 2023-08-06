"""_4124.py

ParametricStudyDOEResultVariable
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.math_utility.optimisation import _1362, _1360
from mastapy._internal.python_net import python_net_import

_PARAMETRIC_STUDY_DOE_RESULT_VARIABLE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ParametricStudyDOEResultVariable')


__docformat__ = 'restructuredtext en'
__all__ = ('ParametricStudyDOEResultVariable',)


class ParametricStudyDOEResultVariable(_1360.ParetoOptimisationVariableBase):
    """ParametricStudyDOEResultVariable

    This is a mastapy class.
    """

    TYPE = _PARAMETRIC_STUDY_DOE_RESULT_VARIABLE

    def __init__(self, instance_to_wrap: 'ParametricStudyDOEResultVariable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def entity_name(self) -> 'str':
        """str: 'EntityName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EntityName

        if temp is None:
            return None

        return temp

    @property
    def parameter_name(self) -> 'str':
        """str: 'ParameterName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ParameterName

        if temp is None:
            return None

        return temp

    @property
    def target(self) -> '_1362.PropertyTargetForDominantCandidateSearch':
        """PropertyTargetForDominantCandidateSearch: 'Target' is the original name of this property."""

        temp = self.wrapped.Target

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1362.PropertyTargetForDominantCandidateSearch)(value) if value is not None else None

    @target.setter
    def target(self, value: '_1362.PropertyTargetForDominantCandidateSearch'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Target = value
