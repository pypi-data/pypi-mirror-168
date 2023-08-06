"""_61.py

FEModalFrequencyComparison
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FE_MODAL_FREQUENCY_COMPARISON = python_net_import('SMT.MastaAPI.NodalAnalysis', 'FEModalFrequencyComparison')


__docformat__ = 'restructuredtext en'
__all__ = ('FEModalFrequencyComparison',)


class FEModalFrequencyComparison(_0.APIBase):
    """FEModalFrequencyComparison

    This is a mastapy class.
    """

    TYPE = _FE_MODAL_FREQUENCY_COMPARISON

    def __init__(self, instance_to_wrap: 'FEModalFrequencyComparison.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def difference_in_frequencies(self) -> 'float':
        """float: 'DifferenceInFrequencies' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DifferenceInFrequencies

        if temp is None:
            return None

        return temp

    @property
    def full_model_frequency(self) -> 'float':
        """float: 'FullModelFrequency' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FullModelFrequency

        if temp is None:
            return None

        return temp

    @property
    def mode(self) -> 'int':
        """int: 'Mode' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Mode

        if temp is None:
            return None

        return temp

    @property
    def percentage_error(self) -> 'float':
        """float: 'PercentageError' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PercentageError

        if temp is None:
            return None

        return temp

    @property
    def reduced_model_frequency(self) -> 'float':
        """float: 'ReducedModelFrequency' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReducedModelFrequency

        if temp is None:
            return None

        return temp
