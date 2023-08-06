"""_4369.py

FEPartModalAnalysis
"""


from typing import List

from mastapy.system_model.part_model import _2203
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6611
from mastapy.system_model.analyses_and_results.system_deflections import _2501
from mastapy.nodal_analysis.component_mode_synthesis import _210
from mastapy.system_model.analyses_and_results.modal_analyses import _4314
from mastapy._internal.python_net import python_net_import

_FE_PART_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'FEPartModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartModalAnalysis',)


class FEPartModalAnalysis(_4314.AbstractShaftOrHousingModalAnalysis):
    """FEPartModalAnalysis

    This is a mastapy class.
    """

    TYPE = _FE_PART_MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'FEPartModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2203.FEPart':
        """FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6611.FEPartLoadCase':
        """FEPartLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2501.FEPartSystemDeflection':
        """FEPartSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def modal_full_fe_results(self) -> 'List[_210.ModalCMSResults]':
        """List[ModalCMSResults]: 'ModalFullFEResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModalFullFEResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planetaries(self) -> 'List[FEPartModalAnalysis]':
        """List[FEPartModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def calculate_all_strain_and_kinetic_energies(self):
        """ 'CalculateAllStrainAndKineticEnergies' is the original name of this method."""

        self.wrapped.CalculateAllStrainAndKineticEnergies()

    def calculate_mode_shapes(self):
        """ 'CalculateModeShapes' is the original name of this method."""

        self.wrapped.CalculateModeShapes()

    def calculate_selected_strain_and_kinetic_energy(self):
        """ 'CalculateSelectedStrainAndKineticEnergy' is the original name of this method."""

        self.wrapped.CalculateSelectedStrainAndKineticEnergy()
