"""_5586.py

HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic
"""


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import _5599, _5588
from mastapy._internal.python_net import python_net_import

_HARMONIC_ANALYSIS_RESULTS_BROKEN_DOWN_BY_COMPONENT_WITHIN_A_HARMONIC = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults', 'HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic',)


class HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic(_5588.HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic):
    """HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic

    This is a mastapy class.
    """

    TYPE = _HARMONIC_ANALYSIS_RESULTS_BROKEN_DOWN_BY_COMPONENT_WITHIN_A_HARMONIC

    def __init__(self, instance_to_wrap: 'HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_name(self) -> 'str':
        """str: 'ComponentName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentName

        if temp is None:
            return None

        return temp

    @property
    def dynamic_mesh_force(self) -> '_5599.ResultsForResponseOfAComponentOrSurfaceInAHarmonic':
        """ResultsForResponseOfAComponentOrSurfaceInAHarmonic: 'DynamicMeshForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicMeshForce

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def dynamic_mesh_moment(self) -> '_5599.ResultsForResponseOfAComponentOrSurfaceInAHarmonic':
        """ResultsForResponseOfAComponentOrSurfaceInAHarmonic: 'DynamicMeshMoment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicMeshMoment

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def dynamic_misalignment(self) -> '_5599.ResultsForResponseOfAComponentOrSurfaceInAHarmonic':
        """ResultsForResponseOfAComponentOrSurfaceInAHarmonic: 'DynamicMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicMisalignment

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def dynamic_te(self) -> '_5599.ResultsForResponseOfAComponentOrSurfaceInAHarmonic':
        """ResultsForResponseOfAComponentOrSurfaceInAHarmonic: 'DynamicTE' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicTE

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def kinetic_energy(self) -> '_5599.ResultsForResponseOfAComponentOrSurfaceInAHarmonic':
        """ResultsForResponseOfAComponentOrSurfaceInAHarmonic: 'KineticEnergy' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KineticEnergy

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def strain_energy(self) -> '_5599.ResultsForResponseOfAComponentOrSurfaceInAHarmonic':
        """ResultsForResponseOfAComponentOrSurfaceInAHarmonic: 'StrainEnergy' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StrainEnergy

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
