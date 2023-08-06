"""_1113.py

ConicalMeshedGearDesign
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs import _911
from mastapy._internal.python_net import python_net_import

_CONICAL_MESHED_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Conical', 'ConicalMeshedGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshedGearDesign',)


class ConicalMeshedGearDesign(_911.GearDesignComponent):
    """ConicalMeshedGearDesign

    This is a mastapy class.
    """

    TYPE = _CONICAL_MESHED_GEAR_DESIGN

    def __init__(self, instance_to_wrap: 'ConicalMeshedGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axial_force_type(self) -> 'str':
        """str: 'AxialForceType' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialForceType

        if temp is None:
            return None

        return temp

    @property
    def axial_force_type_convex(self) -> 'str':
        """str: 'AxialForceTypeConvex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialForceTypeConvex

        if temp is None:
            return None

        return temp

    @property
    def gleason_axial_factor_concave(self) -> 'float':
        """float: 'GleasonAxialFactorConcave' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GleasonAxialFactorConcave

        if temp is None:
            return None

        return temp

    @property
    def gleason_axial_factor_convex(self) -> 'float':
        """float: 'GleasonAxialFactorConvex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GleasonAxialFactorConvex

        if temp is None:
            return None

        return temp

    @property
    def gleason_separating_factor_concave(self) -> 'float':
        """float: 'GleasonSeparatingFactorConcave' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GleasonSeparatingFactorConcave

        if temp is None:
            return None

        return temp

    @property
    def gleason_separating_factor_convex(self) -> 'float':
        """float: 'GleasonSeparatingFactorConvex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GleasonSeparatingFactorConvex

        if temp is None:
            return None

        return temp

    @property
    def module(self) -> 'float':
        """float: 'Module' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Module

        if temp is None:
            return None

        return temp

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property."""

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else ''

    @property
    def pitch_angle(self) -> 'float':
        """float: 'PitchAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchAngle

        if temp is None:
            return None

        return temp

    @property
    def radial_force_type_concave(self) -> 'str':
        """str: 'RadialForceTypeConcave' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadialForceTypeConcave

        if temp is None:
            return None

        return temp

    @property
    def radial_force_type_convex(self) -> 'str':
        """str: 'RadialForceTypeConvex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadialForceTypeConvex

        if temp is None:
            return None

        return temp
