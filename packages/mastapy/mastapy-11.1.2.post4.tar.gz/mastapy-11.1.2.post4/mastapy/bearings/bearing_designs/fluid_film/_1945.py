"""_1945.py

PlainGreaseFilledJournalBearing
"""


from mastapy.bearings.bearing_designs.fluid_film import (
    _1946, _1948, _1941, _1942,
    _1944, _1947
)
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_PLAIN_GREASE_FILLED_JOURNAL_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm', 'PlainGreaseFilledJournalBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('PlainGreaseFilledJournalBearing',)


class PlainGreaseFilledJournalBearing(_1947.PlainJournalBearing):
    """PlainGreaseFilledJournalBearing

    This is a mastapy class.
    """

    TYPE = _PLAIN_GREASE_FILLED_JOURNAL_BEARING

    def __init__(self, instance_to_wrap: 'PlainGreaseFilledJournalBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def housing_type(self) -> '_1946.PlainGreaseFilledJournalBearingHousingType':
        """PlainGreaseFilledJournalBearingHousingType: 'HousingType' is the original name of this property."""

        temp = self.wrapped.HousingType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1946.PlainGreaseFilledJournalBearingHousingType)(value) if value is not None else None

    @housing_type.setter
    def housing_type(self, value: '_1946.PlainGreaseFilledJournalBearingHousingType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HousingType = value

    @property
    def housing_detail(self) -> '_1948.PlainJournalHousing':
        """PlainJournalHousing: 'HousingDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HousingDetail

        if temp is None:
            return None

        if _1948.PlainJournalHousing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast housing_detail to PlainJournalHousing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def housing_detail_of_type_cylindrical_housing_journal_bearing(self) -> '_1941.CylindricalHousingJournalBearing':
        """CylindricalHousingJournalBearing: 'HousingDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HousingDetail

        if temp is None:
            return None

        if _1941.CylindricalHousingJournalBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast housing_detail to CylindricalHousingJournalBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def housing_detail_of_type_machinery_encased_journal_bearing(self) -> '_1942.MachineryEncasedJournalBearing':
        """MachineryEncasedJournalBearing: 'HousingDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HousingDetail

        if temp is None:
            return None

        if _1942.MachineryEncasedJournalBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast housing_detail to MachineryEncasedJournalBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def housing_detail_of_type_pedestal_journal_bearing(self) -> '_1944.PedestalJournalBearing':
        """PedestalJournalBearing: 'HousingDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HousingDetail

        if temp is None:
            return None

        if _1944.PedestalJournalBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast housing_detail to PedestalJournalBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
