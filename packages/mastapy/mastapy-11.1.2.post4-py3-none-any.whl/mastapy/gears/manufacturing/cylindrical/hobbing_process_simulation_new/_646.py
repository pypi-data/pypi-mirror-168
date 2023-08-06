"""_646.py

ProcessCalculation
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _651, _638, _665
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PROCESS_CALCULATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'ProcessCalculation')


__docformat__ = 'restructuredtext en'
__all__ = ('ProcessCalculation',)


class ProcessCalculation(_0.APIBase):
    """ProcessCalculation

    This is a mastapy class.
    """

    TYPE = _PROCESS_CALCULATION

    def __init__(self, instance_to_wrap: 'ProcessCalculation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def centre_distance(self) -> 'float':
        """float: 'CentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CentreDistance

        if temp is None:
            return None

        return temp

    @property
    def centre_distance_parabolic_parameter(self) -> 'float':
        """float: 'CentreDistanceParabolicParameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CentreDistanceParabolicParameter

        if temp is None:
            return None

        return temp

    @property
    def cutter_gear_rotation_ratio(self) -> 'float':
        """float: 'CutterGearRotationRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CutterGearRotationRatio

        if temp is None:
            return None

        return temp

    @property
    def cutter_minimum_effective_length(self) -> 'float':
        """float: 'CutterMinimumEffectiveLength' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CutterMinimumEffectiveLength

        if temp is None:
            return None

        return temp

    @property
    def idle_distance(self) -> 'float':
        """float: 'IdleDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IdleDistance

        if temp is None:
            return None

        return temp

    @property
    def minimum_allowable_neck_width(self) -> 'float':
        """float: 'MinimumAllowableNeckWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumAllowableNeckWidth

        if temp is None:
            return None

        return temp

    @property
    def neck_width(self) -> 'float':
        """float: 'NeckWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NeckWidth

        if temp is None:
            return None

        return temp

    @property
    def setting_angle(self) -> 'float':
        """float: 'SettingAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SettingAngle

        if temp is None:
            return None

        return temp

    @property
    def shaft_angle(self) -> 'float':
        """float: 'ShaftAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftAngle

        if temp is None:
            return None

        return temp

    @property
    def shaft_mark_length(self) -> 'float':
        """float: 'ShaftMarkLength' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftMarkLength

        if temp is None:
            return None

        return temp

    @property
    def inputs(self) -> '_651.ProcessSimulationInput':
        """ProcessSimulationInput: 'Inputs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Inputs

        if temp is None:
            return None

        if _651.ProcessSimulationInput.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inputs to ProcessSimulationInput. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inputs_of_type_hobbing_process_simulation_input(self) -> '_638.HobbingProcessSimulationInput':
        """HobbingProcessSimulationInput: 'Inputs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Inputs

        if temp is None:
            return None

        if _638.HobbingProcessSimulationInput.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inputs to HobbingProcessSimulationInput. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inputs_of_type_worm_grinding_process_simulation_input(self) -> '_665.WormGrindingProcessSimulationInput':
        """WormGrindingProcessSimulationInput: 'Inputs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Inputs

        if temp is None:
            return None

        if _665.WormGrindingProcessSimulationInput.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inputs to WormGrindingProcessSimulationInput. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def report_names(self) -> 'List[str]':
        """List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReportNames

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)
        return value

    def calculate_idle_distance(self):
        """ 'CalculateIdleDistance' is the original name of this method."""

        self.wrapped.CalculateIdleDistance()

    def calculate_left_modifications(self):
        """ 'CalculateLeftModifications' is the original name of this method."""

        self.wrapped.CalculateLeftModifications()

    def calculate_left_total_modifications(self):
        """ 'CalculateLeftTotalModifications' is the original name of this method."""

        self.wrapped.CalculateLeftTotalModifications()

    def calculate_maximum_shaft_mark_length(self):
        """ 'CalculateMaximumShaftMarkLength' is the original name of this method."""

        self.wrapped.CalculateMaximumShaftMarkLength()

    def calculate_modifications(self):
        """ 'CalculateModifications' is the original name of this method."""

        self.wrapped.CalculateModifications()

    def calculate_right_modifications(self):
        """ 'CalculateRightModifications' is the original name of this method."""

        self.wrapped.CalculateRightModifications()

    def calculate_right_total_modifications(self):
        """ 'CalculateRightTotalModifications' is the original name of this method."""

        self.wrapped.CalculateRightTotalModifications()

    def calculate_shaft_mark(self):
        """ 'CalculateShaftMark' is the original name of this method."""

        self.wrapped.CalculateShaftMark()

    def output_default_report_to(self, file_path: 'str'):
        """ 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else '')

    def get_default_report_with_encoded_images(self) -> 'str':
        """ 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        """ 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else '')

    def output_active_report_as_text_to(self, file_path: 'str'):
        """ 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else '')

    def get_active_report_with_encoded_images(self) -> 'str':
        """ 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else '', file_path if file_path else '')

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        """ 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        """

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else '')
        return method_result
