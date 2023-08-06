"""_1265.py

CycloidalDiscModificationsSpecification
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.cycloidal import _1260, _1266
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.math_utility import _1341
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_MODIFICATIONS_SPECIFICATION = python_net_import('SMT.MastaAPI.Cycloidal', 'CycloidalDiscModificationsSpecification')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscModificationsSpecification',)


class CycloidalDiscModificationsSpecification(_0.APIBase):
    """CycloidalDiscModificationsSpecification

    This is a mastapy class.
    """

    TYPE = _CYCLOIDAL_DISC_MODIFICATIONS_SPECIFICATION

    def __init__(self, instance_to_wrap: 'CycloidalDiscModificationsSpecification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angular_offset_modification(self) -> 'float':
        """float: 'AngularOffsetModification' is the original name of this property."""

        temp = self.wrapped.AngularOffsetModification

        if temp is None:
            return None

        return temp

    @angular_offset_modification.setter
    def angular_offset_modification(self, value: 'float'):
        self.wrapped.AngularOffsetModification = float(value) if value else 0.0

    @property
    def coefficient_for_logarithmic_crowning(self) -> 'float':
        """float: 'CoefficientForLogarithmicCrowning' is the original name of this property."""

        temp = self.wrapped.CoefficientForLogarithmicCrowning

        if temp is None:
            return None

        return temp

    @coefficient_for_logarithmic_crowning.setter
    def coefficient_for_logarithmic_crowning(self, value: 'float'):
        self.wrapped.CoefficientForLogarithmicCrowning = float(value) if value else 0.0

    @property
    def crowning_radius(self) -> 'float':
        """float: 'CrowningRadius' is the original name of this property."""

        temp = self.wrapped.CrowningRadius

        if temp is None:
            return None

        return temp

    @crowning_radius.setter
    def crowning_radius(self, value: 'float'):
        self.wrapped.CrowningRadius = float(value) if value else 0.0

    @property
    def crowning_specification_method(self) -> '_1260.CrowningSpecificationMethod':
        """CrowningSpecificationMethod: 'CrowningSpecificationMethod' is the original name of this property."""

        temp = self.wrapped.CrowningSpecificationMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1260.CrowningSpecificationMethod)(value) if value is not None else None

    @crowning_specification_method.setter
    def crowning_specification_method(self, value: '_1260.CrowningSpecificationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CrowningSpecificationMethod = value

    @property
    def direction_of_measured_modifications(self) -> '_1266.DirectionOfMeasuredModifications':
        """DirectionOfMeasuredModifications: 'DirectionOfMeasuredModifications' is the original name of this property."""

        temp = self.wrapped.DirectionOfMeasuredModifications

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1266.DirectionOfMeasuredModifications)(value) if value is not None else None

    @direction_of_measured_modifications.setter
    def direction_of_measured_modifications(self, value: '_1266.DirectionOfMeasuredModifications'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.DirectionOfMeasuredModifications = value

    @property
    def distance_to_where_crowning_starts_from_lobe_centre(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'DistanceToWhereCrowningStartsFromLobeCentre' is the original name of this property."""

        temp = self.wrapped.DistanceToWhereCrowningStartsFromLobeCentre

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @distance_to_where_crowning_starts_from_lobe_centre.setter
    def distance_to_where_crowning_starts_from_lobe_centre(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.DistanceToWhereCrowningStartsFromLobeCentre = value

    @property
    def generating_wheel_centre_circle_diameter_modification(self) -> 'float':
        """float: 'GeneratingWheelCentreCircleDiameterModification' is the original name of this property."""

        temp = self.wrapped.GeneratingWheelCentreCircleDiameterModification

        if temp is None:
            return None

        return temp

    @generating_wheel_centre_circle_diameter_modification.setter
    def generating_wheel_centre_circle_diameter_modification(self, value: 'float'):
        self.wrapped.GeneratingWheelCentreCircleDiameterModification = float(value) if value else 0.0

    @property
    def generating_wheel_diameter_modification(self) -> 'float':
        """float: 'GeneratingWheelDiameterModification' is the original name of this property."""

        temp = self.wrapped.GeneratingWheelDiameterModification

        if temp is None:
            return None

        return temp

    @generating_wheel_diameter_modification.setter
    def generating_wheel_diameter_modification(self, value: 'float'):
        self.wrapped.GeneratingWheelDiameterModification = float(value) if value else 0.0

    @property
    def measured_profile_modification(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'MeasuredProfileModification' is the original name of this property."""

        temp = self.wrapped.MeasuredProfileModification

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measured_profile_modification.setter
    def measured_profile_modification(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.MeasuredProfileModification = value

    @property
    def specify_measured_profile_modification(self) -> 'bool':
        """bool: 'SpecifyMeasuredProfileModification' is the original name of this property."""

        temp = self.wrapped.SpecifyMeasuredProfileModification

        if temp is None:
            return None

        return temp

    @specify_measured_profile_modification.setter
    def specify_measured_profile_modification(self, value: 'bool'):
        self.wrapped.SpecifyMeasuredProfileModification = bool(value) if value else False
