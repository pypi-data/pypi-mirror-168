"""_583.py

CylindricalManufacturedGearLoadCase
"""


from mastapy.gears.analysis import _1171
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MANUFACTURED_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'CylindricalManufacturedGearLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalManufacturedGearLoadCase',)


class CylindricalManufacturedGearLoadCase(_1171.GearImplementationAnalysis):
    """CylindricalManufacturedGearLoadCase

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_MANUFACTURED_GEAR_LOAD_CASE

    def __init__(self, instance_to_wrap: 'CylindricalManufacturedGearLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
