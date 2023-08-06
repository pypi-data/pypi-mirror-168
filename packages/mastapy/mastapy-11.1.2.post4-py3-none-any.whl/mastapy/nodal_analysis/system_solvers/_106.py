"""_106.py

SimpleAccelerationBasedStepHalvingTransientSolver
"""


from mastapy.nodal_analysis.system_solvers import _112
from mastapy._internal.python_net import python_net_import

_SIMPLE_ACCELERATION_BASED_STEP_HALVING_TRANSIENT_SOLVER = python_net_import('SMT.MastaAPI.NodalAnalysis.SystemSolvers', 'SimpleAccelerationBasedStepHalvingTransientSolver')


__docformat__ = 'restructuredtext en'
__all__ = ('SimpleAccelerationBasedStepHalvingTransientSolver',)


class SimpleAccelerationBasedStepHalvingTransientSolver(_112.StepHalvingTransientSolver):
    """SimpleAccelerationBasedStepHalvingTransientSolver

    This is a mastapy class.
    """

    TYPE = _SIMPLE_ACCELERATION_BASED_STEP_HALVING_TRANSIENT_SOLVER

    def __init__(self, instance_to_wrap: 'SimpleAccelerationBasedStepHalvingTransientSolver.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
