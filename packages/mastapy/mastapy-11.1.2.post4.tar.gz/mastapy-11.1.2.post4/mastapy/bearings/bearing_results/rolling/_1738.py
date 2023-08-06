"""_1738.py

ISO14179SettingsPerBearingType
"""


from mastapy._internal.python_net import python_net_import
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings import _1661
from mastapy.bearings.bearing_results.rolling import _1736
from mastapy.utility import _1390

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_ISO14179_SETTINGS_PER_BEARING_TYPE = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'ISO14179SettingsPerBearingType')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO14179SettingsPerBearingType',)


class ISO14179SettingsPerBearingType(_1390.IndependentReportablePropertiesBase['ISO14179SettingsPerBearingType']):
    """ISO14179SettingsPerBearingType

    This is a mastapy class.
    """

    TYPE = _ISO14179_SETTINGS_PER_BEARING_TYPE

    def __init__(self, instance_to_wrap: 'ISO14179SettingsPerBearingType.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def iso14179_settings_database(self) -> 'str':
        """str: 'ISO14179SettingsDatabase' is the original name of this property."""

        temp = self.wrapped.ISO14179SettingsDatabase.SelectedItemName

        if temp is None:
            return None

        return temp

    @iso14179_settings_database.setter
    def iso14179_settings_database(self, value: 'str'):
        self.wrapped.ISO14179SettingsDatabase.SetSelectedItem(str(value) if value else '')

    @property
    def rolling_bearing_type(self) -> '_1661.RollingBearingType':
        """RollingBearingType: 'RollingBearingType' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RollingBearingType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1661.RollingBearingType)(value) if value is not None else None

    @property
    def iso14179_settings(self) -> '_1736.ISO14179Settings':
        """ISO14179Settings: 'ISO14179Settings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO14179Settings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
