"""_5495.py

HarmonicAnalysisFEExportOptions
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value, list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.utility.units_and_measurements import _1411
from mastapy.nodal_analysis.component_mode_synthesis import _203
from mastapy.nodal_analysis.fe_export_utility import _158
from mastapy.system_model.analyses_and_results.harmonic_analyses import (
    _5496, _5484, _5538, _5494
)
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6799
from mastapy._internal.cast_exception import CastException
from mastapy.nodal_analysis.dev_tools_analyses import _160
from mastapy.system_model.analyses_and_results import _2403
from mastapy.system_model.part_model import _2203
from mastapy._internal.python_net import python_net_import

_HARMONIC_ANALYSIS_FE_EXPORT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'HarmonicAnalysisFEExportOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicAnalysisFEExportOptions',)


class HarmonicAnalysisFEExportOptions(_5494.HarmonicAnalysisExportOptions['_2403.IHaveFEPartHarmonicAnalysisResults', '_2203.FEPart']):
    """HarmonicAnalysisFEExportOptions

    This is a mastapy class.
    """

    TYPE = _HARMONIC_ANALYSIS_FE_EXPORT_OPTIONS

    def __init__(self, instance_to_wrap: 'HarmonicAnalysisFEExportOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def combine_excitations_from_different_parts(self) -> 'bool':
        """bool: 'CombineExcitationsFromDifferentParts' is the original name of this property."""

        temp = self.wrapped.CombineExcitationsFromDifferentParts

        if temp is None:
            return None

        return temp

    @combine_excitations_from_different_parts.setter
    def combine_excitations_from_different_parts(self, value: 'bool'):
        self.wrapped.CombineExcitationsFromDifferentParts = bool(value) if value else False

    @property
    def combine_excitations_of_same_order(self) -> 'bool':
        """bool: 'CombineExcitationsOfSameOrder' is the original name of this property."""

        temp = self.wrapped.CombineExcitationsOfSameOrder

        if temp is None:
            return None

        return temp

    @combine_excitations_of_same_order.setter
    def combine_excitations_of_same_order(self, value: 'bool'):
        self.wrapped.CombineExcitationsOfSameOrder = bool(value) if value else False

    @property
    def complex_number_output_option(self) -> 'enum_with_selected_value.EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput':
        """enum_with_selected_value.EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput: 'ComplexNumberOutputOption' is the original name of this property."""

        temp = self.wrapped.ComplexNumberOutputOption

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @complex_number_output_option.setter
    def complex_number_output_option(self, value: 'enum_with_selected_value.EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ComplexNumberOutputOption = value

    @property
    def distance_unit(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        """list_with_selected_item.ListWithSelectedItem_Unit: 'DistanceUnit' is the original name of this property."""

        temp = self.wrapped.DistanceUnit

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_Unit)(temp) if temp is not None else None

    @distance_unit.setter
    def distance_unit(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.DistanceUnit = value

    @property
    def element_face_group_to_export(self) -> 'list_with_selected_item.ListWithSelectedItem_CMSElementFaceGroup':
        """list_with_selected_item.ListWithSelectedItem_CMSElementFaceGroup: 'ElementFaceGroupToExport' is the original name of this property."""

        temp = self.wrapped.ElementFaceGroupToExport

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_CMSElementFaceGroup)(temp) if temp is not None else None

    @element_face_group_to_export.setter
    def element_face_group_to_export(self, value: 'list_with_selected_item.ListWithSelectedItem_CMSElementFaceGroup.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_CMSElementFaceGroup.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_CMSElementFaceGroup.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.ElementFaceGroupToExport = value

    @property
    def export_full_mesh(self) -> 'bool':
        """bool: 'ExportFullMesh' is the original name of this property."""

        temp = self.wrapped.ExportFullMesh

        if temp is None:
            return None

        return temp

    @export_full_mesh.setter
    def export_full_mesh(self, value: 'bool'):
        self.wrapped.ExportFullMesh = bool(value) if value else False

    @property
    def fe_export_format(self) -> 'enum_with_selected_value.EnumWithSelectedValue_FEExportFormat':
        """enum_with_selected_value.EnumWithSelectedValue_FEExportFormat: 'FEExportFormat' is the original name of this property."""

        temp = self.wrapped.FEExportFormat

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @fe_export_format.setter
    def fe_export_format(self, value: 'enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.FEExportFormat = value

    @property
    def force_unit(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        """list_with_selected_item.ListWithSelectedItem_Unit: 'ForceUnit' is the original name of this property."""

        temp = self.wrapped.ForceUnit

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_Unit)(temp) if temp is not None else None

    @force_unit.setter
    def force_unit(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.ForceUnit = value

    @property
    def include_all_fe_models(self) -> 'bool':
        """bool: 'IncludeAllFEModels' is the original name of this property."""

        temp = self.wrapped.IncludeAllFEModels

        if temp is None:
            return None

        return temp

    @include_all_fe_models.setter
    def include_all_fe_models(self, value: 'bool'):
        self.wrapped.IncludeAllFEModels = bool(value) if value else False

    @property
    def include_all_shafts(self) -> 'bool':
        """bool: 'IncludeAllShafts' is the original name of this property."""

        temp = self.wrapped.IncludeAllShafts

        if temp is None:
            return None

        return temp

    @include_all_shafts.setter
    def include_all_shafts(self, value: 'bool'):
        self.wrapped.IncludeAllShafts = bool(value) if value else False

    @property
    def include_original_fe_file(self) -> 'bool':
        """bool: 'IncludeOriginalFEFile' is the original name of this property."""

        temp = self.wrapped.IncludeOriginalFEFile

        if temp is None:
            return None

        return temp

    @include_original_fe_file.setter
    def include_original_fe_file(self, value: 'bool'):
        self.wrapped.IncludeOriginalFEFile = bool(value) if value else False

    @property
    def include_rigid_couplings_and_nodes_added_by_masta(self) -> 'bool':
        """bool: 'IncludeRigidCouplingsAndNodesAddedByMASTA' is the original name of this property."""

        temp = self.wrapped.IncludeRigidCouplingsAndNodesAddedByMASTA

        if temp is None:
            return None

        return temp

    @include_rigid_couplings_and_nodes_added_by_masta.setter
    def include_rigid_couplings_and_nodes_added_by_masta(self, value: 'bool'):
        self.wrapped.IncludeRigidCouplingsAndNodesAddedByMASTA = bool(value) if value else False

    @property
    def reference_speed(self) -> 'float':
        """float: 'ReferenceSpeed' is the original name of this property."""

        temp = self.wrapped.ReferenceSpeed

        if temp is None:
            return None

        return temp

    @reference_speed.setter
    def reference_speed(self, value: 'float'):
        self.wrapped.ReferenceSpeed = float(value) if value else 0.0

    @property
    def status_message_for_export(self) -> 'str':
        """str: 'StatusMessageForExport' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StatusMessageForExport

        if temp is None:
            return None

        return temp

    @property
    def use_single_speed(self) -> 'bool':
        """bool: 'UseSingleSpeed' is the original name of this property."""

        temp = self.wrapped.UseSingleSpeed

        if temp is None:
            return None

        return temp

    @use_single_speed.setter
    def use_single_speed(self, value: 'bool'):
        self.wrapped.UseSingleSpeed = bool(value) if value else False

    @property
    def analysis_options(self) -> '_5496.HarmonicAnalysisOptions':
        """HarmonicAnalysisOptions: 'AnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AnalysisOptions

        if temp is None:
            return None

        if _5496.HarmonicAnalysisOptions.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast analysis_options to HarmonicAnalysisOptions. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def eigenvalue_options(self) -> '_160.EigenvalueOptions':
        """EigenvalueOptions: 'EigenvalueOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EigenvalueOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def frequency_options(self) -> '_5484.FrequencyOptionsForHarmonicAnalysisResults':
        """FrequencyOptionsForHarmonicAnalysisResults: 'FrequencyOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FrequencyOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def reference_speed_options(self) -> '_5538.SpeedOptionsForHarmonicAnalysisResults':
        """SpeedOptionsForHarmonicAnalysisResults: 'ReferenceSpeedOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReferenceSpeedOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def export_to_folder(self, folder_path: 'str') -> 'List[str]':
        """ 'ExportToFolder' is the original name of this method.

        Args:
            folder_path (str)

        Returns:
            List[str]
        """

        folder_path = str(folder_path)
        return conversion.pn_to_mp_objects_in_list(self.wrapped.ExportToFolder(folder_path if folder_path else ''), str)
