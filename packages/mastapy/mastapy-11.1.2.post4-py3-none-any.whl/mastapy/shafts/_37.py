"""_37.py

ShaftSettings
"""


from mastapy._internal.python_net import python_net_import
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.shafts import _33, _13
from mastapy._internal.implicit import enum_with_selected_value
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.utility import _1395

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_SHAFT_SETTINGS = python_net_import('SMT.MastaAPI.Shafts', 'ShaftSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftSettings',)


class ShaftSettings(_1395.PerMachineSettings):
    """ShaftSettings

    This is a mastapy class.
    """

    TYPE = _SHAFT_SETTINGS

    def __init__(self, instance_to_wrap: 'ShaftSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def material_database(self) -> 'str':
        """str: 'MaterialDatabase' is the original name of this property."""

        temp = self.wrapped.MaterialDatabase.SelectedItemName

        if temp is None:
            return None

        return temp

    @material_database.setter
    def material_database(self, value: 'str'):
        self.wrapped.MaterialDatabase.SetSelectedItem(str(value) if value else '')

    @property
    def reliability_factor(self) -> 'float':
        """float: 'ReliabilityFactor' is the original name of this property."""

        temp = self.wrapped.ReliabilityFactor

        if temp is None:
            return None

        return temp

    @reliability_factor.setter
    def reliability_factor(self, value: 'float'):
        self.wrapped.ReliabilityFactor = float(value) if value else 0.0

    @property
    def required_shaft_reliability(self) -> 'float':
        """float: 'RequiredShaftReliability' is the original name of this property."""

        temp = self.wrapped.RequiredShaftReliability

        if temp is None:
            return None

        return temp

    @required_shaft_reliability.setter
    def required_shaft_reliability(self, value: 'float'):
        self.wrapped.RequiredShaftReliability = float(value) if value else 0.0

    @property
    def shaft_rating_method(self) -> '_33.ShaftRatingMethod':
        """ShaftRatingMethod: 'ShaftRatingMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftRatingMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_33.ShaftRatingMethod)(value) if value is not None else None

    @property
    def shaft_rating_method_selector(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ShaftRatingMethod':
        """enum_with_selected_value.EnumWithSelectedValue_ShaftRatingMethod: 'ShaftRatingMethodSelector' is the original name of this property."""

        temp = self.wrapped.ShaftRatingMethodSelector

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ShaftRatingMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @shaft_rating_method_selector.setter
    def shaft_rating_method_selector(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ShaftRatingMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ShaftRatingMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ShaftRatingMethodSelector = value

    @property
    def version_of_miners_rule(self) -> '_13.FkmVersionOfMinersRule':
        """FkmVersionOfMinersRule: 'VersionOfMinersRule' is the original name of this property."""

        temp = self.wrapped.VersionOfMinersRule

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_13.FkmVersionOfMinersRule)(value) if value is not None else None

    @version_of_miners_rule.setter
    def version_of_miners_rule(self, value: '_13.FkmVersionOfMinersRule'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.VersionOfMinersRule = value
