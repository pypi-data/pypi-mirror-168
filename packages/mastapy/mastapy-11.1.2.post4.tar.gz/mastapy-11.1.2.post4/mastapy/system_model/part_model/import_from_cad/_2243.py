"""_2243.py

ClutchFromCAD
"""


from mastapy._internal import constructor
from mastapy.system_model.part_model.import_from_cad import _2253
from mastapy._internal.python_net import python_net_import

_CLUTCH_FROM_CAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD', 'ClutchFromCAD')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchFromCAD',)


class ClutchFromCAD(_2253.MountableComponentFromCAD):
    """ClutchFromCAD

    This is a mastapy class.
    """

    TYPE = _CLUTCH_FROM_CAD

    def __init__(self, instance_to_wrap: 'ClutchFromCAD.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def clutch_name(self) -> 'str':
        """str: 'ClutchName' is the original name of this property."""

        temp = self.wrapped.ClutchName

        if temp is None:
            return None

        return temp

    @clutch_name.setter
    def clutch_name(self, value: 'str'):
        self.wrapped.ClutchName = str(value) if value else ''

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
