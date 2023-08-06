"""_1867.py

RollerISOTS162812008Results
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling.iso_rating_results import _1865
from mastapy._internal.python_net import python_net_import

_ROLLER_ISOTS162812008_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.IsoRatingResults', 'RollerISOTS162812008Results')


__docformat__ = 'restructuredtext en'
__all__ = ('RollerISOTS162812008Results',)


class RollerISOTS162812008Results(_1865.ISOTS162812008Results):
    """RollerISOTS162812008Results

    This is a mastapy class.
    """

    TYPE = _ROLLER_ISOTS162812008_RESULTS

    def __init__(self, instance_to_wrap: 'RollerISOTS162812008Results.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def basic_dynamic_load_rating_of_a_bearing_lamina_of_the_inner_ring(self) -> 'float':
        """float: 'BasicDynamicLoadRatingOfABearingLaminaOfTheInnerRing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicDynamicLoadRatingOfABearingLaminaOfTheInnerRing

        if temp is None:
            return None

        return temp

    @property
    def basic_dynamic_load_rating_of_a_bearing_lamina_of_the_outer_ring(self) -> 'float':
        """float: 'BasicDynamicLoadRatingOfABearingLaminaOfTheOuterRing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicDynamicLoadRatingOfABearingLaminaOfTheOuterRing

        if temp is None:
            return None

        return temp

    @property
    def equivalent_load_assuming_line_contacts(self) -> 'float':
        """float: 'EquivalentLoadAssumingLineContacts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EquivalentLoadAssumingLineContacts

        if temp is None:
            return None

        return temp
