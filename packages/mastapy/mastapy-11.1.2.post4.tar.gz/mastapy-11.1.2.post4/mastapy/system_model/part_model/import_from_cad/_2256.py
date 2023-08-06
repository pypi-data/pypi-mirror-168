"""_2256.py

RigidConnectorFromCAD
"""


from mastapy._internal import constructor
from mastapy.system_model.part_model.import_from_cad import _2246
from mastapy._internal.python_net import python_net_import

_RIGID_CONNECTOR_FROM_CAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD', 'RigidConnectorFromCAD')


__docformat__ = 'restructuredtext en'
__all__ = ('RigidConnectorFromCAD',)


class RigidConnectorFromCAD(_2246.ConnectorFromCAD):
    """RigidConnectorFromCAD

    This is a mastapy class.
    """

    TYPE = _RIGID_CONNECTOR_FROM_CAD

    def __init__(self, instance_to_wrap: 'RigidConnectorFromCAD.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def length(self) -> 'float':
        """float: 'Length' is the original name of this property."""

        temp = self.wrapped.Length

        if temp is None:
            return None

        return temp

    @length.setter
    def length(self, value: 'float'):
        self.wrapped.Length = float(value) if value else 0.0
