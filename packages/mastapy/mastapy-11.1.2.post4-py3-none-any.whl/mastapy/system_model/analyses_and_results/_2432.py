"""_2432.py

TESetUpForDynamicAnalysisOptions
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_TE_SET_UP_FOR_DYNAMIC_ANALYSIS_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'TESetUpForDynamicAnalysisOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('TESetUpForDynamicAnalysisOptions',)


class TESetUpForDynamicAnalysisOptions(_0.APIBase):
    """TESetUpForDynamicAnalysisOptions

    This is a mastapy class.
    """

    TYPE = _TE_SET_UP_FOR_DYNAMIC_ANALYSIS_OPTIONS

    def __init__(self, instance_to_wrap: 'TESetUpForDynamicAnalysisOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def include_misalignment_excitation(self) -> 'bool':
        """bool: 'IncludeMisalignmentExcitation' is the original name of this property."""

        temp = self.wrapped.IncludeMisalignmentExcitation

        if temp is None:
            return None

        return temp

    @include_misalignment_excitation.setter
    def include_misalignment_excitation(self, value: 'bool'):
        self.wrapped.IncludeMisalignmentExcitation = bool(value) if value else False

    @property
    def use_data_logger_for_advanced_system_deflection_single_tooth_pass_harmonic_excitation_type_options(self) -> 'bool':
        """bool: 'UseDataLoggerForAdvancedSystemDeflectionSingleToothPassHarmonicExcitationTypeOptions' is the original name of this property."""

        temp = self.wrapped.UseDataLoggerForAdvancedSystemDeflectionSingleToothPassHarmonicExcitationTypeOptions

        if temp is None:
            return None

        return temp

    @use_data_logger_for_advanced_system_deflection_single_tooth_pass_harmonic_excitation_type_options.setter
    def use_data_logger_for_advanced_system_deflection_single_tooth_pass_harmonic_excitation_type_options(self, value: 'bool'):
        self.wrapped.UseDataLoggerForAdvancedSystemDeflectionSingleToothPassHarmonicExcitationTypeOptions = bool(value) if value else False
