"""_2250.py

CylindricalRingGearFromCAD
"""


from mastapy.system_model.part_model.import_from_cad import _2248
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_RING_GEAR_FROM_CAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD', 'CylindricalRingGearFromCAD')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalRingGearFromCAD',)


class CylindricalRingGearFromCAD(_2248.CylindricalGearInPlanetarySetFromCAD):
    """CylindricalRingGearFromCAD

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_RING_GEAR_FROM_CAD

    def __init__(self, instance_to_wrap: 'CylindricalRingGearFromCAD.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
