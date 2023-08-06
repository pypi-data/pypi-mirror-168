"""_315.py

PocketingPowerLossCoefficientsDatabase
"""


from mastapy.utility.databases import _1604
from mastapy.gears import _314
from mastapy._internal.python_net import python_net_import

_POCKETING_POWER_LOSS_COEFFICIENTS_DATABASE = python_net_import('SMT.MastaAPI.Gears', 'PocketingPowerLossCoefficientsDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('PocketingPowerLossCoefficientsDatabase',)


class PocketingPowerLossCoefficientsDatabase(_1604.NamedDatabase['_314.PocketingPowerLossCoefficients']):
    """PocketingPowerLossCoefficientsDatabase

    This is a mastapy class.
    """

    TYPE = _POCKETING_POWER_LOSS_COEFFICIENTS_DATABASE

    def __init__(self, instance_to_wrap: 'PocketingPowerLossCoefficientsDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
