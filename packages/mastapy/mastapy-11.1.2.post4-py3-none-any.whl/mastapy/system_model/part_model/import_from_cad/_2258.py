"""_2258.py

ShaftFromCAD
"""


from mastapy._internal import constructor
from mastapy.system_model.part_model.import_from_cad import _2242
from mastapy._internal.python_net import python_net_import

_SHAFT_FROM_CAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD', 'ShaftFromCAD')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftFromCAD',)


class ShaftFromCAD(_2242.AbstractShaftFromCAD):
    """ShaftFromCAD

    This is a mastapy class.
    """

    TYPE = _SHAFT_FROM_CAD

    def __init__(self, instance_to_wrap: 'ShaftFromCAD.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def create_assembly(self) -> 'bool':
        """bool: 'CreateAssembly' is the original name of this property."""

        temp = self.wrapped.CreateAssembly

        if temp is None:
            return None

        return temp

    @create_assembly.setter
    def create_assembly(self, value: 'bool'):
        self.wrapped.CreateAssembly = bool(value) if value else False
