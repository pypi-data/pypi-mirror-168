"""_1152.py

GearMeshFEModel
"""


from mastapy._internal import constructor
from mastapy.gears.analysis import _1177
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_FE_MODEL = python_net_import('SMT.MastaAPI.Gears.FEModel', 'GearMeshFEModel')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshFEModel',)


class GearMeshFEModel(_1177.GearMeshImplementationDetail):
    """GearMeshFEModel

    This is a mastapy class.
    """

    TYPE = _GEAR_MESH_FE_MODEL

    def __init__(self, instance_to_wrap: 'GearMeshFEModel.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_loads_per_contact(self) -> 'int':
        """int: 'NumberOfLoadsPerContact' is the original name of this property."""

        temp = self.wrapped.NumberOfLoadsPerContact

        if temp is None:
            return None

        return temp

    @number_of_loads_per_contact.setter
    def number_of_loads_per_contact(self, value: 'int'):
        self.wrapped.NumberOfLoadsPerContact = int(value) if value else 0

    @property
    def number_of_rotations(self) -> 'int':
        """int: 'NumberOfRotations' is the original name of this property."""

        temp = self.wrapped.NumberOfRotations

        if temp is None:
            return None

        return temp

    @number_of_rotations.setter
    def number_of_rotations(self, value: 'int'):
        self.wrapped.NumberOfRotations = int(value) if value else 0
