"""_792.py

ConicalGearRootFilletStressResults
"""


from mastapy.gears.ltca import _811
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_ROOT_FILLET_STRESS_RESULTS = python_net_import('SMT.MastaAPI.Gears.LTCA', 'ConicalGearRootFilletStressResults')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearRootFilletStressResults',)


class ConicalGearRootFilletStressResults(_811.GearRootFilletStressResults):
    """ConicalGearRootFilletStressResults

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_ROOT_FILLET_STRESS_RESULTS

    def __init__(self, instance_to_wrap: 'ConicalGearRootFilletStressResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
