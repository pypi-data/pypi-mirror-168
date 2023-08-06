"""_978.py

CylindricalGearDesignConstraintsDatabase
"""


from mastapy.utility.databases import _1604
from mastapy.gears.gear_designs.cylindrical import _977
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_DESIGN_CONSTRAINTS_DATABASE = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearDesignConstraintsDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearDesignConstraintsDatabase',)


class CylindricalGearDesignConstraintsDatabase(_1604.NamedDatabase['_977.CylindricalGearDesignConstraints']):
    """CylindricalGearDesignConstraintsDatabase

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_DESIGN_CONSTRAINTS_DATABASE

    def __init__(self, instance_to_wrap: 'CylindricalGearDesignConstraintsDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
