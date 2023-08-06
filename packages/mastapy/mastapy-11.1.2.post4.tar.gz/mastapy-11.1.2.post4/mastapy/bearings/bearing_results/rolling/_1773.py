"""_1773.py

LoadedFourPointContactBallBearingElement
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling import _1777
from mastapy._internal.python_net import python_net_import

_LOADED_FOUR_POINT_CONTACT_BALL_BEARING_ELEMENT = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedFourPointContactBallBearingElement')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedFourPointContactBallBearingElement',)


class LoadedFourPointContactBallBearingElement(_1777.LoadedMultiPointContactBallBearingElement):
    """LoadedFourPointContactBallBearingElement

    This is a mastapy class.
    """

    TYPE = _LOADED_FOUR_POINT_CONTACT_BALL_BEARING_ELEMENT

    def __init__(self, instance_to_wrap: 'LoadedFourPointContactBallBearingElement.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contact_angle_outer_left(self) -> 'float':
        """float: 'ContactAngleOuterLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactAngleOuterLeft

        if temp is None:
            return None

        return temp

    @property
    def contact_angle_outer_right(self) -> 'float':
        """float: 'ContactAngleOuterRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactAngleOuterRight

        if temp is None:
            return None

        return temp

    @property
    def hertzian_semi_major_dimension_outer_left(self) -> 'float':
        """float: 'HertzianSemiMajorDimensionOuterLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianSemiMajorDimensionOuterLeft

        if temp is None:
            return None

        return temp

    @property
    def hertzian_semi_major_dimension_outer_right(self) -> 'float':
        """float: 'HertzianSemiMajorDimensionOuterRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianSemiMajorDimensionOuterRight

        if temp is None:
            return None

        return temp

    @property
    def hertzian_semi_minor_dimension_outer_left(self) -> 'float':
        """float: 'HertzianSemiMinorDimensionOuterLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianSemiMinorDimensionOuterLeft

        if temp is None:
            return None

        return temp

    @property
    def hertzian_semi_minor_dimension_outer_right(self) -> 'float':
        """float: 'HertzianSemiMinorDimensionOuterRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianSemiMinorDimensionOuterRight

        if temp is None:
            return None

        return temp

    @property
    def maximum_normal_stress_outer_left(self) -> 'float':
        """float: 'MaximumNormalStressOuterLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumNormalStressOuterLeft

        if temp is None:
            return None

        return temp

    @property
    def maximum_normal_stress_outer_right(self) -> 'float':
        """float: 'MaximumNormalStressOuterRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumNormalStressOuterRight

        if temp is None:
            return None

        return temp

    @property
    def maximum_normal_stress_outer(self) -> 'float':
        """float: 'MaximumNormalStressOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumNormalStressOuter

        if temp is None:
            return None

        return temp

    @property
    def maximum_shear_stress_outer_left(self) -> 'float':
        """float: 'MaximumShearStressOuterLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumShearStressOuterLeft

        if temp is None:
            return None

        return temp

    @property
    def maximum_shear_stress_outer_right(self) -> 'float':
        """float: 'MaximumShearStressOuterRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumShearStressOuterRight

        if temp is None:
            return None

        return temp

    @property
    def minimum_lubricating_film_thickness_outer_left(self) -> 'float':
        """float: 'MinimumLubricatingFilmThicknessOuterLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLubricatingFilmThicknessOuterLeft

        if temp is None:
            return None

        return temp

    @property
    def minimum_lubricating_film_thickness_outer_right(self) -> 'float':
        """float: 'MinimumLubricatingFilmThicknessOuterRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLubricatingFilmThicknessOuterRight

        if temp is None:
            return None

        return temp

    @property
    def minimum_lubricating_film_thickness_outer(self) -> 'float':
        """float: 'MinimumLubricatingFilmThicknessOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLubricatingFilmThicknessOuter

        if temp is None:
            return None

        return temp

    @property
    def normal_load_outer_left(self) -> 'float':
        """float: 'NormalLoadOuterLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalLoadOuterLeft

        if temp is None:
            return None

        return temp

    @property
    def normal_load_outer_right(self) -> 'float':
        """float: 'NormalLoadOuterRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalLoadOuterRight

        if temp is None:
            return None

        return temp
