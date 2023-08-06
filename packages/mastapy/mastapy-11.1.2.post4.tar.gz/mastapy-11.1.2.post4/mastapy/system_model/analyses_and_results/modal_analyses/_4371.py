"""_4371.py

FrequencyResponseAnalysisOptions
"""


from mastapy._internal import constructor
from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.analyses_and_results.analysis_cases import _7262
from mastapy.system_model.analyses_and_results.static_loads import _6527
from mastapy._internal.python_net import python_net_import

_FREQUENCY_RESPONSE_ANALYSIS_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'FrequencyResponseAnalysisOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('FrequencyResponseAnalysisOptions',)


class FrequencyResponseAnalysisOptions(_7262.AbstractAnalysisOptions['_6527.LoadCase']):
    """FrequencyResponseAnalysisOptions

    This is a mastapy class.
    """

    TYPE = _FREQUENCY_RESPONSE_ANALYSIS_OPTIONS

    def __init__(self, instance_to_wrap: 'FrequencyResponseAnalysisOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_gear_mesh_harmonics(self) -> 'int':
        """int: 'NumberOfGearMeshHarmonics' is the original name of this property."""

        temp = self.wrapped.NumberOfGearMeshHarmonics

        if temp is None:
            return None

        return temp

    @number_of_gear_mesh_harmonics.setter
    def number_of_gear_mesh_harmonics(self, value: 'int'):
        self.wrapped.NumberOfGearMeshHarmonics = int(value) if value else 0

    @property
    def number_of_input_shaft_harmonics(self) -> 'int':
        """int: 'NumberOfInputShaftHarmonics' is the original name of this property."""

        temp = self.wrapped.NumberOfInputShaftHarmonics

        if temp is None:
            return None

        return temp

    @number_of_input_shaft_harmonics.setter
    def number_of_input_shaft_harmonics(self, value: 'int'):
        self.wrapped.NumberOfInputShaftHarmonics = int(value) if value else 0

    @property
    def number_of_shaft_harmonics(self) -> 'int':
        """int: 'NumberOfShaftHarmonics' is the original name of this property."""

        temp = self.wrapped.NumberOfShaftHarmonics

        if temp is None:
            return None

        return temp

    @number_of_shaft_harmonics.setter
    def number_of_shaft_harmonics(self, value: 'int'):
        self.wrapped.NumberOfShaftHarmonics = int(value) if value else 0

    @property
    def reference_power_load(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'ReferencePowerLoad' is the original name of this property."""

        temp = self.wrapped.ReferencePowerLoad

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else None

    @reference_power_load.setter
    def reference_power_load(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.ReferencePowerLoad = value

    @property
    def threshold_for_significant_kinetic_energy(self) -> 'float':
        """float: 'ThresholdForSignificantKineticEnergy' is the original name of this property."""

        temp = self.wrapped.ThresholdForSignificantKineticEnergy

        if temp is None:
            return None

        return temp

    @threshold_for_significant_kinetic_energy.setter
    def threshold_for_significant_kinetic_energy(self, value: 'float'):
        self.wrapped.ThresholdForSignificantKineticEnergy = float(value) if value else 0.0

    @property
    def threshold_for_significant_strain_energy(self) -> 'float':
        """float: 'ThresholdForSignificantStrainEnergy' is the original name of this property."""

        temp = self.wrapped.ThresholdForSignificantStrainEnergy

        if temp is None:
            return None

        return temp

    @threshold_for_significant_strain_energy.setter
    def threshold_for_significant_strain_energy(self, value: 'float'):
        self.wrapped.ThresholdForSignificantStrainEnergy = float(value) if value else 0.0
