"""_1137.py

BevelMeshedGearDesign
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.agma_gleason_conical import _1150
from mastapy._internal.python_net import python_net_import

_BEVEL_MESHED_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Bevel', 'BevelMeshedGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelMeshedGearDesign',)


class BevelMeshedGearDesign(_1150.AGMAGleasonConicalMeshedGearDesign):
    """BevelMeshedGearDesign

    This is a mastapy class.
    """

    TYPE = _BEVEL_MESHED_GEAR_DESIGN

    def __init__(self, instance_to_wrap: 'BevelMeshedGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bending_strength_geometry_factor_concave(self) -> 'float':
        """float: 'BendingStrengthGeometryFactorConcave' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BendingStrengthGeometryFactorConcave

        if temp is None:
            return None

        return temp

    @property
    def bending_strength_geometry_factor_convex(self) -> 'float':
        """float: 'BendingStrengthGeometryFactorConvex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BendingStrengthGeometryFactorConvex

        if temp is None:
            return None

        return temp

    @property
    def distance_factor(self) -> 'float':
        """float: 'DistanceFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DistanceFactor

        if temp is None:
            return None

        return temp

    @property
    def durability_factor_agma(self) -> 'float':
        """float: 'DurabilityFactorAGMA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DurabilityFactorAGMA

        if temp is None:
            return None

        return temp

    @property
    def durability_factor_gleason(self) -> 'float':
        """float: 'DurabilityFactorGleason' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DurabilityFactorGleason

        if temp is None:
            return None

        return temp

    @property
    def geometry_factor_j_concave(self) -> 'float':
        """float: 'GeometryFactorJConcave' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GeometryFactorJConcave

        if temp is None:
            return None

        return temp

    @property
    def geometry_factor_j_convex(self) -> 'float':
        """float: 'GeometryFactorJConvex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GeometryFactorJConvex

        if temp is None:
            return None

        return temp

    @property
    def minimum_root_fillet_radius(self) -> 'float':
        """float: 'MinimumRootFilletRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumRootFilletRadius

        if temp is None:
            return None

        return temp

    @property
    def normal_chordal_thickness_at_mean_of_contact(self) -> 'float':
        """float: 'NormalChordalThicknessAtMeanOfContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalChordalThicknessAtMeanOfContact

        if temp is None:
            return None

        return temp

    @property
    def strength_factor_concave(self) -> 'float':
        """float: 'StrengthFactorConcave' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StrengthFactorConcave

        if temp is None:
            return None

        return temp

    @property
    def strength_factor_convex(self) -> 'float':
        """float: 'StrengthFactorConvex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StrengthFactorConvex

        if temp is None:
            return None

        return temp
