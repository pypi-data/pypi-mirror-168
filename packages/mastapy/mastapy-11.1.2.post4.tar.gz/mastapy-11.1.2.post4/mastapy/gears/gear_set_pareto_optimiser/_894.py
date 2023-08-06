"""_894.py

ParetoFaceGearSetOptimisationStrategyDatabase
"""


from mastapy.gears.gear_set_pareto_optimiser import _895
from mastapy._internal.python_net import python_net_import

_PARETO_FACE_GEAR_SET_OPTIMISATION_STRATEGY_DATABASE = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'ParetoFaceGearSetOptimisationStrategyDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ParetoFaceGearSetOptimisationStrategyDatabase',)


class ParetoFaceGearSetOptimisationStrategyDatabase(_895.ParetoFaceRatingOptimisationStrategyDatabase):
    """ParetoFaceGearSetOptimisationStrategyDatabase

    This is a mastapy class.
    """

    TYPE = _PARETO_FACE_GEAR_SET_OPTIMISATION_STRATEGY_DATABASE

    def __init__(self, instance_to_wrap: 'ParetoFaceGearSetOptimisationStrategyDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
