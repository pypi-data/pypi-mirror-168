"""_6308.py

CriticalSpeedAnalysisOptions
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CRITICAL_SPEED_ANALYSIS_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'CriticalSpeedAnalysisOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('CriticalSpeedAnalysisOptions',)


class CriticalSpeedAnalysisOptions(_0.APIBase):
    """CriticalSpeedAnalysisOptions

    This is a mastapy class.
    """

    TYPE = _CRITICAL_SPEED_ANALYSIS_OPTIONS

    def __init__(self, instance_to_wrap: 'CriticalSpeedAnalysisOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axial_stiffness(self) -> 'float':
        """float: 'AxialStiffness' is the original name of this property."""

        temp = self.wrapped.AxialStiffness

        if temp is None:
            return None

        return temp

    @axial_stiffness.setter
    def axial_stiffness(self, value: 'float'):
        self.wrapped.AxialStiffness = float(value) if value else 0.0

    @property
    def final_stiffness(self) -> 'float':
        """float: 'FinalStiffness' is the original name of this property."""

        temp = self.wrapped.FinalStiffness

        if temp is None:
            return None

        return temp

    @final_stiffness.setter
    def final_stiffness(self, value: 'float'):
        self.wrapped.FinalStiffness = float(value) if value else 0.0

    @property
    def include_damping_effects(self) -> 'bool':
        """bool: 'IncludeDampingEffects' is the original name of this property."""

        temp = self.wrapped.IncludeDampingEffects

        if temp is None:
            return None

        return temp

    @include_damping_effects.setter
    def include_damping_effects(self, value: 'bool'):
        self.wrapped.IncludeDampingEffects = bool(value) if value else False

    @property
    def include_gyroscopic_effects(self) -> 'bool':
        """bool: 'IncludeGyroscopicEffects' is the original name of this property."""

        temp = self.wrapped.IncludeGyroscopicEffects

        if temp is None:
            return None

        return temp

    @include_gyroscopic_effects.setter
    def include_gyroscopic_effects(self, value: 'bool'):
        self.wrapped.IncludeGyroscopicEffects = bool(value) if value else False

    @property
    def initial_stiffness(self) -> 'float':
        """float: 'InitialStiffness' is the original name of this property."""

        temp = self.wrapped.InitialStiffness

        if temp is None:
            return None

        return temp

    @initial_stiffness.setter
    def initial_stiffness(self, value: 'float'):
        self.wrapped.InitialStiffness = float(value) if value else 0.0

    @property
    def number_of_modes(self) -> 'int':
        """int: 'NumberOfModes' is the original name of this property."""

        temp = self.wrapped.NumberOfModes

        if temp is None:
            return None

        return temp

    @number_of_modes.setter
    def number_of_modes(self, value: 'int'):
        self.wrapped.NumberOfModes = int(value) if value else 0

    @property
    def number_of_stiffnesses(self) -> 'int':
        """int: 'NumberOfStiffnesses' is the original name of this property."""

        temp = self.wrapped.NumberOfStiffnesses

        if temp is None:
            return None

        return temp

    @number_of_stiffnesses.setter
    def number_of_stiffnesses(self, value: 'int'):
        self.wrapped.NumberOfStiffnesses = int(value) if value else 0

    @property
    def sort_modes(self) -> 'bool':
        """bool: 'SortModes' is the original name of this property."""

        temp = self.wrapped.SortModes

        if temp is None:
            return None

        return temp

    @sort_modes.setter
    def sort_modes(self, value: 'bool'):
        self.wrapped.SortModes = bool(value) if value else False

    @property
    def tilt_stiffness(self) -> 'float':
        """float: 'TiltStiffness' is the original name of this property."""

        temp = self.wrapped.TiltStiffness

        if temp is None:
            return None

        return temp

    @tilt_stiffness.setter
    def tilt_stiffness(self, value: 'float'):
        self.wrapped.TiltStiffness = float(value) if value else 0.0
