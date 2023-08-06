"""_1766.py

LoadedCylindricalRollerBearingElement
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling import _1785
from mastapy._internal.python_net import python_net_import

_LOADED_CYLINDRICAL_ROLLER_BEARING_ELEMENT = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedCylindricalRollerBearingElement')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedCylindricalRollerBearingElement',)


class LoadedCylindricalRollerBearingElement(_1785.LoadedNonBarrelRollerElement):
    """LoadedCylindricalRollerBearingElement

    This is a mastapy class.
    """

    TYPE = _LOADED_CYLINDRICAL_ROLLER_BEARING_ELEMENT

    def __init__(self, instance_to_wrap: 'LoadedCylindricalRollerBearingElement.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def height_of_rib_roller_contact_above_race_inner_left(self) -> 'float':
        """float: 'HeightOfRibRollerContactAboveRaceInnerLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HeightOfRibRollerContactAboveRaceInnerLeft

        if temp is None:
            return None

        return temp

    @property
    def height_of_rib_roller_contact_above_race_inner_right(self) -> 'float':
        """float: 'HeightOfRibRollerContactAboveRaceInnerRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HeightOfRibRollerContactAboveRaceInnerRight

        if temp is None:
            return None

        return temp

    @property
    def height_of_rib_roller_contact_above_race_outer_left(self) -> 'float':
        """float: 'HeightOfRibRollerContactAboveRaceOuterLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HeightOfRibRollerContactAboveRaceOuterLeft

        if temp is None:
            return None

        return temp

    @property
    def height_of_rib_roller_contact_above_race_outer_right(self) -> 'float':
        """float: 'HeightOfRibRollerContactAboveRaceOuterRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HeightOfRibRollerContactAboveRaceOuterRight

        if temp is None:
            return None

        return temp

    @property
    def maximum_rib_stress_inner_left(self) -> 'float':
        """float: 'MaximumRibStressInnerLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumRibStressInnerLeft

        if temp is None:
            return None

        return temp

    @property
    def maximum_rib_stress_inner_right(self) -> 'float':
        """float: 'MaximumRibStressInnerRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumRibStressInnerRight

        if temp is None:
            return None

        return temp

    @property
    def maximum_rib_stress_outer_left(self) -> 'float':
        """float: 'MaximumRibStressOuterLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumRibStressOuterLeft

        if temp is None:
            return None

        return temp

    @property
    def maximum_rib_stress_outer_right(self) -> 'float':
        """float: 'MaximumRibStressOuterRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumRibStressOuterRight

        if temp is None:
            return None

        return temp
