"""_829.py

ConicalGearBendingStiffness
"""


from mastapy.gears.ltca import _799
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_BENDING_STIFFNESS = python_net_import('SMT.MastaAPI.Gears.LTCA.Conical', 'ConicalGearBendingStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearBendingStiffness',)


class ConicalGearBendingStiffness(_799.GearBendingStiffness):
    """ConicalGearBendingStiffness

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_BENDING_STIFFNESS

    def __init__(self, instance_to_wrap: 'ConicalGearBendingStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
