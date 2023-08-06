"""_154.py

GeometryModellerSettings
"""


from typing import Optional

from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.utility import _1395
from mastapy._internal.python_net import python_net_import

_GEOMETRY_MODELLER_SETTINGS = python_net_import('SMT.MastaAPI.NodalAnalysis.GeometryModellerLink', 'GeometryModellerSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('GeometryModellerSettings',)


class GeometryModellerSettings(_1395.PerMachineSettings):
    """GeometryModellerSettings

    This is a mastapy class.
    """

    TYPE = _GEOMETRY_MODELLER_SETTINGS

    def __init__(self, instance_to_wrap: 'GeometryModellerSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def auto_detected_geometry_modeller_path(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'AutoDetectedGeometryModellerPath' is the original name of this property."""

        temp = self.wrapped.AutoDetectedGeometryModellerPath

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else None

    @auto_detected_geometry_modeller_path.setter
    def auto_detected_geometry_modeller_path(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.AutoDetectedGeometryModellerPath = value

    @property
    def disable_intel_mkl_internal_multithreading(self) -> 'bool':
        """bool: 'DisableIntelMKLInternalMultithreading' is the original name of this property."""

        temp = self.wrapped.DisableIntelMKLInternalMultithreading

        if temp is None:
            return None

        return temp

    @disable_intel_mkl_internal_multithreading.setter
    def disable_intel_mkl_internal_multithreading(self, value: 'bool'):
        self.wrapped.DisableIntelMKLInternalMultithreading = bool(value) if value else False

    @property
    def folder_path(self) -> 'str':
        """str: 'FolderPath' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FolderPath

        if temp is None:
            return None

        return temp

    @property
    def geometry_modeller_arguments(self) -> 'str':
        """str: 'GeometryModellerArguments' is the original name of this property."""

        temp = self.wrapped.GeometryModellerArguments

        if temp is None:
            return None

        return temp

    @geometry_modeller_arguments.setter
    def geometry_modeller_arguments(self, value: 'str'):
        self.wrapped.GeometryModellerArguments = str(value) if value else ''

    @property
    def hide_geometry_modeller_instead_of_closing(self) -> 'bool':
        """bool: 'HideGeometryModellerInsteadOfClosing' is the original name of this property."""

        temp = self.wrapped.HideGeometryModellerInsteadOfClosing

        if temp is None:
            return None

        return temp

    @hide_geometry_modeller_instead_of_closing.setter
    def hide_geometry_modeller_instead_of_closing(self, value: 'bool'):
        self.wrapped.HideGeometryModellerInsteadOfClosing = bool(value) if value else False

    @property
    def no_licence_for_geometry_modeller(self) -> 'str':
        """str: 'NoLicenceForGeometryModeller' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NoLicenceForGeometryModeller

        if temp is None:
            return None

        return temp

    @property
    def show_message_when_hiding_geometry_modeller(self) -> 'bool':
        """bool: 'ShowMessageWhenHidingGeometryModeller' is the original name of this property."""

        temp = self.wrapped.ShowMessageWhenHidingGeometryModeller

        if temp is None:
            return None

        return temp

    @show_message_when_hiding_geometry_modeller.setter
    def show_message_when_hiding_geometry_modeller(self, value: 'bool'):
        self.wrapped.ShowMessageWhenHidingGeometryModeller = bool(value) if value else False

    @property
    def use_auto_detected_geometry_modeller_path(self) -> 'bool':
        """bool: 'UseAutoDetectedGeometryModellerPath' is the original name of this property."""

        temp = self.wrapped.UseAutoDetectedGeometryModellerPath

        if temp is None:
            return None

        return temp

    @use_auto_detected_geometry_modeller_path.setter
    def use_auto_detected_geometry_modeller_path(self, value: 'bool'):
        self.wrapped.UseAutoDetectedGeometryModellerPath = bool(value) if value else False

    def launch_geometry_modeller(self, file_path: Optional['str'] = 'None'):
        """ 'LaunchGeometryModeller' is the original name of this method.

        Args:
            file_path (str, optional)
        """

        file_path = str(file_path)
        self.wrapped.LaunchGeometryModeller(file_path if file_path else '')

    def select_folder_path(self, path: 'str'):
        """ 'SelectFolderPath' is the original name of this method.

        Args:
            path (str)
        """

        path = str(path)
        self.wrapped.SelectFolderPath(path if path else '')
