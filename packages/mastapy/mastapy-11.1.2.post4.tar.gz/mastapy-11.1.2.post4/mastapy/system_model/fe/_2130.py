"""_2130.py

FEPartWithBatchOptions
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.fe import _2139
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FE_PART_WITH_BATCH_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.FE', 'FEPartWithBatchOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartWithBatchOptions',)


class FEPartWithBatchOptions(_0.APIBase):
    """FEPartWithBatchOptions

    This is a mastapy class.
    """

    TYPE = _FE_PART_WITH_BATCH_OPTIONS

    def __init__(self, instance_to_wrap: 'FEPartWithBatchOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def all_selected(self) -> 'bool':
        """bool: 'AllSelected' is the original name of this property."""

        temp = self.wrapped.AllSelected

        if temp is None:
            return None

        return temp

    @all_selected.setter
    def all_selected(self, value: 'bool'):
        self.wrapped.AllSelected = bool(value) if value else False

    @property
    def fe_part(self) -> 'str':
        """str: 'FEPart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FEPart

        if temp is None:
            return None

        return temp

    @property
    def f_es(self) -> 'List[_2139.FESubstructureWithBatchOptions]':
        """List[FESubstructureWithBatchOptions]: 'FEs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FEs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def f_es_with_external_files(self) -> 'List[_2139.FESubstructureWithBatchOptions]':
        """List[FESubstructureWithBatchOptions]: 'FEsWithExternalFiles' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FEsWithExternalFiles

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
