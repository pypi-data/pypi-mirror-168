"""_1697.py

RollerBearingFlatProfile
"""


from mastapy.bearings.roller_bearing_profiles import _1700
from mastapy._internal.python_net import python_net_import

_ROLLER_BEARING_FLAT_PROFILE = python_net_import('SMT.MastaAPI.Bearings.RollerBearingProfiles', 'RollerBearingFlatProfile')


__docformat__ = 'restructuredtext en'
__all__ = ('RollerBearingFlatProfile',)


class RollerBearingFlatProfile(_1700.RollerBearingProfile):
    """RollerBearingFlatProfile

    This is a mastapy class.
    """

    TYPE = _ROLLER_BEARING_FLAT_PROFILE

    def __init__(self, instance_to_wrap: 'RollerBearingFlatProfile.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
