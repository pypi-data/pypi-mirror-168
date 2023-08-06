"""_1021.py

LtcaSettings
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import _1020
from mastapy.utility import _1390
from mastapy._internal.python_net import python_net_import

_LTCA_SETTINGS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'LtcaSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('LtcaSettings',)


class LtcaSettings(_1390.IndependentReportablePropertiesBase['LtcaSettings']):
    """LtcaSettings

    This is a mastapy class.
    """

    TYPE = _LTCA_SETTINGS

    def __init__(self, instance_to_wrap: 'LtcaSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def face_utilization_load_cutoff_parameter(self) -> 'float':
        """float: 'FaceUtilizationLoadCutoffParameter' is the original name of this property."""

        temp = self.wrapped.FaceUtilizationLoadCutoffParameter

        if temp is None:
            return None

        return temp

    @face_utilization_load_cutoff_parameter.setter
    def face_utilization_load_cutoff_parameter(self, value: 'float'):
        self.wrapped.FaceUtilizationLoadCutoffParameter = float(value) if value else 0.0

    @property
    def include_extended_tip_contact(self) -> 'bool':
        """bool: 'IncludeExtendedTipContact' is the original name of this property."""

        temp = self.wrapped.IncludeExtendedTipContact

        if temp is None:
            return None

        return temp

    @include_extended_tip_contact.setter
    def include_extended_tip_contact(self, value: 'bool'):
        self.wrapped.IncludeExtendedTipContact = bool(value) if value else False

    @property
    def load_case_modifiable_settings(self) -> '_1020.LTCALoadCaseModifiableSettings':
        """LTCALoadCaseModifiableSettings: 'LoadCaseModifiableSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadCaseModifiableSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
