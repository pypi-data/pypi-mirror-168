"""_1348.py

MicroGeometryDesignSpaceSearchStrategyDatabase
"""


from mastapy.math_utility.optimisation import _1346
from mastapy._internal.python_net import python_net_import

_MICRO_GEOMETRY_DESIGN_SPACE_SEARCH_STRATEGY_DATABASE = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'MicroGeometryDesignSpaceSearchStrategyDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('MicroGeometryDesignSpaceSearchStrategyDatabase',)


class MicroGeometryDesignSpaceSearchStrategyDatabase(_1346.DesignSpaceSearchStrategyDatabase):
    """MicroGeometryDesignSpaceSearchStrategyDatabase

    This is a mastapy class.
    """

    TYPE = _MICRO_GEOMETRY_DESIGN_SPACE_SEARCH_STRATEGY_DATABASE

    def __init__(self, instance_to_wrap: 'MicroGeometryDesignSpaceSearchStrategyDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
