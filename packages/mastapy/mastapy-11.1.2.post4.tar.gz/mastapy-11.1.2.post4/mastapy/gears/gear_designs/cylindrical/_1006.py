"""_1006.py

FinishStockSpecification
"""


from mastapy.gears.gear_designs.cylindrical.thickness_stock_and_backlash import _1050
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.cylindrical import (
    _1044, _997, _1000, _1029
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_FINISH_STOCK_SPECIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'FinishStockSpecification')


__docformat__ = 'restructuredtext en'
__all__ = ('FinishStockSpecification',)


class FinishStockSpecification(_1029.RelativeValuesSpecification['FinishStockSpecification']):
    """FinishStockSpecification

    This is a mastapy class.
    """

    TYPE = _FINISH_STOCK_SPECIFICATION

    def __init__(self, instance_to_wrap: 'FinishStockSpecification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def finish_stock_rough_thickness_specification_method(self) -> '_1050.FinishStockType':
        """FinishStockType: 'FinishStockRoughThicknessSpecificationMethod' is the original name of this property."""

        temp = self.wrapped.FinishStockRoughThicknessSpecificationMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1050.FinishStockType)(value) if value is not None else None

    @finish_stock_rough_thickness_specification_method.setter
    def finish_stock_rough_thickness_specification_method(self, value: '_1050.FinishStockType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FinishStockRoughThicknessSpecificationMethod = value

    @property
    def normal(self) -> '_1044.TolerancedValueSpecification[FinishStockSpecification]':
        """TolerancedValueSpecification[FinishStockSpecification]: 'Normal' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Normal

        if temp is None:
            return None

        if _1044.TolerancedValueSpecification[FinishStockSpecification].TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast normal to TolerancedValueSpecification[FinishStockSpecification]. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[FinishStockSpecification](temp) if temp is not None else None

    @property
    def tangent_to_reference_circle(self) -> '_1044.TolerancedValueSpecification[FinishStockSpecification]':
        """TolerancedValueSpecification[FinishStockSpecification]: 'TangentToReferenceCircle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TangentToReferenceCircle

        if temp is None:
            return None

        if _1044.TolerancedValueSpecification[FinishStockSpecification].TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast tangent_to_reference_circle to TolerancedValueSpecification[FinishStockSpecification]. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[FinishStockSpecification](temp) if temp is not None else None
