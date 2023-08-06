"""_1733.py

ForceAtLaminaReportable
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FORCE_AT_LAMINA_REPORTABLE = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'ForceAtLaminaReportable')


__docformat__ = 'restructuredtext en'
__all__ = ('ForceAtLaminaReportable',)


class ForceAtLaminaReportable(_0.APIBase):
    """ForceAtLaminaReportable

    This is a mastapy class.
    """

    TYPE = _FORCE_AT_LAMINA_REPORTABLE

    def __init__(self, instance_to_wrap: 'ForceAtLaminaReportable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def dynamic_equivalent_load(self) -> 'float':
        """float: 'DynamicEquivalentLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicEquivalentLoad

        if temp is None:
            return None

        return temp

    @property
    def lamina_index(self) -> 'int':
        """int: 'LaminaIndex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LaminaIndex

        if temp is None:
            return None

        return temp
