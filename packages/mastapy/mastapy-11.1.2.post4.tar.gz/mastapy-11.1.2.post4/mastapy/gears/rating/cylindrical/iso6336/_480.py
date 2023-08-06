"""_480.py

ISO63362006GearSingleFlankRating
"""


from mastapy._internal import constructor
from mastapy.gears.rating.cylindrical.iso6336 import _475, _486
from mastapy._internal.python_net import python_net_import

_ISO63362006_GEAR_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336', 'ISO63362006GearSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO63362006GearSingleFlankRating',)


class ISO63362006GearSingleFlankRating(_486.ISO6336AbstractMetalGearSingleFlankRating):
    """ISO63362006GearSingleFlankRating

    This is a mastapy class.
    """

    TYPE = _ISO63362006_GEAR_SINGLE_FLANK_RATING

    def __init__(self, instance_to_wrap: 'ISO63362006GearSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def nominal_tooth_root_stress(self) -> 'float':
        """float: 'NominalToothRootStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalToothRootStress

        if temp is None:
            return None

        return temp

    @property
    def rim_thickness_factor(self) -> 'float':
        """float: 'RimThicknessFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RimThicknessFactor

        if temp is None:
            return None

        return temp

    @property
    def rim_thickness_over_whole_depth(self) -> 'float':
        """float: 'RimThicknessOverWholeDepth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RimThicknessOverWholeDepth

        if temp is None:
            return None

        return temp

    @property
    def work_hardening_factor_for_reference_contact_stress(self) -> 'float':
        """float: 'WorkHardeningFactorForReferenceContactStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorkHardeningFactorForReferenceContactStress

        if temp is None:
            return None

        return temp

    @property
    def work_hardening_factor_for_static_contact_stress(self) -> 'float':
        """float: 'WorkHardeningFactorForStaticContactStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorkHardeningFactorForStaticContactStress

        if temp is None:
            return None

        return temp

    @property
    def tooth_fatigue_fracture_results(self) -> '_475.CylindricalGearToothFatigueFractureResults':
        """CylindricalGearToothFatigueFractureResults: 'ToothFatigueFractureResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothFatigueFractureResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
