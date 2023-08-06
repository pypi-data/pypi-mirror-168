"""_109.py

SingularValuesAnalysis
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.nodal_analysis.system_solvers import _110
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SINGULAR_VALUES_ANALYSIS = python_net_import('SMT.MastaAPI.NodalAnalysis.SystemSolvers', 'SingularValuesAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SingularValuesAnalysis',)


class SingularValuesAnalysis(_0.APIBase):
    """SingularValuesAnalysis

    This is a mastapy class.
    """

    TYPE = _SINGULAR_VALUES_ANALYSIS

    def __init__(self, instance_to_wrap: 'SingularValuesAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def condition_number(self) -> 'float':
        """float: 'ConditionNumber' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConditionNumber

        if temp is None:
            return None

        return temp

    @property
    def stiffness_matrix_degrees_of_freedom(self) -> 'int':
        """int: 'StiffnessMatrixDegreesOfFreedom' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessMatrixDegreesOfFreedom

        if temp is None:
            return None

        return temp

    @property
    def stiffness_matrix_rank(self) -> 'int':
        """int: 'StiffnessMatrixRank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessMatrixRank

        if temp is None:
            return None

        return temp

    @property
    def largest_singular_vectors(self) -> 'List[_110.SingularVectorAnalysis]':
        """List[SingularVectorAnalysis]: 'LargestSingularVectors' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LargestSingularVectors

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def smallest_singular_vectors(self) -> 'List[_110.SingularVectorAnalysis]':
        """List[SingularVectorAnalysis]: 'SmallestSingularVectors' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SmallestSingularVectors

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
