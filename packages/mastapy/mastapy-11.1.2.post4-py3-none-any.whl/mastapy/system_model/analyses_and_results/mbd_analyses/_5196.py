"""_5196.py

MBDAnalysisOptions
"""


from mastapy.system_model.analyses_and_results.mbd_analyses import (
    _5118, _5121, _5173, _5218,
    _5180, _5181, _5197
)
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import overridable, enum_with_selected_value, list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.part_model import _2222
from mastapy.system_model.analyses_and_results.mbd_analyses.external_interfaces import _5262
from mastapy.system_model.analyses_and_results.modal_analyses import _4371
from mastapy.nodal_analysis import _84
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_MBD_ANALYSIS_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'MBDAnalysisOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('MBDAnalysisOptions',)


class MBDAnalysisOptions(_0.APIBase):
    """MBDAnalysisOptions

    This is a mastapy class.
    """

    TYPE = _MBD_ANALYSIS_OPTIONS

    def __init__(self, instance_to_wrap: 'MBDAnalysisOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def analysis_type(self) -> '_5118.AnalysisTypes':
        """AnalysisTypes: 'AnalysisType' is the original name of this property."""

        temp = self.wrapped.AnalysisType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_5118.AnalysisTypes)(value) if value is not None else None

    @analysis_type.setter
    def analysis_type(self, value: '_5118.AnalysisTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AnalysisType = value

    @property
    def bearing_rayleigh_damping_beta(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'BearingRayleighDampingBeta' is the original name of this property."""

        temp = self.wrapped.BearingRayleighDampingBeta

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @bearing_rayleigh_damping_beta.setter
    def bearing_rayleigh_damping_beta(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.BearingRayleighDampingBeta = value

    @property
    def bearing_stiffness_model(self) -> 'enum_with_selected_value.EnumWithSelectedValue_BearingStiffnessModel':
        """enum_with_selected_value.EnumWithSelectedValue_BearingStiffnessModel: 'BearingStiffnessModel' is the original name of this property."""

        temp = self.wrapped.BearingStiffnessModel

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_BearingStiffnessModel.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @bearing_stiffness_model.setter
    def bearing_stiffness_model(self, value: 'enum_with_selected_value.EnumWithSelectedValue_BearingStiffnessModel.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_BearingStiffnessModel.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.BearingStiffnessModel = value

    @property
    def belt_rayleigh_damping_beta(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'BeltRayleighDampingBeta' is the original name of this property."""

        temp = self.wrapped.BeltRayleighDampingBeta

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @belt_rayleigh_damping_beta.setter
    def belt_rayleigh_damping_beta(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.BeltRayleighDampingBeta = value

    @property
    def create_inertia_adjusted_static_load_cases(self) -> 'bool':
        """bool: 'CreateInertiaAdjustedStaticLoadCases' is the original name of this property."""

        temp = self.wrapped.CreateInertiaAdjustedStaticLoadCases

        if temp is None:
            return None

        return temp

    @create_inertia_adjusted_static_load_cases.setter
    def create_inertia_adjusted_static_load_cases(self, value: 'bool'):
        self.wrapped.CreateInertiaAdjustedStaticLoadCases = bool(value) if value else False

    @property
    def filter_cut_off(self) -> 'float':
        """float: 'FilterCutOff' is the original name of this property."""

        temp = self.wrapped.FilterCutOff

        if temp is None:
            return None

        return temp

    @filter_cut_off.setter
    def filter_cut_off(self, value: 'float'):
        self.wrapped.FilterCutOff = float(value) if value else 0.0

    @property
    def gear_mesh_rayleigh_damping_beta(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'GearMeshRayleighDampingBeta' is the original name of this property."""

        temp = self.wrapped.GearMeshRayleighDampingBeta

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @gear_mesh_rayleigh_damping_beta.setter
    def gear_mesh_rayleigh_damping_beta(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.GearMeshRayleighDampingBeta = value

    @property
    def gear_mesh_stiffness_model(self) -> 'enum_with_selected_value.EnumWithSelectedValue_GearMeshStiffnessModel':
        """enum_with_selected_value.EnumWithSelectedValue_GearMeshStiffnessModel: 'GearMeshStiffnessModel' is the original name of this property."""

        temp = self.wrapped.GearMeshStiffnessModel

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_GearMeshStiffnessModel.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @gear_mesh_stiffness_model.setter
    def gear_mesh_stiffness_model(self, value: 'enum_with_selected_value.EnumWithSelectedValue_GearMeshStiffnessModel.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_GearMeshStiffnessModel.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.GearMeshStiffnessModel = value

    @property
    def include_gear_backlash(self) -> 'bool':
        """bool: 'IncludeGearBacklash' is the original name of this property."""

        temp = self.wrapped.IncludeGearBacklash

        if temp is None:
            return None

        return temp

    @include_gear_backlash.setter
    def include_gear_backlash(self, value: 'bool'):
        self.wrapped.IncludeGearBacklash = bool(value) if value else False

    @property
    def include_microgeometry(self) -> 'bool':
        """bool: 'IncludeMicrogeometry' is the original name of this property."""

        temp = self.wrapped.IncludeMicrogeometry

        if temp is None:
            return None

        return temp

    @include_microgeometry.setter
    def include_microgeometry(self, value: 'bool'):
        self.wrapped.IncludeMicrogeometry = bool(value) if value else False

    @property
    def include_shaft_and_housing_flexibilities(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption':
        """enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption: 'IncludeShaftAndHousingFlexibilities' is the original name of this property."""

        temp = self.wrapped.IncludeShaftAndHousingFlexibilities

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @include_shaft_and_housing_flexibilities.setter
    def include_shaft_and_housing_flexibilities(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.IncludeShaftAndHousingFlexibilities = value

    @property
    def interference_fit_rayleigh_damping_beta(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'InterferenceFitRayleighDampingBeta' is the original name of this property."""

        temp = self.wrapped.InterferenceFitRayleighDampingBeta

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @interference_fit_rayleigh_damping_beta.setter
    def interference_fit_rayleigh_damping_beta(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.InterferenceFitRayleighDampingBeta = value

    @property
    def load_case_for_component_speed_ratios(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'LoadCaseForComponentSpeedRatios' is the original name of this property."""

        temp = self.wrapped.LoadCaseForComponentSpeedRatios

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else None

    @load_case_for_component_speed_ratios.setter
    def load_case_for_component_speed_ratios(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.LoadCaseForComponentSpeedRatios = value

    @property
    def load_case_for_linearised_bearing_stiffness(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'LoadCaseForLinearisedBearingStiffness' is the original name of this property."""

        temp = self.wrapped.LoadCaseForLinearisedBearingStiffness

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else None

    @load_case_for_linearised_bearing_stiffness.setter
    def load_case_for_linearised_bearing_stiffness(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.LoadCaseForLinearisedBearingStiffness = value

    @property
    def maximum_angular_jerk(self) -> 'float':
        """float: 'MaximumAngularJerk' is the original name of this property."""

        temp = self.wrapped.MaximumAngularJerk

        if temp is None:
            return None

        return temp

    @maximum_angular_jerk.setter
    def maximum_angular_jerk(self, value: 'float'):
        self.wrapped.MaximumAngularJerk = float(value) if value else 0.0

    @property
    def maximum_frequency_in_signal(self) -> 'float':
        """float: 'MaximumFrequencyInSignal' is the original name of this property."""

        temp = self.wrapped.MaximumFrequencyInSignal

        if temp is None:
            return None

        return temp

    @maximum_frequency_in_signal.setter
    def maximum_frequency_in_signal(self, value: 'float'):
        self.wrapped.MaximumFrequencyInSignal = float(value) if value else 0.0

    @property
    def method_to_define_period(self) -> '_5180.InertiaAdjustedLoadCasePeriodMethod':
        """InertiaAdjustedLoadCasePeriodMethod: 'MethodToDefinePeriod' is the original name of this property."""

        temp = self.wrapped.MethodToDefinePeriod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_5180.InertiaAdjustedLoadCasePeriodMethod)(value) if value is not None else None

    @method_to_define_period.setter
    def method_to_define_period(self, value: '_5180.InertiaAdjustedLoadCasePeriodMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MethodToDefinePeriod = value

    @property
    def number_of_static_load_cases(self) -> 'int':
        """int: 'NumberOfStaticLoadCases' is the original name of this property."""

        temp = self.wrapped.NumberOfStaticLoadCases

        if temp is None:
            return None

        return temp

    @number_of_static_load_cases.setter
    def number_of_static_load_cases(self, value: 'int'):
        self.wrapped.NumberOfStaticLoadCases = int(value) if value else 0

    @property
    def power_load_rotation(self) -> 'float':
        """float: 'PowerLoadRotation' is the original name of this property."""

        temp = self.wrapped.PowerLoadRotation

        if temp is None:
            return None

        return temp

    @power_load_rotation.setter
    def power_load_rotation(self, value: 'float'):
        self.wrapped.PowerLoadRotation = float(value) if value else 0.0

    @property
    def reference_power_load_to_define_period(self) -> 'list_with_selected_item.ListWithSelectedItem_PowerLoad':
        """list_with_selected_item.ListWithSelectedItem_PowerLoad: 'ReferencePowerLoadToDefinePeriod' is the original name of this property."""

        temp = self.wrapped.ReferencePowerLoadToDefinePeriod

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_PowerLoad)(temp) if temp is not None else None

    @reference_power_load_to_define_period.setter
    def reference_power_load_to_define_period(self, value: 'list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_PowerLoad.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.ReferencePowerLoadToDefinePeriod = value

    @property
    def sample_length(self) -> 'float':
        """float: 'SampleLength' is the original name of this property."""

        temp = self.wrapped.SampleLength

        if temp is None:
            return None

        return temp

    @sample_length.setter
    def sample_length(self, value: 'float'):
        self.wrapped.SampleLength = float(value) if value else 0.0

    @property
    def shaft_and_housing_rayleigh_damping_beta(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ShaftAndHousingRayleighDampingBeta' is the original name of this property."""

        temp = self.wrapped.ShaftAndHousingRayleighDampingBeta

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @shaft_and_housing_rayleigh_damping_beta.setter
    def shaft_and_housing_rayleigh_damping_beta(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ShaftAndHousingRayleighDampingBeta = value

    @property
    def spline_rayleigh_damping_beta(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'SplineRayleighDampingBeta' is the original name of this property."""

        temp = self.wrapped.SplineRayleighDampingBeta

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @spline_rayleigh_damping_beta.setter
    def spline_rayleigh_damping_beta(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.SplineRayleighDampingBeta = value

    @property
    def start_time(self) -> 'float':
        """float: 'StartTime' is the original name of this property."""

        temp = self.wrapped.StartTime

        if temp is None:
            return None

        return temp

    @start_time.setter
    def start_time(self, value: 'float'):
        self.wrapped.StartTime = float(value) if value else 0.0

    @property
    def start_at_zero_angle(self) -> 'bool':
        """bool: 'StartAtZeroAngle' is the original name of this property."""

        temp = self.wrapped.StartAtZeroAngle

        if temp is None:
            return None

        return temp

    @start_at_zero_angle.setter
    def start_at_zero_angle(self, value: 'bool'):
        self.wrapped.StartAtZeroAngle = bool(value) if value else False

    @property
    def static_load_cases_to_create(self) -> '_5181.InertiaAdjustedLoadCaseResultsToCreate':
        """InertiaAdjustedLoadCaseResultsToCreate: 'StaticLoadCasesToCreate' is the original name of this property."""

        temp = self.wrapped.StaticLoadCasesToCreate

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_5181.InertiaAdjustedLoadCaseResultsToCreate)(value) if value is not None else None

    @static_load_cases_to_create.setter
    def static_load_cases_to_create(self, value: '_5181.InertiaAdjustedLoadCaseResultsToCreate'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.StaticLoadCasesToCreate = value

    @property
    def use_load_sensitive_stiffness(self) -> 'bool':
        """bool: 'UseLoadSensitiveStiffness' is the original name of this property."""

        temp = self.wrapped.UseLoadSensitiveStiffness

        if temp is None:
            return None

        return temp

    @use_load_sensitive_stiffness.setter
    def use_load_sensitive_stiffness(self, value: 'bool'):
        self.wrapped.UseLoadSensitiveStiffness = bool(value) if value else False

    @property
    def use_temperature_model(self) -> 'bool':
        """bool: 'UseTemperatureModel' is the original name of this property."""

        temp = self.wrapped.UseTemperatureModel

        if temp is None:
            return None

        return temp

    @use_temperature_model.setter
    def use_temperature_model(self, value: 'bool'):
        self.wrapped.UseTemperatureModel = bool(value) if value else False

    @property
    def external_interface_options(self) -> '_5262.DynamicExternalInterfaceOptions':
        """DynamicExternalInterfaceOptions: 'ExternalInterfaceOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExternalInterfaceOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def frequency_response_options(self) -> '_4371.FrequencyResponseAnalysisOptions':
        """FrequencyResponseAnalysisOptions: 'FrequencyResponseOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FrequencyResponseOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def run_up_analysis_options(self) -> '_5197.MBDRunUpAnalysisOptions':
        """MBDRunUpAnalysisOptions: 'RunUpAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RunUpAnalysisOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def transient_solver_options(self) -> '_84.TransientSolverOptions':
        """TransientSolverOptions: 'TransientSolverOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransientSolverOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
