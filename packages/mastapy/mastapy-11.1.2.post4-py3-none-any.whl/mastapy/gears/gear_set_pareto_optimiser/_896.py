"""_896.py

ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase
"""


from mastapy.gears.gear_set_pareto_optimiser import _889
from mastapy._internal.python_net import python_net_import

_PARETO_HYPOID_GEAR_SET_DUTY_CYCLE_OPTIMISATION_STRATEGY_DATABASE = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase',)


class ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase(_889.ParetoConicalRatingOptimisationStrategyDatabase):
    """ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase

    This is a mastapy class.
    """

    TYPE = _PARETO_HYPOID_GEAR_SET_DUTY_CYCLE_OPTIMISATION_STRATEGY_DATABASE

    def __init__(self, instance_to_wrap: 'ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
