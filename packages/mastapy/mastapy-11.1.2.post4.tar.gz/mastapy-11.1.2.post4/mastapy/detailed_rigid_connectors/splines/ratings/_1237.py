"""_1237.py

SAESplineHalfRating
"""


from mastapy._internal import constructor
from mastapy.detailed_rigid_connectors.splines.ratings import _1239
from mastapy._internal.python_net import python_net_import

_SAE_SPLINE_HALF_RATING = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines.Ratings', 'SAESplineHalfRating')


__docformat__ = 'restructuredtext en'
__all__ = ('SAESplineHalfRating',)


class SAESplineHalfRating(_1239.SplineHalfRating):
    """SAESplineHalfRating

    This is a mastapy class.
    """

    TYPE = _SAE_SPLINE_HALF_RATING

    def __init__(self, instance_to_wrap: 'SAESplineHalfRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def allowable_compressive_stress(self) -> 'float':
        """float: 'AllowableCompressiveStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableCompressiveStress

        if temp is None:
            return None

        return temp

    @property
    def allowable_shear_stress(self) -> 'float':
        """float: 'AllowableShearStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableShearStress

        if temp is None:
            return None

        return temp

    @property
    def equivalent_stress(self) -> 'float':
        """float: 'EquivalentStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EquivalentStress

        if temp is None:
            return None

        return temp

    @property
    def fatigue_damage_for_compressive_stress(self) -> 'float':
        """float: 'FatigueDamageForCompressiveStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FatigueDamageForCompressiveStress

        if temp is None:
            return None

        return temp

    @property
    def fatigue_damage_for_equivalent_root_stress(self) -> 'float':
        """float: 'FatigueDamageForEquivalentRootStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FatigueDamageForEquivalentRootStress

        if temp is None:
            return None

        return temp

    @property
    def fatigue_damage_for_tooth_shearing_stress(self) -> 'float':
        """float: 'FatigueDamageForToothShearingStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FatigueDamageForToothShearingStress

        if temp is None:
            return None

        return temp

    @property
    def maximum_allowable_compressive_stress(self) -> 'float':
        """float: 'MaximumAllowableCompressiveStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumAllowableCompressiveStress

        if temp is None:
            return None

        return temp

    @property
    def maximum_allowable_shear_stress(self) -> 'float':
        """float: 'MaximumAllowableShearStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumAllowableShearStress

        if temp is None:
            return None

        return temp

    @property
    def maximum_allowable_tensile_stress(self) -> 'float':
        """float: 'MaximumAllowableTensileStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumAllowableTensileStress

        if temp is None:
            return None

        return temp

    @property
    def root_bending_stress(self) -> 'float':
        """float: 'RootBendingStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootBendingStress

        if temp is None:
            return None

        return temp

    @property
    def safety_factor_for_compressive_stress(self) -> 'float':
        """float: 'SafetyFactorForCompressiveStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactorForCompressiveStress

        if temp is None:
            return None

        return temp

    @property
    def safety_factor_for_equivalent_root_stress(self) -> 'float':
        """float: 'SafetyFactorForEquivalentRootStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactorForEquivalentRootStress

        if temp is None:
            return None

        return temp

    @property
    def safety_factor_for_tooth_shearing_stress(self) -> 'float':
        """float: 'SafetyFactorForToothShearingStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactorForToothShearingStress

        if temp is None:
            return None

        return temp

    @property
    def stress_concentration_factor(self) -> 'float':
        """float: 'StressConcentrationFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressConcentrationFactor

        if temp is None:
            return None

        return temp

    @property
    def torsional_shear_stress(self) -> 'float':
        """float: 'TorsionalShearStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorsionalShearStress

        if temp is None:
            return None

        return temp
