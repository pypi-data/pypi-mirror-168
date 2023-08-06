"""_1129.py

ConicalGearProfileModification
"""


from mastapy.gears.micro_geometry import _548
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_PROFILE_MODIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Conical.MicroGeometry', 'ConicalGearProfileModification')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearProfileModification',)


class ConicalGearProfileModification(_548.ProfileModification):
    """ConicalGearProfileModification

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_PROFILE_MODIFICATION

    def __init__(self, instance_to_wrap: 'ConicalGearProfileModification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
