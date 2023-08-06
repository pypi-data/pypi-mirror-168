"""_1777.py

LoadedMultiPointContactBallBearingElement
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling import _1758
from mastapy._internal.python_net import python_net_import

_LOADED_MULTI_POINT_CONTACT_BALL_BEARING_ELEMENT = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedMultiPointContactBallBearingElement')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedMultiPointContactBallBearingElement',)


class LoadedMultiPointContactBallBearingElement(_1758.LoadedBallBearingElement):
    """LoadedMultiPointContactBallBearingElement

    This is a mastapy class.
    """

    TYPE = _LOADED_MULTI_POINT_CONTACT_BALL_BEARING_ELEMENT

    def __init__(self, instance_to_wrap: 'LoadedMultiPointContactBallBearingElement.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contact_angle_inner_left(self) -> 'float':
        """float: 'ContactAngleInnerLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactAngleInnerLeft

        if temp is None:
            return None

        return temp

    @property
    def contact_angle_inner_right(self) -> 'float':
        """float: 'ContactAngleInnerRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactAngleInnerRight

        if temp is None:
            return None

        return temp

    @property
    def hertzian_semi_major_dimension_inner_left(self) -> 'float':
        """float: 'HertzianSemiMajorDimensionInnerLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianSemiMajorDimensionInnerLeft

        if temp is None:
            return None

        return temp

    @property
    def hertzian_semi_major_dimension_inner_right(self) -> 'float':
        """float: 'HertzianSemiMajorDimensionInnerRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianSemiMajorDimensionInnerRight

        if temp is None:
            return None

        return temp

    @property
    def hertzian_semi_minor_dimension_inner_left(self) -> 'float':
        """float: 'HertzianSemiMinorDimensionInnerLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianSemiMinorDimensionInnerLeft

        if temp is None:
            return None

        return temp

    @property
    def hertzian_semi_minor_dimension_inner_right(self) -> 'float':
        """float: 'HertzianSemiMinorDimensionInnerRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianSemiMinorDimensionInnerRight

        if temp is None:
            return None

        return temp

    @property
    def maximum_normal_stress_inner_left(self) -> 'float':
        """float: 'MaximumNormalStressInnerLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumNormalStressInnerLeft

        if temp is None:
            return None

        return temp

    @property
    def maximum_normal_stress_inner_right(self) -> 'float':
        """float: 'MaximumNormalStressInnerRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumNormalStressInnerRight

        if temp is None:
            return None

        return temp

    @property
    def maximum_normal_stress_inner(self) -> 'float':
        """float: 'MaximumNormalStressInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumNormalStressInner

        if temp is None:
            return None

        return temp

    @property
    def maximum_shear_stress_inner_left(self) -> 'float':
        """float: 'MaximumShearStressInnerLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumShearStressInnerLeft

        if temp is None:
            return None

        return temp

    @property
    def maximum_shear_stress_inner_right(self) -> 'float':
        """float: 'MaximumShearStressInnerRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumShearStressInnerRight

        if temp is None:
            return None

        return temp

    @property
    def minimum_lubricating_film_thickness_inner_left(self) -> 'float':
        """float: 'MinimumLubricatingFilmThicknessInnerLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLubricatingFilmThicknessInnerLeft

        if temp is None:
            return None

        return temp

    @property
    def minimum_lubricating_film_thickness_inner_right(self) -> 'float':
        """float: 'MinimumLubricatingFilmThicknessInnerRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLubricatingFilmThicknessInnerRight

        if temp is None:
            return None

        return temp

    @property
    def minimum_lubricating_film_thickness_inner(self) -> 'float':
        """float: 'MinimumLubricatingFilmThicknessInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLubricatingFilmThicknessInner

        if temp is None:
            return None

        return temp

    @property
    def normal_load_inner_left(self) -> 'float':
        """float: 'NormalLoadInnerLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalLoadInnerLeft

        if temp is None:
            return None

        return temp

    @property
    def normal_load_inner_right(self) -> 'float':
        """float: 'NormalLoadInnerRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalLoadInnerRight

        if temp is None:
            return None

        return temp
