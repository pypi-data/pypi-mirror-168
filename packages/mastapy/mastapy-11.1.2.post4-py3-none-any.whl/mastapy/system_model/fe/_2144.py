"""_2144.py

FESubstructureWithSelectionForStaticAnalysis
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.utility.enums import _1598
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.nodal_analysis.component_mode_synthesis import _213
from mastapy.nodal_analysis.dev_tools_analyses import _171
from mastapy.system_model.fe import _2150, _2140
from mastapy.math_utility.measured_vectors import _1371
from mastapy._internal.python_net import python_net_import

_FE_SUBSTRUCTURE_WITH_SELECTION_FOR_STATIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.FE', 'FESubstructureWithSelectionForStaticAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FESubstructureWithSelectionForStaticAnalysis',)


class FESubstructureWithSelectionForStaticAnalysis(_2140.FESubstructureWithSelection):
    """FESubstructureWithSelectionForStaticAnalysis

    This is a mastapy class.
    """

    TYPE = _FE_SUBSTRUCTURE_WITH_SELECTION_FOR_STATIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'FESubstructureWithSelectionForStaticAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def average_stress_to_nodes(self) -> 'bool':
        """bool: 'AverageStressToNodes' is the original name of this property."""

        temp = self.wrapped.AverageStressToNodes

        if temp is None:
            return None

        return temp

    @average_stress_to_nodes.setter
    def average_stress_to_nodes(self, value: 'bool'):
        self.wrapped.AverageStressToNodes = bool(value) if value else False

    @property
    def contour_option(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOption':
        """enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOption: 'ContourOption' is the original name of this property."""

        temp = self.wrapped.ContourOption

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOption.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @contour_option.setter
    def contour_option(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOption.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOption.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ContourOption = value

    @property
    def temperature_change_from_nominal(self) -> 'float':
        """float: 'TemperatureChangeFromNominal' is the original name of this property."""

        temp = self.wrapped.TemperatureChangeFromNominal

        if temp is None:
            return None

        return temp

    @temperature_change_from_nominal.setter
    def temperature_change_from_nominal(self, value: 'float'):
        self.wrapped.TemperatureChangeFromNominal = float(value) if value else 0.0

    @property
    def full_fe_results(self) -> '_213.StaticCMSResults':
        """StaticCMSResults: 'FullFEResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FullFEResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def static_draw_style(self) -> '_171.FEModelStaticAnalysisDrawStyle':
        """FEModelStaticAnalysisDrawStyle: 'StaticDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StaticDrawStyle

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

    @property
    def boundary_conditions_selected_nodes(self) -> 'List[_2150.NodeBoundaryConditionStaticAnalysis]':
        """List[NodeBoundaryConditionStaticAnalysis]: 'BoundaryConditionsSelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BoundaryConditionsSelectedNodes

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def displacement_results(self) -> 'List[_1371.VectorWithLinearAndAngularComponents]':
        """List[VectorWithLinearAndAngularComponents]: 'DisplacementResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DisplacementResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def force_results(self) -> 'List[_1371.VectorWithLinearAndAngularComponents]':
        """List[VectorWithLinearAndAngularComponents]: 'ForceResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def reset_displacements(self):
        """ 'ResetDisplacements' is the original name of this method."""

        self.wrapped.ResetDisplacements()

    def reset_forces(self):
        """ 'ResetForces' is the original name of this method."""

        self.wrapped.ResetForces()

    def solve(self):
        """ 'Solve' is the original name of this method."""

        self.wrapped.Solve()

    def torque_transfer_check(self):
        """ 'TorqueTransferCheck' is the original name of this method."""

        self.wrapped.TorqueTransferCheck()
