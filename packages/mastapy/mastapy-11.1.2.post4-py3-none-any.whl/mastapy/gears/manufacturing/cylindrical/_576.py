"""_576.py

CylindricalCutterDatabase
"""


from typing import Generic, TypeVar

from mastapy.utility.databases import _1604
from mastapy.gears.manufacturing.cylindrical.cutters import _679
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_CUTTER_DATABASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'CylindricalCutterDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalCutterDatabase',)


T = TypeVar('T', bound='_679.CylindricalGearRealCutterDesign')


class CylindricalCutterDatabase(_1604.NamedDatabase['T'], Generic[T]):
    """CylindricalCutterDatabase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _CYLINDRICAL_CUTTER_DATABASE

    def __init__(self, instance_to_wrap: 'CylindricalCutterDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
