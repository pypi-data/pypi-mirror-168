"""_1991.py

OptimizationStrategyDatabase
"""


from mastapy.utility.databases import _1604
from mastapy.system_model.optimization import _1983
from mastapy._internal.python_net import python_net_import

_OPTIMIZATION_STRATEGY_DATABASE = python_net_import('SMT.MastaAPI.SystemModel.Optimization', 'OptimizationStrategyDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('OptimizationStrategyDatabase',)


class OptimizationStrategyDatabase(_1604.NamedDatabase['_1983.CylindricalGearOptimisationStrategy']):
    """OptimizationStrategyDatabase

    This is a mastapy class.
    """

    TYPE = _OPTIMIZATION_STRATEGY_DATABASE

    def __init__(self, instance_to_wrap: 'OptimizationStrategyDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
