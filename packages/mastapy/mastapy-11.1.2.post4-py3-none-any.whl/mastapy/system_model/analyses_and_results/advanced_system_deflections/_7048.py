"""_7048.py

CylindricalGearMeshAdvancedSystemDeflection
"""


from typing import List

from PIL.Image import Image

from mastapy.gears import _295
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.rating.cylindrical import _427
from mastapy.system_model.connections_and_sockets.gears import _2060
from mastapy.system_model.analyses_and_results.static_loads import _6586
from mastapy.gears.gear_designs.cylindrical import _982, _975
from mastapy.gears.cylindrical import _1166
from mastapy.math_utility import _1320
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7047, _7036, _7060
from mastapy.system_model.analyses_and_results.system_deflections import _2484
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'CylindricalGearMeshAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshAdvancedSystemDeflection',)


class CylindricalGearMeshAdvancedSystemDeflection(_7060.GearMeshAdvancedSystemDeflection):
    """CylindricalGearMeshAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_flank(self) -> '_295.CylindricalFlanks':
        """CylindricalFlanks: 'ActiveFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveFlank

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_295.CylindricalFlanks)(value) if value is not None else None

    @property
    def average_operating_axial_contact_ratio_for_first_tooth_passing_period(self) -> 'float':
        """float: 'AverageOperatingAxialContactRatioForFirstToothPassingPeriod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AverageOperatingAxialContactRatioForFirstToothPassingPeriod

        if temp is None:
            return None

        return temp

    @property
    def average_operating_transverse_contact_ratio_for_first_tooth_passing_period(self) -> 'float':
        """float: 'AverageOperatingTransverseContactRatioForFirstToothPassingPeriod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AverageOperatingTransverseContactRatioForFirstToothPassingPeriod

        if temp is None:
            return None

        return temp

    @property
    def calculated_load_sharing_factor(self) -> 'float':
        """float: 'CalculatedLoadSharingFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CalculatedLoadSharingFactor

        if temp is None:
            return None

        return temp

    @property
    def contact_chart_gap_to_loaded_flank_gear_a(self) -> 'Image':
        """Image: 'ContactChartGapToLoadedFlankGearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactChartGapToLoadedFlankGearA

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def contact_chart_gap_to_loaded_flank_gear_b(self) -> 'Image':
        """Image: 'ContactChartGapToLoadedFlankGearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactChartGapToLoadedFlankGearB

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def contact_chart_gap_to_unloaded_flank_gear_a(self) -> 'Image':
        """Image: 'ContactChartGapToUnloadedFlankGearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactChartGapToUnloadedFlankGearA

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def contact_chart_gap_to_unloaded_flank_gear_b(self) -> 'Image':
        """Image: 'ContactChartGapToUnloadedFlankGearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactChartGapToUnloadedFlankGearB

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def contact_chart_max_pressure_gear_a(self) -> 'Image':
        """Image: 'ContactChartMaxPressureGearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactChartMaxPressureGearA

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def contact_chart_max_pressure_gear_b(self) -> 'Image':
        """Image: 'ContactChartMaxPressureGearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactChartMaxPressureGearB

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def face_load_factor_contact(self) -> 'float':
        """float: 'FaceLoadFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceLoadFactorContact

        if temp is None:
            return None

        return temp

    @property
    def inactive_flank(self) -> '_295.CylindricalFlanks':
        """CylindricalFlanks: 'InactiveFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InactiveFlank

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_295.CylindricalFlanks)(value) if value is not None else None

    @property
    def maximum_contact_pressure(self) -> 'float':
        """float: 'MaximumContactPressure' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumContactPressure

        if temp is None:
            return None

        return temp

    @property
    def maximum_edge_stress(self) -> 'float':
        """float: 'MaximumEdgeStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumEdgeStress

        if temp is None:
            return None

        return temp

    @property
    def maximum_edge_stress_including_tip_contact(self) -> 'float':
        """float: 'MaximumEdgeStressIncludingTipContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumEdgeStressIncludingTipContact

        if temp is None:
            return None

        return temp

    @property
    def maximum_edge_stress_on_gear_a_including_tip_contact(self) -> 'float':
        """float: 'MaximumEdgeStressOnGearAIncludingTipContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumEdgeStressOnGearAIncludingTipContact

        if temp is None:
            return None

        return temp

    @property
    def maximum_edge_stress_on_gear_b_including_tip_contact(self) -> 'float':
        """float: 'MaximumEdgeStressOnGearBIncludingTipContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumEdgeStressOnGearBIncludingTipContact

        if temp is None:
            return None

        return temp

    @property
    def maximum_principal_root_stress_on_tension_side_from_gear_fe_model(self) -> 'List[float]':
        """List[float]: 'MaximumPrincipalRootStressOnTensionSideFromGearFEModel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumPrincipalRootStressOnTensionSideFromGearFEModel

        if temp is None:
            return None

        value = conversion.to_list_any(temp)
        return value

    @property
    def mean_mesh_stiffness(self) -> 'float':
        """float: 'MeanMeshStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanMeshStiffness

        if temp is None:
            return None

        return temp

    @property
    def mean_mesh_tilt_stiffness(self) -> 'float':
        """float: 'MeanMeshTiltStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanMeshTiltStiffness

        if temp is None:
            return None

        return temp

    @property
    def mean_te_excluding_backlash(self) -> 'float':
        """float: 'MeanTEExcludingBacklash' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanTEExcludingBacklash

        if temp is None:
            return None

        return temp

    @property
    def mean_total_contact_ratio(self) -> 'float':
        """float: 'MeanTotalContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanTotalContactRatio

        if temp is None:
            return None

        return temp

    @property
    def peak_to_peak_mesh_stiffness(self) -> 'float':
        """float: 'PeakToPeakMeshStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PeakToPeakMeshStiffness

        if temp is None:
            return None

        return temp

    @property
    def peak_to_peak_te(self) -> 'float':
        """float: 'PeakToPeakTE' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PeakToPeakTE

        if temp is None:
            return None

        return temp

    @property
    def torque_share(self) -> 'float':
        """float: 'TorqueShare' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorqueShare

        if temp is None:
            return None

        return temp

    @property
    def use_advanced_ltca(self) -> 'bool':
        """bool: 'UseAdvancedLTCA' is the original name of this property."""

        temp = self.wrapped.UseAdvancedLTCA

        if temp is None:
            return None

        return temp

    @use_advanced_ltca.setter
    def use_advanced_ltca(self, value: 'bool'):
        self.wrapped.UseAdvancedLTCA = bool(value) if value else False

    @property
    def component_detailed_analysis(self) -> '_427.CylindricalGearMeshRating':
        """CylindricalGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDetailedAnalysis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design(self) -> '_2060.CylindricalGearMesh':
        """CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6586.CylindricalGearMeshLoadCase':
        """CylindricalGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mesh_design(self) -> '_982.CylindricalGearMeshDesign':
        """CylindricalGearMeshDesign: 'GearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMeshDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def points_with_worst_results(self) -> '_1166.PointsWithWorstResults':
        """PointsWithWorstResults: 'PointsWithWorstResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PointsWithWorstResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def transmission_error_fourier_series_for_first_tooth_passing_period(self) -> '_1320.FourierSeries':
        """FourierSeries: 'TransmissionErrorFourierSeriesForFirstToothPassingPeriod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransmissionErrorFourierSeriesForFirstToothPassingPeriod

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_gear_advanced_analyses(self) -> 'List[_7047.CylindricalGearAdvancedSystemDeflection]':
        """List[CylindricalGearAdvancedSystemDeflection]: 'CylindricalGearAdvancedAnalyses' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearAdvancedAnalyses

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cylindrical_gear_mesh_system_deflection_results(self) -> 'List[_2484.CylindricalGearMeshSystemDeflectionTimestep]':
        """List[CylindricalGearMeshSystemDeflectionTimestep]: 'CylindricalGearMeshSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearMeshSystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def gear_designs(self) -> 'List[_975.CylindricalGearDesign]':
        """List[CylindricalGearDesign]: 'GearDesigns' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearDesigns

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def max_pressure_contact_chart_for_each_tooth_pass_for_gear_a(self) -> 'List[_7036.ContactChartPerToothPass]':
        """List[ContactChartPerToothPass]: 'MaxPressureContactChartForEachToothPassForGearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaxPressureContactChartForEachToothPassForGearA

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshAdvancedSystemDeflection]':
        """List[CylindricalGearMeshAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def animation_of_max_pressure_contact_chart_for_each_tooth_pass_for_gear_a(self):
        """ 'AnimationOfMaxPressureContactChartForEachToothPassForGearA' is the original name of this method."""

        self.wrapped.AnimationOfMaxPressureContactChartForEachToothPassForGearA()

    def contact_chart_gap_to_loaded_flank_gear_a_as_text_file(self):
        """ 'ContactChartGapToLoadedFlankGearAAsTextFile' is the original name of this method."""

        self.wrapped.ContactChartGapToLoadedFlankGearAAsTextFile()

    def contact_chart_gap_to_loaded_flank_gear_b_as_text_file(self):
        """ 'ContactChartGapToLoadedFlankGearBAsTextFile' is the original name of this method."""

        self.wrapped.ContactChartGapToLoadedFlankGearBAsTextFile()

    def contact_chart_gap_to_unloaded_flank_gear_a_as_text_file(self):
        """ 'ContactChartGapToUnloadedFlankGearAAsTextFile' is the original name of this method."""

        self.wrapped.ContactChartGapToUnloadedFlankGearAAsTextFile()

    def contact_chart_gap_to_unloaded_flank_gear_b_as_text_file(self):
        """ 'ContactChartGapToUnloadedFlankGearBAsTextFile' is the original name of this method."""

        self.wrapped.ContactChartGapToUnloadedFlankGearBAsTextFile()

    def contact_chart_max_pressure_gear_a_as_text_file(self):
        """ 'ContactChartMaxPressureGearAAsTextFile' is the original name of this method."""

        self.wrapped.ContactChartMaxPressureGearAAsTextFile()

    def contact_chart_max_pressure_gear_b_as_text_file(self):
        """ 'ContactChartMaxPressureGearBAsTextFile' is the original name of this method."""

        self.wrapped.ContactChartMaxPressureGearBAsTextFile()
