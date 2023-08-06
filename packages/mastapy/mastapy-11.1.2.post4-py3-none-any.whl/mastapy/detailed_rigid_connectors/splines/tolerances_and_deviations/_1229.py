"""_1229.py

FitAndTolerance
"""


from mastapy._internal.implicit import enum_with_selected_value
from mastapy.detailed_rigid_connectors.splines import _1220, _1226
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FIT_AND_TOLERANCE = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines.TolerancesAndDeviations', 'FitAndTolerance')


__docformat__ = 'restructuredtext en'
__all__ = ('FitAndTolerance',)


class FitAndTolerance(_0.APIBase):
    """FitAndTolerance

    This is a mastapy class.
    """

    TYPE = _FIT_AND_TOLERANCE

    def __init__(self, instance_to_wrap: 'FitAndTolerance.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def fit_class(self) -> 'enum_with_selected_value.EnumWithSelectedValue_SplineFitClassType':
        """enum_with_selected_value.EnumWithSelectedValue_SplineFitClassType: 'FitClass' is the original name of this property."""

        temp = self.wrapped.FitClass

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_SplineFitClassType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @fit_class.setter
    def fit_class(self, value: 'enum_with_selected_value.EnumWithSelectedValue_SplineFitClassType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_SplineFitClassType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.FitClass = value

    @property
    def tolerance_class(self) -> 'enum_with_selected_value.EnumWithSelectedValue_SplineToleranceClassTypes':
        """enum_with_selected_value.EnumWithSelectedValue_SplineToleranceClassTypes: 'ToleranceClass' is the original name of this property."""

        temp = self.wrapped.ToleranceClass

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_SplineToleranceClassTypes.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @tolerance_class.setter
    def tolerance_class(self, value: 'enum_with_selected_value.EnumWithSelectedValue_SplineToleranceClassTypes.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_SplineToleranceClassTypes.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ToleranceClass = value
