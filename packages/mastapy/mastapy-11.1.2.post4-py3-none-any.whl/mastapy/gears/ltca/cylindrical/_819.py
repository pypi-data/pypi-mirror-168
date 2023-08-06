"""_819.py

CylindricalGearContactStiffness
"""


from mastapy.gears.ltca import _801
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_CONTACT_STIFFNESS = python_net_import('SMT.MastaAPI.Gears.LTCA.Cylindrical', 'CylindricalGearContactStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearContactStiffness',)


class CylindricalGearContactStiffness(_801.GearContactStiffness):
    """CylindricalGearContactStiffness

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_CONTACT_STIFFNESS

    def __init__(self, instance_to_wrap: 'CylindricalGearContactStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
