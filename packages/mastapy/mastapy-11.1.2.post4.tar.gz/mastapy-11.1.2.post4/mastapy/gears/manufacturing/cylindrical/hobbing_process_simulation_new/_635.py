"""_635.py

HobbingProcessMarkOnShaft
"""


from mastapy._internal import constructor
from mastapy.utility_gui.charts import _1632
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _632
from mastapy._internal.python_net import python_net_import

_HOBBING_PROCESS_MARK_ON_SHAFT = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'HobbingProcessMarkOnShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('HobbingProcessMarkOnShaft',)


class HobbingProcessMarkOnShaft(_632.HobbingProcessCalculation):
    """HobbingProcessMarkOnShaft

    This is a mastapy class.
    """

    TYPE = _HOBBING_PROCESS_MARK_ON_SHAFT

    def __init__(self, instance_to_wrap: 'HobbingProcessMarkOnShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_profile_bands(self) -> 'int':
        """int: 'NumberOfProfileBands' is the original name of this property."""

        temp = self.wrapped.NumberOfProfileBands

        if temp is None:
            return None

        return temp

    @number_of_profile_bands.setter
    def number_of_profile_bands(self, value: 'int'):
        self.wrapped.NumberOfProfileBands = int(value) if value else 0

    @property
    def number_of_transverse_plane(self) -> 'int':
        """int: 'NumberOfTransversePlane' is the original name of this property."""

        temp = self.wrapped.NumberOfTransversePlane

        if temp is None:
            return None

        return temp

    @number_of_transverse_plane.setter
    def number_of_transverse_plane(self, value: 'int'):
        self.wrapped.NumberOfTransversePlane = int(value) if value else 0

    @property
    def shaft_diameter(self) -> 'float':
        """float: 'ShaftDiameter' is the original name of this property."""

        temp = self.wrapped.ShaftDiameter

        if temp is None:
            return None

        return temp

    @shaft_diameter.setter
    def shaft_diameter(self, value: 'float'):
        self.wrapped.ShaftDiameter = float(value) if value else 0.0

    @property
    def shaft_mark_chart(self) -> '_1632.ThreeDChartDefinition':
        """ThreeDChartDefinition: 'ShaftMarkChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftMarkChart

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
