"""_1996.py

ContourDrawStyle
"""


from mastapy.utility.enums import _1598
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.system_model.drawing import _2006, _2002
from mastapy.geometry import _282
from mastapy._internal.python_net import python_net_import

_CONTOUR_DRAW_STYLE = python_net_import('SMT.MastaAPI.SystemModel.Drawing', 'ContourDrawStyle')


__docformat__ = 'restructuredtext en'
__all__ = ('ContourDrawStyle',)


class ContourDrawStyle(_282.DrawStyleBase):
    """ContourDrawStyle

    This is a mastapy class.
    """

    TYPE = _CONTOUR_DRAW_STYLE

    def __init__(self, instance_to_wrap: 'ContourDrawStyle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contour(self) -> '_1598.ThreeDViewContourOption':
        """ThreeDViewContourOption: 'Contour' is the original name of this property."""

        temp = self.wrapped.Contour

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1598.ThreeDViewContourOption)(value) if value is not None else None

    @contour.setter
    def contour(self, value: '_1598.ThreeDViewContourOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Contour = value

    @property
    def minimum_peak_value_displacement(self) -> 'float':
        """float: 'MinimumPeakValueDisplacement' is the original name of this property."""

        temp = self.wrapped.MinimumPeakValueDisplacement

        if temp is None:
            return None

        return temp

    @minimum_peak_value_displacement.setter
    def minimum_peak_value_displacement(self, value: 'float'):
        self.wrapped.MinimumPeakValueDisplacement = float(value) if value else 0.0

    @property
    def minimum_peak_value_stress(self) -> 'float':
        """float: 'MinimumPeakValueStress' is the original name of this property."""

        temp = self.wrapped.MinimumPeakValueStress

        if temp is None:
            return None

        return temp

    @minimum_peak_value_stress.setter
    def minimum_peak_value_stress(self, value: 'float'):
        self.wrapped.MinimumPeakValueStress = float(value) if value else 0.0

    @property
    def show_local_maxima(self) -> 'bool':
        """bool: 'ShowLocalMaxima' is the original name of this property."""

        temp = self.wrapped.ShowLocalMaxima

        if temp is None:
            return None

        return temp

    @show_local_maxima.setter
    def show_local_maxima(self, value: 'bool'):
        self.wrapped.ShowLocalMaxima = bool(value) if value else False

    @property
    def deflection_scaling(self) -> '_2006.ScalingDrawStyle':
        """ScalingDrawStyle: 'DeflectionScaling' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DeflectionScaling

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def model_view_options(self) -> '_2002.ModelViewOptionsDrawStyle':
        """ModelViewOptionsDrawStyle: 'ModelViewOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModelViewOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
