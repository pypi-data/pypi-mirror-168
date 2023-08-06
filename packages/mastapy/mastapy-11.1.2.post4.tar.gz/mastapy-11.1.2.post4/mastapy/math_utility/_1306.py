"""_1306.py

CoordinateSystemEditor
"""


from typing import List

from PIL.Image import Image

from mastapy._internal import constructor, conversion, enum_with_selected_value_runtime
from mastapy.math_utility import (
    _1307, _1308, _1334, _1305
)
from mastapy._math.vector_3d import Vector3D
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_COORDINATE_SYSTEM_EDITOR = python_net_import('SMT.MastaAPI.MathUtility', 'CoordinateSystemEditor')


__docformat__ = 'restructuredtext en'
__all__ = ('CoordinateSystemEditor',)


class CoordinateSystemEditor(_0.APIBase):
    """CoordinateSystemEditor

    This is a mastapy class.
    """

    TYPE = _COORDINATE_SYSTEM_EDITOR

    def __init__(self, instance_to_wrap: 'CoordinateSystemEditor.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def containing_assembly_image(self) -> 'Image':
        """Image: 'ContainingAssemblyImage' is the original name of this property."""

        temp = self.wrapped.ContainingAssemblyImage

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @containing_assembly_image.setter
    def containing_assembly_image(self, value: 'Image'):
        value = value if value else None
        value = conversion.mp_to_pn_smt_bitmap(value)
        self.wrapped.ContainingAssemblyImage = value

    @property
    def containing_assembly_text(self) -> 'str':
        """str: 'ContainingAssemblyText' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContainingAssemblyText

        if temp is None:
            return None

        return temp

    @property
    def coordinate_system_for_rotation_axes(self) -> '_1307.CoordinateSystemForRotation':
        """CoordinateSystemForRotation: 'CoordinateSystemForRotationAxes' is the original name of this property."""

        temp = self.wrapped.CoordinateSystemForRotationAxes

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1307.CoordinateSystemForRotation)(value) if value is not None else None

    @coordinate_system_for_rotation_axes.setter
    def coordinate_system_for_rotation_axes(self, value: '_1307.CoordinateSystemForRotation'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CoordinateSystemForRotationAxes = value

    @property
    def coordinate_system_for_rotation_origin(self) -> '_1308.CoordinateSystemForRotationOrigin':
        """CoordinateSystemForRotationOrigin: 'CoordinateSystemForRotationOrigin' is the original name of this property."""

        temp = self.wrapped.CoordinateSystemForRotationOrigin

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1308.CoordinateSystemForRotationOrigin)(value) if value is not None else None

    @coordinate_system_for_rotation_origin.setter
    def coordinate_system_for_rotation_origin(self, value: '_1308.CoordinateSystemForRotationOrigin'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CoordinateSystemForRotationOrigin = value

    @property
    def has_modified_coordinate_system_rotation(self) -> 'bool':
        """bool: 'HasModifiedCoordinateSystemRotation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HasModifiedCoordinateSystemRotation

        if temp is None:
            return None

        return temp

    @property
    def has_modified_coordinate_system_translation(self) -> 'bool':
        """bool: 'HasModifiedCoordinateSystemTranslation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HasModifiedCoordinateSystemTranslation

        if temp is None:
            return None

        return temp

    @property
    def has_modified_coordinate_system(self) -> 'bool':
        """bool: 'HasModifiedCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HasModifiedCoordinateSystem

        if temp is None:
            return None

        return temp

    @property
    def has_rotation(self) -> 'bool':
        """bool: 'HasRotation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HasRotation

        if temp is None:
            return None

        return temp

    @property
    def has_translation(self) -> 'bool':
        """bool: 'HasTranslation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HasTranslation

        if temp is None:
            return None

        return temp

    @property
    def root_assembly_image(self) -> 'Image':
        """Image: 'RootAssemblyImage' is the original name of this property."""

        temp = self.wrapped.RootAssemblyImage

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @root_assembly_image.setter
    def root_assembly_image(self, value: 'Image'):
        value = value if value else None
        value = conversion.mp_to_pn_smt_bitmap(value)
        self.wrapped.RootAssemblyImage = value

    @property
    def root_assembly_text(self) -> 'str':
        """str: 'RootAssemblyText' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootAssemblyText

        if temp is None:
            return None

        return temp

    @property
    def rotation_angle(self) -> 'float':
        """float: 'RotationAngle' is the original name of this property."""

        temp = self.wrapped.RotationAngle

        if temp is None:
            return None

        return temp

    @rotation_angle.setter
    def rotation_angle(self, value: 'float'):
        self.wrapped.RotationAngle = float(value) if value else 0.0

    @property
    def rotation_axis(self) -> '_1334.RotationAxis':
        """RotationAxis: 'RotationAxis' is the original name of this property."""

        temp = self.wrapped.RotationAxis

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1334.RotationAxis)(value) if value is not None else None

    @rotation_axis.setter
    def rotation_axis(self, value: '_1334.RotationAxis'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RotationAxis = value

    @property
    def show_preview(self) -> 'bool':
        """bool: 'ShowPreview' is the original name of this property."""

        temp = self.wrapped.ShowPreview

        if temp is None:
            return None

        return temp

    @show_preview.setter
    def show_preview(self, value: 'bool'):
        self.wrapped.ShowPreview = bool(value) if value else False

    @property
    def coordinate_system(self) -> '_1305.CoordinateSystem3D':
        """CoordinateSystem3D: 'CoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CoordinateSystem

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def modified_coordinate_system_for_rotation(self) -> '_1305.CoordinateSystem3D':
        """CoordinateSystem3D: 'ModifiedCoordinateSystemForRotation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedCoordinateSystemForRotation

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def modified_coordinate_system_for_translation(self) -> '_1305.CoordinateSystem3D':
        """CoordinateSystem3D: 'ModifiedCoordinateSystemForTranslation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedCoordinateSystemForTranslation

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rotation_origin(self) -> 'Vector3D':
        """Vector3D: 'RotationOrigin' is the original name of this property."""

        temp = self.wrapped.RotationOrigin

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @rotation_origin.setter
    def rotation_origin(self, value: 'Vector3D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.RotationOrigin = value

    @property
    def specified_rotation_axis(self) -> 'Vector3D':
        """Vector3D: 'SpecifiedRotationAxis' is the original name of this property."""

        temp = self.wrapped.SpecifiedRotationAxis

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @specified_rotation_axis.setter
    def specified_rotation_axis(self, value: 'Vector3D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.SpecifiedRotationAxis = value

    @property
    def translation(self) -> 'Vector3D':
        """Vector3D: 'Translation' is the original name of this property."""

        temp = self.wrapped.Translation

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @translation.setter
    def translation(self, value: 'Vector3D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.Translation = value

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

    def align_to_world_coordinate_system(self):
        """ 'AlignToWorldCoordinateSystem' is the original name of this method."""

        self.wrapped.AlignToWorldCoordinateSystem()

    def apply_rotation(self):
        """ 'ApplyRotation' is the original name of this method."""

        self.wrapped.ApplyRotation()

    def cancel_pending_changes(self):
        """ 'CancelPendingChanges' is the original name of this method."""

        self.wrapped.CancelPendingChanges()

    def set_local_origin_to_world_origin(self):
        """ 'SetLocalOriginToWorldOrigin' is the original name of this method."""

        self.wrapped.SetLocalOriginToWorldOrigin()

    def update_origin(self):
        """ 'UpdateOrigin' is the original name of this method."""

        self.wrapped.UpdateOrigin()

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
