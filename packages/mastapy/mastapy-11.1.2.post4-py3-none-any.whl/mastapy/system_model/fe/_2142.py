"""_2142.py

FESubstructureWithSelectionForHarmonicAnalysis
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.nodal_analysis.dev_tools_analyses import _167
from mastapy.system_model.fe import _2150, _2140
from mastapy._internal.python_net import python_net_import

_FE_SUBSTRUCTURE_WITH_SELECTION_FOR_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.FE', 'FESubstructureWithSelectionForHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FESubstructureWithSelectionForHarmonicAnalysis',)


class FESubstructureWithSelectionForHarmonicAnalysis(_2140.FESubstructureWithSelection):
    """FESubstructureWithSelectionForHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _FE_SUBSTRUCTURE_WITH_SELECTION_FOR_HARMONIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'FESubstructureWithSelectionForHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def alpha_damping_value(self) -> 'float':
        """float: 'AlphaDampingValue' is the original name of this property."""

        temp = self.wrapped.AlphaDampingValue

        if temp is None:
            return None

        return temp

    @alpha_damping_value.setter
    def alpha_damping_value(self, value: 'float'):
        self.wrapped.AlphaDampingValue = float(value) if value else 0.0

    @property
    def beta_damping_value(self) -> 'float':
        """float: 'BetaDampingValue' is the original name of this property."""

        temp = self.wrapped.BetaDampingValue

        if temp is None:
            return None

        return temp

    @beta_damping_value.setter
    def beta_damping_value(self, value: 'float'):
        self.wrapped.BetaDampingValue = float(value) if value else 0.0

    @property
    def frequency(self) -> 'float':
        """float: 'Frequency' is the original name of this property."""

        temp = self.wrapped.Frequency

        if temp is None:
            return None

        return temp

    @frequency.setter
    def frequency(self, value: 'float'):
        self.wrapped.Frequency = float(value) if value else 0.0

    @property
    def harmonic_draw_style(self) -> '_167.FEModelHarmonicAnalysisDrawStyle':
        """FEModelHarmonicAnalysisDrawStyle: 'HarmonicDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicDrawStyle

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def boundary_conditions_all_nodes(self) -> 'List[_2150.NodeBoundaryConditionStaticAnalysis]':
        """List[NodeBoundaryConditionStaticAnalysis]: 'BoundaryConditionsAllNodes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BoundaryConditionsAllNodes

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def export_velocity_to_file(self):
        """ 'ExportVelocityToFile' is the original name of this method."""

        self.wrapped.ExportVelocityToFile()

    def solve_for_current_inputs(self):
        """ 'SolveForCurrentInputs' is the original name of this method."""

        self.wrapped.SolveForCurrentInputs()
