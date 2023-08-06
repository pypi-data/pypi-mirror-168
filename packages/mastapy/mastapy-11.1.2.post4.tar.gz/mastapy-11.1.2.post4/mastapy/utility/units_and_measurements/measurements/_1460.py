"""_1460.py

LengthShort
"""


from mastapy.utility.units_and_measurements import (
    _1411, _1403, _1404, _1405,
    _1409, _1410, _1412, _1406
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_LENGTH_SHORT = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'LengthShort')


__docformat__ = 'restructuredtext en'
__all__ = ('LengthShort',)


class LengthShort(_1406.MeasurementBase):
    """LengthShort

    This is a mastapy class.
    """

    TYPE = _LENGTH_SHORT

    def __init__(self, instance_to_wrap: 'LengthShort.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def feet(self) -> '_1411.Unit':
        """Unit: 'Feet' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Feet

        if temp is None:
            return None

        if _1411.Unit.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast feet to Unit. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def inches(self) -> '_1411.Unit':
        """Unit: 'Inches' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Inches

        if temp is None:
            return None

        if _1411.Unit.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast inches to Unit. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def metres(self) -> '_1411.Unit':
        """Unit: 'Metres' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Metres

        if temp is None:
            return None

        if _1411.Unit.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast metres to Unit. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def micrometres(self) -> '_1411.Unit':
        """Unit: 'Micrometres' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Micrometres

        if temp is None:
            return None

        if _1411.Unit.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast micrometres to Unit. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def millimetres(self) -> '_1411.Unit':
        """Unit: 'Millimetres' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Millimetres

        if temp is None:
            return None

        if _1411.Unit.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast millimetres to Unit. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def thousandths_of_an_inch(self) -> '_1411.Unit':
        """Unit: 'ThousandthsOfAnInch' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThousandthsOfAnInch

        if temp is None:
            return None

        if _1411.Unit.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast thousandths_of_an_inch to Unit. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
