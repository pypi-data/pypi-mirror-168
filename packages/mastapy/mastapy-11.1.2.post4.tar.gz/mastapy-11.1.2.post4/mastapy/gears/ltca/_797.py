"""_797.py

CylindricalGearRootFilletStressResults
"""


from mastapy.gears.ltca import _811
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_ROOT_FILLET_STRESS_RESULTS = python_net_import('SMT.MastaAPI.Gears.LTCA', 'CylindricalGearRootFilletStressResults')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearRootFilletStressResults',)


class CylindricalGearRootFilletStressResults(_811.GearRootFilletStressResults):
    """CylindricalGearRootFilletStressResults

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_ROOT_FILLET_STRESS_RESULTS

    def __init__(self, instance_to_wrap: 'CylindricalGearRootFilletStressResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
