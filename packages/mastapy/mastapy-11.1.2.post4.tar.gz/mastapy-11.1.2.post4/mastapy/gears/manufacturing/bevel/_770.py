"""_770.py

PinionConicalMachineSettingsSpecified
"""


from mastapy.gears.manufacturing.bevel import _772
from mastapy._internal.python_net import python_net_import

_PINION_CONICAL_MACHINE_SETTINGS_SPECIFIED = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'PinionConicalMachineSettingsSpecified')


__docformat__ = 'restructuredtext en'
__all__ = ('PinionConicalMachineSettingsSpecified',)


class PinionConicalMachineSettingsSpecified(_772.PinionFinishMachineSettings):
    """PinionConicalMachineSettingsSpecified

    This is a mastapy class.
    """

    TYPE = _PINION_CONICAL_MACHINE_SETTINGS_SPECIFIED

    def __init__(self, instance_to_wrap: 'PinionConicalMachineSettingsSpecified.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
