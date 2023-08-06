"""_45.py

AnalysisSettings
"""


from mastapy._internal.python_net import python_net_import
from mastapy._internal import constructor
from mastapy.nodal_analysis import _47
from mastapy.utility import _1395

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_ANALYSIS_SETTINGS = python_net_import('SMT.MastaAPI.NodalAnalysis', 'AnalysisSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('AnalysisSettings',)


class AnalysisSettings(_1395.PerMachineSettings):
    """AnalysisSettings

    This is a mastapy class.
    """

    TYPE = _ANALYSIS_SETTINGS

    def __init__(self, instance_to_wrap: 'AnalysisSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def analysis_settings_database(self) -> 'str':
        """str: 'AnalysisSettingsDatabase' is the original name of this property."""

        temp = self.wrapped.AnalysisSettingsDatabase.SelectedItemName

        if temp is None:
            return None

        return temp

    @analysis_settings_database.setter
    def analysis_settings_database(self, value: 'str'):
        self.wrapped.AnalysisSettingsDatabase.SetSelectedItem(str(value) if value else '')

    @property
    def analysis_settings_items(self) -> '_47.AnalysisSettingsObjects':
        """AnalysisSettingsObjects: 'AnalysisSettingsItems' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AnalysisSettingsItems

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
