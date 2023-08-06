"""_496.py

ToothFlankFractureAnalysisPointN1457
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._math.vector_2d import Vector2D
from mastapy.gears.rating.cylindrical.iso6336 import _498
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_TOOTH_FLANK_FRACTURE_ANALYSIS_POINT_N1457 = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336', 'ToothFlankFractureAnalysisPointN1457')


__docformat__ = 'restructuredtext en'
__all__ = ('ToothFlankFractureAnalysisPointN1457',)


class ToothFlankFractureAnalysisPointN1457(_0.APIBase):
    """ToothFlankFractureAnalysisPointN1457

    This is a mastapy class.
    """

    TYPE = _TOOTH_FLANK_FRACTURE_ANALYSIS_POINT_N1457

    def __init__(self, instance_to_wrap: 'ToothFlankFractureAnalysisPointN1457.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def depth_from_surface(self) -> 'float':
        """float: 'DepthFromSurface' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DepthFromSurface

        if temp is None:
            return None

        return temp

    @property
    def fatigue_damage(self) -> 'float':
        """float: 'FatigueDamage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FatigueDamage

        if temp is None:
            return None

        return temp

    @property
    def hardness_conversion_factor(self) -> 'float':
        """float: 'HardnessConversionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HardnessConversionFactor

        if temp is None:
            return None

        return temp

    @property
    def local_material_hardness(self) -> 'float':
        """float: 'LocalMaterialHardness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LocalMaterialHardness

        if temp is None:
            return None

        return temp

    @property
    def local_permissible_shear_strength(self) -> 'float':
        """float: 'LocalPermissibleShearStrength' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LocalPermissibleShearStrength

        if temp is None:
            return None

        return temp

    @property
    def maximum_equivalent_stress(self) -> 'float':
        """float: 'MaximumEquivalentStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumEquivalentStress

        if temp is None:
            return None

        return temp

    @property
    def normalised_depth_from_surface(self) -> 'float':
        """float: 'NormalisedDepthFromSurface' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalisedDepthFromSurface

        if temp is None:
            return None

        return temp

    @property
    def tangential_component_of_compressive_residual_stresses(self) -> 'float':
        """float: 'TangentialComponentOfCompressiveResidualStresses' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TangentialComponentOfCompressiveResidualStresses

        if temp is None:
            return None

        return temp

    @property
    def coordinates(self) -> 'Vector2D':
        """Vector2D: 'Coordinates' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Coordinates

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)
        return value

    @property
    def stress_analysis_with_maximum_equivalent_stress(self) -> '_498.ToothFlankFractureStressStepAtAnalysisPointN1457':
        """ToothFlankFractureStressStepAtAnalysisPointN1457: 'StressAnalysisWithMaximumEquivalentStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressAnalysisWithMaximumEquivalentStress

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def stress_history(self) -> 'List[_498.ToothFlankFractureStressStepAtAnalysisPointN1457]':
        """List[ToothFlankFractureStressStepAtAnalysisPointN1457]: 'StressHistory' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressHistory

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
