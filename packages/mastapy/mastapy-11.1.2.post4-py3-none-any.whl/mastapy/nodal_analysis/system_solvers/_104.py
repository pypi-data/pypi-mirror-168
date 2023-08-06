"""_104.py

NewmarkTransientSolver
"""


from mastapy.nodal_analysis.system_solvers import _107
from mastapy._internal.python_net import python_net_import

_NEWMARK_TRANSIENT_SOLVER = python_net_import('SMT.MastaAPI.NodalAnalysis.SystemSolvers', 'NewmarkTransientSolver')


__docformat__ = 'restructuredtext en'
__all__ = ('NewmarkTransientSolver',)


class NewmarkTransientSolver(_107.SimpleVelocityBasedStepHalvingTransientSolver):
    """NewmarkTransientSolver

    This is a mastapy class.
    """

    TYPE = _NEWMARK_TRANSIENT_SOLVER

    def __init__(self, instance_to_wrap: 'NewmarkTransientSolver.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
