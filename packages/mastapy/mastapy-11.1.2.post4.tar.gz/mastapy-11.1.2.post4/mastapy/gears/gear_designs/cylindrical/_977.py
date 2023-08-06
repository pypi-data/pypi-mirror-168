"""_977.py

CylindricalGearDesignConstraints
"""


from typing import List

from mastapy.gears.gear_designs.cylindrical import _976
from mastapy._internal import constructor, conversion
from mastapy.utility.databases import _1605
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_DESIGN_CONSTRAINTS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearDesignConstraints')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearDesignConstraints',)


class CylindricalGearDesignConstraints(_1605.NamedDatabaseItem):
    """CylindricalGearDesignConstraints

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_DESIGN_CONSTRAINTS

    def __init__(self, instance_to_wrap: 'CylindricalGearDesignConstraints.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def design_constraints(self) -> 'List[_976.CylindricalGearDesignConstraint]':
        """List[CylindricalGearDesignConstraint]: 'DesignConstraints' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DesignConstraints

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
