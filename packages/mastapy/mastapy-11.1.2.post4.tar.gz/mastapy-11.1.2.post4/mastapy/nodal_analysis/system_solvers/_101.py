"""_101.py

LobattoIIIATransientSolver
"""


from mastapy.nodal_analysis.system_solvers import _107
from mastapy._internal.python_net import python_net_import

_LOBATTO_IIIA_TRANSIENT_SOLVER = python_net_import('SMT.MastaAPI.NodalAnalysis.SystemSolvers', 'LobattoIIIATransientSolver')


__docformat__ = 'restructuredtext en'
__all__ = ('LobattoIIIATransientSolver',)


class LobattoIIIATransientSolver(_107.SimpleVelocityBasedStepHalvingTransientSolver):
    """LobattoIIIATransientSolver

    This is a mastapy class.
    """

    TYPE = _LOBATTO_IIIA_TRANSIENT_SOLVER

    def __init__(self, instance_to_wrap: 'LobattoIIIATransientSolver.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
