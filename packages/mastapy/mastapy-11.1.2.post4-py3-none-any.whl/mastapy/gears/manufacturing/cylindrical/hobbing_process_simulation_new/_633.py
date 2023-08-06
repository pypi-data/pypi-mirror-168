"""_633.py

HobbingProcessGearShape
"""


from mastapy.utility_gui.charts import (
    _1634, _1625, _1630, _1631
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _632
from mastapy._internal.python_net import python_net_import

_HOBBING_PROCESS_GEAR_SHAPE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'HobbingProcessGearShape')


__docformat__ = 'restructuredtext en'
__all__ = ('HobbingProcessGearShape',)


class HobbingProcessGearShape(_632.HobbingProcessCalculation):
    """HobbingProcessGearShape

    This is a mastapy class.
    """

    TYPE = _HOBBING_PROCESS_GEAR_SHAPE

    def __init__(self, instance_to_wrap: 'HobbingProcessGearShape.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_tooth_shape_chart(self) -> '_1634.TwoDChartDefinition':
        """TwoDChartDefinition: 'GearToothShapeChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearToothShapeChart

        if temp is None:
            return None

        if _1634.TwoDChartDefinition.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast gear_tooth_shape_chart to TwoDChartDefinition. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def number_of_gear_shape_bands(self) -> 'int':
        """int: 'NumberOfGearShapeBands' is the original name of this property."""

        temp = self.wrapped.NumberOfGearShapeBands

        if temp is None:
            return None

        return temp

    @number_of_gear_shape_bands.setter
    def number_of_gear_shape_bands(self, value: 'int'):
        self.wrapped.NumberOfGearShapeBands = int(value) if value else 0

    @property
    def result_z_plane(self) -> 'float':
        """float: 'ResultZPlane' is the original name of this property."""

        temp = self.wrapped.ResultZPlane

        if temp is None:
            return None

        return temp

    @result_z_plane.setter
    def result_z_plane(self, value: 'float'):
        self.wrapped.ResultZPlane = float(value) if value else 0.0
