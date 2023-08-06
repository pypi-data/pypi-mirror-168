"""_5262.py

DynamicExternalInterfaceOptions
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5182
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DYNAMIC_EXTERNAL_INTERFACE_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.ExternalInterfaces', 'DynamicExternalInterfaceOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicExternalInterfaceOptions',)


class DynamicExternalInterfaceOptions(_0.APIBase):
    """DynamicExternalInterfaceOptions

    This is a mastapy class.
    """

    TYPE = _DYNAMIC_EXTERNAL_INTERFACE_OPTIONS

    def __init__(self, instance_to_wrap: 'DynamicExternalInterfaceOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def generate_load_case(self) -> 'bool':
        """bool: 'GenerateLoadCase' is the original name of this property."""

        temp = self.wrapped.GenerateLoadCase

        if temp is None:
            return None

        return temp

    @generate_load_case.setter
    def generate_load_case(self, value: 'bool'):
        self.wrapped.GenerateLoadCase = bool(value) if value else False

    @property
    def input_signal_filter_level(self) -> '_5182.InputSignalFilterLevel':
        """InputSignalFilterLevel: 'InputSignalFilterLevel' is the original name of this property."""

        temp = self.wrapped.InputSignalFilterLevel

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_5182.InputSignalFilterLevel)(value) if value is not None else None

    @input_signal_filter_level.setter
    def input_signal_filter_level(self, value: '_5182.InputSignalFilterLevel'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.InputSignalFilterLevel = value

    @property
    def path_of_saved_file(self) -> 'str':
        """str: 'PathOfSavedFile' is the original name of this property."""

        temp = self.wrapped.PathOfSavedFile

        if temp is None:
            return None

        return temp

    @path_of_saved_file.setter
    def path_of_saved_file(self, value: 'str'):
        self.wrapped.PathOfSavedFile = str(value) if value else ''

    @property
    def sample_time(self) -> 'float':
        """float: 'SampleTime' is the original name of this property."""

        temp = self.wrapped.SampleTime

        if temp is None:
            return None

        return temp

    @sample_time.setter
    def sample_time(self, value: 'float'):
        self.wrapped.SampleTime = float(value) if value else 0.0

    @property
    def save_results(self) -> 'bool':
        """bool: 'SaveResults' is the original name of this property."""

        temp = self.wrapped.SaveResults

        if temp is None:
            return None

        return temp

    @save_results.setter
    def save_results(self, value: 'bool'):
        self.wrapped.SaveResults = bool(value) if value else False
