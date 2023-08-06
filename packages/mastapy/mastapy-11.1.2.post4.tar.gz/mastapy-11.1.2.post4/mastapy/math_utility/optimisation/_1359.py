"""_1359.py

ParetoOptimisationStrategyDatabase
"""


from mastapy.math_utility.optimisation import _1346
from mastapy._internal.python_net import python_net_import

_PARETO_OPTIMISATION_STRATEGY_DATABASE = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'ParetoOptimisationStrategyDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ParetoOptimisationStrategyDatabase',)


class ParetoOptimisationStrategyDatabase(_1346.DesignSpaceSearchStrategyDatabase):
    """ParetoOptimisationStrategyDatabase

    This is a mastapy class.
    """

    TYPE = _PARETO_OPTIMISATION_STRATEGY_DATABASE

    def __init__(self, instance_to_wrap: 'ParetoOptimisationStrategyDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
