"""_891.py

ParetoCylindricalGearSetOptimisationStrategyDatabase
"""


from mastapy.gears.gear_set_pareto_optimiser import _892
from mastapy._internal.python_net import python_net_import

_PARETO_CYLINDRICAL_GEAR_SET_OPTIMISATION_STRATEGY_DATABASE = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'ParetoCylindricalGearSetOptimisationStrategyDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ParetoCylindricalGearSetOptimisationStrategyDatabase',)


class ParetoCylindricalGearSetOptimisationStrategyDatabase(_892.ParetoCylindricalRatingOptimisationStrategyDatabase):
    """ParetoCylindricalGearSetOptimisationStrategyDatabase

    This is a mastapy class.
    """

    TYPE = _PARETO_CYLINDRICAL_GEAR_SET_OPTIMISATION_STRATEGY_DATABASE

    def __init__(self, instance_to_wrap: 'ParetoCylindricalGearSetOptimisationStrategyDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
