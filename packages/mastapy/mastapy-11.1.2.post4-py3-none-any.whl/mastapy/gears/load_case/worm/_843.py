"""_843.py

WormGearSetLoadCase
"""


from mastapy.gears.load_case import _840
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.Gears.LoadCase.Worm', 'WormGearSetLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetLoadCase',)


class WormGearSetLoadCase(_840.GearSetLoadCaseBase):
    """WormGearSetLoadCase

    This is a mastapy class.
    """

    TYPE = _WORM_GEAR_SET_LOAD_CASE

    def __init__(self, instance_to_wrap: 'WormGearSetLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
