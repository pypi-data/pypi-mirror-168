"""_5402.py

SystemOptimisationGearSet
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SYSTEM_OPTIMISATION_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'SystemOptimisationGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('SystemOptimisationGearSet',)


class SystemOptimisationGearSet(_0.APIBase):
    """SystemOptimisationGearSet

    This is a mastapy class.
    """

    TYPE = _SYSTEM_OPTIMISATION_GEAR_SET

    def __init__(self, instance_to_wrap: 'SystemOptimisationGearSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def design_with_highest_number_of_pinion_teeth(self) -> 'str':
        """str: 'DesignWithHighestNumberOfPinionTeeth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DesignWithHighestNumberOfPinionTeeth

        if temp is None:
            return None

        return temp

    @property
    def design_with_lowest_number_of_pinion_teeth(self) -> 'str':
        """str: 'DesignWithLowestNumberOfPinionTeeth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DesignWithLowestNumberOfPinionTeeth

        if temp is None:
            return None

        return temp

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @property
    def number_of_candidate_designs(self) -> 'int':
        """int: 'NumberOfCandidateDesigns' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfCandidateDesigns

        if temp is None:
            return None

        return temp

    def create_designs(self):
        """ 'CreateDesigns' is the original name of this method."""

        self.wrapped.CreateDesigns()

    def create_designs_dont_attempt_to_fix(self):
        """ 'CreateDesignsDontAttemptToFix' is the original name of this method."""

        self.wrapped.CreateDesignsDontAttemptToFix()
