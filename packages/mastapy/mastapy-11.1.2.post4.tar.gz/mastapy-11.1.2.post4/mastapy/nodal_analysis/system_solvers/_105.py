"""_105.py

SemiImplicitTransientSolver
"""


from mastapy.nodal_analysis.system_solvers import _100
from mastapy._internal.python_net import python_net_import

_SEMI_IMPLICIT_TRANSIENT_SOLVER = python_net_import('SMT.MastaAPI.NodalAnalysis.SystemSolvers', 'SemiImplicitTransientSolver')


__docformat__ = 'restructuredtext en'
__all__ = ('SemiImplicitTransientSolver',)


class SemiImplicitTransientSolver(_100.InternalTransientSolver):
    """SemiImplicitTransientSolver

    This is a mastapy class.
    """

    TYPE = _SEMI_IMPLICIT_TRANSIENT_SOLVER

    def __init__(self, instance_to_wrap: 'SemiImplicitTransientSolver.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
