"""_823.py

CylindricalGearMeshLoadDistributionAnalysis
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.load_case.cylindrical import _850
from mastapy.gears.ltca import _798, _807
from mastapy.gears.cylindrical import _1166
from mastapy.gears.rating.cylindrical import _427
from mastapy.gears.ltca.cylindrical import _827
from mastapy._math.vector_2d import Vector2D
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_LOAD_DISTRIBUTION_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.LTCA.Cylindrical', 'CylindricalGearMeshLoadDistributionAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshLoadDistributionAnalysis',)


class CylindricalGearMeshLoadDistributionAnalysis(_807.GearMeshLoadDistributionAnalysis):
    """CylindricalGearMeshLoadDistributionAnalysis

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_MESH_LOAD_DISTRIBUTION_ANALYSIS

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshLoadDistributionAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def average_flash_temperature(self) -> 'float':
        """float: 'AverageFlashTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AverageFlashTemperature

        if temp is None:
            return None

        return temp

    @property
    def calculated_face_load_factor_contact(self) -> 'float':
        """float: 'CalculatedFaceLoadFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CalculatedFaceLoadFactorContact

        if temp is None:
            return None

        return temp

    @property
    def din_scuffing_bulk_tooth_temperature(self) -> 'float':
        """float: 'DINScuffingBulkToothTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DINScuffingBulkToothTemperature

        if temp is None:
            return None

        return temp

    @property
    def iso63362006_mesh_stiffness(self) -> 'float':
        """float: 'ISO63362006MeshStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO63362006MeshStiffness

        if temp is None:
            return None

        return temp

    @property
    def iso63362006_mesh_stiffness_across_face_width(self) -> 'float':
        """float: 'ISO63362006MeshStiffnessAcrossFaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO63362006MeshStiffnessAcrossFaceWidth

        if temp is None:
            return None

        return temp

    @property
    def iso63362006_single_stiffness(self) -> 'float':
        """float: 'ISO63362006SingleStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO63362006SingleStiffness

        if temp is None:
            return None

        return temp

    @property
    def iso63362006_single_stiffness_across_face_width(self) -> 'float':
        """float: 'ISO63362006SingleStiffnessAcrossFaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISO63362006SingleStiffnessAcrossFaceWidth

        if temp is None:
            return None

        return temp

    @property
    def iso_scuffing_bulk_tooth_temperature(self) -> 'float':
        """float: 'ISOScuffingBulkToothTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISOScuffingBulkToothTemperature

        if temp is None:
            return None

        return temp

    @property
    def maximum_edge_pressure(self) -> 'float':
        """float: 'MaximumEdgePressure' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumEdgePressure

        if temp is None:
            return None

        return temp

    @property
    def mean_te(self) -> 'float':
        """float: 'MeanTE' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanTE

        if temp is None:
            return None

        return temp

    @property
    def misalignment(self) -> 'float':
        """float: 'Misalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Misalignment

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
    def strip_loads_deviation(self) -> 'float':
        """float: 'StripLoadsDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StripLoadsDeviation

        if temp is None:
            return None

        return temp

    @property
    def strip_loads_maximum(self) -> 'float':
        """float: 'StripLoadsMaximum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StripLoadsMaximum

        if temp is None:
            return None

        return temp

    @property
    def strip_loads_minimum(self) -> 'float':
        """float: 'StripLoadsMinimum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StripLoadsMinimum

        if temp is None:
            return None

        return temp

    @property
    def theoretical_total_contact_ratio(self) -> 'float':
        """float: 'TheoreticalTotalContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TheoreticalTotalContactRatio

        if temp is None:
            return None

        return temp

    @property
    def tooth_temperature(self) -> 'float':
        """float: 'ToothTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothTemperature

        if temp is None:
            return None

        return temp

    @property
    def utilization_force_per_unit_length_cutoff_value(self) -> 'float':
        """float: 'UtilizationForcePerUnitLengthCutoffValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.UtilizationForcePerUnitLengthCutoffValue

        if temp is None:
            return None

        return temp

    @property
    def cylindrical_mesh_load_case(self) -> '_850.CylindricalMeshLoadCase':
        """CylindricalMeshLoadCase: 'CylindricalMeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalMeshLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a_in_mesh(self) -> '_798.CylindricalMeshedGearLoadDistributionAnalysis':
        """CylindricalMeshedGearLoadDistributionAnalysis: 'GearAInMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearAInMesh

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b_in_mesh(self) -> '_798.CylindricalMeshedGearLoadDistributionAnalysis':
        """CylindricalMeshedGearLoadDistributionAnalysis: 'GearBInMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBInMesh

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
    def rating(self) -> '_427.CylindricalGearMeshRating':
        """CylindricalGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rating

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def load_distribution_analyses_at_single_rotation(self) -> 'List[_827.CylindricalMeshLoadDistributionAtRotation]':
        """List[CylindricalMeshLoadDistributionAtRotation]: 'LoadDistributionAnalysesAtSingleRotation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadDistributionAnalysesAtSingleRotation

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def meshed_gears(self) -> 'List[_798.CylindricalMeshedGearLoadDistributionAnalysis]':
        """List[CylindricalMeshedGearLoadDistributionAnalysis]: 'MeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshedGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def transmission_error_against_rotation(self) -> 'List[Vector2D]':
        """List[Vector2D]: 'TransmissionErrorAgainstRotation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransmissionErrorAgainstRotation

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
