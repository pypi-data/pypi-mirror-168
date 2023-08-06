"""_5590.py

HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic
"""


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import _5599, _5588
from mastapy._internal.python_net import python_net_import

_HARMONIC_ANALYSIS_RESULTS_BROKEN_DOWN_BY_SURFACE_WITHIN_A_HARMONIC = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults', 'HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic',)


class HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic(_5588.HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic):
    """HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic

    This is a mastapy class.
    """

    TYPE = _HARMONIC_ANALYSIS_RESULTS_BROKEN_DOWN_BY_SURFACE_WITHIN_A_HARMONIC

    def __init__(self, instance_to_wrap: 'HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def surface_name(self) -> 'str':
        """str: 'SurfaceName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfaceName

        if temp is None:
            return None

        return temp

    @property
    def airborne_sound_power(self) -> '_5599.ResultsForResponseOfAComponentOrSurfaceInAHarmonic':
        """ResultsForResponseOfAComponentOrSurfaceInAHarmonic: 'AirborneSoundPower' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AirborneSoundPower

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def maximum_normal_velocity(self) -> '_5599.ResultsForResponseOfAComponentOrSurfaceInAHarmonic':
        """ResultsForResponseOfAComponentOrSurfaceInAHarmonic: 'MaximumNormalVelocity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumNormalVelocity

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def root_mean_squared_normal_acceleration(self) -> '_5599.ResultsForResponseOfAComponentOrSurfaceInAHarmonic':
        """ResultsForResponseOfAComponentOrSurfaceInAHarmonic: 'RootMeanSquaredNormalAcceleration' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootMeanSquaredNormalAcceleration

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def root_mean_squared_normal_displacement(self) -> '_5599.ResultsForResponseOfAComponentOrSurfaceInAHarmonic':
        """ResultsForResponseOfAComponentOrSurfaceInAHarmonic: 'RootMeanSquaredNormalDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootMeanSquaredNormalDisplacement

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def root_mean_squared_normal_velocity(self) -> '_5599.ResultsForResponseOfAComponentOrSurfaceInAHarmonic':
        """ResultsForResponseOfAComponentOrSurfaceInAHarmonic: 'RootMeanSquaredNormalVelocity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootMeanSquaredNormalVelocity

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def sound_intensity(self) -> '_5599.ResultsForResponseOfAComponentOrSurfaceInAHarmonic':
        """ResultsForResponseOfAComponentOrSurfaceInAHarmonic: 'SoundIntensity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SoundIntensity

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def sound_pressure(self) -> '_5599.ResultsForResponseOfAComponentOrSurfaceInAHarmonic':
        """ResultsForResponseOfAComponentOrSurfaceInAHarmonic: 'SoundPressure' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SoundPressure

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
