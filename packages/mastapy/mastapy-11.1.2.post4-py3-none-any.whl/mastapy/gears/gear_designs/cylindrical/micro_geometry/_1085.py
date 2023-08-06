"""_1085.py

SingleCylindricalGearTriangularEndModification
"""


from typing import List

from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _987
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SINGLE_CYLINDRICAL_GEAR_TRIANGULAR_END_MODIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'SingleCylindricalGearTriangularEndModification')


__docformat__ = 'restructuredtext en'
__all__ = ('SingleCylindricalGearTriangularEndModification',)


class SingleCylindricalGearTriangularEndModification(_0.APIBase):
    """SingleCylindricalGearTriangularEndModification

    This is a mastapy class.
    """

    TYPE = _SINGLE_CYLINDRICAL_GEAR_TRIANGULAR_END_MODIFICATION

    def __init__(self, instance_to_wrap: 'SingleCylindricalGearTriangularEndModification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angle(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'Angle' is the original name of this property."""

        temp = self.wrapped.Angle

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @angle.setter
    def angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.Angle = value

    @property
    def face_width_position(self) -> 'float':
        """float: 'FaceWidthPosition' is the original name of this property."""

        temp = self.wrapped.FaceWidthPosition

        if temp is None:
            return None

        return temp

    @face_width_position.setter
    def face_width_position(self, value: 'float'):
        self.wrapped.FaceWidthPosition = float(value) if value else 0.0

    @property
    def face_width_position_factor(self) -> 'float':
        """float: 'FaceWidthPositionFactor' is the original name of this property."""

        temp = self.wrapped.FaceWidthPositionFactor

        if temp is None:
            return None

        return temp

    @face_width_position_factor.setter
    def face_width_position_factor(self, value: 'float'):
        self.wrapped.FaceWidthPositionFactor = float(value) if value else 0.0

    @property
    def profile_evaluation_diameter(self) -> 'float':
        """float: 'ProfileEvaluationDiameter' is the original name of this property."""

        temp = self.wrapped.ProfileEvaluationDiameter

        if temp is None:
            return None

        return temp

    @profile_evaluation_diameter.setter
    def profile_evaluation_diameter(self, value: 'float'):
        self.wrapped.ProfileEvaluationDiameter = float(value) if value else 0.0

    @property
    def profile_evaluation_factor(self) -> 'float':
        """float: 'ProfileEvaluationFactor' is the original name of this property."""

        temp = self.wrapped.ProfileEvaluationFactor

        if temp is None:
            return None

        return temp

    @profile_evaluation_factor.setter
    def profile_evaluation_factor(self, value: 'float'):
        self.wrapped.ProfileEvaluationFactor = float(value) if value else 0.0

    @property
    def profile_evaluation_radius(self) -> 'float':
        """float: 'ProfileEvaluationRadius' is the original name of this property."""

        temp = self.wrapped.ProfileEvaluationRadius

        if temp is None:
            return None

        return temp

    @profile_evaluation_radius.setter
    def profile_evaluation_radius(self, value: 'float'):
        self.wrapped.ProfileEvaluationRadius = float(value) if value else 0.0

    @property
    def profile_evaluation_roll_angle(self) -> 'float':
        """float: 'ProfileEvaluationRollAngle' is the original name of this property."""

        temp = self.wrapped.ProfileEvaluationRollAngle

        if temp is None:
            return None

        return temp

    @profile_evaluation_roll_angle.setter
    def profile_evaluation_roll_angle(self, value: 'float'):
        self.wrapped.ProfileEvaluationRollAngle = float(value) if value else 0.0

    @property
    def profile_evaluation_roll_distance(self) -> 'float':
        """float: 'ProfileEvaluationRollDistance' is the original name of this property."""

        temp = self.wrapped.ProfileEvaluationRollDistance

        if temp is None:
            return None

        return temp

    @profile_evaluation_roll_distance.setter
    def profile_evaluation_roll_distance(self, value: 'float'):
        self.wrapped.ProfileEvaluationRollDistance = float(value) if value else 0.0

    @property
    def profile_start_diameter(self) -> 'float':
        """float: 'ProfileStartDiameter' is the original name of this property."""

        temp = self.wrapped.ProfileStartDiameter

        if temp is None:
            return None

        return temp

    @profile_start_diameter.setter
    def profile_start_diameter(self, value: 'float'):
        self.wrapped.ProfileStartDiameter = float(value) if value else 0.0

    @property
    def profile_start_factor(self) -> 'float':
        """float: 'ProfileStartFactor' is the original name of this property."""

        temp = self.wrapped.ProfileStartFactor

        if temp is None:
            return None

        return temp

    @profile_start_factor.setter
    def profile_start_factor(self, value: 'float'):
        self.wrapped.ProfileStartFactor = float(value) if value else 0.0

    @property
    def profile_start_radius(self) -> 'float':
        """float: 'ProfileStartRadius' is the original name of this property."""

        temp = self.wrapped.ProfileStartRadius

        if temp is None:
            return None

        return temp

    @profile_start_radius.setter
    def profile_start_radius(self, value: 'float'):
        self.wrapped.ProfileStartRadius = float(value) if value else 0.0

    @property
    def profile_start_roll_angle(self) -> 'float':
        """float: 'ProfileStartRollAngle' is the original name of this property."""

        temp = self.wrapped.ProfileStartRollAngle

        if temp is None:
            return None

        return temp

    @profile_start_roll_angle.setter
    def profile_start_roll_angle(self, value: 'float'):
        self.wrapped.ProfileStartRollAngle = float(value) if value else 0.0

    @property
    def profile_start_roll_distance(self) -> 'float':
        """float: 'ProfileStartRollDistance' is the original name of this property."""

        temp = self.wrapped.ProfileStartRollDistance

        if temp is None:
            return None

        return temp

    @profile_start_roll_distance.setter
    def profile_start_roll_distance(self, value: 'float'):
        self.wrapped.ProfileStartRollDistance = float(value) if value else 0.0

    @property
    def relief(self) -> 'float':
        """float: 'Relief' is the original name of this property."""

        temp = self.wrapped.Relief

        if temp is None:
            return None

        return temp

    @relief.setter
    def relief(self, value: 'float'):
        self.wrapped.Relief = float(value) if value else 0.0

    @property
    def profile_evaluation(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'ProfileEvaluation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileEvaluation

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def profile_start(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'ProfileStart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileStart

        if temp is None:
            return None

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
