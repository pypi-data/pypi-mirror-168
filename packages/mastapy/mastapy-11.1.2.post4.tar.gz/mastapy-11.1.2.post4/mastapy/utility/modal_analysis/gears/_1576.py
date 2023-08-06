"""_1576.py

GearMeshForTE
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.utility.modal_analysis.gears import _1577, _1581
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_FOR_TE = python_net_import('SMT.MastaAPI.Utility.ModalAnalysis.Gears', 'GearMeshForTE')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshForTE',)


class GearMeshForTE(_1581.OrderForTE):
    """GearMeshForTE

    This is a mastapy class.
    """

    TYPE = _GEAR_MESH_FOR_TE

    def __init__(self, instance_to_wrap: 'GearMeshForTE.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_teeth(self) -> 'str':
        """str: 'NumberOfTeeth' is the original name of this property."""

        temp = self.wrapped.NumberOfTeeth

        if temp is None:
            return None

        return temp

    @number_of_teeth.setter
    def number_of_teeth(self, value: 'str'):
        self.wrapped.NumberOfTeeth = str(value) if value else ''

    @property
    def attached_gears(self) -> 'List[_1577.GearOrderForTE]':
        """List[GearOrderForTE]: 'AttachedGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AttachedGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
