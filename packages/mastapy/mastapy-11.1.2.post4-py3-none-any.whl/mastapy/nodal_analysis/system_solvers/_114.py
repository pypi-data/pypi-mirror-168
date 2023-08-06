"""_114.py

TransientSolver
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.nodal_analysis import _85
from mastapy.nodal_analysis.system_solvers import _99
from mastapy._internal.python_net import python_net_import

_TRANSIENT_SOLVER = python_net_import('SMT.MastaAPI.NodalAnalysis.SystemSolvers', 'TransientSolver')


__docformat__ = 'restructuredtext en'
__all__ = ('TransientSolver',)


class TransientSolver(_99.DynamicSolver):
    """TransientSolver

    This is a mastapy class.
    """

    TYPE = _TRANSIENT_SOLVER

    def __init__(self, instance_to_wrap: 'TransientSolver.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def average_number_of_jacobian_evaluations_per_newton_raphson_solve(self) -> 'float':
        """float: 'AverageNumberOfJacobianEvaluationsPerNewtonRaphsonSolve' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AverageNumberOfJacobianEvaluationsPerNewtonRaphsonSolve

        if temp is None:
            return None

        return temp

    @property
    def interface_analysis_time(self) -> 'float':
        """float: 'InterfaceAnalysisTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InterfaceAnalysisTime

        if temp is None:
            return None

        return temp

    @property
    def number_of_failed_newton_raphson_solves(self) -> 'int':
        """int: 'NumberOfFailedNewtonRaphsonSolves' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfFailedNewtonRaphsonSolves

        if temp is None:
            return None

        return temp

    @property
    def number_of_failed_time_steps(self) -> 'int':
        """int: 'NumberOfFailedTimeSteps' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfFailedTimeSteps

        if temp is None:
            return None

        return temp

    @property
    def number_of_failed_time_steps_at_minimum_time_step(self) -> 'int':
        """int: 'NumberOfFailedTimeStepsAtMinimumTimeStep' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfFailedTimeStepsAtMinimumTimeStep

        if temp is None:
            return None

        return temp

    @property
    def number_of_interface_time_steps(self) -> 'int':
        """int: 'NumberOfInterfaceTimeSteps' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfInterfaceTimeSteps

        if temp is None:
            return None

        return temp

    @property
    def number_of_newton_raphson_jacobian_evaluations(self) -> 'int':
        """int: 'NumberOfNewtonRaphsonJacobianEvaluations' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfNewtonRaphsonJacobianEvaluations

        if temp is None:
            return None

        return temp

    @property
    def number_of_newton_raphson_maximum_iterations_reached(self) -> 'int':
        """int: 'NumberOfNewtonRaphsonMaximumIterationsReached' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfNewtonRaphsonMaximumIterationsReached

        if temp is None:
            return None

        return temp

    @property
    def number_of_newton_raphson_other_status_results(self) -> 'int':
        """int: 'NumberOfNewtonRaphsonOtherStatusResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfNewtonRaphsonOtherStatusResults

        if temp is None:
            return None

        return temp

    @property
    def number_of_newton_raphson_residual_evaluations(self) -> 'int':
        """int: 'NumberOfNewtonRaphsonResidualEvaluations' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfNewtonRaphsonResidualEvaluations

        if temp is None:
            return None

        return temp

    @property
    def number_of_newton_raphson_residual_tolerance_met(self) -> 'int':
        """int: 'NumberOfNewtonRaphsonResidualToleranceMet' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfNewtonRaphsonResidualToleranceMet

        if temp is None:
            return None

        return temp

    @property
    def number_of_newton_raphson_solves(self) -> 'int':
        """int: 'NumberOfNewtonRaphsonSolves' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfNewtonRaphsonSolves

        if temp is None:
            return None

        return temp

    @property
    def number_of_newton_raphson_values_not_changing(self) -> 'int':
        """int: 'NumberOfNewtonRaphsonValuesNotChanging' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfNewtonRaphsonValuesNotChanging

        if temp is None:
            return None

        return temp

    @property
    def number_of_time_steps_taken(self) -> 'int':
        """int: 'NumberOfTimeStepsTaken' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfTimeStepsTaken

        if temp is None:
            return None

        return temp

    @property
    def number_of_times_step_error_tolerance_not_met(self) -> 'int':
        """int: 'NumberOfTimesStepErrorToleranceNotMet' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfTimesStepErrorToleranceNotMet

        if temp is None:
            return None

        return temp

    @property
    def solver_status(self) -> '_85.TransientSolverStatus':
        """TransientSolverStatus: 'SolverStatus' is the original name of this property."""

        temp = self.wrapped.SolverStatus

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_85.TransientSolverStatus)(value) if value is not None else None

    @solver_status.setter
    def solver_status(self, value: '_85.TransientSolverStatus'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SolverStatus = value

    def times_of_logged_results(self) -> 'List[float]':
        """ 'TimesOfLoggedResults' is the original name of this method.

        Returns:
            List[float]
        """

        return conversion.pn_to_mp_objects_in_list(self.wrapped.TimesOfLoggedResults(), float)
